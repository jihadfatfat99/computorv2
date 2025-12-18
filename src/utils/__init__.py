"""
Utility functions for Computorv2.

This module provides:
    - GCD/LCM arithmetic utilities
    - Input validation helpers
    - Global constants and configuration
"""

from .gcd import (
    gcd,
    lcm,
    gcd_multiple,
    lcm_multiple,
    extended_gcd,
)

from .validation import (
    is_valid_identifier,
    normalize_identifier,
    is_reserved_keyword,
    is_valid_matrix_size,
    is_valid_power_exponent,
    is_valid_polynomial_degree,
    is_approximately_zero,
    is_approximately_equal,
    is_integer_value,
    validate_matrix_consistency,
    parse_number_string,
    sanitize_input,
    is_empty_input,
)

from .constants import (
    DECIMAL_PRECISION,
    MAX_DISPLAY_DIGITS,
    EPSILON,
    MAX_MATRIX_ROWS,
    MAX_MATRIX_COLS,
    MAX_POLYNOMIAL_DEGREE,
    MAX_POWER_EXPONENT,
    RESERVED_KEYWORDS,
    OPERATORS,
    PRECEDENCE,
    RIGHT_ASSOCIATIVE,
    PROMPT,
    EXIT_COMMANDS,
)

__all__ = [
    # GCD utilities
    'gcd',
    'lcm',
    'gcd_multiple',
    'lcm_multiple',
    'extended_gcd',
    
    # Validation utilities
    'is_valid_identifier',
    'normalize_identifier',
    'is_reserved_keyword',
    'is_valid_matrix_size',
    'is_valid_power_exponent',
    'is_valid_polynomial_degree',
    'is_approximately_zero',
    'is_approximately_equal',
    'is_integer_value',
    'validate_matrix_consistency',
    'parse_number_string',
    'sanitize_input',
    'is_empty_input',
    
    # Constants
    'DECIMAL_PRECISION',
    'MAX_DISPLAY_DIGITS',
    'EPSILON',
    'MAX_MATRIX_ROWS',
    'MAX_MATRIX_COLS',
    'MAX_POLYNOMIAL_DEGREE',
    'MAX_POWER_EXPONENT',
    'RESERVED_KEYWORDS',
    'OPERATORS',
    'PRECEDENCE',
    'RIGHT_ASSOCIATIVE',
    'PROMPT',
    'EXIT_COMMANDS',
]