"""
Matrix implementation for Computorv2.

Represents matrices with Rational or Complex entries.
Supports standard matrix operations and element-wise operations.
"""

from __future__ import annotations
from typing import Any, Union, List

from .base import (
    MathType,
    DivisionByZeroError,
    InvalidOperationError,
    InvalidExponentError,
    DimensionMismatchError,
)
from .rational import Rational
from .complex import Complex
from ..utils import validate_matrix_consistency


# Type alias for matrix entries
Entry = Union[Rational, Complex]


class Matrix(MathType):
    """
    Matrix with Rational or Complex entries.
    
    Stored as a list of lists (row-major order).
    Supports element-wise operations (*) and matrix multiplication (**).
    
    Examples:
        >>> Matrix([[Rational(1), Rational(2)], [Rational(3), Rational(4)]])
        >>> Matrix.identity(3)
        >>> Matrix.zeros(2, 3)
    """
    
    __slots__ = ('_data', '_rows', '_cols')
    
    def __init__(self, data: List[List[Entry]]):
        """
        Create a Matrix from a 2D list.
        
        Args:
            data: List of rows, each row is a list of Rational/Complex values
        
        Raises:
            InvalidOperationError: If matrix is empty or rows have inconsistent lengths
        """
        # Validate structure
        is_valid, error_msg = validate_matrix_consistency(data)
        if not is_valid:
            raise InvalidOperationError(error_msg)
        
        self._rows = len(data)
        self._cols = len(data[0])
        
        # Deep copy and ensure all entries are proper types
        self._data: List[List[Entry]] = []
        for row in data:
            new_row: List[Entry] = []
            for val in row:
                new_row.append(self._ensure_entry(val))
            self._data.append(new_row)
    
    @staticmethod
    def _ensure_entry(value: Any) -> Entry:
        """Convert a value to a valid matrix entry (Rational or Complex)"""
        if isinstance(value, Complex):
            return value
        if isinstance(value, Rational):
            return value
        if isinstance(value, int):
            return Rational.from_int(value)
        if isinstance(value, float):
            return Rational.from_float(value)
        raise InvalidOperationError(
            f"Cannot use {type(value).__name__} as matrix entry"
        )
    
    # ========================
    # Properties
    # ========================
    
    @property
    def rows(self) -> int:
        """Number of rows"""
        return self._rows
    
    @property
    def cols(self) -> int:
        """Number of columns"""
        return self._cols
    
    @property
    def shape(self) -> tuple[int, int]:
        """Matrix dimensions as (rows, cols)"""
        return (self._rows, self._cols)
    
    @property
    def type_name(self) -> str:
        return "Matrix"
    
    def is_square(self) -> bool:
        """Check if matrix is square"""
        return self._rows == self._cols
    
    def is_vector(self) -> bool:
        """Check if matrix is a row or column vector"""
        return self._rows == 1 or self._cols == 1
    
    # ========================
    # Element Access
    # ========================
    
    def get(self, row: int, col: int) -> Entry:
        """Get element at (row, col) - 0-indexed"""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"Index ({row}, {col}) out of bounds for {self.shape} matrix")
        return self._data[row][col]
    
    def set(self, row: int, col: int, value: Any) -> None:
        """Set element at (row, col) - 0-indexed"""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"Index ({row}, {col}) out of bounds for {self.shape} matrix")
        self._data[row][col] = self._ensure_entry(value)
    
    def __getitem__(self, key: tuple[int, int]) -> Entry:
        """Access element via matrix[row, col]"""
        row, col = key
        return self.get(row, col)
    
    def __setitem__(self, key: tuple[int, int], value: Any) -> None:
        """Set element via matrix[row, col] = value"""
        row, col = key
        self.set(row, col, value)
    
    # ========================
    # Factory Methods
    # ========================
    
    @classmethod
    def zeros(cls, rows: int, cols: int) -> Matrix:
        """Create a matrix of zeros"""
        data = [[Rational.zero() for _ in range(cols)] for _ in range(rows)]
        return cls(data)
    
    @classmethod
    def ones(cls, rows: int, cols: int) -> Matrix:
        """Create a matrix of ones"""
        data = [[Rational.one() for _ in range(cols)] for _ in range(rows)]
        return cls(data)
    
    @classmethod
    def identity(cls, size: int) -> Matrix:
        """Create an identity matrix"""
        data = []
        for i in range(size):
            row = [Rational.one() if i == j else Rational.zero() for j in range(size)]
            data.append(row)
        return cls(data)
    
    @classmethod
    def zero(cls) -> Matrix:
        """Return a 1x1 zero matrix"""
        return cls.zeros(1, 1)
    
    @classmethod
    def one(cls) -> Matrix:
        """Return a 1x1 identity matrix"""
        return cls.identity(1)
    
    # ========================
    # Type Properties
    # ========================
    
    def is_zero(self) -> bool:
        """Check if all elements are zero"""
        for row in self._data:
            for val in row:
                if not val.is_zero():
                    return False
        return True
    
    def is_one(self) -> bool:
        """Check if this is an identity matrix"""
        if not self.is_square():
            return False
        for i in range(self._rows):
            for j in range(self._cols):
                expected = Rational.one() if i == j else Rational.zero()
                if self._data[i][j] != expected:
                    return False
        return True
    
    def copy(self) -> Matrix:
        """Deep copy the matrix"""
        data = [[val.copy() for val in row] for row in self._data]
        return Matrix(data)
    
    # ========================
    # Matrix Operations
    # ========================
    
    def transpose(self) -> Matrix:
        """Return the transpose of this matrix"""
        data = []
        for j in range(self._cols):
            row = [self._data[i][j].copy() for i in range(self._rows)]
            data.append(row)
        return Matrix(data)
    
    def determinant(self) -> Entry:
        """
        Compute the determinant of a square matrix.
        
        Uses recursive expansion by minors for small matrices,
        and LU decomposition concept for larger ones.
        
        Returns:
            The determinant as Rational or Complex
            
        Raises:
            InvalidOperationError: If matrix is not square
        """
        if not self.is_square():
            raise InvalidOperationError("Determinant only defined for square matrices")
        
        n = self._rows
        
        # Base cases
        if n == 1:
            return self._data[0][0].copy()
        
        if n == 2:
            # det = a*d - b*c
            a, b = self._data[0][0], self._data[0][1]
            c, d = self._data[1][0], self._data[1][1]
            return a * d - b * c
        
        # For larger matrices, use expansion by first row
        det: Entry = Rational.zero()
        for j in range(n):
            # Get minor matrix (exclude row 0 and column j)
            minor_data = []
            for i in range(1, n):
                minor_row = []
                for k in range(n):
                    if k != j:
                        minor_row.append(self._data[i][k].copy())
                minor_data.append(minor_row)
            
            minor = Matrix(minor_data)
            cofactor = minor.determinant()
            
            # Alternate signs: (-1)^(0+j)
            if j % 2 == 0:
                det = det + self._data[0][j] * cofactor
            else:
                det = det - self._data[0][j] * cofactor
        
        return det
    
    def inverse(self) -> Matrix:
        """
        Compute the inverse of a square matrix using Gauss-Jordan elimination.
        
        Returns:
            The inverse matrix
            
        Raises:
            InvalidOperationError: If matrix is not square or is singular
        """
        if not self.is_square():
            raise InvalidOperationError("Inverse only defined for square matrices")
        
        n = self._rows
        
        # Check if determinant is zero (singular matrix)
        det = self.determinant()
        if det.is_zero():
            raise InvalidOperationError("Matrix is singular (determinant = 0), cannot compute inverse")
        
        # Create augmented matrix [A | I]
        aug_data = []
        for i in range(n):
            row = [self._data[i][j].copy() for j in range(n)]
            # Append identity row
            for j in range(n):
                if i == j:
                    row.append(Rational.one())
                else:
                    row.append(Rational.zero())
            aug_data.append(row)
        
        # Gauss-Jordan elimination
        for col in range(n):
            # Find pivot (largest absolute value in column)
            max_row = col
            for row in range(col + 1, n):
                # Compare absolute values
                curr_val = aug_data[row][col]
                max_val = aug_data[max_row][col]
                
                # Simple comparison for Rational
                if isinstance(curr_val, Rational) and isinstance(max_val, Rational):
                    if abs(curr_val.numerator * max_val.denominator) > abs(max_val.numerator * curr_val.denominator):
                        max_row = row
            
            # Swap rows
            aug_data[col], aug_data[max_row] = aug_data[max_row], aug_data[col]
            
            # Check for zero pivot
            pivot = aug_data[col][col]
            if pivot.is_zero():
                raise InvalidOperationError("Matrix is singular, cannot compute inverse")
            
            # Scale pivot row to make pivot = 1
            for j in range(2 * n):
                aug_data[col][j] = aug_data[col][j] / pivot
            
            # Eliminate column in other rows
            for row in range(n):
                if row != col:
                    factor = aug_data[row][col]
                    for j in range(2 * n):
                        aug_data[row][j] = aug_data[row][j] - factor * aug_data[col][j]
        
        # Extract inverse from right half of augmented matrix
        inv_data = []
        for i in range(n):
            inv_row = [aug_data[i][j + n] for j in range(n)]
            inv_data.append(inv_row)
        
        return Matrix(inv_data)
    
    # ========================
    # Arithmetic Operations
    # ========================
    
    def _ensure_matrix(self, other: Any) -> Matrix:
        """Convert other to Matrix if possible"""
        if isinstance(other, Matrix):
            return other
        raise InvalidOperationError(
            f"Cannot perform operation between Matrix and {type(other).__name__}"
        )
    
    def _is_scalar(self, other: Any) -> bool:
        """Check if other is a scalar type"""
        return isinstance(other, (int, float, Rational, Complex))
    
    def _ensure_scalar(self, other: Any) -> Entry:
        """Convert other to scalar entry"""
        return self._ensure_entry(other)
    
    def __add__(self, other: Any) -> Matrix:
        """Element-wise addition (matrices must have same shape)"""
        other = self._ensure_matrix(other)
        
        if self.shape != other.shape:
            raise DimensionMismatchError(
                f"Cannot add matrices with shapes {self.shape} and {other.shape}"
            )
        
        data = []
        for i in range(self._rows):
            row = []
            for j in range(self._cols):
                row.append(self._data[i][j] + other._data[i][j])
            data.append(row)
        
        return Matrix(data)
    
    def __radd__(self, other: Any) -> Matrix:
        return self.__add__(other)
    
    def __sub__(self, other: Any) -> Matrix:
        """Element-wise subtraction"""
        other = self._ensure_matrix(other)
        
        if self.shape != other.shape:
            raise DimensionMismatchError(
                f"Cannot subtract matrices with shapes {self.shape} and {other.shape}"
            )
        
        data = []
        for i in range(self._rows):
            row = []
            for j in range(self._cols):
                row.append(self._data[i][j] - other._data[i][j])
            data.append(row)
        
        return Matrix(data)
    
    def __rsub__(self, other: Any) -> Matrix:
        other = self._ensure_matrix(other)
        return other.__sub__(self)
    
    def __mul__(self, other: Any) -> Matrix:
        """
        Element-wise multiplication.
        
        - Matrix * Matrix: element-wise (same shape required)
        - Matrix * Scalar: multiply all elements by scalar
        """
        if self._is_scalar(other):
            scalar = self._ensure_scalar(other)
            data = [[val * scalar for val in row] for row in self._data]
            return Matrix(data)
        
        other = self._ensure_matrix(other)
        
        if self.shape != other.shape:
            raise DimensionMismatchError(
                f"Cannot perform element-wise multiplication with shapes {self.shape} and {other.shape}"
            )
        
        data = []
        for i in range(self._rows):
            row = []
            for j in range(self._cols):
                row.append(self._data[i][j] * other._data[i][j])
            data.append(row)
        
        return Matrix(data)
    
    def __rmul__(self, other: Any) -> Matrix:
        return self.__mul__(other)
    
    def matmul(self, other: Matrix) -> Matrix:
        """
        Matrix multiplication (self ** other).
        
        For A (m×n) and B (n×p), result is (m×p).
        """
        other = self._ensure_matrix(other)
        
        if self._cols != other._rows:
            raise DimensionMismatchError(
                f"Cannot multiply matrices: {self.shape} @ {other.shape} "
                f"(inner dimensions {self._cols} != {other._rows})"
            )
        
        data = []
        for i in range(self._rows):
            row = []
            for j in range(other._cols):
                # Dot product of row i of self with column j of other
                total: Entry = Rational.zero()
                for k in range(self._cols):
                    total = total + self._data[i][k] * other._data[k][j]
                row.append(total)
            data.append(row)
        
        return Matrix(data)
    
    def __truediv__(self, other: Any) -> Matrix:
        """Element-wise division by scalar"""
        if not self._is_scalar(other):
            raise InvalidOperationError("Matrix division only supported with scalars")
        
        scalar = self._ensure_scalar(other)
        if scalar.is_zero():
            raise DivisionByZeroError("Cannot divide matrix by zero")
        
        data = [[val / scalar for val in row] for row in self._data]
        return Matrix(data)
    
    def __rtruediv__(self, other: Any) -> Matrix:
        raise InvalidOperationError("Cannot divide scalar by matrix")
    
    def __mod__(self, other: Any) -> Matrix:
        """Element-wise modulo by scalar"""
        if not self._is_scalar(other):
            raise InvalidOperationError("Matrix modulo only supported with scalars")
        
        scalar = self._ensure_scalar(other)
        if scalar.is_zero():
            raise DivisionByZeroError("Cannot compute matrix modulo zero")
        
        data = [[val % scalar for val in row] for row in self._data]
        return Matrix(data)
    
    def __rmod__(self, other: Any) -> Matrix:
        raise InvalidOperationError("Cannot compute scalar modulo matrix")
    
    def __pow__(self, other: Any) -> Matrix:
        """Matrix power (only for square matrices with non-negative integer exponent)"""
        if not self.is_square():
            raise InvalidOperationError("Matrix power only defined for square matrices")
        
        # Parse exponent
        if isinstance(other, Rational):
            if not other.is_integer():
                raise InvalidExponentError("Matrix exponent must be an integer")
            exp = other.to_int()
        elif isinstance(other, int):
            exp = other
        else:
            raise InvalidExponentError(f"Cannot use {type(other).__name__} as matrix exponent")
        
        if exp < 0:
            raise InvalidExponentError("Matrix exponent must be non-negative")
        
        if exp == 0:
            return Matrix.identity(self._rows)
        
        # Compute power by repeated multiplication
        result = Matrix.identity(self._rows)
        base = self.copy()
        
        while exp > 0:
            if exp % 2 == 1:
                result = result.matmul(base)
            base = base.matmul(base)
            exp //= 2
        
        return result
    
    def __neg__(self) -> Matrix:
        data = [[-val for val in row] for row in self._data]
        return Matrix(data)
    
    def __pos__(self) -> Matrix:
        return self.copy()
    
    # ========================
    # Comparison Operations
    # ========================
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Matrix):
            return False
        if self.shape != other.shape:
            return False
        for i in range(self._rows):
            for j in range(self._cols):
                if self._data[i][j] != other._data[i][j]:
                    return False
        return True
    
    # ========================
    # Hashing
    # ========================
    
    def __hash__(self) -> int:
        return hash(tuple(tuple(hash(val) for val in row) for row in self._data))
    
    # ========================
    # String Representation
    # ========================
    
    def __str__(self) -> str:
        lines = []
        for row in self._data:
            elements = [str(val) for val in row]
            lines.append("[ " + " , ".join(elements) + " ]")
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return f"Matrix({self._data!r})"