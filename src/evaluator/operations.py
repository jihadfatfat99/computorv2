"""
Operation dispatch for Computorv2 evaluator.

Handles binary and unary operations between different types.
"""

from typing import Any
from ..math_types import Rational, Complex, Matrix, Polynomial, Function
from ..math_types.base import (
    DivisionByZeroError,
    InvalidOperationError,
    InvalidExponentError,
    DimensionMismatchError,
)
from .type_coercion import coerce_numeric, is_scalar, get_type_name, simplify_result
from .errors import TypeMismatchError, InvalidOperandError


def apply_binary_op(operator: str, left: Any, right: Any) -> Any:
    """
    Apply a binary operation.
    
    Args:
        operator: The operator (+, -, *, **, /, %, ^)
        left: Left operand
        right: Right operand
    
    Returns:
        Result of the operation
    
    Raises:
        TypeMismatchError: If operation not supported for types
        InvalidOperandError: If operands are invalid
    """
    try:
        if operator == '+':
            return _apply_add(left, right)
        elif operator == '-':
            return _apply_sub(left, right)
        elif operator == '*':
            return _apply_mul(left, right)
        elif operator == '**':
            return _apply_matmul(left, right)
        elif operator == '/':
            return _apply_div(left, right)
        elif operator == '%':
            return _apply_mod(left, right)
        elif operator == '^':
            return _apply_pow(left, right)
        else:
            raise InvalidOperandError(f"Unknown operator: {operator}")
    
    except DivisionByZeroError:
        raise InvalidOperandError("Division by zero")
    except InvalidExponentError as e:
        raise InvalidOperandError(str(e))
    except DimensionMismatchError as e:
        raise InvalidOperandError(str(e))
    except InvalidOperationError as e:
        raise TypeMismatchError(operator, get_type_name(left), get_type_name(right))


def apply_unary_op(operator: str, operand: Any) -> Any:
    """
    Apply a unary operation.
    
    Args:
        operator: The operator (+, -)
        operand: The operand
    
    Returns:
        Result of the operation
    """
    try:
        if operator == '+':
            return +operand
        elif operator == '-':
            return -operand
        else:
            raise InvalidOperandError(f"Unknown unary operator: {operator}")
    except Exception as e:
        raise TypeMismatchError(operator, get_type_name(operand))


def _apply_add(left: Any, right: Any) -> Any:
    """Addition: left + right"""
    # Scalar + Scalar
    if is_scalar(left) and is_scalar(right):
        left, right = coerce_numeric(left, right)
        return simplify_result(left + right)
    
    # Matrix + Matrix
    if isinstance(left, Matrix) and isinstance(right, Matrix):
        return left + right
    
    # Polynomial + Polynomial/Scalar or Scalar + Polynomial
    if isinstance(left, Polynomial):
        return left + right
    if isinstance(right, Polynomial):
        return right + left  # Polynomial handles scalar addition
    
    # Function + Function/Scalar/Polynomial
    if isinstance(left, Function) or isinstance(right, Function):
        return left + right
    
    raise TypeMismatchError('+', get_type_name(left), get_type_name(right))


def _apply_sub(left: Any, right: Any) -> Any:
    """Subtraction: left - right"""
    # Scalar - Scalar
    if is_scalar(left) and is_scalar(right):
        left, right = coerce_numeric(left, right)
        return simplify_result(left - right)
    
    # Matrix - Matrix
    if isinstance(left, Matrix) and isinstance(right, Matrix):
        return left - right
    
    # Polynomial - Polynomial/Scalar
    if isinstance(left, Polynomial):
        return left - right
    # Scalar - Polynomial: convert scalar to polynomial first
    if isinstance(right, Polynomial):
        left_poly = Polynomial.from_constant(left, right.variable)
        return left_poly - right
    
    # Function - Function/Scalar/Polynomial
    if isinstance(left, Function) or isinstance(right, Function):
        return left - right
    
    raise TypeMismatchError('-', get_type_name(left), get_type_name(right))


