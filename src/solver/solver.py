"""
Equation solver for Computorv2.

Solves polynomial equations of degree 0, 1, and 2.
"""

from typing import Tuple

from ..math_types import Rational, Complex, Polynomial
from ..simplifier import SimplifiedEquation, simplify_equation, get_reduced_form
from .errors import NoSolutionError, InfiniteSolutionsError, UnsolvableEquationError
from .solution import (
    Solution, SolutionType, SolutionValue,
    no_solution, infinite_solutions, single_solution,
    double_solution, two_real_solutions, two_complex_solutions
)
from .sqrt import sqrt_value


def solve(equation: SimplifiedEquation) -> Solution:
    """
    Solve a simplified equation.
    
    Args:
        equation: SimplifiedEquation from simplifier module
    
    Returns:
        Solution object containing roots and metadata
    
    Raises:
        UnsolvableEquationError: If degree > 2
    """
    if not equation.is_valid:
        raise UnsolvableEquationError(equation.degree)
    
    reduced_form = get_reduced_form(equation)
    variable = equation.variable
    
    if equation.degree == 0:
        return _solve_degree_0(equation, reduced_form, variable)
    elif equation.degree == 1:
        return _solve_degree_1(equation, reduced_form, variable)
    elif equation.degree == 2:
        return _solve_degree_2(equation, reduced_form, variable)
    else:
        raise UnsolvableEquationError(equation.degree)


def solve_equation(left: Polynomial, right: Polynomial) -> Solution:
    """
    Solve an equation given left and right polynomials.
    
    Convenience function that simplifies then solves.
    
    Args:
        left: Left side polynomial
        right: Right side polynomial
    
    Returns:
        Solution object
    """
    equation = simplify_equation(left, right)
    return solve(equation)


def _solve_degree_0(
    eq: SimplifiedEquation, 
    reduced_form: str, 
    variable: str
) -> Solution:
    """
    Solve degree 0 equation: c = 0
    
    - If c == 0: infinite solutions (0 = 0)
    - If c != 0: no solution (c = 0 is false)
    """
    c = eq.c
    
    # Check if c is zero
    is_zero = False
    if isinstance(c, Rational):
        is_zero = c.numerator == 0
    elif isinstance(c, Complex):
        is_zero = c.real.numerator == 0 and c.imag.numerator == 0
    
    if is_zero:
        return infinite_solutions(variable, reduced_form)
    else:
        return no_solution(0, variable, reduced_form)


def _solve_degree_1(
    eq: SimplifiedEquation, 
    reduced_form: str, 
    variable: str
) -> Solution:
    """
    Solve degree 1 equation: bx + c = 0
    
    Solution: x = -c / b
    """
    b = eq.b
    c = eq.c
    
    # x = -c / b
    neg_c = _negate(c)
    root = _divide(neg_c, b)
    
    # Simplify if possible
    root = _simplify_value(root)
    
    return single_solution(root, 1, variable, reduced_form)


