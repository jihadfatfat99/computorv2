"""
Rational number implementation for Computorv2.

Represents numbers as fractions (numerator/denominator) to maintain
exact precision. Automatically reduces fractions to lowest terms.
"""

from __future__ import annotations
from typing import Any

from .base import (
    MathType,
    DivisionByZeroError,
    InvalidOperationError,
    InvalidExponentError,
)
from ..utils import gcd, is_approximately_zero, DECIMAL_PRECISION


class Rational(MathType):
    """
    Rational number represented as a fraction.
    
    Stores numerator and denominator as integers, always reduced
    to lowest terms with positive denominator.
    
    Examples:
        >>> Rational(3, 4)      # 3/4
        >>> Rational(6, 8)      # Automatically reduced to 3/4
        >>> Rational(5)         # 5/1 = 5
        >>> Rational.from_float(0.5)  # 1/2
    """
    
    __slots__ = ('_numerator', '_denominator')
    
    def __init__(self, numerator: int = 0, denominator: int = 1):
        """
        Create a Rational number.
        
        Args:
            numerator: The numerator (top of fraction)
            denominator: The denominator (bottom of fraction), must be non-zero
        
        Raises:
            DivisionByZeroError: If denominator is zero
        """
        if denominator == 0:
            raise DivisionByZeroError("Denominator cannot be zero")
        
        # Ensure denominator is positive
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        
        # Reduce to lowest terms
        common = gcd(numerator, denominator)
        self._numerator = numerator // common
        self._denominator = denominator // common
    
    # ========================
    # Properties
    # ========================
    
    @property
    def numerator(self) -> int:
        """Get the numerator"""
        return self._numerator
    
    @property
    def denominator(self) -> int:
        """Get the denominator"""
        return self._denominator
    
    @property
    def type_name(self) -> str:
        return "Rational"
    
    # ========================
    # Factory Methods
    # ========================
    
    @classmethod
    def from_float(cls, value: float, precision: int = DECIMAL_PRECISION) -> Rational:
        """
        Create a Rational from a floating point number.
        
        Args:
            value: The float value to convert
            precision: Number of decimal places to consider
        
        Returns:
            Rational approximation of the float
        
        Examples:
            >>> Rational.from_float(0.5)
            Rational(1, 2)
            >>> Rational.from_float(0.333, precision=3)
            Rational(333, 1000)
        """
        if is_approximately_zero(value):
            return cls(0, 1)
        
        # Handle negative values
        sign = 1 if value >= 0 else -1
        value = abs(value)
        
        # Convert to fraction using decimal precision
        scale = 10 ** precision
        numerator = round(value * scale)
        denominator = scale
        
        return cls(sign * numerator, denominator)
    
    @classmethod
    def from_int(cls, value: int) -> Rational:
        """Create a Rational from an integer"""
        return cls(value, 1)
    
    @classmethod
    def zero(cls) -> Rational:
        """Return rational zero (0/1)"""
        return cls(0, 1)
    
    @classmethod
    def one(cls) -> Rational:
        """Return rational one (1/1)"""
        return cls(1, 1)
    
    # ========================
    # Conversion Methods
    # ========================
    
    def to_float(self) -> float:
        """Convert to floating point"""
        return self._numerator / self._denominator
    
    def to_int(self) -> int:
        """
        Convert to integer (truncates toward zero).
        
        Raises:
            InvalidOperationError: If not a whole number
        """
        if self._denominator != 1:
            raise InvalidOperationError(
                f"Cannot convert {self} to integer: not a whole number"
            )
        return self._numerator
    
    def is_integer(self) -> bool:
        """Check if this rational is a whole number"""
        return self._denominator == 1
    
    # ========================
    # Type Properties
    # ========================
    
    def is_zero(self) -> bool:
        return self._numerator == 0
    
    def is_one(self) -> bool:
        return self._numerator == 1 and self._denominator == 1
    
    def is_negative(self) -> bool:
        """Check if value is negative"""
        return self._numerator < 0
    
    def is_positive(self) -> bool:
        """Check if value is positive"""
        return self._numerator > 0
    
    def copy(self) -> Rational:
        return Rational(self._numerator, self._denominator)
    
    # ========================
    # Arithmetic Operations
    # ========================
    
    def _ensure_rational(self, other: Any) -> Rational:
        """Convert other to Rational if possible"""
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational.from_int(other)
        if isinstance(other, float):
            return Rational.from_float(other)
        raise InvalidOperationError(
            f"Cannot perform operation between Rational and {type(other).__name__}"
        )
    
    def __add__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        # a/b + c/d = (ad + bc) / bd
        num = self._numerator * other._denominator + other._numerator * self._denominator
        den = self._denominator * other._denominator
        return Rational(num, den)
    
    def __radd__(self, other: Any) -> Rational:
        return self.__add__(other)
    
    def __sub__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        # a/b - c/d = (ad - bc) / bd
        num = self._numerator * other._denominator - other._numerator * self._denominator
        den = self._denominator * other._denominator
        return Rational(num, den)
    
    def __rsub__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        return other.__sub__(self)
    
    def __mul__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        # a/b * c/d = ac / bd
        num = self._numerator * other._numerator
        den = self._denominator * other._denominator
        return Rational(num, den)
    
    def __rmul__(self, other: Any) -> Rational:
        return self.__mul__(other)
    
    def __truediv__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        if other.is_zero():
            raise DivisionByZeroError("Cannot divide by zero")
        # a/b / c/d = ad / bc
        num = self._numerator * other._denominator
        den = self._denominator * other._numerator
        return Rational(num, den)
    
    def __rtruediv__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        return other.__truediv__(self)
    
    def __mod__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        if other.is_zero():
            raise DivisionByZeroError("Cannot compute modulo with zero")
        # a % b = a - b * floor(a / b)
        quotient = self / other
        floored = Rational(int(quotient.to_float() // 1), 1)
        return self - other * floored
    
    def __rmod__(self, other: Any) -> Rational:
        other = self._ensure_rational(other)
        return other.__mod__(self)
    
    def __pow__(self, other: Any) -> Rational:
        # Only non-negative integer exponents allowed
        if isinstance(other, Rational):
            if not other.is_integer():
                raise InvalidExponentError("Exponent must be an integer")
            exp = other.to_int()
        elif isinstance(other, int):
            exp = other
        elif isinstance(other, float):
            if not is_approximately_zero(other - round(other)):
                raise InvalidExponentError("Exponent must be an integer")
            exp = int(round(other))
        else:
            raise InvalidExponentError(
                f"Cannot use {type(other).__name__} as exponent"
            )
        
        if exp < 0:
            raise InvalidExponentError("Exponent must be non-negative")
        
        if exp == 0:
            return Rational.one()
        
        # Compute power
        num = self._numerator ** exp
        den = self._denominator ** exp
        return Rational(num, den)
    
    def __neg__(self) -> Rational:
        return Rational(-self._numerator, self._denominator)
    
    def __pos__(self) -> Rational:
        return self.copy()
    
    def __abs__(self) -> Rational:
        return Rational(abs(self._numerator), self._denominator)
    
    # ========================
    # Comparison Operations
    # ========================
    
    def __eq__(self, other: Any) -> bool:
        try:
            other = self._ensure_rational(other)
            return (
                self._numerator == other._numerator and
                self._denominator == other._denominator
            )
        except InvalidOperationError:
            return False
    
    def __lt__(self, other: Any) -> bool:
        other = self._ensure_rational(other)
        return self._numerator * other._denominator < other._numerator * self._denominator
    
    def __le__(self, other: Any) -> bool:
        return self == other or self < other
    
    def __gt__(self, other: Any) -> bool:
        other = self._ensure_rational(other)
        return self._numerator * other._denominator > other._numerator * self._denominator
    
    def __ge__(self, other: Any) -> bool:
        return self == other or self > other
    
    # ========================
    # Hashing
    # ========================
    
    def __hash__(self) -> int:
        return hash((self._numerator, self._denominator))
    
    # ========================
    # String Representation
    # ========================
    
    def __str__(self) -> str:
        if self._denominator == 1:
            return str(self._numerator)
        
        # Check if it's a clean decimal
        float_val = self.to_float()
        if abs(float_val - round(float_val, DECIMAL_PRECISION)) < 1e-15:
            # Format as decimal, strip trailing zeros
            formatted = f"{float_val:.{DECIMAL_PRECISION}f}".rstrip('0').rstrip('.')
            return formatted
        
        return str(self._numerator) if self._denominator == 1 else f"{self._numerator}/{self._denominator}"
    
    def __repr__(self) -> str:
        return f"Rational({self._numerator}, {self._denominator})"