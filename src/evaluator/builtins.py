"""
Built-in mathematical functions for Computorv2.

Provides sin, cos, tan, sqrt, abs, exp, log, etc.
All functions work with Rational and Complex numbers.
"""

from typing import Any, Dict, Callable, Union
from ..math_types import Rational, Complex
from .errors import InvalidOperandError


# Type alias for numeric values
Numeric = Union[Rational, Complex]


class BuiltinFunction:
    """Wrapper for a built-in mathematical function."""
    
    def __init__(self, name: str, func: Callable[[Numeric], Numeric], description: str = ""):
        self.name = name
        self.func = func
        self.description = description
    
    def __call__(self, arg: Numeric) -> Numeric:
        return self.func(arg)
    
    def __str__(self) -> str:
        return f"{self.name}(x)"
    
    def __repr__(self) -> str:
        return f"BuiltinFunction({self.name})"


# ============================================================
# Helper functions for manual computation (no math library)
# ============================================================

def _to_float(val: Numeric) -> float:
    """Convert Rational to float for computation."""
    if isinstance(val, Rational):
        return val.numerator / val.denominator
    raise InvalidOperandError(f"Cannot convert {type(val).__name__} to float")


def _from_float(val: float) -> Rational:
    """Convert float back to Rational."""
    return Rational.from_float(val)


def _abs_rational(x: Rational) -> Rational:
    """Absolute value of Rational."""
    if x.is_negative():
        return -x
    return x


def _sqrt_rational(x: Rational) -> Numeric:
    """
    Square root using Newton's method.
    Returns Complex if input is negative.
    """
    if x.is_zero():
        return Rational.zero()
    
    if x.is_negative():
        # sqrt(-x) = i * sqrt(x)
        pos_sqrt = _sqrt_rational(-x)
        return Complex(Rational.zero(), pos_sqrt)
    
    # Newton's method for square root
    # x_{n+1} = (x_n + S/x_n) / 2
    val = _to_float(x)
    guess = val / 2 if val > 1 else val
    
    for _ in range(50):  # Sufficient iterations for convergence
        new_guess = (guess + val / guess) / 2
        if abs(new_guess - guess) < 1e-15:
            break
        guess = new_guess
    
    return _from_float(guess)


def _exp_rational(x: Rational) -> Rational:
    """
    Exponential function e^x using Taylor series.
    e^x = 1 + x + x²/2! + x³/3! + ...
    """
    val = _to_float(x)
    
    result = 1.0
    term = 1.0
    
    for n in range(1, 100):
        term *= val / n
        result += term
        if abs(term) < 1e-15:
            break
    
    return _from_float(result)


def _log_rational(x: Rational) -> Rational:
    """
    Natural logarithm using the series:
    ln(x) = 2 * (y + y³/3 + y⁵/5 + ...) where y = (x-1)/(x+1)
    """
    if x.is_zero() or x.is_negative():
        raise InvalidOperandError("Logarithm undefined for non-positive numbers")
    
    val = _to_float(x)
    
    # For better convergence, reduce to ln(x) = ln(a * 2^n) = ln(a) + n*ln(2)
    # where 0.5 <= a < 1
    n = 0
    a = val
    while a >= 2:
        a /= 2
        n += 1
    while a < 0.5:
        a *= 2
        n -= 1
    
    # ln(2) ≈ 0.693147180559945
    ln2 = 0.6931471805599453
    
    # Series for ln(a) where 0.5 <= a < 2
    y = (a - 1) / (a + 1)
    y2 = y * y
    
    result = 0.0
    term = y
    for k in range(1, 100, 2):
        result += term / k
        term *= y2
        if abs(term / k) < 1e-15:
            break
    
    result = 2 * result + n * ln2
    
    return _from_float(result)


def _sin_rational(x: Rational) -> Rational:
    """
    Sine using Taylor series.
    sin(x) = x - x³/3! + x⁵/5! - ...
    """
    val = _to_float(x)
    
    # Reduce to [-π, π] for better convergence
    pi = 3.141592653589793
    while val > pi:
        val -= 2 * pi
    while val < -pi:
        val += 2 * pi
    
    result = 0.0
    term = val
    val2 = val * val
    
    for n in range(0, 50):
        result += term
        term *= -val2 / ((2*n + 2) * (2*n + 3))
        if abs(term) < 1e-15:
            break
    
    return _from_float(result)


