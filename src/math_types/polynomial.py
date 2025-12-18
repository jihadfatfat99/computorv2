"""
Polynomial implementation for Computorv2.

Represents polynomials as a mapping of degree to coefficient.
Used for symbolic expressions and equation solving.
"""

from __future__ import annotations
from typing import Any, Dict, Union

from .base import (
    MathType,
    DivisionByZeroError,
    InvalidOperationError,
    InvalidExponentError,
)
from .rational import Rational
from .complex import Complex
from ..utils import MAX_POLYNOMIAL_DEGREE


# Type alias for coefficients
Coefficient = Union[Rational, Complex]


class Polynomial(MathType):
    """
    Polynomial with Rational or Complex coefficients.
    
    Stored as a dictionary mapping degree (int) to coefficient.
    Example: 3x² + 2x - 1 is stored as {2: 3, 1: 2, 0: -1}
    
    The variable name is stored for display purposes.
    
    Examples:
        >>> Polynomial({2: Rational(1), 1: Rational(2), 0: Rational(1)})  # x² + 2x + 1
        >>> Polynomial.from_constant(5)  # 5 (degree 0)
        >>> Polynomial.x()  # x (degree 1)
    """
    
    __slots__ = ('_coeffs', '_variable')
    
    def __init__(self, coefficients: Dict[int, Coefficient] = None, variable: str = 'x'):
        """
        Create a Polynomial.
        
        Args:
            coefficients: Dictionary mapping degree to coefficient
            variable: Variable name for display (default 'x')
        """
        self._variable = variable.lower()
        self._coeffs: Dict[int, Coefficient] = {}
        
        if coefficients:
            for degree, coeff in coefficients.items():
                if not isinstance(degree, int) or degree < 0:
                    raise InvalidOperationError(f"Polynomial degree must be non-negative integer, got {degree}")
                coeff = self._ensure_coefficient(coeff)
                if not coeff.is_zero():
                    self._coeffs[degree] = coeff
    
    @staticmethod
    def _ensure_coefficient(value: Any) -> Coefficient:
        """Convert a value to a valid coefficient (Rational or Complex)"""
        if isinstance(value, Complex):
            return value
        if isinstance(value, Rational):
            return value
        if isinstance(value, int):
            return Rational.from_int(value)
        if isinstance(value, float):
            return Rational.from_float(value)
        raise InvalidOperationError(
            f"Cannot use {type(value).__name__} as polynomial coefficient"
        )
    
    # ========================
    # Properties
    # ========================
    
    @property
    def variable(self) -> str:
        """Get the variable name"""
        return self._variable
    
    @property
    def degree(self) -> int:
        """Get the highest degree with non-zero coefficient"""
        if not self._coeffs:
            return 0
        return max(self._coeffs.keys())
    
    @property
    def type_name(self) -> str:
        return "Polynomial"
    
    @property
    def coefficients(self) -> Dict[int, Coefficient]:
        """Get a copy of the coefficients dictionary"""
        return dict(self._coeffs)
    
    # ========================
    # Coefficient Access
    # ========================
    
    def get_coefficient(self, degree: int) -> Coefficient:
        """Get coefficient for a specific degree (returns 0 if not present)"""
        return self._coeffs.get(degree, Rational.zero())
    
    def set_coefficient(self, degree: int, value: Any) -> None:
        """Set coefficient for a specific degree"""
        coeff = self._ensure_coefficient(value)
        if coeff.is_zero():
            self._coeffs.pop(degree, None)
        else:
            self._coeffs[degree] = coeff
    
    def leading_coefficient(self) -> Coefficient:
        """Get the coefficient of the highest degree term"""
        if not self._coeffs:
            return Rational.zero()
        return self._coeffs[self.degree]
    
    # ========================
    # Factory Methods
    # ========================
    
    @classmethod
    def from_constant(cls, value: Any, variable: str = 'x') -> Polynomial:
        """Create a constant polynomial (degree 0)"""
        coeff = cls._ensure_coefficient(value)
        if coeff.is_zero():
            return cls({}, variable)
        return cls({0: coeff}, variable)
    
    @classmethod
    def x(cls, variable: str = 'x') -> Polynomial:
        """Create the polynomial 'x' (degree 1 with coefficient 1)"""
        return cls({1: Rational.one()}, variable)
    
    @classmethod
    def zero(cls, variable: str = 'x') -> Polynomial:
        """Return the zero polynomial"""
        return cls({}, variable)
    
    @classmethod
    def one(cls, variable: str = 'x') -> Polynomial:
        """Return the constant polynomial 1"""
        return cls({0: Rational.one()}, variable)
    
    # ========================
    # Type Properties
    # ========================
    
    def is_zero(self) -> bool:
        """Check if polynomial is zero"""
        return len(self._coeffs) == 0
    
    def is_one(self) -> bool:
        """Check if polynomial is the constant 1"""
        return (
            len(self._coeffs) == 1 and
            0 in self._coeffs and
            self._coeffs[0].is_one()
        )
    
    def is_constant(self) -> bool:
        """Check if polynomial is a constant (degree 0)"""
        return self.degree == 0
    
    def is_solvable(self) -> bool:
        """Check if polynomial degree is within solvable range"""
        return self.degree <= MAX_POLYNOMIAL_DEGREE
    
    def copy(self) -> Polynomial:
        """Deep copy the polynomial"""
        new_coeffs = {deg: coeff.copy() for deg, coeff in self._coeffs.items()}
        return Polynomial(new_coeffs, self._variable)
    
    def to_constant(self) -> Coefficient:
        """
        Convert to a constant if this is a degree-0 polynomial.
        
        Raises:
            InvalidOperationError: If polynomial has degree > 0
        """
        if self.degree > 0:
            raise InvalidOperationError(
                f"Cannot convert polynomial of degree {self.degree} to constant"
            )
        return self.get_coefficient(0)
    
    # ========================
    # Evaluation
    # ========================
    
    def evaluate(self, value: Any) -> Coefficient:
        """
        Evaluate polynomial at a given value.
        
        Args:
            value: The value to substitute for the variable
        
        Returns:
            The result of the evaluation
        """
        x = self._ensure_coefficient(value)
        
        if not self._coeffs:
            return Rational.zero()
        
        # Determine if we need Complex arithmetic
        use_complex = isinstance(x, Complex) or any(
            isinstance(c, Complex) for c in self._coeffs.values()
        )
        
        # Initialize result with appropriate type
        if use_complex:
            result: Coefficient = Complex.from_rational(Rational.zero())
        else:
            result = Rational.zero()
        
        for degree, coeff in self._coeffs.items():
            # Promote coefficient to Complex if needed
            if use_complex and isinstance(coeff, Rational):
                coeff = Complex.from_rational(coeff)
            
            if degree == 0:
                term = coeff
            else:
                # x^degree
                x_power = x
                for _ in range(degree - 1):
                    x_power = x_power * x
                term = coeff * x_power
            
            # Promote result if needed for addition
            if use_complex and isinstance(result, Rational):
                result = Complex.from_rational(result)
            if use_complex and isinstance(term, Rational):
                term = Complex.from_rational(term)
            
            result = result + term
        
        # Simplify Complex to Rational if purely real
        if isinstance(result, Complex) and result.is_real():
            return result.real
        
        return result
    
    # ========================
    # Arithmetic Operations
    # ========================
    
    def _ensure_polynomial(self, other: Any) -> Polynomial:
        """Convert other to Polynomial if possible"""
        if isinstance(other, Polynomial):
            # Handle variable mismatch
            if other._variable != self._variable and not other.is_constant() and not self.is_constant():
                raise InvalidOperationError(
                    f"Cannot combine polynomials with different variables: {self._variable} and {other._variable}"
                )
            return other
        if isinstance(other, (Rational, Complex, int, float)):
            return Polynomial.from_constant(other, self._variable)
        raise InvalidOperationError(
            f"Cannot perform operation between Polynomial and {type(other).__name__}"
        )
    
    def __add__(self, other: Any) -> Polynomial:
        other = self._ensure_polynomial(other)
        
        # Determine variable (prefer non-constant)
        var = self._variable if not self.is_constant() else other._variable
        
        result_coeffs: Dict[int, Coefficient] = {}
        
        # Combine all degrees
        all_degrees = set(self._coeffs.keys()) | set(other._coeffs.keys())
        
        for degree in all_degrees:
            coeff = self.get_coefficient(degree) + other.get_coefficient(degree)
            if not coeff.is_zero():
                result_coeffs[degree] = coeff
        
        return Polynomial(result_coeffs, var)
    
    def __radd__(self, other: Any) -> Polynomial:
        return self.__add__(other)
    
    def __sub__(self, other: Any) -> Polynomial:
        other = self._ensure_polynomial(other)
        
        var = self._variable if not self.is_constant() else other._variable
        
        result_coeffs: Dict[int, Coefficient] = {}
        all_degrees = set(self._coeffs.keys()) | set(other._coeffs.keys())
        
        for degree in all_degrees:
            coeff = self.get_coefficient(degree) - other.get_coefficient(degree)
            if not coeff.is_zero():
                result_coeffs[degree] = coeff
        
        return Polynomial(result_coeffs, var)
    
    def __rsub__(self, other: Any) -> Polynomial:
        other = self._ensure_polynomial(other)
        return other.__sub__(self)
    
    def __mul__(self, other: Any) -> Polynomial:
        other = self._ensure_polynomial(other)
    
        var = self._variable if not self.is_constant() else other._variable
    
        if self.is_zero() or other.is_zero():
            return Polynomial.zero(var)
    
        result_coeffs: Dict[int, Coefficient] = {}
    
        for deg1, coeff1 in self._coeffs.items():
            for deg2, coeff2 in other._coeffs.items():
                new_degree = deg1 + deg2
            
                if isinstance(coeff1, Complex) or isinstance(coeff2, Complex):
                    if isinstance(coeff1, Rational):
                        coeff1 = Complex.from_rational(coeff1)
                    if isinstance(coeff2, Rational):
                        coeff2 = Complex.from_rational(coeff2)
            
                product = coeff1 * coeff2
            
                if new_degree in result_coeffs:
                    existing = result_coeffs[new_degree]
                    if isinstance(existing, Complex) or isinstance(product, Complex):
                        if isinstance(existing, Rational):
                            existing = Complex.from_rational(existing)
                        if isinstance(product, Rational):
                            product = Complex.from_rational(product)
                    result_coeffs[new_degree] = existing + product
                else:
                    result_coeffs[new_degree] = product
    
        # Remove zero coefficients
        result_coeffs = {d: c for d, c in result_coeffs.items() if not c.is_zero()}
    
        return Polynomial(result_coeffs, var)
    
    def __rmul__(self, other: Any) -> Polynomial:
        return self.__mul__(other)
    
    def __truediv__(self, other: Any) -> Polynomial:
        """Division by a constant only"""
        other = self._ensure_polynomial(other)
        
        if not other.is_constant():
            raise InvalidOperationError(
                "Polynomial division only supported by constants. "
                "For polynomial long division, use the simplifier module."
            )
        
        divisor = other.get_coefficient(0)
        if divisor.is_zero():
            raise DivisionByZeroError("Cannot divide polynomial by zero")
        
        result_coeffs = {deg: coeff / divisor for deg, coeff in self._coeffs.items()}
        return Polynomial(result_coeffs, self._variable)
    
    def __rtruediv__(self, other: Any) -> Polynomial:
        raise InvalidOperationError("Cannot divide by a polynomial")
    
    def __mod__(self, other: Any) -> Polynomial:
        """Modulo by a constant only"""
        other = self._ensure_polynomial(other)
        
        if not other.is_constant():
            raise InvalidOperationError("Polynomial modulo only supported with constants")
        
        divisor = other.get_coefficient(0)
        if divisor.is_zero():
            raise DivisionByZeroError("Cannot compute polynomial modulo zero")
        
        result_coeffs = {deg: coeff % divisor for deg, coeff in self._coeffs.items()}
        return Polynomial(result_coeffs, self._variable)
    
    def __rmod__(self, other: Any) -> Polynomial:
        raise InvalidOperationError("Cannot compute modulo with polynomial divisor")
    
    def __pow__(self, other: Any) -> Polynomial:
        """Polynomial power with non-negative integer exponent"""
        if isinstance(other, Polynomial):
            if not other.is_constant():
                raise InvalidExponentError("Polynomial exponent must be a constant")
            exp_val = other.get_coefficient(0)
            if isinstance(exp_val, Complex) and not exp_val.is_real():
                raise InvalidExponentError("Exponent must be a real number")
            if isinstance(exp_val, Complex):
                exp_val = exp_val.to_rational()
            if not exp_val.is_integer():
                raise InvalidExponentError("Exponent must be an integer")
            exp = exp_val.to_int()
        elif isinstance(other, Rational):
            if not other.is_integer():
                raise InvalidExponentError("Exponent must be an integer")
            exp = other.to_int()
        elif isinstance(other, int):
            exp = other
        else:
            raise InvalidExponentError(f"Cannot use {type(other).__name__} as exponent")
        
        if exp < 0:
            raise InvalidExponentError("Exponent must be non-negative")
        
        if exp == 0:
            return Polynomial.one(self._variable)
        
        # Compute power by repeated multiplication
        result = Polynomial.one(self._variable)
        base = self.copy()
        
        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            base = base * base
            exp //= 2
        
        return result
    
    def __neg__(self) -> Polynomial:
        result_coeffs = {deg: -coeff for deg, coeff in self._coeffs.items()}
        return Polynomial(result_coeffs, self._variable)
    
    def __pos__(self) -> Polynomial:
        return self.copy()
    
    # ========================
    # Comparison Operations
    # ========================
    
    def __eq__(self, other: Any) -> bool:
        try:
            other = self._ensure_polynomial(other)
            if self._coeffs.keys() != other._coeffs.keys():
                return False
            for degree in self._coeffs:
                if self._coeffs[degree] != other._coeffs[degree]:
                    return False
            return True
        except InvalidOperationError:
            return False
    
    # ========================
    # Hashing
    # ========================
    
    def __hash__(self) -> int:
        return hash(tuple(sorted((d, hash(c)) for d, c in self._coeffs.items())))
    
    # ========================
    # String Representation
    # ========================
    
    def __str__(self) -> str:
        if not self._coeffs:
            return "0"
        
        terms = []
        
        for degree in sorted(self._coeffs.keys(), reverse=True):
            coeff = self._coeffs[degree]
            
            # Format coefficient
            coeff_str = str(coeff)
            is_negative = False
            
            if isinstance(coeff, Rational) and coeff.is_negative():
                is_negative = True
                coeff_str = str(-coeff)
            elif isinstance(coeff, Complex):
                if coeff.is_real() and coeff.real.is_negative():
                    is_negative = True
                    coeff_str = str(-coeff)
            
            # Build term string
            if degree == 0:
                term = coeff_str
            elif degree == 1:
                if coeff.is_one():
                    term = self._variable
                elif isinstance(coeff, Rational) and coeff == Rational(-1, 1):
                    term = self._variable
                    is_negative = True
                else:
                    term = f"{coeff_str} * {self._variable}"
            else:
                if coeff.is_one():
                    term = f"{self._variable}^{degree}"
                elif isinstance(coeff, Rational) and coeff == Rational(-1, 1):
                    term = f"{self._variable}^{degree}"
                    is_negative = True
                else:
                    term = f"{coeff_str} * {self._variable}^{degree}"
            
            # Add sign
            if not terms:
                if is_negative:
                    term = f"-{term}"
            else:
                if is_negative:
                    term = f" - {term}"
                else:
                    term = f" + {term}"
            
            terms.append(term)
        
        return "".join(terms)
    
    def __repr__(self) -> str:
        return f"Polynomial({self._coeffs!r}, variable='{self._variable}')"