def _solve_degree_2(
    eq: SimplifiedEquation, 
    reduced_form: str, 
    variable: str
) -> Solution:
    """
    Solve degree 2 equation: ax² + bx + c = 0
    
    Using quadratic formula: x = (-b ± √(b² - 4ac)) / (2a)
    """
    a = eq.a
    b = eq.b
    c = eq.c
    
    # Calculate discriminant: Δ = b² - 4ac
    discriminant = _compute_discriminant(a, b, c)
    
    # Simplify discriminant
    discriminant = _simplify_value(discriminant)
    
    # Check discriminant sign
    disc_sign = _get_sign(discriminant)
    
    # Calculate 2a (denominator)
    two_a = _multiply(Rational(2), a)
    
    # Calculate -b
    neg_b = _negate(b)
    
    if disc_sign == 0:
        # Discriminant = 0: one double root
        # x = -b / (2a)
        root = _divide(neg_b, two_a)
        root = _simplify_value(root)
        return double_solution(root, discriminant, variable, reduced_form)
    
    elif disc_sign > 0:
        # Discriminant > 0: two distinct real roots
        sqrt_disc = sqrt_value(discriminant)
        sqrt_disc = _simplify_value(sqrt_disc)
        
        # x1 = (-b + √Δ) / (2a)
        root1 = _divide(_add(neg_b, sqrt_disc), two_a)
        root1 = _simplify_value(root1)
        
        # x2 = (-b - √Δ) / (2a)
        root2 = _divide(_subtract(neg_b, sqrt_disc), two_a)
        root2 = _simplify_value(root2)
        
        return two_real_solutions(root1, root2, discriminant, variable, reduced_form)
    
    else:
        # Discriminant < 0: two complex conjugate roots
        # √Δ is imaginary
        neg_discriminant = _negate(discriminant)
        sqrt_neg_disc = sqrt_value(neg_discriminant)
        sqrt_neg_disc = _simplify_value(sqrt_neg_disc)
        
        # Real part: -b / (2a)
        real_part = _divide(neg_b, two_a)
        real_part = _simplify_value(real_part)
        
        # Imaginary part: √|Δ| / (2a)
        imag_part = _divide(sqrt_neg_disc, two_a)
        imag_part = _simplify_value(imag_part)
        
        # Ensure we have Rational for Complex construction
        if isinstance(real_part, Complex):
            real_part = real_part.real
        if isinstance(imag_part, Complex):
            imag_part = imag_part.real
        
        # x1 = real_part + imag_part * i
        root1 = Complex(real_part, imag_part)
        
        # x2 = real_part - imag_part * i (conjugate)
        root2 = Complex(real_part, _negate(imag_part))
        
        return two_complex_solutions(root1, root2, discriminant, variable, reduced_form)


def _compute_discriminant(
    a: SolutionValue, 
    b: SolutionValue, 
    c: SolutionValue
) -> SolutionValue:
    """Compute discriminant: b² - 4ac"""
    b_squared = _multiply(b, b)
    four_ac = _multiply(_multiply(Rational(4), a), c)
    return _subtract(b_squared, four_ac)


def _get_sign(value: SolutionValue) -> int:
    """Get sign of value: -1, 0, or 1"""
    if isinstance(value, Rational):
        if value.numerator == 0:
            return 0
        return 1 if value.numerator > 0 else -1
    elif isinstance(value, Complex):
        if value.is_real():
            return _get_sign(value.real)
        # Complex number doesn't have a simple sign
        # For discriminant purposes, if we got here it's an error
        return 0
    return 0


def _negate(value: SolutionValue) -> SolutionValue:
    """Negate a value."""
    return -value


def _add(a: SolutionValue, b: SolutionValue) -> SolutionValue:
    """Add two values with type coercion."""
    if isinstance(a, Complex) or isinstance(b, Complex):
        if isinstance(a, Rational):
            a = Complex.from_rational(a)
        if isinstance(b, Rational):
            b = Complex.from_rational(b)
    return a + b


def _subtract(a: SolutionValue, b: SolutionValue) -> SolutionValue:
    """Subtract two values with type coercion."""
    if isinstance(a, Complex) or isinstance(b, Complex):
        if isinstance(a, Rational):
            a = Complex.from_rational(a)
        if isinstance(b, Rational):
            b = Complex.from_rational(b)
    return a - b


def _multiply(a: SolutionValue, b: SolutionValue) -> SolutionValue:
    """Multiply two values with type coercion."""
    if isinstance(a, Complex) or isinstance(b, Complex):
        if isinstance(a, Rational):
            a = Complex.from_rational(a)
        if isinstance(b, Rational):
            b = Complex.from_rational(b)
    return a * b


def _divide(a: SolutionValue, b: SolutionValue) -> SolutionValue:
    """Divide two values with type coercion."""
    if isinstance(a, Complex) or isinstance(b, Complex):
        if isinstance(a, Rational):
            a = Complex.from_rational(a)
        if isinstance(b, Rational):
            b = Complex.from_rational(b)
    return a / b


def _simplify_value(value: SolutionValue) -> SolutionValue:
    """Simplify a value (Complex to Rational if purely real)."""
    if isinstance(value, Complex) and value.is_real():
        return value.real
    return value