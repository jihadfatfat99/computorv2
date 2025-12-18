"""
Main formatter module for Computorv2.

Provides a unified interface for formatting all mathematical types.
"""

from typing import Any, Union

from ..math_types import Rational, Complex, Matrix, Polynomial, Function
from .rational_fmt import format_rational, format_rational_signed
from .complex_fmt import format_complex, format_complex_as_solution
from .matrix_fmt import format_matrix, format_matrix_inline, format_matrix_with_label
from .polynomial_fmt import format_polynomial, format_polynomial_equation
from .function_fmt import format_function, format_function_evaluation


# Type alias for all formattable types
Formattable = Union[Rational, Complex, Matrix, Polynomial, Function, int, float, str]


def format_value(value: Any) -> str:
    """
    Format any value for display.
    
    Automatically dispatches to the appropriate formatter based on type.
    
    Args:
        value: The value to format
    
    Returns:
        Formatted string representation
    
    Examples:
        >>> format_value(Rational(1, 2))
        '0.5'
        >>> format_value(Complex(Rational(3), Rational(2)))
        '3 + 2i'
        >>> format_value(Matrix([[Rational(1), Rational(2)]]))
        '[ 1 , 2 ]'
    """
    if value is None:
        return "None"
    
    if isinstance(value, Rational):
        return format_rational(value)
    
    if isinstance(value, Complex):
        return format_complex(value)
    
    if isinstance(value, Matrix):
        return format_matrix(value)
    
    if isinstance(value, Polynomial):
        return format_polynomial(value)
    
    if isinstance(value, Function):
        return format_function(value)
    
    if isinstance(value, bool):
        return str(value).lower()
    
    if isinstance(value, int):
        return str(value)
    
    if isinstance(value, float):
        # Format float cleanly
        if value == int(value):
            return str(int(value))
        return f"{value:.10g}"
    
    if isinstance(value, str):
        return value
    
    # Fallback
    return str(value)


def format_result(value: Any, label: str = None) -> str:
    """
    Format a computation result, optionally with a label.
    
    Args:
        value: The result value
        label: Optional label (variable name, etc.)
    
    Returns:
        Formatted result string
    
    Examples:
        >>> format_result(Rational(5))
        '5'
        >>> format_result(Rational(5), label='x')
        'x = 5'
    """
    formatted = format_value(value)
    
    if label:
        # Handle multi-line values (like matrices)
        if '\n' in formatted:
            return f"{label} =\n{formatted}"
        return f"{label} = {formatted}"
    
    return formatted


def format_assignment(name: str, value: Any) -> str:
    """
    Format an assignment result.
    
    Args:
        name: Variable/function name
        value: The assigned value
    
    Returns:
        Formatted string (just the value, or function definition)
    """
    if isinstance(value, Function):
        return format_function(value)
    
    return format_value(value)


def format_error(message: str) -> str:
    """
    Format an error message.
    
    Args:
        message: The error message
    
    Returns:
        Formatted error string
    """
    return f"Error: {message}"


def format_solution(solutions: list, variable: str = "x", domain: str = "R") -> str:
    """
    Format equation solutions.
    
    Args:
        solutions: List of solution values
        variable: The variable name
        domain: The solution domain ("R" or "C")
    
    Returns:
        Formatted solutions string
    """
    if not solutions:
        return f"No solution in {domain}"
    
    if len(solutions) == 1:
        sol = solutions[0]
        return f"Solution in {domain}:\n{variable} = {format_value(sol)}"
    
    lines = [f"Solutions in {domain}:"]
    for sol in solutions:
        lines.append(f"{variable} = {format_value(sol)}")
    
    return "\n".join(lines)


def format_equation_info(reduced_form: str, degree: int) -> str:
    """
    Format equation information (reduced form and degree).
    
    Args:
        reduced_form: The reduced equation string
        degree: The polynomial degree
    
    Returns:
        Formatted info string
    """
    return f"Reduced form: {reduced_form}\nPolynomial degree: {degree}"


class Formatter:
    """
    Formatter class with configurable options.
    
    Attributes:
        show_fractions: Display rationals as fractions instead of decimals
        precision: Number of decimal places
        align_matrices: Align matrix columns
    """
    
    def __init__(
        self,
        show_fractions: bool = False,
        precision: int = 10,
        align_matrices: bool = True
    ):
        self.show_fractions = show_fractions
        self.precision = precision
        self.align_matrices = align_matrices
    
    def format(self, value: Any) -> str:
        """Format a value with current settings"""
        if isinstance(value, Rational):
            return format_rational(value, show_fraction=self.show_fractions)
        
        if isinstance(value, Matrix):
            return format_matrix(value, align=self.align_matrices)
        
        return format_value(value)
    
    def format_result(self, value: Any, label: str = None) -> str:
        """Format a result with current settings"""
        formatted = self.format(value)
        
        if label:
            if '\n' in formatted:
                return f"{label} =\n{formatted}"
            return f"{label} = {formatted}"
        
        return formatted