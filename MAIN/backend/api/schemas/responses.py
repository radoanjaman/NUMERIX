"""
Pydantic Response Schemas for NUMERIX API.
"""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field

from numerix.learning.solution_models import SolutionDocument


class IterationItem(BaseModel):
    n: int
    values: dict[str, Any]
    approximate_error: float | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class MetricsResponse(BaseModel):
    iterations: int = 0
    execution_time_seconds: float = 0.0
    final_approximate_error: float | None = None
    final_residual: float | None = None
    final_exact_error: float | None = None


class GraphCurveData(BaseModel):
    x: list[float] = Field(default_factory=list)
    y: list[float] = Field(default_factory=list)
    label: str = "Function"
    type: str = "line"  # "line", "scatter", "bar"


class SolverAPIResponse(BaseModel):
    method: str
    problem_type: str
    status: str
    termination_reason: str
    success: bool

    # Solution fields
    root: float | None = None
    f_root: float | None = None
    solution_vector: list[float] | None = None
    ode_table: list[dict[str, Any]] | None = None

    # Iteration steps
    iterations: list[IterationItem] = Field(default_factory=list)

    # Metrics
    metrics: MetricsResponse = Field(default_factory=MetricsResponse)

    # Visualizations ready for Plotly.js / SVG
    curves: list[GraphCurveData] = Field(default_factory=list)
    markers: list[dict[str, Any]] = Field(default_factory=list)

    # Diagnostic & warnings
    warnings: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)
    solution_document: SolutionDocument | None = None


class MethodComparisonItem(BaseModel):
    method: str
    solution_summary: str
    iterations_or_steps: int
    final_error_or_residual: float | None = None
    execution_time_seconds: float
    status: str
    raw_result: SolverAPIResponse


class ComparisonAPIResponse(BaseModel):
    category: str
    items: list[MethodComparisonItem] = Field(default_factory=list)
    curves: list[GraphCurveData] = Field(default_factory=list)