def _cos_rational(x: Rational) -> Rational:
    """
    Cosine using Taylor series.
    cos(x) = 1 - x²/2! + x⁴/4! - ...
    """
    val = _to_float(x)
    
    # Reduce to [-π, π]
    pi = 3.141592653589793
    while val > pi:
        val -= 2 * pi
    while val < -pi:
        val += 2 * pi
    
    result = 0.0
    term = 1.0
    val2 = val * val
    
    for n in range(0, 50):
        result += term
        term *= -val2 / ((2*n + 1) * (2*n + 2))
        if abs(term) < 1e-15:
            break
    
    return _from_float(result)


def _tan_rational(x: Rational) -> Rational:
    """Tangent as sin/cos."""
    cos_val = _cos_rational(x)
    if abs(_to_float(cos_val)) < 1e-15:
        raise InvalidOperandError("Tangent undefined at this value (cos = 0)")
    
    sin_val = _sin_rational(x)
    return sin_val / cos_val


# ============================================================
# Complex number extensions
# ============================================================

def _abs_complex(z: Complex) -> Rational:
    """
    Absolute value (modulus) of complex number.
    |a + bi| = sqrt(a² + b²)
    """
    a2 = z.real * z.real
    b2 = z.imag * z.imag
    return _sqrt_rational(a2 + b2)


def _sqrt_complex(z: Complex) -> Complex:
    """
    Square root of complex number.
    sqrt(a + bi) = sqrt((|z| + a)/2) + i*sign(b)*sqrt((|z| - a)/2)
    """
    if z.is_real():
        result = _sqrt_rational(z.real)
        if isinstance(result, Complex):
            return result
        return Complex.from_rational(result)
    
    a = _to_float(z.real)
    b = _to_float(z.imag)
    
    modulus = (a*a + b*b) ** 0.5
    
    real_part = ((modulus + a) / 2) ** 0.5
    imag_part = ((modulus - a) / 2) ** 0.5
    
    if b < 0:
        imag_part = -imag_part
    
    return Complex(_from_float(real_part), _from_float(imag_part))


def _exp_complex(z: Complex) -> Complex:
    """
    Complex exponential.
    e^(a+bi) = e^a * (cos(b) + i*sin(b))
    """
    if z.is_real():
        return Complex.from_rational(_exp_rational(z.real))
    
    a = z.real
    b = z.imag
    
    ea = _exp_rational(a)
    cos_b = _cos_rational(b)
    sin_b = _sin_rational(b)
    
    return Complex(ea * cos_b, ea * sin_b)


def _sin_complex(z: Complex) -> Complex:
    """
    Complex sine.
    sin(a+bi) = sin(a)cosh(b) + i*cos(a)sinh(b)
    """
    if z.is_real():
        return Complex.from_rational(_sin_rational(z.real))
    
    a = _to_float(z.real)
    b = _to_float(z.imag)
    
    # sinh(b) = (e^b - e^-b) / 2
    # cosh(b) = (e^b + e^-b) / 2
    eb = _to_float(_exp_rational(_from_float(b)))
    emb = _to_float(_exp_rational(_from_float(-b)))
    sinh_b = (eb - emb) / 2
    cosh_b = (eb + emb) / 2
    
    sin_a = _to_float(_sin_rational(_from_float(a)))
    cos_a = _to_float(_cos_rational(_from_float(a)))
    
    real = sin_a * cosh_b
    imag = cos_a * sinh_b
    
    return Complex(_from_float(real), _from_float(imag))


def _cos_complex(z: Complex) -> Complex:
    """
    Complex cosine.
    cos(a+bi) = cos(a)cosh(b) - i*sin(a)sinh(b)
    """
    if z.is_real():
        return Complex.from_rational(_cos_rational(z.real))
    
    a = _to_float(z.real)
    b = _to_float(z.imag)
    
    eb = _to_float(_exp_rational(_from_float(b)))
    emb = _to_float(_exp_rational(_from_float(-b)))
    sinh_b = (eb - emb) / 2
    cosh_b = (eb + emb) / 2
    
    sin_a = _to_float(_sin_rational(_from_float(a)))
    cos_a = _to_float(_cos_rational(_from_float(a)))
    
    real = cos_a * cosh_b
    imag = -sin_a * sinh_b
    
    return Complex(_from_float(real), _from_float(imag))


