"""
Simplifier module for Computorv2.

Handles simplification of expressions and equations:
- Expression simplification (values to canonical form)
- Polynomial simplification (combining terms, reducing)
- Equation simplification (converting to standard form for solving)

Main components:
    - simplify_value(): Simplify any value to canonical form
    - simplify_equation(): Prepare equation for solving
    - SimplifiedEquation: Result container for equation solving
"""

from .errors import (
    SimplifierError,
    CannotSimplifyError,
    UnsupportedExpressionError,
)

from .expression_simplifier import (
    simplify_value,
    simplify_complex,
    simplify_polynomial_value,
    simplify_matrix,
    simplify_function,
    is_simplified,
    deep_simplify,
)

from .polynomial_simplifier import (
    simplify_polynomial,
    reduce_polynomial,
    normalize_polynomial,
    make_monic,
    polynomial_to_standard_form,
    subtract_polynomials,
    equation_to_standard_form,
    extract_coefficients,
)

from .equation_simplifier import (
    SimplifiedEquation,
    simplify_equation,
    analyze_equation,
    get_reduced_form,
    validate_for_solving,
)


__all__ = [
    # Errors
    'SimplifierError',
    'CannotSimplifyError',
    'UnsupportedExpressionError',
    
    # Expression simplification
    'simplify_value',
    'simplify_complex',
    'simplify_polynomial_value',
    'simplify_matrix',
    'simplify_function',
    'is_simplified',
    'deep_simplify',
    
    # Polynomial simplification
    'simplify_polynomial',
    'reduce_polynomial',
    'normalize_polynomial',
    'make_monic',
    'polynomial_to_standard_form',
    'subtract_polynomials',
    'equation_to_standard_form',
    'extract_coefficients',
    
    # Equation simplification
    'SimplifiedEquation',
    'simplify_equation',
    'analyze_equation',
    'get_reduced_form',
    'validate_for_solving',
]