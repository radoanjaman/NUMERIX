"""
Bisection Method — root finding.

Mathematical basis: If f(a)*f(b) < 0, there is at least one root in [a, b].
Halve the interval each step, keeping the sub-interval that contains the sign change.

Error metric: |b - a| / 2  (half-width of remaining interval).
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
from numerix.core.validators import (
    validate_max_iterations,
    validate_root_finding_bracket,
    validate_tolerance,
)


def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> SolverResult:
    """
    Bisection method for root finding.

    Parameters
    ----------
    f        : callable  — f(x), must be continuous on [a, b]
    a, b     : float     — initial bracket  (a < b, f(a)*f(b) < 0)
    tol      : float     — stop when interval half-width < tol
    max_iter : int       — maximum number of bisections

    Returns
    -------
    SolverResult with root, full iteration history, and metrics.
    """
    validate_tolerance(tol)
    validate_max_iterations(max_iter)

    fa = f(a)
    fb = f(b)
    validate_root_finding_bracket(a, b, fa, fb)

    history: list[IterationRecord] = []
    t0 = time.perf_counter()
    mid = a  # will be overwritten on first iteration

    for n in range(1, max_iter + 1):
        mid = (a + b) / 2.0
        fmid = f(mid)
        error = (b - a) / 2.0

        history.append(
            IterationRecord(
                n=n,
                values={
                    "a": a,
                    "b": b,
                    "mid": mid,
                    "f_a": fa,
                    "f_b": fb,
                    "f_mid": fmid,
                },
                approximate_error=error,
            )
        )

        if not math.isfinite(fmid):
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Bisection",
                problem_type="root_finding",
                status=SolverStatus.NON_FINITE,
                termination_reason="f(midpoint) is not finite",
                root=mid,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                    final_approximate_error=error,
                ),
                warnings=[f"Non-finite f(mid) at iteration {n}"],
            )

        if error < tol or fmid == 0.0:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Bisection",
                problem_type="root_finding",
                status=SolverStatus.CONVERGED,
                termination_reason="tolerance_reached",
                root=mid,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                    final_approximate_error=error,
                ),
            )

        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid

    elapsed = time.perf_counter() - t0
    return SolverResult(
        method="Bisection",
        problem_type="root_finding",
        status=SolverStatus.MAX_ITERATIONS,
        termination_reason="max_iterations_reached",
        root=mid,
        iterations=history,
        metrics=SolverMetrics(
            iterations=max_iter,
            execution_time_seconds=elapsed,
            final_approximate_error=history[-1].approximate_error,
        ),
        warnings=[f"Did not converge within {max_iter} iterations"],
    )
