"""
Lexer module for Computorv2.

Provides tokenization of input strings into a stream of tokens
for the parser.

Main components:
    - Lexer: Main tokenizer class
    - Token: Token dataclass
    - TokenType: Enumeration of token types
    - tokenize(): Convenience function
"""

from .tokens import (
    Token,
    TokenType,
    SINGLE_CHAR_TOKENS,
    TOKEN_NAMES,
    token_type_to_str,
)

from .lexer import (
    Lexer,
    tokenize,
)

from .errors import (
    LexerError,
    UnexpectedCharacterError,
    InvalidNumberError,
    UnterminatedError,
)


__all__ = [
    # Token classes
    'Token',
    'TokenType',
    'SINGLE_CHAR_TOKENS',
    'TOKEN_NAMES',
    'token_type_to_str',
    
    # Lexer
    'Lexer',
    'tokenize',
    
    # Errors
    'LexerError',
    'UnexpectedCharacterError',
    'InvalidNumberError',
    'UnterminatedError',
]