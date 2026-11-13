"""
Learning Engine API Endpoints.
"""
from __future__ import annotations

from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from numerix.core.expression_parser import ParseError
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.learning.concept_registry import METHOD_CONCEPTS, get_concept_info
from numerix.learning.formula_registry import get_formula_cards
from numerix.learning.learning_engine import LearningEngine
from numerix.learning.solution_models import SolutionDocument

router = APIRouter(prefix="/learning", tags=["Learning Engine"])
engine = SolverEngine()
learning_engine = LearningEngine()


class LessonGenerateRequest(BaseModel):
    method: str
    expression: str = ""
    a: float | None = None
    b: float | None = None
    x0: float | None = None
    tol: float = 1e-6
    max_iter: int = 100
    A: list[list[float]] = Field(default_factory=list)
    b_vec: list[float] = Field(default_factory=list)
    ode_x0: float | None = None
    ode_y0: float | None = None
    ode_h: float | None = None
    ode_x_end: float | None = None


@router.get("/topics")
def get_topics() -> dict[str, Any]:
    """Retrieve all available learning topics, concepts, and formulas."""
    topics = {}
    for key, data in METHOD_CONCEPTS.items():
        topics[key] = {
            **data,
            "formulas": [f.model_dump() for f in get_formula_cards(key)],
        }
    return {"topics": topics}


@router.post("/generate", response_model=SolutionDocument)
def generate_lesson(req: LessonGenerateRequest) -> SolutionDocument:
    """Generate a structured educational solution document on demand."""
    prob_req = ProblemRequest(
        method=req.method,
        expression=req.expression,
        a=req.a,
        b=req.b,
        x0=req.x0,
        tol=req.tol,
        max_iter=req.max_iter,
        A=req.A,
        b_vec=req.b_vec,
        ode_x0=req.ode_x0,
        ode_y0=req.ode_y0,
        ode_h=req.ode_h,
        ode_x_end=req.ode_x_end,
    )

    try:
        res = engine.solve(prob_req)
    except ParseError as pe:
        raise HTTPException(status_code=400, detail=f"Expression error: {pe}")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Solver execution error: {exc}")

    try:
        doc = learning_engine.generate(prob_req, res)
        return doc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Lesson generation error: {exc}")
