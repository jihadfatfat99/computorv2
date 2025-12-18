"""
Parser-specific exceptions for Computorv2.
"""

from typing import Optional
from ..lexer import Token, TokenType, token_type_to_str


class ParserError(Exception):
    """
    Base exception for parser errors.
    
    Attributes:
        message: Error description
        token: The token where error occurred (if available)
    """
    
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        """Format error message with position info"""
        if self.token:
            return f"Parser error at position {self.token.position}: {self.message}"
        return f"Parser error: {self.message}"


class UnexpectedTokenError(ParserError):
    """Raised when an unexpected token is encountered"""
    
    def __init__(
        self,
        token: Token,
        expected: Optional[str] = None,
        context: Optional[str] = None
    ):
        self.expected = expected
        self.context = context
        
        msg = f"Unexpected {token.type_name}"
        if expected:
            msg += f", expected {expected}"
        if context:
            msg += f" ({context})"
        
        super().__init__(msg, token)


class ExpectedTokenError(ParserError):
    """Raised when an expected token is missing"""
    
    def __init__(
        self,
        expected: TokenType,
        got: Token,
        context: Optional[str] = None
    ):
        self.expected_type = expected
        
        msg = f"Expected {token_type_to_str(expected)}, got {got.type_name}"
        if context:
            msg += f" ({context})"
        
        super().__init__(msg, got)


class InvalidSyntaxError(ParserError):
    """Raised for general syntax errors"""
    
    def __init__(self, message: str, token: Optional[Token] = None):
        super().__init__(message, token)


class InvalidAssignmentError(ParserError):
    """Raised when assignment target is invalid"""
    
    def __init__(self, target: str, token: Optional[Token] = None):
        message = f"Invalid assignment target: {target}"
        super().__init__(message, token)


class InvalidMatrixError(ParserError):
    """Raised when matrix syntax is invalid"""
    
    def __init__(self, reason: str, token: Optional[Token] = None):
        message = f"Invalid matrix: {reason}"
        super().__init__(message, token)


class InvalidFunctionError(ParserError):
    """Raised when function definition/call is invalid"""
    
    def __init__(self, reason: str, token: Optional[Token] = None):
        message = f"Invalid function: {reason}"
        super().__init__(message, token)