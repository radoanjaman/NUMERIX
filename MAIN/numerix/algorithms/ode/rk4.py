"""
Fourth-Order Runge-Kutta (RK4) — ODE solver.

Classic four-stage scheme:
    k1 = h * f(x_n,         y_n)
    k2 = h * f(x_n + h/2,   y_n + k1/2)
    k3 = h * f(x_n + h/2,   y_n + k2/2)
    k4 = h * f(x_n + h,     y_n + k3)
    y_{n+1} = y_n + (1/6)(k1 + 2k2 + 2k3 + k4)

Records k1-k4 and next estimate at every step.
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


def rk4(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    h: float,
    x_end: float,
) -> SolverResult:
    """
    Fourth-Order Runge-Kutta method for dy/dx = f(x, y).

    Parameters
    ----------
    f     : callable — f(x, y) = dy/dx
    x0    : float   — initial x
    y0    : float   — initial y(x0)
    h     : float   — step size
    x_end : float   — stop at or beyond this x value

    Returns
    -------
    SolverResult with ode_table and k1-k4 detail at every step.
    """
    validate_ode_params(x0, x_end, y0, h)

    history: list[IterationRecord] = []
    ode_table: list[dict] = []
    t0 = time.perf_counter()

    x, y = float(x0), float(y0)
    n = 0
    ode_table.append({"n": n, "x": x, "y": y})

    while (h > 0 and x < x_end - 1e-14) or (h < 0 and x > x_end + 1e-14):
        k1 = h * f(x,           y)
        k2 = h * f(x + h / 2,   y + k1 / 2)
        k3 = h * f(x + h / 2,   y + k2 / 2)
        k4 = h * f(x + h,       y + k3)
        y_next = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        x_next = x + h

        history.append(
            IterationRecord(
                n=n,
                values={
                    "x": x,
                    "y": y,
                    "k1": k1,
                    "k2": k2,
                    "k3": k3,
                    "k4": k4,
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
        method="RK4",
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
