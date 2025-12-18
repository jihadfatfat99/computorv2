"""
Complex number formatting for Computorv2.

Handles display of complex numbers in the form a + bi.
"""

from ..math_types import Complex, Rational
from .rational_fmt import format_rational


def format_complex(c: Complex) -> str:
    """
    Format a Complex number for display.
    
    Handles special cases:
        - Pure real: just show real part
        - Pure imaginary: show as bi
        - Zero imaginary coefficient: show as a
        - Unit imaginary: show as i, not 1i
    
    Args:
        c: The Complex number to format
    
    Returns:
        Formatted string representation
    
    Examples:
        >>> format_complex(Complex(Rational(3), Rational(2)))
        '3 + 2i'
        >>> format_complex(Complex(Rational(3), Rational(-2)))
        '3 - 2i'
        >>> format_complex(Complex(Rational(0), Rational(1)))
        'i'
        >>> format_complex(Complex(Rational(5), Rational(0)))
        '5'
    """
    real_zero = c.real.is_zero()
    imag_zero = c.imag.is_zero()
    
    # 0 + 0i -> 0
    if real_zero and imag_zero:
        return "0"
    
    # a + 0i -> a
    if imag_zero:
        return format_rational(c.real)
    
    # 0 + bi -> bi
    if real_zero:
        return _format_imaginary_part(c.imag, is_standalone=True)
    
    # a + bi (general case)
    real_str = format_rational(c.real)
    imag_str = _format_imaginary_part(c.imag, is_standalone=False)
    
    return f"{real_str}{imag_str}"


def _format_imaginary_part(imag: Rational, is_standalone: bool) -> str:
    """
    Format the imaginary part of a complex number.
    
    Args:
        imag: The imaginary coefficient
        is_standalone: If True, format as standalone (e.g., "2i" vs " + 2i")
    
    Returns:
        Formatted imaginary part string
    """
    if imag.is_zero():
        return ""
    
    is_negative = imag.is_negative()
    abs_imag = Rational(abs(imag.numerator), imag.denominator)
    
    # Handle unit coefficient
    if abs_imag.is_one():
        coeff_str = ""
    else:
        coeff_str = format_rational(abs_imag)
    
    if is_standalone:
        if is_negative:
            return f"-{coeff_str}i"
        else:
            return f"{coeff_str}i"
    else:
        if is_negative:
            if coeff_str:
                return f" - {coeff_str}i"
            else:
                return " - i"
        else:
            if coeff_str:
                return f" + {coeff_str}i"
            else:
                return " + i"


def format_complex_polar(c: Complex) -> str:
    """
    Format a Complex number in polar form r * e^(i*theta).
    
    Note: This requires computing magnitude and angle, which
    involves square roots and trigonometry (bonus feature).
    
    Args:
        c: The Complex number to format
    
    Returns:
        Polar form string (simplified, without actual computation)
    """
    # For now, just return rectangular form
    # Polar form would require sqrt and atan2 (bonus)
    return format_complex(c)


def format_complex_as_solution(c: Complex, variable: str = "x") -> str:
    """
    Format a Complex number as an equation solution.
    
    Args:
        c: The solution value
        variable: The variable name
    
    Returns:
        Formatted solution string
    
    Examples:
        >>> format_complex_as_solution(Complex(Rational(3), Rational(2)))
        'x = 3 + 2i'
    """
    return f"{variable} = {format_complex(c)}"