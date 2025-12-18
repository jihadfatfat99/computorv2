"""
Greatest Common Divisor and Least Common Multiple utilities.
Essential for rational number arithmetic and fraction reduction.
"""


def gcd(a: int, b: int) -> int:
    """
    Compute the Greatest Common Divisor using Euclidean algorithm.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        The greatest common divisor of a and b (always positive)
    
    Examples:
        >>> gcd(12, 8)
        4
        >>> gcd(-12, 8)
        4
        >>> gcd(17, 5)
        1
    """
    a, b = abs(a), abs(b)
    
    while b:
        a, b = b, a % b
    
    return a if a != 0 else 1


def lcm(a: int, b: int) -> int:
    """
    Compute the Least Common Multiple.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        The least common multiple of a and b (always positive)
    
    Examples:
        >>> lcm(4, 6)
        12
        >>> lcm(3, 5)
        15
    """
    if a == 0 or b == 0:
        return 0
    
    return abs(a * b) // gcd(a, b)


def gcd_multiple(*numbers: int) -> int:
    """
    Compute GCD of multiple integers.
    
    Args:
        *numbers: Variable number of integers
    
    Returns:
        The GCD of all provided numbers
    
    Examples:
        >>> gcd_multiple(12, 8, 4)
        4
        >>> gcd_multiple(15, 25, 35)
        5
    """
    if not numbers:
        return 1
    
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
        if result == 1:
            break
    
    return result


def lcm_multiple(*numbers: int) -> int:
    """
    Compute LCM of multiple integers.
    
    Args:
        *numbers: Variable number of integers
    
    Returns:
        The LCM of all provided numbers
    
    Examples:
        >>> lcm_multiple(2, 3, 4)
        12
        >>> lcm_multiple(5, 7, 10)
        70
    """
    if not numbers:
        return 1
    
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    
    return result


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    
    Computes gcd(a, b) and coefficients x, y such that:
        a * x + b * y = gcd(a, b)
    
    Useful for modular arithmetic and finding multiplicative inverses.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        Tuple (gcd, x, y) where a*x + b*y = gcd
    
    Examples:
        >>> g, x, y = extended_gcd(35, 15)
        >>> 35 * x + 15 * y == g
        True
    """
    if b == 0:
        return a, 1, 0
    
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return g, x, y