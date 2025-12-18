"""
Parser for Computorv2.

Converts a stream of tokens into an Abstract Syntax Tree (AST).
Uses recursive descent parsing with operator precedence climbing.
"""

from typing import List, Optional

from ..lexer import Token, TokenType, Lexer, tokenize
from .ast_nodes import (
    ASTNode,
    NumberNode,
    IdentifierNode,
    ImaginaryNode,
    BinaryOpNode,
    UnaryOpNode,
    MatrixNode,
    FunctionCallNode,
    AssignmentNode,
    FunctionDefNode,
    QueryNode,
    EquationNode,
)
from .precedence import (
    Precedence,
    get_precedence,
    is_right_associative,
    get_operator,
    is_binary_operator,
)
from .errors import (
    ParserError,
    UnexpectedTokenError,
    ExpectedTokenError,
    InvalidSyntaxError,
    InvalidAssignmentError,
    InvalidMatrixError,
    InvalidFunctionError,
)
from ..utils import is_valid_identifier, is_reserved_keyword


class Parser:
    """
    Recursive descent parser for Computorv2.
    
    Grammar (simplified):
        statement     → assignment | function_def | query | equation | expression
        assignment    → IDENTIFIER '=' expression
        function_def  → IDENTIFIER '(' IDENTIFIER ')' '=' expression
        query         → expression '=' '?'
        equation      → expression '=' expression '?'
        expression    → term (('+' | '-') term)*
        term          → power (('*' | '**' | '/' | '%') power)*
        power         → unary ('^' power)?
        unary         → ('+' | '-') unary | call
        call          → primary ('(' expression ')')?
        primary       → NUMBER | IDENTIFIER | IMAGINARY | '(' expression ')' | matrix
        matrix        → '[' '[' expr_list ']' (';' '[' expr_list ']')* ']'
        expr_list     → expression (',' expression)*
    
    Examples:
        >>> parser = Parser("x = 2 + 3")
        >>> ast = parser.parse()
    """
    
    def __init__(self, source: str):
        """
        Initialize parser with source string.
        
        Args:
            source: The input string to parse
        """
        self._tokens: List[Token] = tokenize(source)
        self._pos = 0
        self._source = source
    
    # ========================
    # Token Navigation
    # ========================
    
    @property
    def _current(self) -> Token:
        """Get current token"""
        if self._pos >= len(self._tokens):
            return self._tokens[-1]  # Return EOF
        return self._tokens[self._pos]
    
    def _peek(self, offset: int = 0) -> Token:
        """Peek at token at current position + offset"""
        pos = self._pos + offset
        if pos >= len(self._tokens):
            return self._tokens[-1]  # Return EOF
        return self._tokens[pos]
    
    def _advance(self) -> Token:
        """Advance and return current token"""
        token = self._current
        if self._pos < len(self._tokens) - 1:
            self._pos += 1
        return token
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens"""
        return self._current.type == TokenType.EOF
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type"""
        return self._current.type == token_type
    
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of given types, advance if so"""
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False
    
    def _expect(self, token_type: TokenType, context: str = "") -> Token:
        """Expect current token to be of given type, raise error if not"""
        if self._check(token_type):
            return self._advance()
        raise ExpectedTokenError(token_type, self._current, context)
    
    # ========================
    # Main Parse Entry
    # ========================
    
    def parse(self) -> ASTNode:
        """
        Parse the input and return the AST.
        
        Returns:
            The root AST node
        
        Raises:
            ParserError: If parsing fails
        """
        result = self._parse_statement()
        
        if not self._is_at_end():
            raise UnexpectedTokenError(
                self._current,
                expected="end of input",
                context="after statement"
            )
        
        return result
    
    # ========================
    # Statement Parsing
    # ========================
    
    def _parse_statement(self) -> ASTNode:
        """
        Parse a statement.
        
        Determines if input is:
            - Function definition: f(x) = ...
            - Variable assignment: x = ...
            - Query: expr = ?
            - Equation: expr = expr ?
            - Simple expression
        """
        # Look ahead to determine statement type
        if self._check(TokenType.IDENTIFIER):
            # Could be: assignment, function def, or expression
            
            # Check for function definition: name(param) = ...
            if self._peek(1).type == TokenType.LPAREN:
                if self._is_function_definition():
                    return self._parse_function_definition()
            
            # Check for assignment: name = ...
            if self._peek(1).type == TokenType.EQUALS:
                # Make sure it's not: name = expr ?  (which is a query)
                # or: name = expr ? (which could be equation)
                return self._parse_assignment_or_query()
        
        # Otherwise parse as expression (might become query/equation)
        return self._parse_expression_statement()
    
    def _is_function_definition(self) -> bool:
        """
        Look ahead to determine if this is a function definition.
        
        Pattern: IDENTIFIER '(' IDENTIFIER ')' '='
        """
        if not self._check(TokenType.IDENTIFIER):
            return False
        if self._peek(1).type != TokenType.LPAREN:
            return False
        if self._peek(2).type != TokenType.IDENTIFIER:
            return False
        if self._peek(3).type != TokenType.RPAREN:
            return False
        if self._peek(4).type != TokenType.EQUALS:
            return False
        return True
    
    def _parse_function_definition(self) -> ASTNode:
        """
        Parse function definition or equation involving function.
        
        - f(x) = expr     → Function definition
        - f(x) = expr ?   → Equation to solve (left side is function call)
        """
        name_token = self._expect(TokenType.IDENTIFIER, "function name")
        name = name_token.value
        
        if is_reserved_keyword(name):
            raise InvalidFunctionError(f"'{name}' is reserved", name_token)
        
        self._expect(TokenType.LPAREN, "function definition")
        
        param_token = self._expect(TokenType.IDENTIFIER, "function parameter")
        param = param_token.value
        
        if is_reserved_keyword(param):
            raise InvalidFunctionError(f"parameter '{param}' is reserved", param_token)
        
        self._expect(TokenType.RPAREN, "function definition")
        self._expect(TokenType.EQUALS, "function definition")
        
        body = self._parse_expression()
        
        # Check for equation: f(x) = expr ?
        if self._check(TokenType.QUESTION):
            self._advance()
            # This is an equation: f(x) = expr, to be solved
            # Return as EquationNode with left=FunctionCall, right=body
            left = FunctionCallNode(name, IdentifierNode(param))
            return EquationNode(left, body)
        
        return FunctionDefNode(name, param, body)
    
    def _parse_assignment_or_query(self) -> ASTNode:
        """
        Parse assignment, query, or equation starting with identifier.
        
        Patterns:
            - x = expr         → Assignment
            - x = expr ?       → Query (evaluate expr after assigning)
            - x = ?            → Query (get value of x)
        """
        name_token = self._expect(TokenType.IDENTIFIER, "assignment")
        name = name_token.value
        
        if is_reserved_keyword(name):
            raise InvalidAssignmentError(f"'{name}' is reserved", name_token)
        
        self._expect(TokenType.EQUALS, "assignment")
        
        # Check for simple query: x = ?
        if self._check(TokenType.QUESTION):
            self._advance()
            return QueryNode(IdentifierNode(name))
        
        # Parse the right side
        expr = self._parse_expression()
        
        # Check for query after assignment: x = expr ?
        if self._check(TokenType.QUESTION):
            self._advance()
            # This assigns and then queries
            return AssignmentNode(name, expr)
        
        # Check for equation: x = expr = ? (where left side already parsed)
        # Actually this would be: var = expr, not equation
        
        return AssignmentNode(name, expr)
    
    def _parse_expression_statement(self) -> ASTNode:
        """
        Parse expression that might be followed by = ? or = expr ?
        """
        expr = self._parse_expression()
        
        # Check for = ?
        if self._check(TokenType.EQUALS):
            self._advance()
            
            # Simple query: expr = ?
            if self._check(TokenType.QUESTION):
                self._advance()
                return QueryNode(expr)
            
            # Equation: expr = expr ?
            right = self._parse_expression()
            
            if self._check(TokenType.QUESTION):
                self._advance()
                return EquationNode(expr, right)
            
            # This is invalid: expr = expr without ?
            raise InvalidSyntaxError(
                "Expected '?' after equation or expression",
                self._current
            )
        
        return expr
    
    # ========================
    # Expression Parsing
    # ========================
    
    def _parse_expression(self) -> ASTNode:
        """Parse expression using precedence climbing"""
        return self._parse_precedence(Precedence.ADDITIVE)
    
    def _parse_precedence(self, min_precedence: int) -> ASTNode:
        """
        Parse expression with minimum precedence level.
        
        Uses precedence climbing algorithm for correct associativity.
        """
        left = self._parse_unary()
        
        while True:
            # Check if current token is a binary operator with sufficient precedence
            if not is_binary_operator(self._current.type):
                break
            
            prec = get_precedence(self._current.type)
            if prec < min_precedence:
                break
            
            op_token = self._advance()
            operator = get_operator(op_token.type)
            
            # Handle right associativity
            next_min_prec = prec + 1
            if is_right_associative(op_token.type):
                next_min_prec = prec
            
            right = self._parse_precedence(next_min_prec)
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def _parse_unary(self) -> ASTNode:
        """Parse unary expression: +expr, -expr, or call"""
        if self._check(TokenType.PLUS) or self._check(TokenType.MINUS):
            op_token = self._advance()
            operator = '+' if op_token.type == TokenType.PLUS else '-'
            operand = self._parse_unary()
            return UnaryOpNode(operator, operand)
        
        return self._parse_power()
    
    def _parse_power(self) -> ASTNode:
        """Parse power expression: base ^ exponent (right associative)"""
        left = self._parse_call()
        
        if self._check(TokenType.CARET):
            self._advance()
            right = self._parse_unary()  # Right associative
            return BinaryOpNode('^', left, right)
        
        return left
    
    def _parse_call(self) -> ASTNode:
        """Parse function call or primary"""
        # Check for function call: identifier(expr)
        if self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.LPAREN:
            # Could be function call
            name_token = self._advance()
            name = name_token.value
            
            self._expect(TokenType.LPAREN, "function call")
            
            # Handle empty parentheses (not typical but handle gracefully)
            if self._check(TokenType.RPAREN):
                raise InvalidFunctionError("function call requires an argument", self._current)
            
            argument = self._parse_expression()
            
            self._expect(TokenType.RPAREN, "function call")
            
            return FunctionCallNode(name, argument)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> ASTNode:
        """Parse primary expression: literals, grouping, matrix"""
        # Number
        if self._check(TokenType.NUMBER):
            token = self._advance()
            return NumberNode(token.value)
        
        # Identifier
        if self._check(TokenType.IDENTIFIER):
            token = self._advance()
            return IdentifierNode(token.value)
        
        # Imaginary unit
        if self._check(TokenType.IMAGINARY):
            self._advance()
            return ImaginaryNode()
        
        # Grouped expression: (expr)
        if self._check(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "grouped expression")
            return expr
        
        # Matrix: [[...];[...]]
        if self._check(TokenType.LBRACKET):
            return self._parse_matrix()
        
        raise UnexpectedTokenError(
            self._current,
            expected="expression",
            context="primary"
        )
    
    # ========================
    # Matrix Parsing
    # ========================
    
    def _parse_matrix(self) -> MatrixNode:
        """
        Parse matrix literal: [[a,b];[c,d]]
        
        Syntax:
            - Outer brackets: [ ... ]
            - Rows separated by semicolon: [row1];[row2]
            - Elements separated by comma: a,b,c
        """
        self._expect(TokenType.LBRACKET, "matrix")
        
        rows: List[List[ASTNode]] = []
        
        # Parse first row
        first_row = self._parse_matrix_row()
        rows.append(first_row)
        expected_cols = len(first_row)
        
        # Parse additional rows
        while self._check(TokenType.SEMICOLON):
            self._advance()  # consume ;
            row = self._parse_matrix_row()
            
            if len(row) != expected_cols:
                raise InvalidMatrixError(
                    f"row has {len(row)} elements, expected {expected_cols}",
                    self._current
                )
            
            rows.append(row)
        
        self._expect(TokenType.RBRACKET, "matrix")
        
        return MatrixNode(rows)
    
    def _parse_matrix_row(self) -> List[ASTNode]:
        """Parse a single matrix row: [a, b, c]"""
        self._expect(TokenType.LBRACKET, "matrix row")
        
        elements: List[ASTNode] = []
        
        # Parse first element
        elements.append(self._parse_expression())
        
        # Parse additional elements
        while self._check(TokenType.COMMA):
            self._advance()  # consume ,
            elements.append(self._parse_expression())
        
        self._expect(TokenType.RBRACKET, "matrix row")
        
        return elements


def parse(source: str) -> ASTNode:
    """
    Convenience function to parse a string.
    
    Args:
        source: Input string to parse
    
    Returns:
        The root AST node
    """
    parser = Parser(source)
    return parser.parse()