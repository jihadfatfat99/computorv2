"""
Rational number formatting for Computorv2.

Handles display of rational numbers as integers, decimals, or fractions.
"""

from ..math_types import Rational
from ..utils import DECIMAL_PRECISION, is_approximately_zero


def format_rational(r: Rational, show_fraction: bool = False) -> str:
    """
    Format a Rational number for display.
    
    Args:
        r: The Rational to format
        show_fraction: If True, show as fraction (e.g., 3/4) instead of decimal
    
    Returns:
        Formatted string representation
    
    Examples:
        >>> format_rational(Rational(1, 2))
        '0.5'
        >>> format_rational(Rational(1, 2), show_fraction=True)
        '1/2'
        >>> format_rational(Rational(6, 1))
        '6'
    """
    # Zero case
    if r.is_zero():
        return "0"
    
    # Integer case (denominator is 1)
    if r.denominator == 1:
        return str(r.numerator)
    
    # Fraction display
    if show_fraction:
        return f"{r.numerator}/{r.denominator}"
    
    # Decimal display
    float_val = r.to_float()
    
    # Check if it's a clean integer
    if is_approximately_zero(float_val - round(float_val)):
        return str(int(round(float_val)))
    
    # Format as decimal
    formatted = f"{float_val:.{DECIMAL_PRECISION}f}"
    
    # Strip trailing zeros but keep at least one decimal place if not integer
    formatted = formatted.rstrip('0').rstrip('.')
    
    return formatted


def format_rational_signed(r: Rational, force_sign: bool = False) -> str:
    """
    Format a Rational with explicit sign handling.
    
    Args:
        r: The Rational to format
        force_sign: If True, show '+' for positive numbers
    
    Returns:
        Formatted string with sign
    
    Examples:
        >>> format_rational_signed(Rational(3, 1), force_sign=True)
        '+3'
        >>> format_rational_signed(Rational(-3, 1))
        '-3'
    """
    result = format_rational(r)
    
    if force_sign and r.is_positive():
        return f"+{result}"
    
    return result


def format_rational_coefficient(r: Rational, is_first: bool = True) -> tuple[str, str]:
    """
    Format a Rational as a coefficient (for polynomials).
    
    Returns the sign separately for proper formatting like "- 3x" vs "-3x".
    
    Args:
        r: The Rational coefficient
        is_first: Whether this is the first term (no leading sign for positive)
    
    Returns:
        Tuple of (sign_str, coefficient_str)
        sign_str is '', '+', or '-'
        coefficient_str is the absolute value formatted
    
    Examples:
        >>> format_rational_coefficient(Rational(3, 1), is_first=True)
        ('', '3')
        >>> format_rational_coefficient(Rational(-3, 1), is_first=True)
        ('-', '3')
        >>> format_rational_coefficient(Rational(3, 1), is_first=False)
        (' + ', '3')
        >>> format_rational_coefficient(Rational(-3, 1), is_first=False)
        (' - ', '3')
    """
    abs_r = Rational(abs(r.numerator), r.denominator)
    coeff_str = format_rational(abs_r)
    
    if r.is_negative():
        sign = "-" if is_first else " - "
    else:
        sign = "" if is_first else " + "
    
    return sign, coeff_str