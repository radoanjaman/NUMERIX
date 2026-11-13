"""
Linear systems calculation endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from numerix.core.result_models import SolverStatus
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.learning.learning_engine import LearningEngine
from backend.api.schemas.requests import LinearSystemRequest
from backend.api.schemas.responses import (
    GraphCurveData,
    IterationItem,
    MetricsResponse,
    SolverAPIResponse,
)

router = APIRouter(tags=["Linear Systems"])
engine = SolverEngine()
learning_engine = LearningEngine()


@router.post("/solve/linear", response_model=SolverAPIResponse)
@router.post("/solve/linear-systems", response_model=SolverAPIResponse)
def solve_linear_system(req: LinearSystemRequest) -> SolverAPIResponse:
    problem_req = ProblemRequest(
        method=req.method,
        A=req.A,
        b_vec=req.b,
    )

    try:
        res = engine.solve(problem_req)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Linear system calculation error: {str(exc)}")

    iter_items = [
        IterationItem(
            n=it.n,
            values=it.values,
            approximate_error=it.approximate_error,
            extra=it.extra,
        )
        for it in res.iterations
    ]

    # Bar chart for solution vector coordinates if solved
    curves: list[GraphCurveData] = []
    if res.solution_vector:
        curves.append(
            GraphCurveData(
                x=[i + 1 for i in range(len(res.solution_vector))],
                y=[round(val, 6) for val in res.solution_vector],
                label="Solution Vector x",
                type="bar",
            )
        )

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
        solution_vector=[round(x, 7) for x in res.solution_vector] if res.solution_vector else None,
        iterations=iter_items,
        metrics=MetricsResponse(
            iterations=res.metrics.iterations,
            execution_time_seconds=round(res.metrics.execution_time_seconds, 6),
            final_residual=res.metrics.final_residual,
        ),
        curves=curves,
        warnings=res.warnings,
        extra=res.extra,
        solution_document=solution_doc,
    )
