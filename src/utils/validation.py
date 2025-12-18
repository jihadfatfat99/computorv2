"""
Input validation utilities for Computorv2.
Handles identifier validation, type checking, and constraint enforcement.
"""

import re
from .constants import (
    RESERVED_KEYWORDS,
    MAX_MATRIX_ROWS,
    MAX_MATRIX_COLS,
    MAX_POWER_EXPONENT,
    MAX_POLYNOMIAL_DEGREE,
    EPSILON,
)


def is_valid_identifier(name: str) -> bool:
    """
    Check if a string is a valid variable/function name.
    
    Rules:
        - Must contain only letters (a-z, A-Z)
        - Cannot be empty
        - Cannot be a reserved keyword (case-insensitive)
    
    Args:
        name: The identifier to validate
    
    Returns:
        True if valid, False otherwise
    
    Examples:
        >>> is_valid_identifier("varA")
        True
        >>> is_valid_identifier("x")
        True
        >>> is_valid_identifier("i")
        False
        >>> is_valid_identifier("var1")
        False
    """
    if not name:
        return False
    
    if not name.isalpha():
        return False
    
    if name.lower() in RESERVED_KEYWORDS:
        return False
    
    return True


def normalize_identifier(name: str) -> str:
    """
    Normalize an identifier to lowercase for case-insensitive comparison.
    
    Args:
        name: The identifier to normalize
    
    Returns:
        Lowercase version of the identifier
    
    Examples:
        >>> normalize_identifier("VarA")
        'vara'
        >>> normalize_identifier("MATRIX")
        'matrix'
    """
    return name.lower()


def is_reserved_keyword(name: str) -> bool:
    """
    Check if a name is a reserved keyword.
    
    Args:
        name: The name to check
    
    Returns:
        True if reserved, False otherwise
    """
    return name.lower() in RESERVED_KEYWORDS


def is_valid_matrix_size(rows: int, cols: int) -> bool:
    """
    Check if matrix dimensions are within allowed limits.
    
    Args:
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if valid, False otherwise
    """
    return (
        0 < rows <= MAX_MATRIX_ROWS and
        0 < cols <= MAX_MATRIX_COLS
    )


def is_valid_power_exponent(exp: int) -> bool:
    """
    Check if a power exponent is valid.
    
    Rules:
        - Must be non-negative integer
        - Must not exceed maximum limit
    
    Args:
        exp: The exponent to validate
    
    Returns:
        True if valid, False otherwise
    """
    return isinstance(exp, int) and 0 <= exp <= MAX_POWER_EXPONENT


def is_valid_polynomial_degree(degree: int) -> bool:
    """
    Check if polynomial degree is solvable.
    
    Args:
        degree: The polynomial degree
    
    Returns:
        True if can be solved, False otherwise
    """
    return 0 <= degree <= MAX_POLYNOMIAL_DEGREE


def is_approximately_zero(value: float) -> bool:
    """
    Check if a floating point value is approximately zero.
    
    Args:
        value: The value to check
    
    Returns:
        True if within epsilon of zero
    """
    return abs(value) < EPSILON


def is_approximately_equal(a: float, b: float) -> bool:
    """
    Check if two floating point values are approximately equal.
    
    Args:
        a: First value
        b: Second value
    
    Returns:
        True if within epsilon of each other
    """
    return abs(a - b) < EPSILON


def is_integer_value(value: float) -> bool:
    """
    Check if a float represents an integer value.
    
    Args:
        value: The value to check
    
    Returns:
        True if value is effectively an integer
    
    Examples:
        >>> is_integer_value(3.0)
        True
        >>> is_integer_value(3.0001)
        False
    """
    return is_approximately_equal(value, round(value))


def validate_matrix_consistency(rows: list[list]) -> tuple[bool, str]:
    """
    Validate that a matrix has consistent row lengths.
    
    Args:
        rows: List of rows, each row is a list of values
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not rows:
        return False, "Matrix cannot be empty"
    
    first_row_len = len(rows[0])
    
    if first_row_len == 0:
        return False, "Matrix rows cannot be empty"
    
    for idx, row in enumerate(rows[1:], start=2):
        if len(row) != first_row_len:
            return False, f"Row {idx} has {len(row)} elements, expected {first_row_len}"
    
    num_rows = len(rows)
    num_cols = first_row_len
    
    if not is_valid_matrix_size(num_rows, num_cols):
        return False, f"Matrix size {num_rows}x{num_cols} exceeds maximum allowed"
    
    return True, ""


def parse_number_string(s: str) -> tuple[bool, float | None]:
    """
    Parse a string as a number (integer or decimal).
    
    Args:
        s: String to parse
    
    Returns:
        Tuple of (success, value or None)
    
    Examples:
        >>> parse_number_string("42")
        (True, 42.0)
        >>> parse_number_string("-3.14")
        (True, -3.14)
        >>> parse_number_string("abc")
        (False, None)
    """
    pattern = r'^-?\d+(\.\d+)?$'
    
    if re.match(pattern, s):
        return True, float(s)
    
    return False, None


def sanitize_input(line: str) -> str:
    """
    Sanitize user input by removing leading/trailing whitespace.
    
    Args:
        line: Raw input line
    
    Returns:
        Sanitized string
    """
    return line.strip()


def is_empty_input(line: str) -> bool:
    """
    Check if input line is empty or whitespace only.
    
    Args:
        line: Input line to check
    
    Returns:
        True if empty/whitespace
    """
    return not line or line.isspace()