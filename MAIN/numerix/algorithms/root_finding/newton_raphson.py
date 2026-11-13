"""
Newton-Raphson Method — root finding.

Iterates:  x_{n+1} = x_n - f(x_n) / f'(x_n)

f'(x) is computed symbolically via SymPy when an expression string is
supplied, or numerically via a user-provided callable.

Error metric: |x_{n+1} - x_n|.
"""
from __future__ import annotations

import math
import time
from typing import Callable

from numerix.core.result_models import (
    IterationRecord,
    SolverMetrics,
    SolverResult,
    SolverStatus,
)
from numerix.core.validators import validate_max_iterations, validate_tolerance

# derivative-too-small threshold
_DERIV_EPS = 1e-14


def newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> SolverResult:
    """
    Newton-Raphson method for root finding.

    Parameters
    ----------
    f        : callable — f(x)
    df       : callable — f'(x)  (use expression_parser.differentiate_x to get this)
    x0       : float    — initial guess
    tol      : float    — stop when |x_new - x_old| < tol
    max_iter : int      — maximum iterations

    Returns
    -------
    SolverResult with root, full iteration history, and metrics.
    """
    validate_tolerance(tol)
    validate_max_iterations(max_iter)
    if not math.isfinite(x0):
        raise ValueError(f"Initial guess x0 must be finite, got {x0}.")

    history: list[IterationRecord] = []
    t0 = time.perf_counter()
    x = float(x0)

    for n in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < _DERIV_EPS:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Newton-Raphson",
                problem_type="root_finding",
                status=SolverStatus.ZERO_DERIVATIVE,
                termination_reason="derivative_too_small",
                root=x,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                ),
                warnings=[f"f'(x) ≈ 0 at x={x:.8g} (iteration {n})"],
            )

        x_new = x - fx / dfx
        error = abs(x_new - x)

        history.append(
            IterationRecord(
                n=n,
                values={
                    "x_n": x,
                    "f_xn": fx,
                    "df_xn": dfx,
                    "x_new": x_new,
                },
                approximate_error=error,
            )
        )

        if not math.isfinite(x_new):
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Newton-Raphson",
                problem_type="root_finding",
                status=SolverStatus.NON_FINITE,
                termination_reason="x_new is not finite",
                root=x_new,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                ),
                warnings=[f"Non-finite x_new at iteration {n}"],
            )

        x = x_new
        if error < tol:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Newton-Raphson",
                problem_type="root_finding",
                status=SolverStatus.CONVERGED,
                termination_reason="tolerance_reached",
                root=x,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                    final_approximate_error=error,
                ),
            )

    elapsed = time.perf_counter() - t0
    return SolverResult(
        method="Newton-Raphson",
        problem_type="root_finding",
        status=SolverStatus.MAX_ITERATIONS,
        termination_reason="max_iterations_reached",
        root=x,
        iterations=history,
        metrics=SolverMetrics(
            iterations=max_iter,
            execution_time_seconds=elapsed,
            final_approximate_error=history[-1].approximate_error if history else None,
        ),
        warnings=[f"Did not converge within {max_iter} iterations"],
    )