# ============================================================
# Unified function wrappers
# ============================================================

def builtin_abs(x: Numeric) -> Numeric:
    """Absolute value for Rational or Complex."""
    if isinstance(x, Complex):
        result = _abs_complex(x)
        # Return Rational, not Complex
        return result if isinstance(result, Rational) else result
    return _abs_rational(x)


def builtin_sqrt(x: Numeric) -> Numeric:
    """Square root for Rational or Complex."""
    if isinstance(x, Complex):
        result = _sqrt_complex(x)
        if result.is_real():
            return result.real
        return result
    result = _sqrt_rational(x)
    if isinstance(result, Complex) and result.is_real():
        return result.real
    return result


def builtin_exp(x: Numeric) -> Numeric:
    """Exponential for Rational or Complex."""
    if isinstance(x, Complex):
        result = _exp_complex(x)
        if result.is_real():
            return result.real
        return result
    return _exp_rational(x)


def builtin_log(x: Numeric) -> Numeric:
    """Natural logarithm for Rational (Complex not fully supported)."""
    if isinstance(x, Complex):
        if x.is_real():
            return _log_rational(x.real)
        raise InvalidOperandError("Complex logarithm not yet supported")
    return _log_rational(x)


def builtin_sin(x: Numeric) -> Numeric:
    """Sine for Rational or Complex."""
    if isinstance(x, Complex):
        result = _sin_complex(x)
        if result.is_real():
            return result.real
        return result
    return _sin_rational(x)


def builtin_cos(x: Numeric) -> Numeric:
    """Cosine for Rational or Complex."""
    if isinstance(x, Complex):
        result = _cos_complex(x)
        if result.is_real():
            return result.real
        return result
    return _cos_rational(x)


def builtin_tan(x: Numeric) -> Numeric:
    """Tangent for Rational."""
    if isinstance(x, Complex) and not x.is_real():
        raise InvalidOperandError("Complex tangent not yet supported")
    if isinstance(x, Complex):
        x = x.real
    return _tan_rational(x)


# ============================================================
# Matrix functions
# ============================================================

def builtin_det(x):
    """Determinant of a matrix."""
    from ..math_types import Matrix
    if not isinstance(x, Matrix):
        raise InvalidOperandError(f"det() requires a Matrix, got {type(x).__name__}")
    return x.determinant()


def builtin_inv(x):
    """Inverse of a matrix."""
    from ..math_types import Matrix
    if not isinstance(x, Matrix):
        raise InvalidOperandError(f"inv() requires a Matrix, got {type(x).__name__}")
    return x.inverse()


def builtin_transpose(x):
    """Transpose of a matrix."""
    from ..math_types import Matrix
    if not isinstance(x, Matrix):
        raise InvalidOperandError(f"transpose() requires a Matrix, got {type(x).__name__}")
    return x.transpose()


# ============================================================
# Registry of built-in functions
# ============================================================

BUILTIN_FUNCTIONS: Dict[str, BuiltinFunction] = {
    'abs': BuiltinFunction('abs', builtin_abs, 'Absolute value'),
    'sqrt': BuiltinFunction('sqrt', builtin_sqrt, 'Square root'),
    'exp': BuiltinFunction('exp', builtin_exp, 'Exponential (e^x)'),
    'log': BuiltinFunction('log', builtin_log, 'Natural logarithm'),
    'ln': BuiltinFunction('ln', builtin_log, 'Natural logarithm (alias)'),
    'sin': BuiltinFunction('sin', builtin_sin, 'Sine'),
    'cos': BuiltinFunction('cos', builtin_cos, 'Cosine'),
    'tan': BuiltinFunction('tan', builtin_tan, 'Tangent'),
    'det': BuiltinFunction('det', builtin_det, 'Matrix determinant'),
    'inv': BuiltinFunction('inv', builtin_inv, 'Matrix inverse'),
    'transpose': BuiltinFunction('transpose', builtin_transpose, 'Matrix transpose'),
}


def is_builtin(name: str) -> bool:
    """Check if a function name is a built-in."""
    return name.lower() in BUILTIN_FUNCTIONS


def get_builtin(name: str) -> BuiltinFunction:
    """Get a built-in function by name."""
    return BUILTIN_FUNCTIONS[name.lower()]


def list_builtins() -> list:
    """List all built-in function names."""
    return list(BUILTIN_FUNCTIONS.keys())