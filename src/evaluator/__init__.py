"""
Evaluator module for Computorv2.

Executes AST nodes and computes values with a managed context.

Main components:
    - Evaluator: AST visitor that computes values
    - Context: Symbol table for variables and functions
    - evaluate(): Convenience function
    - Built-in functions: sin, cos, tan, sqrt, abs, exp, log
"""

from .context import Context

from .evaluator import (
    Evaluator,
    EvaluationResult,
    evaluate,
)

from .operations import (
    apply_binary_op,
    apply_unary_op,
)

from .type_coercion import (
    to_rational,
    to_complex,
    coerce_numeric,
    get_type_name,
    is_numeric,
    is_scalar,
    is_math_type,
    simplify_result,
)

from .errors import (
    EvaluatorError,
    UndefinedVariableError,
    UndefinedFunctionError,
    TypeMismatchError,
    InvalidOperandError,
    ReservedNameError,
)

from .builtins import (
    is_builtin,
    get_builtin,
    list_builtins,
    BUILTIN_FUNCTIONS,
)


__all__ = [
    # Core classes
    'Evaluator',
    'EvaluationResult',
    'Context',
    
    # Convenience function
    'evaluate',
    
    # Operations
    'apply_binary_op',
    'apply_unary_op',
    
    # Type coercion
    'to_rational',
    'to_complex',
    'coerce_numeric',
    'get_type_name',
    'is_numeric',
    'is_scalar',
    'is_math_type',
    'simplify_result',
    
    # Built-in functions
    'is_builtin',
    'get_builtin',
    'list_builtins',
    'BUILTIN_FUNCTIONS',
    
    # Errors
    'EvaluatorError',
    'UndefinedVariableError',
    'UndefinedFunctionError',
    'TypeMismatchError',
    'InvalidOperandError',
    'ReservedNameError',
]