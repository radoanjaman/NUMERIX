"""
Euler Method — ODE solver.

Explicit first-order forward Euler:
    y_{n+1} = y_n + h * f(x_n, y_n)

Records slope and next estimate at every step.
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


def euler(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    h: float,
    x_end: float,
) -> SolverResult:
    """
    Euler method for dy/dx = f(x, y).

    Parameters
    ----------
    f     : callable — f(x, y) = dy/dx
    x0    : float   — initial x
    y0    : float   — initial y(x0)
    h     : float   — step size (positive for forward integration)
    x_end : float   — stop at or beyond this x value

    Returns
    -------
    SolverResult with ode_table containing (n, x, y, slope, y_next).
    """
    validate_ode_params(x0, x_end, y0, h)

    history: list[IterationRecord] = []
    ode_table: list[dict] = []
    t0 = time.perf_counter()

    x, y = float(x0), float(y0)
    n = 0

    # include the initial point
    ode_table.append({"n": n, "x": x, "y": y})

    while (h > 0 and x < x_end - 1e-14) or (h < 0 and x > x_end + 1e-14):
        slope = f(x, y)
        y_next = y + h * slope
        x_next = x + h

        history.append(
            IterationRecord(
                n=n,
                values={
                    "x": x,
                    "y": y,
                    "slope": slope,
                    "y_next": y_next,
                    "x_next": x_next,
                },
            )
        )

        x, y = x_next, y_next
        n += 1
        ode_table.append({"n": n, "x": x, "y": y})

    elapsed = time.perf_counter() - t0

    return SolverResult(
        method="Euler",
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
