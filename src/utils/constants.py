"""
Global constants and configuration for Computorv2.
"""

# Display precision for decimal numbers
DECIMAL_PRECISION = 10

# Maximum digits before switching to scientific notation
MAX_DISPLAY_DIGITS = 15

# Tolerance for floating point comparisons
EPSILON = 1e-10

# Maximum matrix dimensions
MAX_MATRIX_ROWS = 100
MAX_MATRIX_COLS = 100

# Maximum polynomial degree for equation solving
MAX_POLYNOMIAL_DEGREE = 2

# Maximum power exponent allowed
MAX_POWER_EXPONENT = 1000

# Reserved keywords that cannot be used as variable names
RESERVED_KEYWORDS = frozenset({
    'i',  # Imaginary unit
})

# Valid operators
OPERATORS = frozenset({
    '+', '-', '*', '/', '%', '^', '**',
})

# Operator precedence (higher = binds tighter)
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '**': 3,
    '^': 4,
}

# Right-associative operators
RIGHT_ASSOCIATIVE = frozenset({
    '^',
})

# REPL prompt
PROMPT = "> "

# Exit commands
EXIT_COMMANDS = frozenset({
    'exit',
    'quit',
    'q',
})
