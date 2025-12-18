"""
Abstract base class for all mathematical types in Computorv2.

All custom types (Rational, Complex, Matrix, Polynomial, Function)
must inherit from this base and implement the required interface.
"""

from abc import ABC, abstractmethod
from typing import Any


class MathType(ABC):
    """
    Abstract base class defining the interface for mathematical types.
    
    All mathematical types must support:
        - Arithmetic operations (+, -, *, /, %, ^)
        - Equality comparison
        - String representation
        - Type identification
    """
    
    # ========================
    # Arithmetic Operations
    # ========================
    
    @abstractmethod
    def __add__(self, other: Any) -> 'MathType':
        """Addition: self + other"""
        pass
    
    @abstractmethod
    def __radd__(self, other: Any) -> 'MathType':
        """Reverse addition: other + self"""
        pass
    
    @abstractmethod
    def __sub__(self, other: Any) -> 'MathType':
        """Subtraction: self - other"""
        pass
    
    @abstractmethod
    def __rsub__(self, other: Any) -> 'MathType':
        """Reverse subtraction: other - self"""
        pass
    
    @abstractmethod
    def __mul__(self, other: Any) -> 'MathType':
        """Multiplication: self * other"""
        pass
    
    @abstractmethod
    def __rmul__(self, other: Any) -> 'MathType':
        """Reverse multiplication: other * self"""
        pass
    
    @abstractmethod
    def __truediv__(self, other: Any) -> 'MathType':
        """Division: self / other"""
        pass
    
    @abstractmethod
    def __rtruediv__(self, other: Any) -> 'MathType':
        """Reverse division: other / self"""
        pass
    
    @abstractmethod
    def __mod__(self, other: Any) -> 'MathType':
        """Modulo: self % other"""
        pass
    
    @abstractmethod
    def __rmod__(self, other: Any) -> 'MathType':
        """Reverse modulo: other % self"""
        pass
    
    @abstractmethod
    def __pow__(self, other: Any) -> 'MathType':
        """Power: self ^ other (non-negative integer exponent)"""
        pass
    
    @abstractmethod
    def __neg__(self) -> 'MathType':
        """Negation: -self"""
        pass
    
    @abstractmethod
    def __pos__(self) -> 'MathType':
        """Positive: +self"""
        pass
    
    # ========================
    # Comparison Operations
    # ========================
    
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Equality comparison"""
        pass
    
    def __ne__(self, other: Any) -> bool:
        """Inequality comparison"""
        return not self.__eq__(other)
    
    # ========================
    # Type Properties
    # ========================
    
    @abstractmethod
    def is_zero(self) -> bool:
        """Check if value is zero"""
        pass
    
    @abstractmethod
    def is_one(self) -> bool:
        """Check if value is one"""
        pass
    
    @classmethod
    @abstractmethod
    def zero(cls) -> 'MathType':
        """Return the zero element of this type"""
        pass
    
    @classmethod
    @abstractmethod
    def one(cls) -> 'MathType':
        """Return the one element of this type"""
        pass
    
    @abstractmethod
    def copy(self) -> 'MathType':
        """Return a deep copy of this value"""
        pass
    
    # ========================
    # String Representation
    # ========================
    
    @abstractmethod
    def __str__(self) -> str:
        """Human-readable string representation"""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation"""
        pass
    
    # ========================
    # Type Identification
    # ========================
    
    @property
    @abstractmethod
    def type_name(self) -> str:
        """Return the type name as a string"""
        pass
    
    def is_rational(self) -> bool:
        """Check if this is a Rational type"""
        return self.type_name == "Rational"
    
    def is_complex(self) -> bool:
        """Check if this is a Complex type"""
        return self.type_name == "Complex"
    
    def is_matrix(self) -> bool:
        """Check if this is a Matrix type"""
        return self.type_name == "Matrix"
    
    def is_polynomial(self) -> bool:
        """Check if this is a Polynomial type"""
        return self.type_name == "Polynomial"
    
    def is_function(self) -> bool:
        """Check if this is a Function type"""
        return self.type_name == "Function"


class MathTypeError(Exception):
    """Base exception for mathematical type errors"""
    pass


class DivisionByZeroError(MathTypeError):
    """Raised when attempting to divide by zero"""
    pass


class InvalidOperationError(MathTypeError):
    """Raised when an operation is not supported between types"""
    pass


class DimensionMismatchError(MathTypeError):
    """Raised when matrix dimensions don't match for an operation"""
    pass


class InvalidExponentError(MathTypeError):
    """Raised when exponent is invalid (negative or non-integer)"""
    pass