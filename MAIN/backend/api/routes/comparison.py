"""
Multi-method comparison endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from numerix.engine.solver_engine import ComparisonEngine, ProblemRequest
from backend.api.schemas.requests import ComparisonRequest
from backend.api.schemas.responses import (
    ComparisonAPIResponse,
    GraphCurveData,
    IterationItem,
    MethodComparisonItem,
    MetricsResponse,
    SolverAPIResponse,
)

router = APIRouter(tags=["Comparison"])
comp_engine = ComparisonEngine()

_COLOR_CYCLE = ["#2563EB", "#7C3AED", "#059669", "#D97706", "#DC2626"]


@router.post("/compare", response_model=ComparisonAPIResponse)
def compare_methods(req: ComparisonRequest) -> ComparisonAPIResponse:
    if not req.methods:
        raise HTTPException(status_code=422, detail="At least one method must be selected for comparison.")

    # Build underlying ProblemRequest based on category
    if req.category == "root_finding":
        if not req.root_input:
            raise HTTPException(status_code=422, detail="root_input data is required for root_finding comparison.")
        base_req = ProblemRequest(
            expression=req.root_input.expression,
            a=req.root_input.a,
            b=req.root_input.b,
            x0=req.root_input.x0,
            tol=req.root_input.tol,
            max_iter=req.root_input.max_iter,
        )
    elif req.category == "linear_systems":
        if not req.linear_input:
            raise HTTPException(status_code=422, detail="linear_input data is required for linear_systems comparison.")
        base_req = ProblemRequest(
            A=req.linear_input.A,
            b_vec=req.linear_input.b,
        )
    elif req.category == "ode":
        if not req.ode_input:
            raise HTTPException(status_code=422, detail="ode_input data is required for ode comparison.")
        base_req = ProblemRequest(
            expression=req.ode_input.expression,
            ode_x0=req.ode_input.x0,
            ode_y0=req.ode_input.y0,
            ode_h=req.ode_input.h,
            ode_x_end=req.ode_input.x_end,
        )
    else:
        raise HTTPException(status_code=422, detail=f"Unsupported comparison category '{req.category}'.")

    try:
        raw_results = comp_engine.compare(req.methods, base_req)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Comparison engine error: {str(exc)}")

    items: list[MethodComparisonItem] = []
    curves: list[GraphCurveData] = []

    for i, (m_id, res) in enumerate(raw_results.items()):
        color = _COLOR_CYCLE[i % len(_COLOR_CYCLE)]

        # Determine summary string
        if res.problem_type == "root_finding":
            summary = f"Root: {res.root:.7g}" if res.root is not None else "Failed"
            err_val = res.metrics.final_approximate_error
        elif res.problem_type == "linear_system":
            summary = f"x: {[round(v, 4) for v in (res.solution_vector or [])]}"
            err_val = res.metrics.final_residual
        else:
            final_y = res.ode_table[-1]["y"] if res.ode_table else None
            summary = f"y(end): {final_y:.6g}" if final_y is not None else "Failed"
            err_val = None

            # Add ODE trajectory to comparison curves
            if res.ode_table:
                curves.append(
                    GraphCurveData(
                        x=[round(row["x"], 5) for row in res.ode_table if "x" in row],
                        y=[round(row["y"], 6) for row in res.ode_table if "y" in row],
                        label=res.method,
                        type="line",
                    )
                )

        # Standard solver API response item
        api_res = SolverAPIResponse(
            method=res.method,
            problem_type=res.problem_type,
            status=res.status.value,
            termination_reason=res.termination_reason,
            success="converge" in res.status.value.lower() or "success" in res.status.value.lower(),
            root=round(res.root, 7) if res.root is not None else None,
            solution_vector=[round(v, 7) for v in res.solution_vector] if res.solution_vector else None,
            ode_table=res.ode_table,
            iterations=[
                IterationItem(
                    n=it.n,
                    values=it.values,
                    approximate_error=it.approximate_error,
                    extra=it.extra,
                )
                for it in res.iterations
            ],
            metrics=MetricsResponse(
                iterations=res.metrics.iterations,
                execution_time_seconds=round(res.metrics.execution_time_seconds, 6),
                final_approximate_error=res.metrics.final_approximate_error,
                final_residual=res.metrics.final_residual,
            ),
        )

        items.append(
            MethodComparisonItem(
                method=res.method,
                solution_summary=summary,
                iterations_or_steps=res.metrics.iterations,
                final_error_or_residual=err_val,
                execution_time_seconds=round(res.metrics.execution_time_seconds, 6),
                status=res.status.value,
                raw_result=api_res,
            )
        )

    return ComparisonAPIResponse(
        category=req.category,
        items=items,
        curves=curves,
    )
