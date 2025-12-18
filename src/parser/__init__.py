"""
Parser module for Computorv2.

Converts tokens into an Abstract Syntax Tree (AST) for evaluation.

Main components:
    - Parser: Main recursive descent parser
    - parse(): Convenience function
    - AST Nodes: All node types for the syntax tree
"""

from .ast_nodes import (
    # Base classes
    ASTNode,
    ASTVisitor,
    
    # Literal nodes
    NumberNode,
    IdentifierNode,
    ImaginaryNode,
    
    # Operation nodes
    BinaryOpNode,
    UnaryOpNode,
    
    # Structure nodes
    MatrixNode,
    FunctionCallNode,
    
    # Statement nodes
    AssignmentNode,
    FunctionDefNode,
    QueryNode,
    EquationNode,
    
    # Helper functions
    is_literal,
    is_operation,
    is_statement,
)

from .precedence import (
    Precedence,
    get_precedence,
    is_right_associative,
    get_operator,
    is_binary_operator,
    is_additive_operator,
    is_multiplicative_operator,
)

from .parser import (
    Parser,
    parse,
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


__all__ = [
    # Base classes
    'ASTNode',
    'ASTVisitor',
    
    # Literal nodes
    'NumberNode',
    'IdentifierNode',
    'ImaginaryNode',
    
    # Operation nodes
    'BinaryOpNode',
    'UnaryOpNode',
    
    # Structure nodes
    'MatrixNode',
    'FunctionCallNode',
    
    # Statement nodes
    'AssignmentNode',
    'FunctionDefNode',
    'QueryNode',
    'EquationNode',
    
    # Helper functions
    'is_literal',
    'is_operation',
    'is_statement',
    
    # Precedence
    'Precedence',
    'get_precedence',
    'is_right_associative',
    'get_operator',
    'is_binary_operator',
    'is_additive_operator',
    'is_multiplicative_operator',
    
    # Parser
    'Parser',
    'parse',
    
    # Errors
    'ParserError',
    'UnexpectedTokenError',
    'ExpectedTokenError',
    'InvalidSyntaxError',
    'InvalidAssignmentError',
    'InvalidMatrixError',
    'InvalidFunctionError',
]