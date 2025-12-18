"""
Square root implementation for Computorv2 solver.

Implements square root for Rational numbers using Newton's method,
without using any math library functions.
"""

from ..math_types import Rational, Complex
from ..utils import EPSILON


def sqrt_rational(value: Rational) -> Rational | Complex:
    """
    Compute square root of a Rational number.
    
    Uses Newton's method (Babylonian method) for positive numbers.
    Returns Complex for negative numbers.
    
    Args:
        value: Rational number
    
    Returns:
        Rational if value >= 0, Complex if value < 0
    """
    # Handle zero
    if value.numerator == 0:
        return Rational.zero()
    
    # Handle negative numbers -> complex result
    if value.numerator < 0:
        # sqrt(-x) = i * sqrt(x)
        positive_sqrt = sqrt_rational(-value)
        if isinstance(positive_sqrt, Rational):
            return Complex(Rational.zero(), positive_sqrt)
        else:
            # Should not happen for real input
            raise ValueError("Unexpected complex result for positive value")
    
    # Positive number: use Newton's method
    # Convert to float for iteration, then convert back
    x = value.to_float()
    
    # Initial guess
    guess = x / 2 if x > 1 else x
    if guess == 0:
        guess = 1.0
    
    # Newton's method: x_new = (x + n/x) / 2
    max_iterations = 100
    for _ in range(max_iterations):
        new_guess = (guess + x / guess) / 2
        if abs(new_guess - guess) < EPSILON:
            break
        guess = new_guess
    
    # Convert back to Rational
    return Rational.from_float(guess)


def sqrt_complex(value: Complex) -> Complex:
    """
    Compute square root of a Complex number.
    
    For z = a + bi, sqrt(z) = sqrt((|z| + a) / 2) + i * sign(b) * sqrt((|z| - a) / 2)
    
    Args:
        value: Complex number
    
    Returns:
        Complex square root (principal root)
    """
    a = value.real
    b = value.imag
    
    # If purely real, use rational sqrt
    if b.numerator == 0:
        result = sqrt_rational(a)
        if isinstance(result, Complex):
            return result
        return Complex.from_rational(result)
    
    # Compute |z| = sqrt(a² + b²)
    a_squared = a * a
    b_squared = b * b
    magnitude_squared = a_squared + b_squared
    magnitude = sqrt_rational(magnitude_squared)
    
    if isinstance(magnitude, Complex):
        # Should not happen for real a² + b²
        raise ValueError("Unexpected complex magnitude")
    
    # real_part = sqrt((|z| + a) / 2)
    real_part_squared = (magnitude + a) / Rational(2)
    real_part = sqrt_rational(real_part_squared)
    
    if isinstance(real_part, Complex):
        real_part = real_part.real  # Take real part
    
    # imag_part = sign(b) * sqrt((|z| - a) / 2)
    imag_part_squared = (magnitude - a) / Rational(2)
    imag_part = sqrt_rational(imag_part_squared)
    
    if isinstance(imag_part, Complex):
        imag_part = imag_part.real  # Take real part
    
    # Apply sign of b
    if b.numerator < 0:
        imag_part = -imag_part
    
    return Complex(real_part, imag_part)


def sqrt_value(value: Rational | Complex) -> Rational | Complex:
    """
    Compute square root of a Rational or Complex value.
    
    Args:
        value: Rational or Complex number
    
    Returns:
        Square root (Rational, or Complex if needed)
    """
    if isinstance(value, Complex):
        result = sqrt_complex(value)
        # Simplify to Rational if purely real
        if result.is_real():
            return result.real
        return result
    else:
        return sqrt_rational(value)