def _apply_mul(left: Any, right: Any) -> Any:
    """Multiplication: left * right (element-wise for matrices)"""
    # Scalar * Scalar
    if is_scalar(left) and is_scalar(right):
        left, right = coerce_numeric(left, right)
        return simplify_result(left * right)
    
    # Matrix * Scalar or Scalar * Matrix
    if isinstance(left, Matrix) and is_scalar(right):
        return left * right
    if is_scalar(left) and isinstance(right, Matrix):
        return right * left
    
    # Matrix * Matrix (element-wise)
    if isinstance(left, Matrix) and isinstance(right, Matrix):
        return left * right
    
    # Polynomial * Polynomial/Scalar or Scalar * Polynomial
    if isinstance(left, Polynomial):
        return left * right
    if isinstance(right, Polynomial):
        return right * left  # Polynomial handles scalar multiplication
    
    # Function * Function/Scalar/Polynomial
    if isinstance(left, Function) or isinstance(right, Function):
        return left * right
    
    raise TypeMismatchError('*', get_type_name(left), get_type_name(right))


def _apply_matmul(left: Any, right: Any) -> Any:
    """Matrix multiplication: left ** right"""
    if isinstance(left, Matrix) and isinstance(right, Matrix):
        return left.matmul(right)
    
    raise TypeMismatchError('**', get_type_name(left), get_type_name(right))


def _apply_div(left: Any, right: Any) -> Any:
    """Division: left / right"""
    # Scalar / Scalar
    if is_scalar(left) and is_scalar(right):
        left, right = coerce_numeric(left, right)
        return simplify_result(left / right)
    
    # Matrix / Scalar
    if isinstance(left, Matrix) and is_scalar(right):
        return left / right
    
    # Polynomial / Scalar
    if isinstance(left, Polynomial) and is_scalar(right):
        return left / right
    
    # Function / Scalar
    if isinstance(left, Function) and is_scalar(right):
        return left / right
    
    raise TypeMismatchError('/', get_type_name(left), get_type_name(right))


def _apply_mod(left: Any, right: Any) -> Any:
    """Modulo: left % right"""
    # Scalar % Scalar
    if is_scalar(left) and is_scalar(right):
        left, right = coerce_numeric(left, right)
        return simplify_result(left % right)
    
    # Matrix % Scalar
    if isinstance(left, Matrix) and is_scalar(right):
        return left % right
    
    # Polynomial % Scalar
    if isinstance(left, Polynomial) and is_scalar(right):
        return left % right
    
    raise TypeMismatchError('%', get_type_name(left), get_type_name(right))


def _apply_pow(left: Any, right: Any) -> Any:
    """Power: left ^ right (non-negative integer exponent)"""
    # Validate exponent is non-negative integer
    exp = _get_exponent(right)
    
    # Scalar ^ int
    if is_scalar(left):
        if isinstance(left, (int, float)):
            left = Rational.from_float(float(left)) if isinstance(left, float) else Rational.from_int(left)
        return simplify_result(left ** exp)
    
    # Matrix ^ int
    if isinstance(left, Matrix):
        return left ** exp
    
    # Polynomial ^ int
    if isinstance(left, Polynomial):
        return left ** exp
    
    # Function ^ int
    if isinstance(left, Function):
        return left ** exp
    
    raise TypeMismatchError('^', get_type_name(left), get_type_name(right))


def _get_exponent(value: Any) -> int:
    """
    Extract integer exponent from a value.
    
    Raises:
        InvalidOperandError: If not a valid non-negative integer
    """
    if isinstance(value, int):
        exp = value
    elif isinstance(value, float):
        if value != int(value):
            raise InvalidOperandError("Exponent must be an integer")
        exp = int(value)
    elif isinstance(value, Rational):
        if not value.is_integer():
            raise InvalidOperandError("Exponent must be an integer")
        exp = value.to_int()
    elif isinstance(value, Complex):
        if not value.is_real():
            raise InvalidOperandError("Exponent must be a real number")
        if not value.real.is_integer():
            raise InvalidOperandError("Exponent must be an integer")
        exp = value.real.to_int()
    else:
        raise InvalidOperandError(f"Cannot use {get_type_name(value)} as exponent")
    
    if exp < 0:
        raise InvalidOperandError("Exponent must be non-negative")
    
    return exp