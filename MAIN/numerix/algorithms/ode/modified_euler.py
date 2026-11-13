"""
Modified Euler Method (Heun's predictor-corrector) — ODE solver.

Two-stage scheme:
    predictor:  y*_{n+1}  = y_n + h * f(x_n, y_n)
    corrector:  y_{n+1}   = y_n + (h/2) * [f(x_n, y_n) + f(x_{n+1}, y*_{n+1})]

Records predictor, predicted slope, corrected estimate, and corrector slope.
"""
from __future__ import annotations

import time
from typing import Callable

from numerix.core.result_models import (
    IterationRecord,
    SolverMetrics,
    SolverResult,
    SolverStatus,
)
from numerix.core.validators import validate_ode_params


def modified_euler(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    h: float,
    x_end: float,
) -> SolverResult:
    """
    Modified Euler (Heun) method for dy/dx = f(x, y).

    Parameters
    ----------
    f     : callable — f(x, y) = dy/dx
    x0    : float   — initial x
    y0    : float   — initial y(x0)
    h     : float   — step size
    x_end : float   — stop at or beyond this x value

    Returns
    -------
    SolverResult with ode_table and full predictor-corrector detail.
    """
    validate_ode_params(x0, x_end, y0, h)

    history: list[IterationRecord] = []
    ode_table: list[dict] = []
    t0 = time.perf_counter()

    x, y = float(x0), float(y0)
    n = 0
    ode_table.append({"n": n, "x": x, "y": y})

    while (h > 0 and x < x_end - 1e-14) or (h < 0 and x > x_end + 1e-14):
        f1 = f(x, y)                    # slope at current point
        y_pred = y + h * f1             # predictor
        x_next = x + h
        f2 = f(x_next, y_pred)          # slope at predicted point
        y_corr = y + (h / 2) * (f1 + f2)  # corrector

        history.append(
            IterationRecord(
                n=n,
                values={
                    "x": x,
                    "y": y,
                    "f1_slope": f1,
                    "y_predictor": y_pred,
                    "x_next": x_next,
                    "f2_slope": f2,
                    "y_corrector": y_corr,
                },
            )
        )

        x, y = x_next, y_corr
        n += 1
        ode_table.append({"n": n, "x": x, "y": y})

    elapsed = time.perf_counter() - t0

    return SolverResult(
        method="Modified Euler",
        problem_type="ode",
        status=SolverStatus.SUCCESS,
        termination_reason="x_end_reached",
        ode_table=ode_table,
        iterations=history,
        metrics=SolverMetrics(
            iterations=n,
            execution_time_seconds=elapsed,
        ),
    )
