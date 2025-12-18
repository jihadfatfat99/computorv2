"""
Expression simplification for Computorv2.

Handles simplification of evaluated values:
- Simplify Complex to Rational if purely real
- Simplify Polynomial to constant if degree 0
- Reduce fractions to lowest terms
"""

from typing import Any, Union
from ..math_types import Rational, Complex, Matrix, Polynomial, Function


Value = Union[Rational, Complex, Matrix, Polynomial, Function]


def simplify_value(value: Any) -> Value:
    """
    Simplify an evaluated value to its canonical form.
    
    Operations:
    - int/float -> Rational
    - Complex with imag=0 -> Rational
    - Constant Polynomial -> Rational/Complex
    - Rational fractions reduced to lowest terms (automatic in Rational)
    
    Args:
        value: Value to simplify
    
    Returns:
        Simplified value
    """
    if isinstance(value, int):
        return Rational.from_int(value)
    
    if isinstance(value, float):
        return Rational.from_float(value)
    
    if isinstance(value, Complex):
        return simplify_complex(value)
    
    if isinstance(value, Polynomial):
        return simplify_polynomial_value(value)
    
    if isinstance(value, Rational):
        return value
    
    return value


def simplify_complex(c: Complex) -> Rational | Complex:
    """
    Simplify Complex number.
    
    If imaginary part is zero, return as Rational.
    
    Args:
        c: Complex number
    
    Returns:
        Rational if purely real, otherwise Complex
    """
    if c.is_real():
        return c.real
    return c


def simplify_polynomial_value(poly: Polynomial) -> Rational | Complex | Polynomial:
    """
    Simplify Polynomial value.
    
    If polynomial is constant (degree 0), return the constant value.
    
    Args:
        poly: Polynomial
    
    Returns:
        Constant value if degree 0, otherwise simplified Polynomial
    """
    if poly.is_constant():
        const = poly.to_constant()
        if isinstance(const, Complex):
            return simplify_complex(const)
        return const
    
    from .polynomial_simplifier import simplify_polynomial
    return simplify_polynomial(poly)


def simplify_matrix(m: Matrix) -> Matrix:
    """
    Simplify Matrix by simplifying each element.
    
    Args:
        m: Matrix
    
    Returns:
        Matrix with simplified elements
    """
    new_data = []
    for row in m._data:
        new_row = []
        for elem in row:
            simplified = simplify_value(elem)
            new_row.append(simplified)
        new_data.append(new_row)
    
    return Matrix(new_data)


def simplify_function(f: Function) -> Function:
    """
    Simplify Function by simplifying its body polynomial.
    
    Args:
        f: Function
    
    Returns:
        Function with simplified body
    """
    from .polynomial_simplifier import simplify_polynomial
    simplified_body = simplify_polynomial(f.body)
    
    return Function(f.name, f.variable, simplified_body)


def is_simplified(value: Any) -> bool:
    """
    Check if a value is already in simplified form.
    
    Args:
        value: Value to check
    
    Returns:
        True if already simplified
    """
    if isinstance(value, (int, float)):
        return False
    
    if isinstance(value, Complex):
        return not value.is_real()
    
    if isinstance(value, Polynomial):
        return not value.is_constant()
    
    return True


def deep_simplify(value: Any) -> Value:
    """
    Recursively simplify a value and all its components.
    
    Args:
        value: Value to simplify
    
    Returns:
        Deeply simplified value
    """
    result = simplify_value(value)
    
    if isinstance(result, Matrix):
        return simplify_matrix(result)
    
    if isinstance(result, Function):
        return simplify_function(result)
    
    return result