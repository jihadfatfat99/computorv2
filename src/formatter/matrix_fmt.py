"""
Matrix formatting for Computorv2.

Handles pretty-printing of matrices with aligned columns.
"""

from typing import List

from ..math_types import Matrix, Rational, Complex
from .rational_fmt import format_rational
from .complex_fmt import format_complex


def format_matrix(m: Matrix, align: bool = True) -> str:
    """
    Format a Matrix for display.
    
    Args:
        m: The Matrix to format
        align: If True, align columns for pretty output
    
    Returns:
        Formatted string representation
    
    Examples:
        >>> m = Matrix([[Rational(1), Rational(2)], [Rational(3), Rational(4)]])
        >>> print(format_matrix(m))
        [ 1 , 2 ]
        [ 3 , 4 ]
    """
    if m.rows == 0 or m.cols == 0:
        return "[]"
    
    # Format all elements
    formatted_elements: List[List[str]] = []
    for i in range(m.rows):
        row_strs: List[str] = []
        for j in range(m.cols):
            element = m.get(i, j)
            row_strs.append(_format_element(element))
        formatted_elements.append(row_strs)
    
    if align:
        return _format_aligned(formatted_elements)
    else:
        return _format_simple(formatted_elements)


def _format_element(element) -> str:
    """Format a single matrix element"""
    if isinstance(element, Rational):
        return format_rational(element)
    elif isinstance(element, Complex):
        return format_complex(element)
    else:
        return str(element)


def _format_simple(elements: List[List[str]]) -> str:
    """Format without column alignment"""
    lines = []
    for row in elements:
        line = "[ " + " , ".join(row) + " ]"
        lines.append(line)
    return "\n".join(lines)


def _format_aligned(elements: List[List[str]]) -> str:
    """Format with column alignment"""
    if not elements or not elements[0]:
        return "[]"
    
    num_cols = len(elements[0])
    
    # Find maximum width for each column
    col_widths = [0] * num_cols
    for row in elements:
        for j, val in enumerate(row):
            col_widths[j] = max(col_widths[j], len(val))
    
    # Build formatted rows
    lines = []
    for row in elements:
        padded = [val.rjust(col_widths[j]) for j, val in enumerate(row)]
        line = "[ " + " , ".join(padded) + " ]"
        lines.append(line)
    
    return "\n".join(lines)


def format_matrix_inline(m: Matrix) -> str:
    """
    Format a Matrix as a single line (for compact display).
    
    Args:
        m: The Matrix to format
    
    Returns:
        Single-line string representation
    
    Examples:
        >>> format_matrix_inline(m)
        '[[1, 2]; [3, 4]]'
    """
    rows_str = []
    for i in range(m.rows):
        row_elements = []
        for j in range(m.cols):
            element = m.get(i, j)
            row_elements.append(_format_element(element))
        rows_str.append("[" + ", ".join(row_elements) + "]")
    
    return "[" + "; ".join(rows_str) + "]"


def format_matrix_dimensions(m: Matrix) -> str:
    """
    Format matrix dimensions.
    
    Args:
        m: The Matrix
    
    Returns:
        Dimension string like "2x3"
    """
    return f"{m.rows}x{m.cols}"


def format_matrix_with_label(m: Matrix, label: str) -> str:
    """
    Format a Matrix with a label.
    
    Args:
        m: The Matrix to format
        label: Label to show (e.g., variable name)
    
    Returns:
        Labeled matrix string
    
    Examples:
        >>> format_matrix_with_label(m, "A")
        'A =
        [ 1 , 2 ]
        [ 3 , 4 ]'
    """
    matrix_str = format_matrix(m)
    lines = matrix_str.split('\n')
    
    if len(lines) == 1:
        return f"{label} = {lines[0]}"
    
    # Multi-line: put label on first line
    result = [f"{label} ="]
    result.extend(lines)
    return "\n".join(result)