"""
Solution formatting for Computorv2 solver.

Produces human-readable output for equation solutions.
"""

from .solution import Solution, SolutionType
from ..formatter import format_value


def format_solution(solution: Solution) -> str:
    """
    Format a solution for display.
    
    Produces output matching 42 project requirements.
    
    Args:
        solution: Solution object from solver
    
    Returns:
        Formatted string for display
    """
    lines = []
    
    # Reduced form
    lines.append(f"Reduced form: {solution.reduced_form}")
    
    # Polynomial degree
    lines.append(f"Polynomial degree: {solution.degree}")
    
    # Solution based on type
    if solution.solution_type == SolutionType.NO_SOLUTION:
        lines.append("The equation has no solution.")
    
    elif solution.solution_type == SolutionType.INFINITE:
        lines.append("All real numbers are solutions.")
    
    elif solution.solution_type == SolutionType.SINGLE:
        lines.append("The solution is:")
        lines.append(f"{solution.variable} = {format_value(solution.roots[0])}")
    
    elif solution.solution_type == SolutionType.DOUBLE:
        lines.append(f"Discriminant is zero, the solution is:")
        lines.append(f"{solution.variable} = {format_value(solution.roots[0])}")
    
    elif solution.solution_type == SolutionType.TWO_REAL:
        lines.append(f"Discriminant is strictly positive, the two solutions are:")
        lines.append(f"{solution.variable} = {format_value(solution.roots[0])}")
        lines.append(f"{solution.variable} = {format_value(solution.roots[1])}")
    
    elif solution.solution_type == SolutionType.TWO_COMPLEX:
        lines.append(f"Discriminant is strictly negative, the two complex solutions are:")
        lines.append(f"{solution.variable} = {format_value(solution.roots[0])}")
        lines.append(f"{solution.variable} = {format_value(solution.roots[1])}")
    
    return "\n".join(lines)


def format_solution_short(solution: Solution) -> str:
    """
    Format solution in short form (just the roots).
    
    Args:
        solution: Solution object
    
    Returns:
        Short formatted string
    """
    if solution.solution_type == SolutionType.NO_SOLUTION:
        return "No solution"
    
    if solution.solution_type == SolutionType.INFINITE:
        return "All real numbers"
    
    if len(solution.roots) == 1:
        return f"{solution.variable} = {format_value(solution.roots[0])}"
    
    roots_str = ", ".join(format_value(r) for r in solution.roots)
    return f"{solution.variable} = {{{roots_str}}}"


def format_discriminant_info(solution: Solution) -> str:
    """
    Format discriminant information.
    
    Args:
        solution: Solution object (should be quadratic)
    
    Returns:
        Discriminant info string
    """
    if solution.discriminant is None:
        return ""
    
    disc_value = format_value(solution.discriminant)
    
    if solution.solution_type == SolutionType.DOUBLE:
        return f"Δ = {disc_value} = 0"
    elif solution.solution_type == SolutionType.TWO_REAL:
        return f"Δ = {disc_value} > 0"
    elif solution.solution_type == SolutionType.TWO_COMPLEX:
        return f"Δ = {disc_value} < 0"
    
    return f"Δ = {disc_value}"