"""
Input validators for all solver types.

Each function raises ValueError with a descriptive message on bad input.
"""
from __future__ import annotations

import math


def validate_root_finding_bracket(a: float, b: float, fa: float, fb: float) -> None:
    """Ensure [a, b] brackets a root (sign change required)."""
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("Interval bounds must be finite numbers.")
    if a >= b:
        raise ValueError(f"Interval [a, b] requires a < b, got a={a}, b={b}.")
    if fa * fb > 0:
        raise ValueError(
            f"f(a)={fa:.6g} and f(b)={fb:.6g} have the same sign. "
            "No sign change in [a, b]; bracket may not contain a root."
        )


def validate_tolerance(tol: float) -> None:
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError(f"Tolerance must be a finite positive number, got {tol}.")


def validate_max_iterations(max_iter: int) -> None:
    if not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError(f"max_iterations must be a positive integer, got {max_iter}.")


def validate_matrix(A: list[list[float]], b: list[float]) -> None:
    n = len(b)
    if n == 0:
        raise ValueError("System must have at least one equation.")
    if len(A) != n:
        raise ValueError(f"A has {len(A)} rows but b has {n} elements.")
    for i, row in enumerate(A):
        if len(row) != n:
            raise ValueError(
                f"Row {i} of A has {len(row)} elements; expected {n} (square matrix required)."
            )
    for i, row in enumerate(A):
        for j, v in enumerate(row):
            if not math.isfinite(v):
                raise ValueError(f"A[{i}][{j}] = {v} is not finite.")
    for i, v in enumerate(b):
        if not math.isfinite(v):
            raise ValueError(f"b[{i}] = {v} is not finite.")


def validate_ode_params(x0: float, x_end: float, y0: float, h: float) -> None:
    for name, val in [("x0", x0), ("x_end", x_end), ("y0", y0), ("h", h)]:
        if not math.isfinite(val):
            raise ValueError(f"{name} must be finite, got {val}.")
    if h == 0:
        raise ValueError("Step size h must be nonzero.")
    if (x_end - x0) * h <= 0:
        raise ValueError(
            f"Step size h={h} direction is inconsistent with interval "
            f"[{x0}, {x_end}]."
        )
