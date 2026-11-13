"""
Safe mathematical expression parser using SymPy.

Never uses unrestricted eval() or exec().  Only an explicit allowlist of
symbols and functions is accepted.  Symbolic differentiation is supported.
"""
from __future__ import annotations

import math
from typing import Callable

import sympy
from sympy import symbols, sympify, diff, lambdify, SympifyError
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

# allowed names the parser resolves
_ALLOWED_FUNCTIONS: dict[str, object] = {
    "sin": sympy.sin,
    "cos": sympy.cos,
    "tan": sympy.tan,
    "exp": sympy.exp,
    "log": sympy.log,
    "sqrt": sympy.sqrt,
    "abs": sympy.Abs,
    "pi": sympy.pi,
    "e": sympy.E,
}

_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)

# pre-declare the two independent symbols used across the app
x_sym = symbols("x")
y_sym = symbols("y")


class ParseError(ValueError):
    """Raised when an expression cannot be parsed or uses illegal symbols."""


def _check_symbols(expr_sym: sympy.Expr, allowed: set[sympy.Symbol]) -> None:
    """Reject any free symbol not in *allowed*."""
    free = expr_sym.free_symbols
    illegal = free - allowed
    if illegal:
        names = ", ".join(str(s) for s in sorted(illegal, key=str))
        raise ParseError(
            f"Unsupported symbol(s): {names}. "
            f"Allowed: {', '.join(str(s) for s in sorted(allowed, key=str))}"
        )


def parse_function_x(expression: str) -> tuple[sympy.Expr, Callable[[float], float]]:
    """
    Parse a single-variable expression in `x`.

    Returns (sympy_expr, numeric_callable).
    Raises ParseError on invalid input.
    """
    expr_sym = _parse_sympy(expression, {x_sym})
    f = lambdify(x_sym, expr_sym, modules=["numpy", "math"])

    def safe_f(val: float) -> float:
        result = f(val)
        if not math.isfinite(result):
            raise ValueError(f"f({val}) = {result} is not finite")
        return float(result)

    return expr_sym, safe_f


def parse_function_xy(
    expression: str,
) -> tuple[sympy.Expr, Callable[[float, float], float]]:
    """
    Parse a two-variable expression in `x` and `y`.

    Returns (sympy_expr, numeric_callable).
    Raises ParseError on invalid input.
    """
    expr_sym = _parse_sympy(expression, {x_sym, y_sym})
    f = lambdify((x_sym, y_sym), expr_sym, modules=["numpy", "math"])

    def safe_f(xv: float, yv: float) -> float:
        result = f(xv, yv)
        if not math.isfinite(result):
            raise ValueError(f"f({xv}, {yv}) = {result} is not finite")
        return float(result)

    return expr_sym, safe_f


def differentiate_x(expr_sym: sympy.Expr) -> tuple[sympy.Expr, Callable[[float], float]]:
    """Return the symbolic derivative wrt x and a numeric callable."""
    deriv_sym = diff(expr_sym, x_sym)
    df = lambdify(x_sym, deriv_sym, modules=["numpy", "math"])

    def safe_df(val: float) -> float:
        result = df(val)
        if not math.isfinite(result):
            raise ValueError(f"f'({val}) = {result} is not finite")
        return float(result)

    return deriv_sym, safe_df


_BLOCKED_TOKENS = frozenset(["__", "import", "eval", "exec", "open", "compile", "globals", "locals", "lambda"])

_BLOCKED_CHARS = frozenset([".", "[", "]", ";"])


def _check_raw(expression: str) -> None:
    """Reject obviously dangerous tokens and characters before SymPy sees the string."""
    # Length guard
    if len(expression) > 500:
        raise ParseError("Expression too long (max 500 chars).")

    # Newline / carriage-return guard
    if "\n" in expression or "\r" in expression:
        raise ParseError("Expression must not contain newlines.")

    # Blocked single characters
    for ch in _BLOCKED_CHARS:
        if ch in expression:
            raise ParseError(f"Forbidden character '{ch}' in expression.")

    # Blocked token substrings (case-insensitive)
    low = expression.lower()
    for token in _BLOCKED_TOKENS:
        if token in low:
            raise ParseError(f"Forbidden token '{token}' in expression.")


def _parse_sympy(expression: str, allowed_symbols: set[sympy.Symbol]) -> sympy.Expr:
    """Internal: parse string → SymPy expr, enforce allowlist."""
    if not isinstance(expression, str) or not expression.strip():
        raise ParseError("Expression must be a non-empty string.")
    _check_raw(expression)
    try:
        expr_sym = parse_expr(
            expression.strip(),
            local_dict=_ALLOWED_FUNCTIONS,
            transformations=_TRANSFORMATIONS,
        )
    except (SympifyError, SyntaxError, TypeError) as exc:
        raise ParseError(f"Cannot parse expression '{expression}': {exc}") from exc

    if not isinstance(expr_sym, sympy.Basic):
        raise ParseError("Expression did not produce a valid symbolic form.")
    _check_symbols(expr_sym, allowed_symbols)
    return expr_sym
