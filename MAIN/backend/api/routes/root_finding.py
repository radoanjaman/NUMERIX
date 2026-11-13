"""
Root-finding calculation endpoint.
"""
from __future__ import annotations

import math
from fastapi import APIRouter, HTTPException

from numerix.core.expression_parser import parse_function_x, ParseError
from numerix.core.result_models import SolverStatus
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.learning.learning_engine import LearningEngine
from backend.api.schemas.requests import RootFindingRequest
from backend.api.schemas.responses import (
    GraphCurveData,
    IterationItem,
    MetricsResponse,
    SolverAPIResponse,
)

router = APIRouter(tags=["Root Finding"])
engine = SolverEngine()
learning_engine = LearningEngine()


@router.post("/solve/root", response_model=SolverAPIResponse)
@router.post("/solve/root-finding", response_model=SolverAPIResponse)
def solve_root_finding(req: RootFindingRequest) -> SolverAPIResponse:
    problem_req = ProblemRequest(
        method=req.method,
        expression=req.expression,
        a=req.a,
        b=req.b,
        x0=req.x0,
        tol=req.tol,
        max_iter=req.max_iter,
    )

    try:
        res = engine.solve(problem_req)
    except ParseError as pe:
        raise HTTPException(status_code=400, detail=f"Math expression error: {pe}")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(exc)}")

    # Parse function to generate graph curve
    curves: list[GraphCurveData] = []
    markers: list[dict] = []
    f_root: float | None = None

    try:
        _, f_eval = parse_function_x(req.expression)
        if res.root is not None:
            try:
                f_root = f_eval(res.root)
            except Exception:
                f_root = None

        # Determine plot domain
        low = req.a if req.a is not None else (req.x0 - 2.0 if req.x0 is not None else -5.0)
        high = req.b if req.b is not None else (req.x0 + 2.0 if req.x0 is not None else 5.0)
        if res.root is not None:
            low = min(low, res.root - 1.0)
            high = max(high, res.root + 1.0)
        span = high - low
        pad = max(span * 0.15, 0.5)
        x_start = low - pad
        x_end = high + pad

        pts = 120
        step = (x_end - x_start) / pts
        x_vals: list[float] = []
        y_vals: list[float] = []
        for i in range(pts + 1):
            xv = x_start + i * step
            try:
                yv = f_eval(xv)
                if math.isfinite(yv) and abs(yv) < 1e6:
                    x_vals.append(round(xv, 5))
                    y_vals.append(round(yv, 5))
            except Exception:
                continue

        curves.append(
            GraphCurveData(
                x=x_vals,
                y=y_vals,
                label=f"f(x) = {req.expression}",
                type="line",
            )
        )

        # Zero reference line
        if x_vals:
            curves.append(
                GraphCurveData(
                    x=[x_vals[0], x_vals[-1]],
                    y=[0.0, 0.0],
                    label="y = 0",
                    type="line",
                )
            )

        # Root marker
        if res.root is not None and f_root is not None:
            markers.append({
                "x": round(res.root, 6),
                "y": round(f_root, 6),
                "label": f"Root ≈ {res.root:.6g}",
                "color": "#2563EB",
            })

    except Exception:
        pass  # If curve generation fails, still return tabular results

    # Convergence curve (Error vs Iteration)
    err_x = []
    err_y = []
    for it in res.iterations:
        if it.approximate_error is not None and it.approximate_error > 0:
            err_x.append(it.n)
            err_y.append(round(it.approximate_error, 8))
    if err_x:
        curves.append(
            GraphCurveData(
                x=err_x,
                y=err_y,
                label="Approximate Error vs Iteration",
                type="line",
            )
        )

    # Format iteration items
    iter_items = [
        IterationItem(
            n=it.n,
            values={k: (round(v, 7) if isinstance(v, float) else v) for k, v in it.values.items()},
            approximate_error=round(it.approximate_error, 8) if it.approximate_error is not None else None,
            extra=it.extra,
        )
        for it in res.iterations
    ]

    # Generate pedagogical solution document
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
        success=res.status == SolverStatus.CONVERGED,
        root=round(res.root, 7) if res.root is not None else None,
        f_root=round(f_root, 7) if f_root is not None else None,
        iterations=iter_items,
        metrics=MetricsResponse(
            iterations=res.metrics.iterations,
            execution_time_seconds=round(res.metrics.execution_time_seconds, 6),
            final_approximate_error=res.metrics.final_approximate_error,
        ),
        curves=curves,
        markers=markers,
        warnings=res.warnings,
        extra=res.extra,
        solution_document=solution_doc,
    )
