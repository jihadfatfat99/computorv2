"""
Solver module for Computorv2.

Solves polynomial equations of degree 0, 1, and 2.

Main components:
    - solve(): Solve a SimplifiedEquation
    - solve_equation(): Solve from left/right polynomials
    - Solution: Result container with roots and metadata
    - format_solution(): Human-readable output

Example:
    >>> from src.simplifier import simplify_equation
    >>> from src.solver import solve, format_solution
    >>> eq = simplify_equation(left_poly, right_poly)
    >>> solution = solve(eq)
    >>> print(format_solution(solution))
"""

from .errors import (
    SolverError,
    NoSolutionError,
    InfiniteSolutionsError,
    UnsolvableEquationError,
)

from .solution import (
    Solution,
    SolutionType,
    SolutionValue,
    no_solution,
    infinite_solutions,
    single_solution,
    double_solution,
    two_real_solutions,
    two_complex_solutions,
)

from .sqrt import (
    sqrt_rational,
    sqrt_complex,
    sqrt_value,
)

from .solver import (
    solve,
    solve_equation,
)

from .formatter import (
    format_solution,
    format_solution_short,
    format_discriminant_info,
)


__all__ = [
    # Errors
    'SolverError',
    'NoSolutionError',
    'InfiniteSolutionsError',
    'UnsolvableEquationError',
    
    # Solution types
    'Solution',
    'SolutionType',
    'SolutionValue',
    'no_solution',
    'infinite_solutions',
    'single_solution',
    'double_solution',
    'two_real_solutions',
    'two_complex_solutions',
    
    # Square root
    'sqrt_rational',
    'sqrt_complex',
    'sqrt_value',
    
    # Solver functions
    'solve',
    'solve_equation',
    
    # Formatting
    'format_solution',
    'format_solution_short',
    'format_discriminant_info',
]