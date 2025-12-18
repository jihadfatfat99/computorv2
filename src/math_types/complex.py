"""
Complex number implementation for Computorv2.

Represents complex numbers as a + bi where both a (real) and b (imaginary)
are Rational numbers. This is a custom implementation - no native complex
types are used as per project requirements.
"""

from __future__ import annotations
from typing import Any, Union

from .base import (
    MathType,
    DivisionByZeroError,
    InvalidOperationError,
    InvalidExponentError,
)
from .rational import Rational


class Complex(MathType):
    """
    Complex number with Rational coefficients.
    
    Represents numbers of the form a + bi where:
        - a is the real part (Rational)
        - b is the imaginary part (Rational)
        - i is the imaginary unit (i² = -1)
    
    Examples:
        >>> Complex(Rational(3), Rational(2))    # 3 + 2i
        >>> Complex.from_real(5)                  # 5 + 0i
        >>> Complex.from_imaginary(3)             # 0 + 3i
        >>> Complex.i()                           # 0 + 1i
    """
    
    __slots__ = ('_real', '_imag')
    
    def __init__(self, real: Rational = None, imag: Rational = None):
        """
        Create a Complex number.
        
        Args:
            real: The real part (defaults to 0)
            imag: The imaginary part (defaults to 0)
        """
        self._real = real if real is not None else Rational.zero()
        self._imag = imag if imag is not None else Rational.zero()
        
        # Ensure both parts are Rational
        if not isinstance(self._real, Rational):
            self._real = self._to_rational(self._real)
        if not isinstance(self._imag, Rational):
            self._imag = self._to_rational(self._imag)
    
    @staticmethod
    def _to_rational(value: Any) -> Rational:
        """Convert a value to Rational"""
        if isinstance(value, Rational):
            return value
        if isinstance(value, int):
            return Rational.from_int(value)
        if isinstance(value, float):
            return Rational.from_float(value)
        raise InvalidOperationError(f"Cannot convert {type(value).__name__} to Rational")
    
    # ========================
    # Properties
    # ========================
    
    @property
    def real(self) -> Rational:
        """Get the real part"""
        return self._real
    
    @property
    def imag(self) -> Rational:
        """Get the imaginary part"""
        return self._imag
    
    @property
    def type_name(self) -> str:
        return "Complex"
    
    # ========================
    # Factory Methods
    # ========================
    
    @classmethod
    def from_real(cls, value: Union[int, float, Rational]) -> Complex:
        """Create a Complex number from a real value (imaginary part = 0)"""
        real = cls._to_rational(value)
        return cls(real, Rational.zero())
    
    @classmethod
    def from_imaginary(cls, value: Union[int, float, Rational]) -> Complex:
        """Create a Complex number from an imaginary value (real part = 0)"""
        imag = cls._to_rational(value)
        return cls(Rational.zero(), imag)
    
    @classmethod
    def from_rational(cls, rational: Rational) -> Complex:
        """Create a Complex number from a Rational (imaginary part = 0)"""
        return cls(rational, Rational.zero())
    
    @classmethod
    def i(cls) -> Complex:
        """Return the imaginary unit i"""
        return cls(Rational.zero(), Rational.one())
    
    @classmethod
    def zero(cls) -> Complex:
        """Return complex zero (0 + 0i)"""
        return cls(Rational.zero(), Rational.zero())
    
    @classmethod
    def one(cls) -> Complex:
        """Return complex one (1 + 0i)"""
        return cls(Rational.one(), Rational.zero())
    
    # ========================
    # Type Properties
    # ========================
    
    def is_zero(self) -> bool:
        return self._real.is_zero() and self._imag.is_zero()
    
    def is_one(self) -> bool:
        return self._real.is_one() and self._imag.is_zero()
    
    def is_real(self) -> bool:
        """Check if this is a real number (imaginary part = 0)"""
        return self._imag.is_zero()
    
    def is_imaginary(self) -> bool:
        """Check if this is purely imaginary (real part = 0)"""
        return self._real.is_zero() and not self._imag.is_zero()
    
    def to_rational(self) -> Rational:
        """
        Convert to Rational if purely real.
        
        Raises:
            InvalidOperationError: If imaginary part is non-zero
        """
        if not self.is_real():
            raise InvalidOperationError(
                f"Cannot convert {self} to Rational: has non-zero imaginary part"
            )
        return self._real.copy()
    
    def copy(self) -> Complex:
        return Complex(self._real.copy(), self._imag.copy())
    
    # ========================
    # Complex Operations
    # ========================
    
    def conjugate(self) -> Complex:
        """Return the complex conjugate (a - bi)"""
        return Complex(self._real.copy(), -self._imag)
    
    def magnitude_squared(self) -> Rational:
        """Return |z|² = a² + b² (avoids square root)"""
        return self._real * self._real + self._imag * self._imag
    
    def inverse(self) -> Complex:
        """
        Return the multiplicative inverse 1/z.
        
        1/(a + bi) = (a - bi) / (a² + b²)
        """
        if self.is_zero():
            raise DivisionByZeroError("Cannot compute inverse of zero")
        
        mag_sq = self.magnitude_squared()
        return Complex(self._real / mag_sq, -self._imag / mag_sq)
    
    # ========================
    # Arithmetic Operations
    # ========================
    
    def _ensure_complex(self, other: Any) -> Complex:
        """Convert other to Complex if possible"""
        if isinstance(other, Complex):
            return other
        if isinstance(other, Rational):
            return Complex.from_rational(other)
        if isinstance(other, (int, float)):
            return Complex.from_real(other)
        raise InvalidOperationError(
            f"Cannot perform operation between Complex and {type(other).__name__}"
        )
    
    def __add__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        return Complex(
            self._real + other._real,
            self._imag + other._imag
        )
    
    def __radd__(self, other: Any) -> Complex:
        return self.__add__(other)
    
    def __sub__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        return Complex(
            self._real - other._real,
            self._imag - other._imag
        )
    
    def __rsub__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        return other.__sub__(self)
    
    def __mul__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        real = self._real * other._real - self._imag * other._imag
        imag = self._real * other._imag + self._imag * other._real
        return Complex(real, imag)
    
    def __rmul__(self, other: Any) -> Complex:
        return self.__mul__(other)
    
    def __truediv__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        if other.is_zero():
            raise DivisionByZeroError("Cannot divide by zero")
        
        # (a + bi) / (c + di) = (a + bi) * (c - di) / (c² + d²)
        conjugate = other.conjugate()
        numerator = self * conjugate
        denominator = other.magnitude_squared()
        
        return Complex(
            numerator._real / denominator,
            numerator._imag / denominator
        )
    
    def __rtruediv__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        return other.__truediv__(self)
    
    def __mod__(self, other: Any) -> Complex:
        # Modulo is not well-defined for complex numbers
        # We'll implement it only for real complex numbers
        if not self.is_real():
            raise InvalidOperationError("Modulo is not defined for complex numbers")
        other = self._ensure_complex(other)
        if not other.is_real():
            raise InvalidOperationError("Modulo is not defined for complex numbers")
        
        return Complex.from_rational(self._real % other._real)
    
    def __rmod__(self, other: Any) -> Complex:
        other = self._ensure_complex(other)
        return other.__mod__(self)
    
    def __pow__(self, other: Any) -> Complex:
        # Only non-negative integer exponents allowed
        if isinstance(other, Complex):
            if not other.is_real():
                raise InvalidExponentError("Exponent must be a real number")
            exp_rational = other._real
        elif isinstance(other, Rational):
            exp_rational = other
        elif isinstance(other, int):
            exp_rational = Rational.from_int(other)
        elif isinstance(other, float):
            exp_rational = Rational.from_float(other)
        else:
            raise InvalidExponentError(
                f"Cannot use {type(other).__name__} as exponent"
            )
        
        if not exp_rational.is_integer():
            raise InvalidExponentError("Exponent must be an integer")
        
        exp = exp_rational.to_int()
        
        if exp < 0:
            raise InvalidExponentError("Exponent must be non-negative")
        
        if exp == 0:
            return Complex.one()
        
        # Compute power by repeated multiplication
        result = Complex.one()
        base = self.copy()
        
        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            base = base * base
            exp //= 2
        
        return result
    
    def __neg__(self) -> Complex:
        return Complex(-self._real, -self._imag)
    
    def __pos__(self) -> Complex:
        return self.copy()
    
    # ========================
    # Comparison Operations
    # ========================
    
    def __eq__(self, other: Any) -> bool:
        try:
            other = self._ensure_complex(other)
            return self._real == other._real and self._imag == other._imag
        except InvalidOperationError:
            return False
    
    # ========================
    # Hashing
    # ========================
    
    def __hash__(self) -> int:
        return hash((hash(self._real), hash(self._imag)))
    
    # ========================
    # String Representation
    # ========================
    
    def __str__(self) -> str:
        real_zero = self._real.is_zero()
        imag_zero = self._imag.is_zero()
        
        # 0 + 0i -> 0
        if real_zero and imag_zero:
            return "0"
        
        # a + 0i -> a
        if imag_zero:
            return str(self._real)
        
        # 0 + bi -> bi
        if real_zero:
            if self._imag.is_one():
                return "i"
            if self._imag == Rational(-1, 1):
                return "-i"
            return f"{self._imag}i"
        
        # a + bi (general case)
        real_str = str(self._real)
        
        if self._imag.is_one():
            imag_str = "i"
        elif self._imag == Rational(-1, 1):
            imag_str = "-i"
        elif self._imag.is_negative():
            imag_str = f"{self._imag}i"
        else:
            imag_str = f"{self._imag}i"
        
        # Format with proper sign
        if self._imag.is_negative():
            return f"{real_str} - {str(-self._imag)}i"
        else:
            return f"{real_str} + {imag_str}"
    
    def __repr__(self) -> str:
        return f"Complex({repr(self._real)}, {repr(self._imag)})"