"""
Formatter module for Computorv2.

Provides formatting utilities for displaying mathematical types
in a clean, consistent manner.

Main components:
    - format_value(): Universal formatter for any type
    - format_result(): Format with optional label
    - Type-specific formatters for fine control
"""

from .rational_fmt import (
    format_rational,
    format_rational_signed,
    format_rational_coefficient,
)

from .complex_fmt import (
    format_complex,
    format_complex_polar,
    format_complex_as_solution,
)

from .matrix_fmt import (
    format_matrix,
    format_matrix_inline,
    format_matrix_dimensions,
    format_matrix_with_label,
)

from .polynomial_fmt import (
    format_polynomial,
    format_polynomial_equation,
    format_polynomial_factored,
    format_polynomial_degree,
)

from .function_fmt import (
    format_function,
    format_function_body,
    format_function_call,
    format_function_evaluation,
    format_function_signature,
    format_function_info,
    format_composition,
)

from .formatter import (
    format_value,
    format_result,
    format_assignment,
    format_error,
    format_solution,
    format_equation_info,
    Formatter,
)


__all__ = [
    # Rational formatting
    'format_rational',
    'format_rational_signed',
    'format_rational_coefficient',
    
    # Complex formatting
    'format_complex',
    'format_complex_polar',
    'format_complex_as_solution',
    
    # Matrix formatting
    'format_matrix',
    'format_matrix_inline',
    'format_matrix_dimensions',
    'format_matrix_with_label',
    
    # Polynomial formatting
    'format_polynomial',
    'format_polynomial_equation',
    'format_polynomial_factored',
    'format_polynomial_degree',
    
    # Function formatting
    'format_function',
    'format_function_body',
    'format_function_call',
    'format_function_evaluation',
    'format_function_signature',
    'format_function_info',
    'format_composition',
    
    # Main formatters
    'format_value',
    'format_result',
    'format_assignment',
    'format_error',
    'format_solution',
    'format_equation_info',
    'Formatter',
]