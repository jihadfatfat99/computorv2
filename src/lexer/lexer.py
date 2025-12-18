"""
Lexer for Computorv2.

Converts input strings into a stream of tokens for the parser.
Handles numbers, identifiers, operators, and special symbols.
"""

from typing import Iterator, List, Optional

from .tokens import Token, TokenType, SINGLE_CHAR_TOKENS
from .errors import (
    LexerError,
    UnexpectedCharacterError,
    InvalidNumberError,
)
from ..utils import is_valid_identifier, is_reserved_keyword


class Lexer:
    """
    Tokenizer for Computorv2 input.
    
    Converts a string into a sequence of tokens. Handles:
        - Numbers (integers and decimals)
        - Identifiers (variable and function names)
        - Imaginary unit 'i'
        - Operators (+, -, *, **, /, %, ^)
        - Delimiters ((, ), [, ], ,, ;)
        - Assignment (=) and query (?)
    
    Examples:
        >>> lexer = Lexer("x = 2 + 3i")
        >>> tokens = lexer.tokenize()
        >>> for tok in tokens:
        ...     print(tok)
    """
    
    def __init__(self, text: str):
        """
        Initialize the lexer with input text.
        
        Args:
            text: The input string to tokenize
        """
        self._text = text
        self._pos = 0
        self._line = 1
        self._column = 1
        self._tokens: List[Token] = []
    
    # ========================
    # Position Management
    # ========================
    
    @property
    def _current_char(self) -> Optional[str]:
        """Get current character or None if at end"""
        if self._pos >= len(self._text):
            return None
        return self._text[self._pos]
    
    def _peek(self, offset: int = 1) -> Optional[str]:
        """Peek at character at current position + offset"""
        pos = self._pos + offset
        if pos >= len(self._text):
            return None
        return self._text[pos]
    
    def _advance(self) -> Optional[str]:
        """Advance position and return current character"""
        char = self._current_char
        if char is not None:
            self._pos += 1
            if char == '\n':
                self._line += 1
                self._column = 1
            else:
                self._column += 1
        return char
    
    def _skip_whitespace(self) -> None:
        """Skip whitespace characters (except newlines if tracking them)"""
        while self._current_char is not None and self._current_char in ' \t\r\n':
            self._advance()
    
    # ========================
    # Token Creation
    # ========================
    
    def _make_token(self, token_type: TokenType, value: any = None) -> Token:
        """Create a token at current position"""
        return Token(
            type=token_type,
            value=value,
            position=self._pos,
            line=self._line,
            column=self._column
        )
    
    # ========================
    # Number Lexing
    # ========================
    
    def _read_number(self) -> Token:
        """
        Read a number token (integer or decimal).
        
        Handles:
            - Integers: 42, 0, 123
            - Decimals: 3.14, 0.5, .5
        """
        start_pos = self._pos
        has_dot = False
        num_str = ""
        
        # Handle leading dot (e.g., .5)
        if self._current_char == '.':
            has_dot = True
            num_str += self._advance()
        
        # Read digits
        while self._current_char is not None:
            if self._current_char.isdigit():
                num_str += self._advance()
            elif self._current_char == '.' and not has_dot:
                # Check if next char is digit (to distinguish from other uses of .)
                if self._peek() is not None and self._peek().isdigit():
                    has_dot = True
                    num_str += self._advance()
                else:
                    break
            else:
                break
        
        # Validate number
        if not num_str or num_str == '.':
            raise InvalidNumberError(num_str, start_pos, self._line, self._column)
        
        # Convert to appropriate type
        try:
            if has_dot:
                value = float(num_str)
            else:
                value = int(num_str)
        except ValueError:
            raise InvalidNumberError(num_str, start_pos, self._line, self._column)
        
        return Token(
            type=TokenType.NUMBER,
            value=value,
            position=start_pos,
            line=self._line,
            column=self._column
        )
    
    # ========================
    # Identifier Lexing
    # ========================
    
    def _read_identifier(self) -> Token:
        """
        Read an identifier token.
        
        Identifiers must contain only letters (a-z, A-Z).
        The special identifier 'i' is returned as IMAGINARY token.
        """
        start_pos = self._pos
        name = ""
        
        while self._current_char is not None and self._current_char.isalpha():
            name += self._advance()
        
        # Normalize to lowercase for case-insensitivity
        name_lower = name.lower()
        
        # Check for imaginary unit
        if name_lower == 'i':
            return Token(
                type=TokenType.IMAGINARY,
                value='i',
                position=start_pos,
                line=self._line,
                column=self._column
            )
        
        return Token(
            type=TokenType.IDENTIFIER,
            value=name_lower,  # Store normalized (lowercase) version
            position=start_pos,
            line=self._line,
            column=self._column
        )
    
    # ========================
    # Operator Lexing
    # ========================
    
    def _read_star(self) -> Token:
        """
        Read * or ** token.
        """
        start_pos = self._pos
        self._advance()  # consume first *
        
        if self._current_char == '*':
            self._advance()  # consume second *
            return Token(
                type=TokenType.STARSTAR,
                value='**',
                position=start_pos,
                line=self._line,
                column=self._column
            )
        
        return Token(
            type=TokenType.STAR,
            value='*',
            position=start_pos,
            line=self._line,
            column=self._column
        )
    
    # ========================
    # Main Tokenization
    # ========================
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire input string.
        
        Returns:
            List of tokens ending with EOF token
        
        Raises:
            LexerError: If invalid input is encountered
        """
        self._tokens = []
        
        while self._current_char is not None:
            # Skip whitespace
            if self._current_char in ' \t\r\n':
                self._skip_whitespace()
                continue
            
            # Number (starts with digit or dot followed by digit)
            if self._current_char.isdigit():
                self._tokens.append(self._read_number())
                continue
            
            if self._current_char == '.' and self._peek() is not None and self._peek().isdigit():
                self._tokens.append(self._read_number())
                continue
            
            # Identifier (starts with letter)
            if self._current_char.isalpha():
                self._tokens.append(self._read_identifier())
                continue
            
            # Star (could be * or **)
            if self._current_char == '*':
                self._tokens.append(self._read_star())
                continue
            
            # Single-character tokens
            if self._current_char in SINGLE_CHAR_TOKENS:
                token_type = SINGLE_CHAR_TOKENS[self._current_char]
                char = self._current_char
                token = Token(
                    type=token_type,
                    value=char,
                    position=self._pos,
                    line=self._line,
                    column=self._column
                )
                self._advance()
                self._tokens.append(token)
                continue
            
            # Unknown character
            raise UnexpectedCharacterError(
                self._current_char,
                self._pos,
                self._line,
                self._column
            )
        
        # Add EOF token
        self._tokens.append(Token(
            type=TokenType.EOF,
            value=None,
            position=self._pos,
            line=self._line,
            column=self._column
        ))
        
        return self._tokens
    
    def __iter__(self) -> Iterator[Token]:
        """Iterate over tokens"""
        if not self._tokens:
            self.tokenize()
        return iter(self._tokens)


def tokenize(text: str) -> List[Token]:
    """
    Convenience function to tokenize a string.
    
    Args:
        text: Input string to tokenize
    
    Returns:
        List of tokens
    """
    lexer = Lexer(text)
    return lexer.tokenize()