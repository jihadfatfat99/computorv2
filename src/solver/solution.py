"""
Solution result types for Computorv2 solver.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union
from enum import Enum

from ..math_types import Rational, Complex


# Solution value type
SolutionValue = Union[Rational, Complex]


class SolutionType(Enum):
    """Type of solution found."""
    NO_SOLUTION = "no_solution"
    SINGLE = "single"
    DOUBLE = "double"  # Two equal roots (discriminant = 0)
    TWO_REAL = "two_real"
    TWO_COMPLEX = "two_complex"
    INFINITE = "infinite"


@dataclass
class Solution:
    """
    Result of solving an equation.
    
    Attributes:
        solution_type: Type of solution (no solution, single, two real, etc.)
        roots: List of solution values
        discriminant: Discriminant value for quadratic equations
        degree: Degree of the equation
        variable: Variable name
        reduced_form: String representation of reduced form
    """
    solution_type: SolutionType
    roots: List[SolutionValue] = field(default_factory=list)
    discriminant: Optional[SolutionValue] = None
    degree: int = 0
    variable: str = 'x'
    reduced_form: str = ""
    
    @property
    def has_solution(self) -> bool:
        """Check if equation has at least one solution."""
        return self.solution_type not in (SolutionType.NO_SOLUTION,)
    
    @property
    def is_infinite(self) -> bool:
        """Check if equation has infinite solutions."""
        return self.solution_type == SolutionType.INFINITE
    
    @property
    def num_roots(self) -> int:
        """Get number of roots."""
        return len(self.roots)
    
    @property
    def has_complex_roots(self) -> bool:
        """Check if any root is complex (non-real)."""
        for root in self.roots:
            if isinstance(root, Complex) and not root.is_real():
                return True
        return False
    
    def get_single_root(self) -> Optional[SolutionValue]:
        """Get single root if exists."""
        if len(self.roots) == 1:
            return self.roots[0]
        return None


def no_solution(degree: int, variable: str, reduced_form: str) -> Solution:
    """Create a no-solution result."""
    return Solution(
        solution_type=SolutionType.NO_SOLUTION,
        roots=[],
        degree=degree,
        variable=variable,
        reduced_form=reduced_form
    )


def infinite_solutions(variable: str, reduced_form: str) -> Solution:
    """Create an infinite solutions result."""
    return Solution(
        solution_type=SolutionType.INFINITE,
        roots=[],
        degree=0,
        variable=variable,
        reduced_form=reduced_form
    )


def single_solution(
    root: SolutionValue, 
    degree: int, 
    variable: str, 
    reduced_form: str
) -> Solution:
    """Create a single solution result."""
    return Solution(
        solution_type=SolutionType.SINGLE,
        roots=[root],
        degree=degree,
        variable=variable,
        reduced_form=reduced_form
    )


def double_solution(
    root: SolutionValue,
    discriminant: SolutionValue,
    variable: str,
    reduced_form: str
) -> Solution:
    """Create a double root solution (discriminant = 0)."""
    return Solution(
        solution_type=SolutionType.DOUBLE,
        roots=[root],
        discriminant=discriminant,
        degree=2,
        variable=variable,
        reduced_form=reduced_form
    )


def two_real_solutions(
    root1: SolutionValue,
    root2: SolutionValue,
    discriminant: SolutionValue,
    variable: str,
    reduced_form: str
) -> Solution:
    """Create a two real solutions result."""
    return Solution(
        solution_type=SolutionType.TWO_REAL,
        roots=[root1, root2],
        discriminant=discriminant,
        degree=2,
        variable=variable,
        reduced_form=reduced_form
    )


def two_complex_solutions(
    root1: Complex,
    root2: Complex,
    discriminant: SolutionValue,
    variable: str,
    reduced_form: str
) -> Solution:
    """Create a two complex solutions result."""
    return Solution(
        solution_type=SolutionType.TWO_COMPLEX,
        roots=[root1, root2],
        discriminant=discriminant,
        degree=2,
        variable=variable,
        reduced_form=reduced_form
    )