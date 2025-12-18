"""
Polynomial simplification for Computorv2.

Handles simplification of polynomial expressions:
- Combining like terms
- Reducing to standard form
- Extracting common factors
- Converting to reduced form for equation solving
"""

from typing import Dict, Tuple
from ..math_types import Rational, Complex, Polynomial
from ..utils import gcd


def simplify_polynomial(poly: Polynomial) -> Polynomial:
    """
    Simplify a polynomial to canonical form.
    
    Operations:
    - Remove zero coefficients
    - Ensure coefficients are in lowest terms (for Rational)
    - Order by degree (handled internally by Polynomial)
    
    Args:
        poly: Polynomial to simplify
    
    Returns:
        Simplified polynomial
    """
    new_coeffs: Dict[int, Rational | Complex] = {}
    
    for degree, coeff in poly.coefficients.items():
        if not _is_zero(coeff):
            new_coeffs[degree] = coeff
    
    if not new_coeffs:
        return Polynomial.zero(poly.variable)
    
    return Polynomial(new_coeffs, poly.variable)


def reduce_polynomial(poly: Polynomial) -> Polynomial:
    """
    Reduce polynomial by extracting common factors from coefficients.
    
    For polynomials with Rational coefficients, divides all coefficients
    by their GCD to get smallest integer coefficients.
    
    Example:
        2x^2 + 4x + 2 -> x^2 + 2x + 1 (divide by 2)
    
    Args:
        poly: Polynomial to reduce
    
    Returns:
        Reduced polynomial
    """
    if poly.is_zero():
        return poly
    
    coeffs = list(poly.coefficients.values())
    if not all(isinstance(c, Rational) for c in coeffs):
        return simplify_polynomial(poly)
    
    numerators = [c.numerator for c in coeffs]
    
    num_gcd = numerators[0]
    for n in numerators[1:]:
        num_gcd = gcd(num_gcd, n)
    
    if num_gcd == 0:
        return Polynomial.zero(poly.variable)
    
    new_coeffs = {}
    for degree, coeff in poly.coefficients.items():
        new_num = coeff.numerator // num_gcd
        new_coeffs[degree] = Rational(new_num, coeff.denominator)
    
    return Polynomial(new_coeffs, poly.variable)


def normalize_polynomial(poly: Polynomial) -> Polynomial:
    """
    Normalize polynomial so leading coefficient is positive.
    
    Args:
        poly: Polynomial to normalize
    
    Returns:
        Normalized polynomial (multiplied by -1 if leading coeff was negative)
    """
    if poly.is_zero():
        return poly
    
    leading = poly.leading_coefficient()
    
    if isinstance(leading, Rational):
        if leading.numerator < 0:
            return -poly
    elif isinstance(leading, Complex):
        if leading.real.numerator < 0:
            return -poly
        if leading.real.numerator == 0 and leading.imag.numerator < 0:
            return -poly
    
    return poly


def make_monic(poly: Polynomial) -> Tuple[Polynomial, Rational | Complex]:
    """
    Make polynomial monic (leading coefficient = 1).
    
    Args:
        poly: Polynomial to make monic
    
    Returns:
        Tuple of (monic polynomial, original leading coefficient)
    """
    if poly.is_zero():
        return poly, Rational(1)
    
    leading = poly.leading_coefficient()
    
    if isinstance(leading, Rational) and leading == Rational(1):
        return poly, Rational(1)
    if isinstance(leading, Complex) and leading == Complex(Rational(1), Rational(0)):
        return poly, Complex(Rational(1), Rational(0))
    
    monic_poly = poly / leading
    
    return monic_poly, leading


def polynomial_to_standard_form(poly: Polynomial) -> Polynomial:
    """
    Convert polynomial to standard form for equation solving.
    
    Standard form: all terms on left side, zero on right.
    This function simplifies and normalizes the polynomial.
    
    Args:
        poly: Polynomial to convert
    
    Returns:
        Polynomial in standard form
    """
    result = simplify_polynomial(poly)
    result = normalize_polynomial(result)
    
    return result


def subtract_polynomials(left: Polynomial, right: Polynomial) -> Polynomial:
    """
    Subtract two polynomials: left - right.
    
    Used for converting equations to standard form: ax² + bx + c = d
    becomes ax² + bx + (c-d) = 0
    
    Args:
        left: Left polynomial
        right: Right polynomial
    
    Returns:
        Difference polynomial
    """
    return simplify_polynomial(left - right)


def equation_to_standard_form(left: Polynomial, right: Polynomial) -> Polynomial:
    """
    Convert equation left = right to standard form (left - right = 0).
    
    Args:
        left: Left side of equation
        right: Right side of equation
    
    Returns:
        Polynomial representing left - right (should equal 0)
    """
    result = subtract_polynomials(left, right)
    result = normalize_polynomial(result)
    
    return result


def extract_coefficients(poly: Polynomial) -> Dict[int, Rational | Complex]:
    """
    Extract coefficients from polynomial in a clean format.
    
    Missing degrees are filled with zero.
    
    Args:
        poly: Polynomial to extract from
    
    Returns:
        Dict mapping degree -> coefficient (including zeros)
    """
    if poly.is_zero():
        return {0: Rational(0)}
    
    max_degree = poly.degree
    result = {}
    
    for d in range(max_degree + 1):
        result[d] = poly.get_coefficient(d)
    
    return result


def _is_zero(value: Rational | Complex) -> bool:
    """Check if a coefficient is zero."""
    if isinstance(value, Rational):
        return value.numerator == 0
    if isinstance(value, Complex):
        return value.real.numerator == 0 and value.imag.numerator == 0
    return False