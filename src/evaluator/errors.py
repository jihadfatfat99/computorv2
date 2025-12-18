"""
Evaluator-specific exceptions for Computorv2.
"""


class EvaluatorError(Exception):
    """Base exception for evaluator errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UndefinedVariableError(EvaluatorError):
    """Raised when referencing an undefined variable."""
    
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Undefined variable: '{name}'")


class UndefinedFunctionError(EvaluatorError):
    """Raised when calling an undefined function."""
    
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Undefined function: '{name}'")


class TypeMismatchError(EvaluatorError):
    """Raised when operation is invalid for given types."""
    
    def __init__(self, operation: str, left_type: str, right_type: str = None):
        self.operation = operation
        self.left_type = left_type
        self.right_type = right_type
        
        if right_type:
            msg = f"Cannot perform '{operation}' between {left_type} and {right_type}"
        else:
            msg = f"Cannot perform '{operation}' on {left_type}"
        
        super().__init__(msg)


class InvalidOperandError(EvaluatorError):
    """Raised when operand is invalid for an operation."""
    
    def __init__(self, message: str):
        super().__init__(message)


class ReservedNameError(EvaluatorError):
    """Raised when trying to assign to a reserved name."""
    
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Cannot assign to reserved name: '{name}'")