"""
Function formatting for Computorv2.

Handles display of function definitions and evaluations.
"""

from ..math_types import Function, Rational, Complex
from .polynomial_fmt import format_polynomial
from .rational_fmt import format_rational
from .complex_fmt import format_complex


def format_function(f: Function) -> str:
    """
    Format a Function definition for display.
    
    Args:
        f: The Function to format
    
    Returns:
        Formatted function definition string
    
    Examples:
        >>> format_function(f)
        'f(x) = 2 * x + 1'
    """
    body_str = format_polynomial(f.body)
    return f"{f.name}({f.variable}) = {body_str}"


def format_function_body(f: Function) -> str:
    """
    Format just the function body (without name and parameter).
    
    Args:
        f: The Function
    
    Returns:
        Body expression string
    """
    return format_polynomial(f.body)


def format_function_call(name: str, argument: str) -> str:
    """
    Format a function call.
    
    Args:
        name: Function name
        argument: Argument string
    
    Returns:
        Call string like 'f(2)'
    """
    return f"{name}({argument})"


def format_function_evaluation(f: Function, input_val, result) -> str:
    """
    Format a function evaluation result.
    
    Args:
        f: The Function
        input_val: The input value
        result: The computed result
    
    Returns:
        Evaluation string like 'f(2) = 5'
    
    Examples:
        >>> format_function_evaluation(f, Rational(2), Rational(5))
        'f(2) = 5'
    """
    # Format input
    if isinstance(input_val, Rational):
        input_str = format_rational(input_val)
    elif isinstance(input_val, Complex):
        input_str = format_complex(input_val)
    else:
        input_str = str(input_val)
    
    # Format result
    if isinstance(result, Rational):
        result_str = format_rational(result)
    elif isinstance(result, Complex):
        result_str = format_complex(result)
    else:
        result_str = str(result)
    
    return f"{f.name}({input_str}) = {result_str}"


def format_function_signature(f: Function) -> str:
    """
    Format just the function signature.
    
    Args:
        f: The Function
    
    Returns:
        Signature string like 'f(x)'
    """
    return f"{f.name}({f.variable})"


def format_function_info(f: Function) -> str:
    """
    Format detailed function information.
    
    Args:
        f: The Function
    
    Returns:
        Multi-line info string
    """
    lines = [
        f"Function: {f.name}",
        f"Parameter: {f.variable}",
        f"Body: {format_polynomial(f.body)}",
        f"Degree: {f.degree}",
    ]
    return "\n".join(lines)


def format_composition(outer: Function, inner: Function) -> str:
    """
    Format a function composition.
    
    Args:
        outer: The outer function f
        inner: The inner function g
    
    Returns:
        Composition string like 'f(g(x))'
    """
    return f"{outer.name}({inner.name}({inner.variable}))"