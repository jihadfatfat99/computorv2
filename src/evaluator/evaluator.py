"""
AST Evaluator for Computorv2.

Walks the AST and computes values, managing the execution context.
"""

from typing import Any, Optional, Tuple, List

from ..math_types import Rational, Complex, Matrix, Polynomial, Function
from ..parser.ast_nodes import (
    ASTNode,
    ASTVisitor,
    NumberNode,
    IdentifierNode,
    ImaginaryNode,
    BinaryOpNode,
    UnaryOpNode,
    MatrixNode,
    FunctionCallNode,
    AssignmentNode,
    FunctionDefNode,
    QueryNode,
    EquationNode,
)
from .context import Context
from .operations import apply_binary_op, apply_unary_op
from .type_coercion import simplify_result, to_rational, is_scalar
from .errors import (
    EvaluatorError,
    UndefinedVariableError,
    UndefinedFunctionError,
    TypeMismatchError,
    InvalidOperandError,
)


class EvaluationResult:
    """
    Result of an evaluation.
    
    Attributes:
        value: The computed value
        is_equation: Whether this was an equation (needs solving)
        equation_data: Data for equation solving (left, right polynomials)
        display_name: Optional name for display (e.g., variable name)
    """
    
    def __init__(
        self,
        value: Any,
        is_equation: bool = False,
        equation_data: Optional[Tuple[Polynomial, Polynomial]] = None,
        display_name: Optional[str] = None,
    ):
        self.value = value
        self.is_equation = is_equation
        self.equation_data = equation_data
        self.display_name = display_name
    
    def __repr__(self):
        return f"EvaluationResult(value={self.value}, is_equation={self.is_equation})"


