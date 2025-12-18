"""
Lexer-specific exceptions for Computorv2.
"""


class LexerError(Exception):
    """
    Base exception for lexer errors.
    
    Attributes:
        message: Error description
        position: Character position where error occurred
        line: Line number
        column: Column number
    """
    
    def __init__(
        self,
        message: str,
        position: int = 0,
        line: int = 1,
        column: int = 0
    ):
        self.message = message
        self.position = position
        self.line = line
        self.column = column
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        """Format error message with position info"""
        return f"Lexer error at position {self.position}: {self.message}"


class UnexpectedCharacterError(LexerError):
    """Raised when an unexpected character is encountered"""
    
    def __init__(self, char: str, position: int, line: int = 1, column: int = 0):
        self.char = char
        message = f"Unexpected character '{char}'"
        super().__init__(message, position, line, column)


class InvalidNumberError(LexerError):
    """Raised when a number is malformed"""
    
    def __init__(self, number_str: str, position: int, line: int = 1, column: int = 0):
        self.number_str = number_str
        message = f"Invalid number format '{number_str}'"
        super().__init__(message, position, line, column)


class UnterminatedError(LexerError):
    """Raised when something is not properly terminated"""
    
    def __init__(self, what: str, position: int, line: int = 1, column: int = 0):
        message = f"Unterminated {what}"
        super().__init__(message, position, line, column)