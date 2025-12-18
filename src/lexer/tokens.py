"""
Token definitions for Computorv2 lexer.

Defines all token types and the Token dataclass used throughout
the parsing pipeline.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """
    Enumeration of all token types recognized by the lexer.
    """
    
    # Literals
    NUMBER = auto()          # Integer or decimal: 42, 3.14
    IDENTIFIER = auto()      # Variable/function name: varA, funB
    IMAGINARY = auto()       # Imaginary unit: i
    
    # Arithmetic operators
    PLUS = auto()            # +
    MINUS = auto()           # -
    STAR = auto()            # *
    STARSTAR = auto()        # ** (matrix multiplication)
    SLASH = auto()           # /
    PERCENT = auto()         # %
    CARET = auto()           # ^
    
    # Delimiters
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    COMMA = auto()           # ,
    SEMICOLON = auto()       # ;
    
    # Assignment and query
    EQUALS = auto()          # =
    QUESTION = auto()        # ?
    
    # Special
    EOF = auto()             # End of input
    NEWLINE = auto()         # End of line (optional)


# Mapping of single-character tokens
SINGLE_CHAR_TOKENS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '/': TokenType.SLASH,
    '%': TokenType.PERCENT,
    '^': TokenType.CARET,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    '=': TokenType.EQUALS,
    '?': TokenType.QUESTION,
}

# Token type display names for error messages
TOKEN_NAMES = {
    TokenType.NUMBER: "number",
    TokenType.IDENTIFIER: "identifier",
    TokenType.IMAGINARY: "imaginary unit 'i'",
    TokenType.PLUS: "'+'",
    TokenType.MINUS: "'-'",
    TokenType.STAR: "'*'",
    TokenType.STARSTAR: "'**'",
    TokenType.SLASH: "'/'",
    TokenType.PERCENT: "'%'",
    TokenType.CARET: "'^'",
    TokenType.LPAREN: "'('",
    TokenType.RPAREN: "')'",
    TokenType.LBRACKET: "'['",
    TokenType.RBRACKET: "']'",
    TokenType.COMMA: "','",
    TokenType.SEMICOLON: "';'",
    TokenType.EQUALS: "'='",
    TokenType.QUESTION: "'?'",
    TokenType.EOF: "end of input",
    TokenType.NEWLINE: "newline",
}


@dataclass(frozen=True, slots=True)
class Token:
    """
    Represents a single token from the input.
    
    Attributes:
        type: The type of token
        value: The actual value (number, identifier name, etc.)
        position: Character position in the input string
        line: Line number (for multi-line support)
        column: Column number within the line
    """
    
    type: TokenType
    value: Any
    position: int
    line: int = 1
    column: int = 0
    
    def __str__(self) -> str:
        if self.type == TokenType.EOF:
            return "EOF"
        if self.type == TokenType.NUMBER:
            return f"NUMBER({self.value})"
        if self.type == TokenType.IDENTIFIER:
            return f"IDENTIFIER({self.value})"
        if self.type == TokenType.IMAGINARY:
            return "IMAGINARY(i)"
        return f"{self.type.name}"
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, pos={self.position})"
    
    @property
    def type_name(self) -> str:
        """Get human-readable token type name"""
        return TOKEN_NAMES.get(self.type, self.type.name)
    
    def is_operator(self) -> bool:
        """Check if this token is an operator"""
        return self.type in {
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.STARSTAR,
            TokenType.SLASH,
            TokenType.PERCENT,
            TokenType.CARET,
        }
    
    def is_additive(self) -> bool:
        """Check if this is an additive operator (+, -)"""
        return self.type in {TokenType.PLUS, TokenType.MINUS}
    
    def is_multiplicative(self) -> bool:
        """Check if this is a multiplicative operator (*, /, %, **)"""
        return self.type in {
            TokenType.STAR,
            TokenType.STARSTAR,
            TokenType.SLASH,
            TokenType.PERCENT,
        }
    
    def is_literal(self) -> bool:
        """Check if this token is a literal value"""
        return self.type in {
            TokenType.NUMBER,
            TokenType.IDENTIFIER,
            TokenType.IMAGINARY,
        }


def token_type_to_str(token_type: TokenType) -> str:
    """Convert token type to human-readable string"""
    return TOKEN_NAMES.get(token_type, token_type.name)