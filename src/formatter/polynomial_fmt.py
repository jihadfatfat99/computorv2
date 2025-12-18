"""
Polynomial formatting for Computorv2.

Handles display of polynomials in standard mathematical notation.
"""

from ..math_types import Polynomial, Rational, Complex
from .rational_fmt import format_rational
from .complex_fmt import format_complex


def format_polynomial(p: Polynomial) -> str:
    """
    Format a Polynomial for display.
    
    Displays in standard form: ax^n + bx^(n-1) + ... + c
    
    Args:
        p: The Polynomial to format
    
    Returns:
        Formatted string representation
    
    Examples:
        >>> format_polynomial(Polynomial({2: Rational(1), 1: Rational(2), 0: Rational(1)}))
        'x^2 + 2 * x + 1'
        >>> format_polynomial(Polynomial({1: Rational(-1), 0: Rational(3)}))
        '-x + 3'
    """
    if p.is_zero():
        return "0"
    
    terms = []
    variable = p.variable
    
    # Sort degrees in descending order
    degrees = sorted(p.coefficients.keys(), reverse=True)
    
    for i, degree in enumerate(degrees):
        coeff = p.get_coefficient(degree)
        
        if coeff.is_zero():
            continue
        
        is_first = (i == 0) or len(terms) == 0
        term_str = _format_term(coeff, degree, variable, is_first)
        
        if term_str:
            terms.append(term_str)
    
    if not terms:
        return "0"
    
    return "".join(terms)


def _format_term(coeff, degree: int, variable: str, is_first: bool) -> str:
    """
    Format a single polynomial term.
    
    Args:
        coeff: The coefficient (Rational or Complex)
        degree: The power of the variable
        variable: The variable name
        is_first: Whether this is the first term
    
    Returns:
        Formatted term string
    """
    # Determine sign and absolute coefficient
    if isinstance(coeff, Rational):
        is_negative = coeff.is_negative()
        abs_coeff = Rational(abs(coeff.numerator), coeff.denominator)
        coeff_str = format_rational(abs_coeff)
        is_one = abs_coeff.is_one()
    elif isinstance(coeff, Complex):
        # Complex coefficients need parentheses if not purely real
        if coeff.is_real():
            is_negative = coeff.real.is_negative()
            abs_coeff = Complex(Rational(abs(coeff.real.numerator), coeff.real.denominator), Rational.zero())
            coeff_str = format_rational(abs_coeff.real)
            is_one = abs_coeff.real.is_one()
        else:
            # Complex with imaginary part - wrap in parentheses
            is_negative = False
            coeff_str = f"({format_complex(coeff)})"
            is_one = False
    else:
        is_negative = False
        coeff_str = str(coeff)
        is_one = False
    
    # Build sign string
    if is_first:
        sign = "-" if is_negative else ""
    else:
        sign = " - " if is_negative else " + "
    
    # Build term string based on degree
    if degree == 0:
        # Constant term
        return f"{sign}{coeff_str}"
    elif degree == 1:
        # Linear term
        if is_one:
            return f"{sign}{variable}"
        else:
            return f"{sign}{coeff_str} * {variable}"
    else:
        # Higher degree term
        if is_one:
            return f"{sign}{variable}^{degree}"
        else:
            return f"{sign}{coeff_str} * {variable}^{degree}"


def format_polynomial_equation(p: Polynomial, rhs: str = "0") -> str:
    """
    Format a Polynomial as an equation.
    
    Args:
        p: The Polynomial (left side)
        rhs: The right-hand side
    
    Returns:
        Equation string
    
    Examples:
        >>> format_polynomial_equation(poly, "0")
        'x^2 + 2 * x + 1 = 0'
    """
    return f"{format_polynomial(p)} = {rhs}"


def format_polynomial_factored(factors: list, variable: str = "x") -> str:
    """
    Format a factored polynomial.
    
    Args:
        factors: List of roots/factors
        variable: The variable name
    
    Returns:
        Factored form string
    
    Examples:
        >>> format_polynomial_factored([Rational(1), Rational(2)])
        '(x - 1)(x - 2)'
    """
    if not factors:
        return "1"
    
    parts = []
    for root in factors:
        if isinstance(root, Rational):
            if root.is_zero():
                parts.append(f"{variable}")
            elif root.is_negative():
                parts.append(f"({variable} + {format_rational(-root)})")
            else:
                parts.append(f"({variable} - {format_rational(root)})")
        elif isinstance(root, Complex):
            parts.append(f"({variable} - ({format_complex(root)}))")
        else:
            parts.append(f"({variable} - {root})")
    
    return "".join(parts)


def format_polynomial_degree(p: Polynomial) -> str:
    """
    Format polynomial with degree information.
    
    Args:
        p: The Polynomial
    
    Returns:
        String with degree info
    """
    return f"{format_polynomial(p)} (degree {p.degree})"