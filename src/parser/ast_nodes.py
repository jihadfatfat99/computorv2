"""
Abstract Syntax Tree (AST) node definitions for Computorv2.

Each node represents a construct in the language:
    - Literals (numbers, identifiers, imaginary)
    - Operations (binary, unary)
    - Structures (matrices, function calls)
    - Statements (assignments, queries)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union


class ASTNode(ABC):
    """
    Abstract base class for all AST nodes.
    """
    
    @abstractmethod
    def __str__(self) -> str:
        """String representation for debugging"""
        pass
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Accept a visitor for tree traversal"""
        pass


class ASTVisitor(ABC):
    """
    Abstract visitor for traversing AST nodes.
    Implement this to create evaluators, printers, etc.
    """
    
    @abstractmethod
    def visit_number(self, node: 'NumberNode') -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: 'IdentifierNode') -> Any:
        pass
    
    @abstractmethod
    def visit_imaginary(self, node: 'ImaginaryNode') -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: 'BinaryOpNode') -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: 'UnaryOpNode') -> Any:
        pass
    
    @abstractmethod
    def visit_matrix(self, node: 'MatrixNode') -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: 'FunctionCallNode') -> Any:
        pass
    
    @abstractmethod
    def visit_assignment(self, node: 'AssignmentNode') -> Any:
        pass
    
    @abstractmethod
    def visit_function_def(self, node: 'FunctionDefNode') -> Any:
        pass
    
    @abstractmethod
    def visit_query(self, node: 'QueryNode') -> Any:
        pass
    
    @abstractmethod
    def visit_equation(self, node: 'EquationNode') -> Any:
        pass


# ============================================================
# Literal Nodes
# ============================================================

@dataclass
class NumberNode(ASTNode):
    """
    Numeric literal (integer or float).
    
    Examples: 42, 3.14, 0.5
    """
    value: Union[int, float]
    
    def __str__(self) -> str:
        return f"Number({self.value})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_number(self)


@dataclass
class IdentifierNode(ASTNode):
    """
    Variable or function name.
    
    Examples: x, varA, funB
    """
    name: str
    
    def __str__(self) -> str:
        return f"Identifier({self.name})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_identifier(self)


@dataclass
class ImaginaryNode(ASTNode):
    """
    The imaginary unit 'i'.
    
    Represents sqrt(-1).
    """
    
    def __str__(self) -> str:
        return "Imaginary(i)"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_imaginary(self)


# ============================================================
# Operation Nodes
# ============================================================

@dataclass
class BinaryOpNode(ASTNode):
    """
    Binary operation: left operator right.
    
    Operators: +, -, *, **, /, %, ^
    """
    operator: str
    left: ASTNode
    right: ASTNode
    
    def __str__(self) -> str:
        return f"BinaryOp({self.left} {self.operator} {self.right})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOpNode(ASTNode):
    """
    Unary operation: operator operand.
    
    Operators: +, -
    """
    operator: str
    operand: ASTNode
    
    def __str__(self) -> str:
        return f"UnaryOp({self.operator}{self.operand})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_unary_op(self)


# ============================================================
# Structure Nodes
# ============================================================

@dataclass
class MatrixNode(ASTNode):
    """
    Matrix literal.
    
    Example: [[1,2];[3,4]]
    Stored as list of rows, each row is list of expressions.
    """
    rows: List[List[ASTNode]]
    
    def __str__(self) -> str:
        rows_str = "; ".join(
            "[" + ", ".join(str(elem) for elem in row) + "]"
            for row in self.rows
        )
        return f"Matrix([{rows_str}])"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_matrix(self)
    
    @property
    def num_rows(self) -> int:
        return len(self.rows)
    
    @property
    def num_cols(self) -> int:
        return len(self.rows[0]) if self.rows else 0


@dataclass
class FunctionCallNode(ASTNode):
    """
    Function call: name(argument).
    
    Example: funA(2), f(x + 1)
    """
    name: str
    argument: ASTNode
    
    def __str__(self) -> str:
        return f"FunctionCall({self.name}({self.argument}))"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_function_call(self)


# ============================================================
# Statement Nodes
# ============================================================

@dataclass
class AssignmentNode(ASTNode):
    """
    Variable assignment: name = expression.
    
    Example: x = 2 + 3
    """
    name: str
    value: ASTNode
    
    def __str__(self) -> str:
        return f"Assignment({self.name} = {self.value})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_assignment(self)


@dataclass
class FunctionDefNode(ASTNode):
    """
    Function definition: name(param) = body.
    
    Example: f(x) = 2*x + 1
    """
    name: str
    parameter: str
    body: ASTNode
    
    def __str__(self) -> str:
        return f"FunctionDef({self.name}({self.parameter}) = {self.body})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_function_def(self)


@dataclass
class QueryNode(ASTNode):
    """
    Query expression: expression = ?
    
    Example: x + 2 = ?
    
    Evaluates and displays the result.
    """
    expression: ASTNode
    
    def __str__(self) -> str:
        return f"Query({self.expression} = ?)"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_query(self)


@dataclass
class EquationNode(ASTNode):
    """
    Equation to solve: left = right ?
    
    Example: f(x) = 0 ?
    
    Both sides can contain the unknown variable.
    """
    left: ASTNode
    right: ASTNode
    
    def __str__(self) -> str:
        return f"Equation({self.left} = {self.right})"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_equation(self)


# ============================================================
# Helper Functions
# ============================================================

def is_literal(node: ASTNode) -> bool:
    """Check if node is a literal (number, identifier, imaginary)"""
    return isinstance(node, (NumberNode, IdentifierNode, ImaginaryNode))


def is_operation(node: ASTNode) -> bool:
    """Check if node is an operation"""
    return isinstance(node, (BinaryOpNode, UnaryOpNode))


def is_statement(node: ASTNode) -> bool:
    """Check if node is a statement"""
    return isinstance(node, (AssignmentNode, FunctionDefNode, QueryNode, EquationNode))