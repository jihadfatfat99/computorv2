"""
Operator precedence definitions for Computorv2 parser.

Defines the binding power of operators for correct parsing
of expressions like 2 + 3 * 4 (should parse as 2 + (3 * 4)).
"""

from ..lexer import TokenType


# Precedence levels (higher = binds tighter)
class Precedence:
    """Precedence levels for operators"""
    NONE = 0
    ASSIGNMENT = 1    # =
    ADDITIVE = 2      # +, -
    MULTIPLICATIVE = 3  # *, /, %, **
    POWER = 4         # ^
    UNARY = 5         # unary +, -
    CALL = 6          # function call ()
    PRIMARY = 7       # literals, grouping


# Map token types to their precedence
PRECEDENCE_MAP = {
    TokenType.PLUS: Precedence.ADDITIVE,
    TokenType.MINUS: Precedence.ADDITIVE,
    TokenType.STAR: Precedence.MULTIPLICATIVE,
    TokenType.STARSTAR: Precedence.MULTIPLICATIVE,
    TokenType.SLASH: Precedence.MULTIPLICATIVE,
    TokenType.PERCENT: Precedence.MULTIPLICATIVE,
    TokenType.CARET: Precedence.POWER,
    TokenType.EQUALS: Precedence.ASSIGNMENT,
}


# Right-associative operators (a^b^c = a^(b^c))
RIGHT_ASSOCIATIVE = {
    TokenType.CARET,
}


# Map token types to operator strings
OPERATOR_MAP = {
    TokenType.PLUS: '+',
    TokenType.MINUS: '-',
    TokenType.STAR: '*',
    TokenType.STARSTAR: '**',
    TokenType.SLASH: '/',
    TokenType.PERCENT: '%',
    TokenType.CARET: '^',
}


def get_precedence(token_type: TokenType) -> int:
    """
    Get the precedence of a token type.
    
    Args:
        token_type: The token type to look up
    
    Returns:
        Precedence level (0 if not an operator)
    """
    return PRECEDENCE_MAP.get(token_type, Precedence.NONE)


def is_right_associative(token_type: TokenType) -> bool:
    """
    Check if an operator is right-associative.
    
    Args:
        token_type: The token type to check
    
    Returns:
        True if right-associative, False otherwise
    """
    return token_type in RIGHT_ASSOCIATIVE


def get_operator(token_type: TokenType) -> str:
    """
    Get the operator string for a token type.
    
    Args:
        token_type: The token type
    
    Returns:
        Operator string or empty string if not an operator
    """
    return OPERATOR_MAP.get(token_type, '')


def is_binary_operator(token_type: TokenType) -> bool:
    """Check if token type is a binary operator"""
    return token_type in OPERATOR_MAP


def is_additive_operator(token_type: TokenType) -> bool:
    """Check if token type is additive (+, -)"""
    return token_type in {TokenType.PLUS, TokenType.MINUS}


def is_multiplicative_operator(token_type: TokenType) -> bool:
    """Check if token type is multiplicative (*, /, %, **)"""
    return token_type in {
        TokenType.STAR,
        TokenType.STARSTAR,
        TokenType.SLASH,
        TokenType.PERCENT,
    }