class Evaluator(ASTVisitor):
    """
    Evaluates AST nodes and computes values.
    
    Implements the ASTVisitor interface to traverse and evaluate
    the syntax tree.
    
    Examples:
        >>> ctx = Context()
        >>> evaluator = Evaluator(ctx)
        >>> ast = parse("x = 2 + 3")
        >>> result = evaluator.evaluate(ast)
        >>> result.value
        Rational(5, 1)
    """
    
    def __init__(self, context: Context = None):
        """
        Initialize evaluator.
        
        Args:
            context: Evaluation context (symbol table). Creates new if None.
        """
        self.context = context if context is not None else Context()
        self._current_function_param: Optional[str] = None
    
    def evaluate(self, node: ASTNode) -> EvaluationResult:
        """
        Evaluate an AST node.
        
        Args:
            node: The AST node to evaluate
        
        Returns:
            EvaluationResult containing the computed value
        """
        value = node.accept(self)
        
        # Check if it's an equation result
        if isinstance(value, tuple) and len(value) == 2:
            left, right = value
            if isinstance(left, Polynomial) and isinstance(right, Polynomial):
                return EvaluationResult(
                    value=None,
                    is_equation=True,
                    equation_data=(left, right)
                )
        
        return EvaluationResult(value=value)
    
    # ========================
    # Literal Visitors
    # ========================
    
    def visit_number(self, node: NumberNode) -> Rational:
        """Evaluate number literal."""
        if isinstance(node.value, int):
            return Rational.from_int(node.value)
        else:
            return Rational.from_float(node.value)
    
    def visit_identifier(self, node: IdentifierNode) -> Any:
        """Evaluate identifier (variable lookup or polynomial variable)."""
        name = node.name
        
        # If we're inside a function definition, check if this is the parameter
        if self._current_function_param and name == self._current_function_param:
            # Return a polynomial representing the variable
            return Polynomial.x(name)
        
        # Otherwise look up in context
        if self.context.has_variable(name):
            return self.context.get_variable(name)
        
        if self.context.has_function(name):
            # Return the function itself (for composition, etc.)
            return self.context.get_function(name)
        
        # Unknown identifier - treat as polynomial variable for equation solving
        return Polynomial.x(name)
    
    def visit_imaginary(self, node: ImaginaryNode) -> Complex:
        """Evaluate imaginary unit."""
        return Complex.i()
    
    # ========================
    # Operation Visitors
    # ========================
    
    def visit_binary_op(self, node: BinaryOpNode) -> Any:
        """Evaluate binary operation."""
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        return apply_binary_op(node.operator, left, right)
    
    def visit_unary_op(self, node: UnaryOpNode) -> Any:
        """Evaluate unary operation."""
        operand = node.operand.accept(self)
        
        return apply_unary_op(node.operator, operand)
    
    # ========================
    # Structure Visitors
    # ========================
    
    def visit_matrix(self, node: MatrixNode) -> Matrix:
        """Evaluate matrix literal."""
        evaluated_rows: List[List[Any]] = []
        
        for row in node.rows:
            evaluated_row = []
            for elem in row:
                value = elem.accept(self)
                
                # Ensure value is a valid matrix entry
                if isinstance(value, Polynomial):
                    if value.is_constant():
                        value = value.to_constant()
                    else:
                        raise InvalidOperandError(
                            "Matrix elements must be scalar values, not polynomials"
                        )
                
                if not is_scalar(value):
                    raise InvalidOperandError(
                        f"Matrix elements must be scalar values, got {type(value).__name__}"
                    )
                
                evaluated_row.append(value)
            
            evaluated_rows.append(evaluated_row)
        
        return Matrix(evaluated_rows)
    
    def visit_function_call(self, node: FunctionCallNode) -> Any:
        """Evaluate function call."""
        from .builtins import is_builtin, get_builtin
        
        name = node.name
        
        # Check for built-in functions first
        if is_builtin(name):
            builtin = get_builtin(name)
            arg_value = node.argument.accept(self)
            
            # Matrix functions can accept Matrix directly
            if isinstance(arg_value, Matrix):
                result = builtin(arg_value)
                return simplify_result(result) if not isinstance(result, Matrix) else result
            
            # If argument is a polynomial with variable, cannot apply builtin
            if isinstance(arg_value, Polynomial) and not arg_value.is_constant():
                raise InvalidOperandError(
                    f"Cannot apply {name}() to polynomial expression"
                )
            
            # Convert polynomial constant to scalar
            if isinstance(arg_value, Polynomial):
                arg_value = arg_value.to_constant()
            
            result = builtin(arg_value)
            return simplify_result(result)
        
        # Check if user-defined function exists
        if not self.context.has_function(name):
            raise UndefinedFunctionError(name)
        
        func = self.context.get_function(name)
        
        # Evaluate the argument
        arg_value = node.argument.accept(self)
        
        # If argument is a polynomial (contains variable), compose
        if isinstance(arg_value, Polynomial) and not arg_value.is_constant():
            # Return composition: f(g(x)) where arg is g(x)
            result_poly = Polynomial.zero(arg_value.variable)
            
            for degree, coeff in func.body.coefficients.items():
                # coeff * (arg_value)^degree
                term = arg_value ** degree
                term = term * coeff
                result_poly = result_poly + term
            
            return result_poly
        
        # Otherwise evaluate numerically
        if isinstance(arg_value, Polynomial):
            arg_value = arg_value.to_constant()
        
        result = func.evaluate(arg_value)
        return simplify_result(result)
    
    # ========================
    # Statement Visitors
    # ========================
    
    def visit_assignment(self, node: AssignmentNode) -> Any:
        """Evaluate variable assignment."""
        name = node.name
        value = node.value.accept(self)
        
        # Simplify polynomial to constant if possible
        if isinstance(value, Polynomial) and value.is_constant():
            value = value.to_constant()
        
        # Simplify complex to rational if purely real
        value = simplify_result(value)
        
        # Store in context
        self.context.set_variable(name, value)
        
        return value
    
    def visit_function_def(self, node: FunctionDefNode) -> Function:
        """Evaluate function definition."""
        name = node.name
        param = node.parameter
        
        # Set current function parameter for identifier resolution
        self._current_function_param = param
        
        try:
            # Evaluate body with parameter as polynomial variable
            body_value = node.body.accept(self)
            
            # Ensure body is a polynomial
            if isinstance(body_value, Polynomial):
                body_poly = body_value
            elif isinstance(body_value, (Rational, Complex)):
                body_poly = Polynomial.from_constant(body_value, param)
            elif isinstance(body_value, Function):
                body_poly = body_value.body
            else:
                raise InvalidOperandError(
                    f"Function body must be a polynomial expression, got {type(body_value).__name__}"
                )
            
            # Ensure polynomial uses correct variable
            body_poly = Polynomial(body_poly.coefficients, param)
            
        finally:
            self._current_function_param = None
        
        # Create and store function
        func = Function(name, param, body_poly)
        self.context.set_function(name, func)
        
        return func
    
    def visit_query(self, node: QueryNode) -> Any:
        """Evaluate query (expression = ?)."""
        value = node.expression.accept(self)
        
        # Simplify if possible
        if isinstance(value, Polynomial) and value.is_constant():
            value = value.to_constant()
        
        return simplify_result(value)
    
    def visit_equation(self, node: EquationNode) -> Tuple[Polynomial, Polynomial]:
        """
        Evaluate equation (left = right ?).
        
        Returns tuple of (left_poly, right_poly) for solver.
        
        Special handling for function equations like f(x) = 0:
        - If left side is a function call f(var) where f is defined,
          use the function's body as the polynomial (don't evaluate)
        """
        from ..parser.ast_nodes import FunctionCallNode, IdentifierNode
        
        # Check if left side is a function call that should be treated symbolically
        if isinstance(node.left, FunctionCallNode):
            func_name = node.left.name
            if self.context.has_function(func_name):
                func = self.context.get_function(func_name)
                # Check if argument is a simple identifier (like x in f(x))
                if isinstance(node.left.argument, IdentifierNode):
                    arg_name = node.left.argument.name
                    # If the argument matches function's parameter, use function body
                    if arg_name.lower() == func.variable.lower():
                        left_poly = func.body
                        right = node.right.accept(self)
                        right_poly = self._to_polynomial(right, func.variable)
                        return (left_poly, right_poly)
        
        # Default behavior: evaluate both sides
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        # Convert to polynomials if needed
        left_poly = self._to_polynomial(left)
        right_poly = self._to_polynomial(right)
        
        return (left_poly, right_poly)
    
    def _to_polynomial(self, value: Any, variable: str = 'x') -> Polynomial:
        """Convert a value to polynomial form."""
        if isinstance(value, Polynomial):
            return value
        if isinstance(value, Function):
            return value.body
        if isinstance(value, (Rational, Complex)):
            return Polynomial.from_constant(value, variable)
        if isinstance(value, (int, float)):
            return Polynomial.from_constant(to_rational(value), variable)
        
        raise InvalidOperandError(
            f"Cannot convert {type(value).__name__} to polynomial for equation solving"
        )


def evaluate(source: str, context: Context = None) -> EvaluationResult:
    """
    Convenience function to parse and evaluate a string.
    
    Args:
        source: Input string to evaluate
        context: Optional context (creates new if None)
    
    Returns:
        EvaluationResult with computed value
    """
    from ..parser import parse
    
    if context is None:
        context = Context()
    
    ast = parse(source)
    evaluator = Evaluator(context)
    
    return evaluator.evaluate(ast)