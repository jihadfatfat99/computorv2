"""
Solver-specific exceptions for Computorv2.
"""


class SolverError(Exception):
    """Base exception for solver errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NoSolutionError(SolverError):
    """Raised when equation has no solution."""
    
    def __init__(self, reason: str = "Equation has no solution"):
        super().__init__(reason)


class InfiniteSolutionsError(SolverError):
    """Raised when equation has infinite solutions."""
    
    def __init__(self, reason: str = "Equation has infinite solutions"):
        super().__init__(reason)


class UnsolvableEquationError(SolverError):
    """Raised when equation cannot be solved (degree > 2)."""
    
    def __init__(self, degree: int):
        self.degree = degree
        super().__init__(
            f"Cannot solve polynomial of degree {degree}. "
            f"Only degrees 0, 1, and 2 are supported."
        )