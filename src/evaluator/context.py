"""
Evaluation context (symbol table) for Computorv2.

Stores variables and functions defined during the session.
"""

from typing import Any, Dict, Optional, List, Tuple
from ..math_types import Rational, Complex, Matrix, Polynomial, Function
from ..utils import normalize_identifier, is_reserved_keyword
from .errors import UndefinedVariableError, UndefinedFunctionError, ReservedNameError


# Type alias for storable values
Value = Rational | Complex | Matrix | Polynomial


class Context:
    """
    Symbol table storing variables and functions.
    
    All identifiers are case-insensitive (stored lowercase).
    
    Examples:
        >>> ctx = Context()
        >>> ctx.set_variable('x', Rational(5))
        >>> ctx.get_variable('X')  # Case insensitive
        Rational(5, 1)
    """
    
    def __init__(self):
        """Initialize empty context."""
        self._variables: Dict[str, Value] = {}
        self._functions: Dict[str, Function] = {}
    
    # ========================
    # Variable Operations
    # ========================
    
    def set_variable(self, name: str, value: Value) -> None:
        """
        Set a variable value.
        
        Args:
            name: Variable name (case-insensitive)
            value: The value to store
        
        Raises:
            ReservedNameError: If name is reserved (e.g., 'i')
        """
        name = normalize_identifier(name)
        
        if is_reserved_keyword(name):
            raise ReservedNameError(name)
        
        self._variables[name] = value
    
    def get_variable(self, name: str) -> Value:
        """
        Get a variable value.
        
        Args:
            name: Variable name (case-insensitive)
        
        Returns:
            The stored value
        
        Raises:
            UndefinedVariableError: If variable doesn't exist
        """
        name = normalize_identifier(name)
        
        if name not in self._variables:
            raise UndefinedVariableError(name)
        
        return self._variables[name]
    
    def has_variable(self, name: str) -> bool:
        """Check if variable exists."""
        return normalize_identifier(name) in self._variables
    
    def delete_variable(self, name: str) -> bool:
        """
        Delete a variable.
        
        Returns:
            True if deleted, False if didn't exist
        """
        name = normalize_identifier(name)
        if name in self._variables:
            del self._variables[name]
            return True
        return False
    
    def list_variables(self) -> List[Tuple[str, Value]]:
        """Get list of all variables as (name, value) tuples."""
        return list(self._variables.items())
    
    # ========================
    # Function Operations
    # ========================
    
    def set_function(self, name: str, func: Function) -> None:
        """
        Set a function.
        
        Args:
            name: Function name (case-insensitive)
            func: The Function object
        
        Raises:
            ReservedNameError: If name is reserved
        """
        name = normalize_identifier(name)
        
        if is_reserved_keyword(name):
            raise ReservedNameError(name)
        
        self._functions[name] = func
    
    def get_function(self, name: str) -> Function:
        """
        Get a function.
        
        Args:
            name: Function name (case-insensitive)
        
        Returns:
            The Function object
        
        Raises:
            UndefinedFunctionError: If function doesn't exist
        """
        name = normalize_identifier(name)
        
        if name not in self._functions:
            raise UndefinedFunctionError(name)
        
        return self._functions[name]
    
    def has_function(self, name: str) -> bool:
        """Check if function exists."""
        return normalize_identifier(name) in self._functions
    
    def delete_function(self, name: str) -> bool:
        """
        Delete a function.
        
        Returns:
            True if deleted, False if didn't exist
        """
        name = normalize_identifier(name)
        if name in self._functions:
            del self._functions[name]
            return True
        return False
    
    def list_functions(self) -> List[Tuple[str, Function]]:
        """Get list of all functions as (name, function) tuples."""
        return list(self._functions.items())
    
    # ========================
    # General Operations
    # ========================
    
    def has(self, name: str) -> bool:
        """Check if name exists as variable or function."""
        return self.has_variable(name) or self.has_function(name)
    
    def get(self, name: str) -> Value | Function:
        """
        Get variable or function by name.
        
        Variables take precedence over functions.
        """
        name = normalize_identifier(name)
        
        if name in self._variables:
            return self._variables[name]
        if name in self._functions:
            return self._functions[name]
        
        raise UndefinedVariableError(name)
    
    def clear(self) -> None:
        """Clear all variables and functions."""
        self._variables.clear()
        self._functions.clear()
    
    def copy(self) -> 'Context':
        """Create a copy of this context."""
        new_ctx = Context()
        new_ctx._variables = dict(self._variables)
        new_ctx._functions = dict(self._functions)
        return new_ctx
    
    def __contains__(self, name: str) -> bool:
        """Support 'in' operator."""
        return self.has(name)
    
    def __repr__(self) -> str:
        return f"Context(variables={list(self._variables.keys())}, functions={list(self._functions.keys())})"