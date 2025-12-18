"""
Mathematical types for Computorv2.

This module provides custom implementations of:
    - Rational: Exact fraction arithmetic
    - Complex: Complex numbers with rational coefficients
    - Matrix: Matrices with rational/complex entries
    - Polynomial: Symbolic polynomial expressions
    - Function: Named single-variable functions

All types inherit from MathType base class and support standard
arithmetic operations.

Note: No native complex types or external math libraries are used,
as per project requirements.
"""

from .base import (
    MathType,
    MathTypeError,
    DivisionByZeroError,
    InvalidOperationError,
    DimensionMismatchError,
    InvalidExponentError,
)

from .rational import Rational
from .complex import Complex
from .matrix import Matrix
from .polynomial import Polynomial
from .function import Function


__all__ = [
    # Base class and exceptions
    'MathType',
    'MathTypeError',
    'DivisionByZeroError',
    'InvalidOperationError',
    'DimensionMismatchError',
    'InvalidExponentError',
    
    # Mathematical types
    'Rational',
    'Complex',
    'Matrix',
    'Polynomial',
    'Function',
]


# Type aliases for convenience
Scalar = Rational | Complex
MatrixEntry = Rational | Complex
Coefficient = Rational | Complex