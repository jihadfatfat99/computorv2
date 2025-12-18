"""
Simplifier-specific exceptions for Computorv2.
"""


class SimplifierError(Exception):
    """Base exception for simplifier errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CannotSimplifyError(SimplifierError):
    """Raised when expression cannot be simplified further."""
    
    def __init__(self, reason: str = "Expression cannot be simplified"):
        super().__init__(reason)


class UnsupportedExpressionError(SimplifierError):
    """Raised when expression type is not supported for simplification."""
    
    def __init__(self, expr_type: str):
        self.expr_type = expr_type
        super().__init__(f"Unsupported expression type for simplification: {expr_type}")