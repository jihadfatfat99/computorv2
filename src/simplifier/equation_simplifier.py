"""
Equation simplification for Computorv2.

Prepares equations for the solver module:
- Converts equation to standard form (polynomial = 0)
- Identifies equation degree
- Extracts coefficients for solving algorithms
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass

from ..math_types import Rational, Complex, Polynomial
from .polynomial_simplifier import (
    equation_to_standard_form,
    normalize_polynomial,
    reduce_polynomial,
    extract_coefficients,
)


@dataclass
class SimplifiedEquation:
    """
    Result of equation simplification.
    
    Attributes:
        polynomial: The equation in standard form (= 0)
        degree: Degree of the polynomial (0, 1, or 2 for solvable)
        variable: The variable name
        coefficients: Dict mapping degree -> coefficient
        is_valid: Whether equation is valid for solving
        error_message: Error message if not valid
    """
    polynomial: Polynomial
    degree: int
    variable: str
    coefficients: Dict[int, Rational | Complex]
    is_valid: bool = True
    error_message: Optional[str] = None
    
    @property
    def a(self) -> Rational | Complex:
        """Coefficient of x² (or 0 if not present)."""
        return self.coefficients.get(2, Rational(0))
    
    @property
    def b(self) -> Rational | Complex:
        """Coefficient of x (or 0 if not present)."""
        return self.coefficients.get(1, Rational(0))
    
    @property
    def c(self) -> Rational | Complex:
        """Constant term (or 0 if not present)."""
        return self.coefficients.get(0, Rational(0))
    
    def is_linear(self) -> bool:
        """Check if equation is linear (degree 1)."""
        return self.degree == 1
    
    def is_quadratic(self) -> bool:
        """Check if equation is quadratic (degree 2)."""
        return self.degree == 2
    
    def is_constant(self) -> bool:
        """Check if equation is constant (degree 0)."""
        return self.degree == 0
    
    def has_complex_coefficients(self) -> bool:
        """Check if any coefficient is complex."""
        return any(isinstance(c, Complex) for c in self.coefficients.values())


def simplify_equation(left: Polynomial, right: Polynomial) -> SimplifiedEquation:
    """
    Simplify an equation for solving.
    
    Converts left = right to standard form polynomial = 0.
    
    Args:
        left: Left side of equation
        right: Right side of equation
    
    Returns:
        SimplifiedEquation ready for solving
    """
    poly = equation_to_standard_form(left, right)
    
    if poly.is_zero():
        return SimplifiedEquation(
            polynomial=poly,
            degree=0,
            variable=left.variable or right.variable or 'x',
            coefficients={0: Rational(0)},
            is_valid=True,
            error_message=None
        )
    
    degree = poly.degree
    variable = poly.variable
    
    if degree > 2:
        return SimplifiedEquation(
            polynomial=poly,
            degree=degree,
            variable=variable,
            coefficients=extract_coefficients(poly),
            is_valid=False,
            error_message=f"Polynomial degree {degree} is too high. Only degrees 0, 1, 2 are supported."
        )
    
    coefficients = extract_coefficients(poly)
    
    return SimplifiedEquation(
        polynomial=poly,
        degree=degree,
        variable=variable,
        coefficients=coefficients,
        is_valid=True
    )


def analyze_equation(eq: SimplifiedEquation) -> str:
    """
    Generate human-readable analysis of the equation.
    
    Args:
        eq: Simplified equation
    
    Returns:
        Analysis string
    """
    lines = []
    
    lines.append(f"Equation: {eq.polynomial} = 0")
    lines.append(f"Variable: {eq.variable}")
    lines.append(f"Degree: {eq.degree}")
    
    if eq.is_constant():
        lines.append("Type: Constant equation")
        if eq.c == Rational(0):
            lines.append("Solution: All values are solutions (0 = 0)")
        else:
            lines.append(f"Solution: No solution ({eq.c} ≠ 0)")
    
    elif eq.is_linear():
        lines.append("Type: Linear equation")
        lines.append(f"Form: {eq.b} * {eq.variable} + {eq.c} = 0")
    
    elif eq.is_quadratic():
        lines.append("Type: Quadratic equation")
        lines.append(f"Form: {eq.a} * {eq.variable}² + {eq.b} * {eq.variable} + {eq.c} = 0")
        
        if not eq.has_complex_coefficients():
            a, b, c = eq.a, eq.b, eq.c
            discriminant = b * b - Rational(4) * a * c
            lines.append(f"Discriminant: {discriminant}")
    
    else:
        lines.append(f"Type: Polynomial of degree {eq.degree}")
        if not eq.is_valid:
            lines.append(f"Note: {eq.error_message}")
    
    return "\n".join(lines)


def get_reduced_form(eq: SimplifiedEquation) -> str:
    """
    Get the reduced form of the equation as a string.
    
    This is the format required by the 42 project specification.
    
    Args:
        eq: Simplified equation
    
    Returns:
        Reduced form string (e.g., "x^2 + 2 * x + 1 = 0")
    """
    from ..formatter import format_polynomial
    
    poly_str = format_polynomial(eq.polynomial)
    return f"{poly_str} = 0"


def validate_for_solving(eq: SimplifiedEquation) -> Tuple[bool, Optional[str]]:
    """
    Validate equation is suitable for solving.
    
    Args:
        eq: Simplified equation
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not eq.is_valid:
        return False, eq.error_message
    
    if eq.degree > 2:
        return False, f"Cannot solve polynomial of degree {eq.degree}. Maximum supported degree is 2."
    
    return True, None