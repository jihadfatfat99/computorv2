"""
Type coercion and promotion for Computorv2.

Handles implicit type conversion between mathematical types.
Type hierarchy: int/float -> Rational -> Complex
"""

from typing import Any, Tuple, Union
from ..math_types import Rational, Complex, Matrix, Polynomial, Function


# Type alias for numeric types
Numeric = Union[int, float, Rational, Complex]
Value = Union[Rational, Complex, Matrix, Polynomial, Function]


def to_rational(value: Any) -> Rational:
    """
    Convert a value to Rational.
    
    Args:
        value: Value to convert (int, float, or Rational)
    
    Returns:
        Rational representation
    
    Raises:
        TypeError: If conversion not possible
    """
    if isinstance(value, Rational):
        return value
    if isinstance(value, int):
        return Rational.from_int(value)
    if isinstance(value, float):
        return Rational.from_float(value)
    if isinstance(value, Complex):
        if value.is_real():
            return value.real
        raise TypeError(f"Cannot convert complex {value} to Rational")
    
    raise TypeError(f"Cannot convert {type(value).__name__} to Rational")


def to_complex(value: Any) -> Complex:
    """
    Convert a value to Complex.
    
    Args:
        value: Value to convert
    
    Returns:
        Complex representation
    
    Raises:
        TypeError: If conversion not possible
    """
    if isinstance(value, Complex):
        return value
    if isinstance(value, Rational):
        return Complex.from_rational(value)
    if isinstance(value, int):
        return Complex.from_real(value)
    if isinstance(value, float):
        return Complex.from_real(value)
    
    raise TypeError(f"Cannot convert {type(value).__name__} to Complex")


def coerce_numeric(left: Numeric, right: Numeric) -> Tuple[Numeric, Numeric]:
    """
    Coerce two numeric values to a common type.
    
    Type promotion: int/float -> Rational -> Complex
    
    Args:
        left: First value
        right: Second value
    
    Returns:
        Tuple of (left, right) coerced to common type
    """
    # If either is Complex, promote both to Complex
    if isinstance(left, Complex) or isinstance(right, Complex):
        return to_complex(left), to_complex(right)
    
    # Otherwise promote to Rational
    return to_rational(left), to_rational(right)


def get_type_name(value: Any) -> str:
    """Get human-readable type name."""
    if isinstance(value, Rational):
        return "Rational"
    if isinstance(value, Complex):
        return "Complex"
    if isinstance(value, Matrix):
        return "Matrix"
    if isinstance(value, Polynomial):
        return "Polynomial"
    if isinstance(value, Function):
        return "Function"
    if isinstance(value, int):
        return "Integer"
    if isinstance(value, float):
        return "Float"
    return type(value).__name__


def is_numeric(value: Any) -> bool:
    """Check if value is a numeric type."""
    return isinstance(value, (int, float, Rational, Complex))


def is_scalar(value: Any) -> bool:
    """Check if value is a scalar (not matrix/polynomial/function)."""
    return isinstance(value, (int, float, Rational, Complex))


def is_math_type(value: Any) -> bool:
    """Check if value is one of our math types."""
    return isinstance(value, (Rational, Complex, Matrix, Polynomial, Function))


def can_coerce_to_rational(value: Any) -> bool:
    """Check if value can be converted to Rational."""
    if isinstance(value, (int, float, Rational)):
        return True
    if isinstance(value, Complex):
        return value.is_real()
    return False


def simplify_complex(value: Complex) -> Rational | Complex:
    """
    Simplify a Complex to Rational if purely real.
    
    Args:
        value: Complex number
    
    Returns:
        Rational if imaginary part is zero, otherwise Complex
    """
    if value.is_real():
        return value.real
    return value


def simplify_result(value: Any) -> Value:
    """
    Simplify a computation result.
    
    - Convert int/float to Rational
    - Convert purely real Complex to Rational
    - Leave other types as-is
    """
    if isinstance(value, int):
        return Rational.from_int(value)
    
    if isinstance(value, float):
        return Rational.from_float(value)
    
    if isinstance(value, Complex):
        return simplify_complex(value)
    
    return value