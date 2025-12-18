"""
Function implementation for Computorv2.

Represents a named function with a single variable parameter.
Wraps a Polynomial (or expression) with metadata for storage and evaluation.
"""

from __future__ import annotations
from typing import Any, Union, TYPE_CHECKING

from .base import (
    MathType,
    InvalidOperationError,
    InvalidExponentError,
)
from .rational import Rational
from .complex import Complex
from .polynomial import Polynomial


class Function(MathType):
    """
    Named function with a single variable.
    
    Stores:
        - name: Function name (e.g., 'funA')
        - variable: Parameter name (e.g., 'x')
        - body: The polynomial expression
    
    Examples:
        >>> f = Function('f', 'x', Polynomial({2: Rational(1), 0: Rational(1)}))  # f(x) = x² + 1
        >>> f.evaluate(Rational(2))  # Returns 5
        >>> f(2)  # Shorthand for evaluate
    """
    
    __slots__ = ('_name', '_variable', '_body')
    
    def __init__(self, name: str, variable: str, body: Polynomial):
        """
        Create a Function.
        
        Args:
            name: Function name (letters only)
            variable: Parameter variable name (single letter typically)
            body: The polynomial expression body
        """
        self._name = name.lower()
        self._variable = variable.lower()
        
        if isinstance(body, Polynomial):
            # Ensure the polynomial uses the correct variable
            self._body = Polynomial(body.coefficients, self._variable)
        else:
            raise InvalidOperationError(
                f"Function body must be a Polynomial, got {type(body).__name__}"
            )
    
    # ========================
    # Properties
    # ========================
    
    @property
    def name(self) -> str:
        """Get the function name"""
        return self._name
    
    @property
    def variable(self) -> str:
        """Get the parameter variable name"""
        return self._variable
    
    @property
    def body(self) -> Polynomial:
        """Get the function body"""
        return self._body
    
    @property
    def degree(self) -> int:
        """Get the degree of the function polynomial"""
        return self._body.degree
    
    @property
    def type_name(self) -> str:
        return "Function"
    
    # ========================
    # Factory Methods
    # ========================
    
    @classmethod
    def from_constant(cls, name: str, variable: str, value: Any) -> Function:
        """Create a constant function"""
        body = Polynomial.from_constant(value, variable)
        return cls(name, variable, body)
    
    @classmethod
    def identity(cls, name: str = 'f', variable: str = 'x') -> Function:
        """Create the identity function f(x) = x"""
        body = Polynomial.x(variable)
        return cls(name, variable, body)
    
    @classmethod
    def zero(cls, name: str = 'f', variable: str = 'x') -> Function:
        """Create the zero function"""
        return cls(name, variable, Polynomial.zero(variable))
    
    @classmethod
    def one(cls, name: str = 'f', variable: str = 'x') -> Function:
        """Create the constant function f(x) = 1"""
        return cls(name, variable, Polynomial.one(variable))
    
    # ========================
    # Type Properties
    # ========================
    
    def is_zero(self) -> bool:
        """Check if function is constantly zero"""
        return self._body.is_zero()
    
    def is_one(self) -> bool:
        """Check if function is constantly one"""
        return self._body.is_one()
    
    def is_constant(self) -> bool:
        """Check if function is a constant"""
        return self._body.is_constant()
    
    def copy(self) -> Function:
        """Deep copy the function"""
        return Function(self._name, self._variable, self._body.copy())
    
    # ========================
    # Evaluation
    # ========================
    
    def evaluate(self, value: Any) -> Union[Rational, Complex]:
        """
        Evaluate the function at a given value.
        
        Args:
            value: The value to substitute for the variable
        
        Returns:
            The result of f(value)
        """
        return self._body.evaluate(value)
    
    def __call__(self, value: Any) -> Union[Rational, Complex]:
        """Shorthand for evaluate: f(x) instead of f.evaluate(x)"""
        return self.evaluate(value)
    
    # ========================
    # Function Composition (Bonus)
    # ========================
    
    def compose(self, other: Function) -> Function:
        """
        Compose two functions: (self ∘ other)(x) = self(other(x))
        
        Args:
            other: The inner function
        
        Returns:
            New function representing the composition
        """
        if not isinstance(other, Function):
            raise InvalidOperationError(
                f"Cannot compose Function with {type(other).__name__}"
            )
        
        # f(g(x)) - substitute g(x) into f
        # This is complex for polynomials: if f(x) = Σ aᵢxⁱ and g(x) is a polynomial,
        # then f(g(x)) = Σ aᵢ(g(x))ⁱ
        
        result = Polynomial.zero(other._variable)
        
        for degree, coeff in self._body.coefficients.items():
            # coeff * (g(x))^degree
            term = other._body ** degree
            term = term * coeff
            result = result + term
        
        new_name = f"{self._name}_{other._name}"  # Composed name
        return Function(new_name, other._variable, result)
    
    # ========================
    # Arithmetic Operations
    # ========================
    
    def _ensure_compatible(self, other: Any) -> Union[Function, Polynomial]:
        """Ensure other is compatible for operations"""
        if isinstance(other, Function):
            if other._variable != self._variable:
                raise InvalidOperationError(
                    f"Cannot combine functions with different variables: "
                    f"{self._variable} and {other._variable}"
                )
            return other
        if isinstance(other, Polynomial):
            return other
        if isinstance(other, (Rational, Complex, int, float)):
            return Polynomial.from_constant(other, self._variable)
        raise InvalidOperationError(
            f"Cannot perform operation between Function and {type(other).__name__}"
        )
    
    def _get_body(self, other: Union[Function, Polynomial]) -> Polynomial:
        """Get polynomial body from Function or Polynomial"""
        if isinstance(other, Function):
            return other._body
        return other
    
    def __add__(self, other: Any) -> Function:
        other = self._ensure_compatible(other)
        other_body = self._get_body(other)
        new_body = self._body + other_body
        return Function(self._name, self._variable, new_body)
    
    def __radd__(self, other: Any) -> Function:
        return self.__add__(other)
    
    def __sub__(self, other: Any) -> Function:
        other = self._ensure_compatible(other)
        other_body = self._get_body(other)
        new_body = self._body - other_body
        return Function(self._name, self._variable, new_body)
    
    def __rsub__(self, other: Any) -> Function:
        other = self._ensure_compatible(other)
        other_body = self._get_body(other)
        new_body = other_body - self._body
        return Function(self._name, self._variable, new_body)
    
    def __mul__(self, other: Any) -> Function:
        other = self._ensure_compatible(other)
        other_body = self._get_body(other)
        new_body = self._body * other_body
        return Function(self._name, self._variable, new_body)
    
    def __rmul__(self, other: Any) -> Function:
        return self.__mul__(other)
    
    def __truediv__(self, other: Any) -> Function:
        other = self._ensure_compatible(other)
        other_body = self._get_body(other)
        new_body = self._body / other_body
        return Function(self._name, self._variable, new_body)
    
    def __rtruediv__(self, other: Any) -> Function:
        raise InvalidOperationError("Cannot divide by a function")
    
    def __mod__(self, other: Any) -> Function:
        other = self._ensure_compatible(other)
        other_body = self._get_body(other)
        new_body = self._body % other_body
        return Function(self._name, self._variable, new_body)
    
    def __rmod__(self, other: Any) -> Function:
        raise InvalidOperationError("Cannot compute modulo with function divisor")
    
    def __pow__(self, other: Any) -> Function:
        new_body = self._body ** other
        return Function(self._name, self._variable, new_body)
    
    def __neg__(self) -> Function:
        return Function(self._name, self._variable, -self._body)
    
    def __pos__(self) -> Function:
        return self.copy()
    
    # ========================
    # Comparison Operations
    # ========================
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Function):
            return False
        return (
            self._name == other._name and
            self._variable == other._variable and
            self._body == other._body
        )
    
    # ========================
    # Hashing
    # ========================
    
    def __hash__(self) -> int:
        return hash((self._name, self._variable, hash(self._body)))
    
    # ========================
    # String Representation
    # ========================
    
    def __str__(self) -> str:
        return f"{self._name}({self._variable}) = {self._body}"
    
    def __repr__(self) -> str:
        return f"Function('{self._name}', '{self._variable}', {self._body!r})"
    
    def format_definition(self) -> str:
        """Format as a function definition"""
        return f"{self._name}({self._variable}) = {self._body}"
    
    def format_body(self) -> str:
        """Format just the body expression"""
        return str(self._body)