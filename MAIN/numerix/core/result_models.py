"""
Typed dataclasses for the common NUMERIX result contract.

Every algorithm returns a SolverResult.  UI code consumes these directly;
no algorithm contains formatting or display logic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SolverStatus(Enum):
    CONVERGED = "converged"
    MAX_ITERATIONS = "max_iterations"
    SINGULAR_MATRIX = "singular_matrix"
    ZERO_DERIVATIVE = "zero_derivative"
    INVALID_BRACKET = "invalid_bracket"
    INVALID_INPUT = "invalid_input"
    NON_FINITE = "non_finite"
    SUCCESS = "success"            # for linear systems (no iteration convergence test)


@dataclass
class IterationRecord:
    """One iteration step — fields vary by method; extras go in `extra`."""
    n: int                                     # iteration / step number
    values: dict[str, float | list[float]]     # labelled numeric values for this step
    approximate_error: float | None = None     # |x_new - x_old| or similar
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class SolverMetrics:
    iterations: int = 0
    execution_time_seconds: float = 0.0
    final_approximate_error: float | None = None
    final_residual: float | None = None        # ||Ax - b|| for linear systems
    final_exact_error: float | None = None     # only when exact answer is known


@dataclass
class SolverResult:
    """Unified result returned by every NUMERIX algorithm."""
    method: str
    problem_type: str                          # "root_finding" | "linear_system" | "ode"
    status: SolverStatus
    termination_reason: str

    # --- solution fields (only relevant fields are set) ---
    root: float | None = None                  # root-finding scalar answer
    solution_vector: list[float] | None = None # linear system x vector
    ode_table: list[dict[str, float]] | None = None  # ODE (x, y, ...) rows

    # --- history ---
    iterations: list[IterationRecord] = field(default_factory=list)

    # --- metrics ---
    metrics: SolverMetrics = field(default_factory=SolverMetrics)

    # --- extra method-specific data ---
    extra: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
