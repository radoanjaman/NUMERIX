"""
False Position (Regula Falsi) Method — root finding.

Uses a linear interpolation between (a, f(a)) and (b, f(b)) to estimate
the root, then replaces the endpoint whose function value has the same sign
as the new estimate.

Error metric: |x_new - x_old| (change in estimated root).
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


def false_position(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> SolverResult:
    """
    False Position (Regula Falsi) method for root finding.

    Parameters
    ----------
    f        : callable — f(x), continuous on [a, b]
    a, b     : float    — initial bracket (f(a)*f(b) < 0)
    tol      : float    — stop when |root_new - root_old| < tol
    max_iter : int      — maximum iterations

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
    root_prev = a
    root = a  # will be set on first iteration

    for n in range(1, max_iter + 1):
        denom = fb - fa
        if denom == 0.0:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="False Position",
                problem_type="root_finding",
                status=SolverStatus.NON_FINITE,
                termination_reason="f(b)-f(a)=0 — denominator zero",
                root=root,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                ),
                warnings=["Denominator f(b)-f(a) became zero"],
            )

        root = (a * fb - b * fa) / denom
        froot = f(root)
        error = abs(root - root_prev) if n > 1 else abs(b - a)

        history.append(
            IterationRecord(
                n=n,
                values={
                    "a": a,
                    "b": b,
                    "f_a": fa,
                    "f_b": fb,
                    "root": root,
                    "f_root": froot,
                },
                approximate_error=error,
            )
        )

        if not math.isfinite(froot):
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="False Position",
                problem_type="root_finding",
                status=SolverStatus.NON_FINITE,
                termination_reason="f(root) is not finite",
                root=root,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                    final_approximate_error=error,
                ),
                warnings=[f"Non-finite f(root) at iteration {n}"],
            )

        if error < tol and n > 1 or froot == 0.0:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="False Position",
                problem_type="root_finding",
                status=SolverStatus.CONVERGED,
                termination_reason="tolerance_reached",
                root=root,
                iterations=history,
                metrics=SolverMetrics(
                    iterations=n,
                    execution_time_seconds=elapsed,
                    final_approximate_error=error,
                ),
            )

        if fa * froot < 0:
            b, fb = root, froot
        else:
            a, fa = root, froot

        root_prev = root

    elapsed = time.perf_counter() - t0
    return SolverResult(
        method="False Position",
        problem_type="root_finding",
        status=SolverStatus.MAX_ITERATIONS,
        termination_reason="max_iterations_reached",
        root=root,
        iterations=history,
        metrics=SolverMetrics(
            iterations=max_iter,
            execution_time_seconds=elapsed,
            final_approximate_error=history[-1].approximate_error if history else None,
        ),
        warnings=[f"Did not converge within {max_iter} iterations"],
    )
