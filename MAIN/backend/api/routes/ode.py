"""
Differential equations calculation endpoint.
"""
from __future__ import annotations

import math
from fastapi import APIRouter, HTTPException

from numerix.core.expression_parser import parse_function_x, ParseError
from numerix.core.result_models import SolverStatus
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.learning.learning_engine import LearningEngine
from backend.api.schemas.requests import ODERequest
from backend.api.schemas.responses import (
    GraphCurveData,
    IterationItem,
    MetricsResponse,
    SolverAPIResponse,
)

router = APIRouter(tags=["Differential Equations"])
engine = SolverEngine()
learning_engine = LearningEngine()


@router.post("/solve/ode", response_model=SolverAPIResponse)
def solve_ode(req: ODERequest) -> SolverAPIResponse:
    problem_req = ProblemRequest(
        method=req.method,
        expression=req.expression,
        ode_x0=req.x0,
        ode_y0=req.y0,
        ode_h=req.h,
        ode_x_end=req.x_end,
    )

    try:
        res = engine.solve(problem_req)
    except ParseError as pe:
        raise HTTPException(status_code=400, detail=f"ODE expression error: {pe}")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ODE calculation error: {str(exc)}")

    curves: list[GraphCurveData] = []
    final_exact_error: float | None = None

    if res.ode_table:
        num_x = [round(row["x"], 5) for row in res.ode_table if "x" in row]
        num_y = [round(row["y"], 6) for row in res.ode_table if "y" in row]
        curves.append(
            GraphCurveData(
                x=num_x,
                y=num_y,
                label=f"{res.method} (Numerical)",
                type="line",
            )
        )

        # Exact analytical curve if provided
        if req.exact_expression and req.exact_expression.strip():
            try:
                _, f_exact = parse_function_x(req.exact_expression.strip())
                dense_pts = 100
                x_min, x_max = min(num_x), max(num_x)
                dx = (x_max - x_min) / dense_pts if dense_pts > 0 else 0.1
                exact_x = []
                exact_y = []
                for i in range(dense_pts + 1):
                    xv = x_min + i * dx
                    try:
                        yv = f_exact(xv)
                        if math.isfinite(yv):
                            exact_x.append(round(xv, 5))
                            exact_y.append(round(yv, 6))
                    except Exception:
                        continue

                curves.append(
                    GraphCurveData(
                        x=exact_x,
                        y=exact_y,
                        label="Exact Solution",
                        type="line",
                    )
                )

                # Compute final exact error
                if num_y:
                    final_exact_y = f_exact(num_x[-1])
                    final_exact_error = abs(num_y[-1] - final_exact_y)
            except Exception:
                pass  # Ignore invalid exact expression

    iter_items = [
        IterationItem(
            n=it.n,
            values={k: (round(v, 7) if isinstance(v, float) else v) for k, v in it.values.items()},
            approximate_error=it.approximate_error,
            extra=it.extra,
        )
        for it in res.iterations
    ]

    solution_doc = None
    try:
        solution_doc = learning_engine.generate(problem_req, res)
    except Exception:
        pass

    return SolverAPIResponse(
        method=res.method,
        problem_type=res.problem_type,
        status=res.status.value,
        termination_reason=res.termination_reason,
        success=res.status == SolverStatus.SUCCESS,
        ode_table=res.ode_table,
        iterations=iter_items,
        metrics=MetricsResponse(
            iterations=res.metrics.iterations,
            execution_time_seconds=round(res.metrics.execution_time_seconds, 6),
            final_exact_error=round(final_exact_error, 8) if final_exact_error is not None else None,
        ),
        curves=curves,
        warnings=res.warnings,
        extra=res.extra,
        solution_document=solution_doc,
    )
