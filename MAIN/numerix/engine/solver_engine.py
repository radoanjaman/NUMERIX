"""
NUMERIX Solver Engine — single entry point for all eight algorithms.

Workflow:
  1. Accept a ProblemRequest.
  2. Validate inputs.
  3. Parse expressions via the safe parser.
  4. Look up the method in the registry.
  5. Execute the algorithm.
  6. Return a normalised SolverResult.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from numerix.core.expression_parser import (
    differentiate_x,
    parse_function_x,
    parse_function_xy,
)
from numerix.core.result_models import SolverResult
from numerix.algorithms.root_finding.bisection import bisection
from numerix.algorithms.root_finding.false_position import false_position
from numerix.algorithms.root_finding.newton_raphson import newton_raphson
from numerix.algorithms.linear_systems.gauss_elimination import gauss_elimination
from numerix.algorithms.linear_systems.gauss_jordan import gauss_jordan
from numerix.algorithms.ode.euler import euler
from numerix.algorithms.ode.modified_euler import modified_euler
from numerix.algorithms.ode.rk4 import rk4


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------

@dataclass
class ProblemRequest:
    """Structured input to the solver engine."""

    method: str = ""  # one of the METHOD_IDS below; set by ComparisonEngine

    # --- root finding ---
    expression: str = ""       # f(x) as string, used for root-finding & ODE
    a: float | None = None     # bracket left / initial guess x0
    b: float | None = None     # bracket right
    x0: float | None = None    # Newton-Raphson initial guess (overrides a)
    tol: float = 1e-6
    max_iter: int = 100

    # --- linear systems ---
    A: list[list[float]] = field(default_factory=list)
    b_vec: list[float] = field(default_factory=list)

    # --- ODE ---
    # expression is reused as f(x, y) string
    ode_x0: float | None = None
    ode_y0: float | None = None
    ode_h: float | None = None
    ode_x_end: float | None = None


# ---------------------------------------------------------------------------
# Method registry
# ---------------------------------------------------------------------------

METHOD_IDS = {
    "bisection",
    "false_position",
    "newton_raphson",
    "gauss_elimination",
    "gauss_jordan",
    "euler",
    "modified_euler",
    "rk4",
}

# Groups for the comparison engine
ROOT_FINDING_METHODS = {"bisection", "false_position", "newton_raphson"}
LINEAR_SYSTEM_METHODS = {"gauss_elimination", "gauss_jordan"}
ODE_METHODS = {"euler", "modified_euler", "rk4"}


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class SolverEngine:
    """Execute any NUMERIX algorithm through one consistent API."""

    def solve(self, req: ProblemRequest) -> SolverResult:
        method = req.method.strip().lower()
        if method not in METHOD_IDS:
            raise ValueError(
                f"Unknown method '{method}'. Choose from: {sorted(METHOD_IDS)}"
            )

        if method in ROOT_FINDING_METHODS:
            return self._solve_root(req, method)
        elif method in LINEAR_SYSTEM_METHODS:
            return self._solve_linear(req, method)
        else:
            return self._solve_ode(req, method)

    # --- root finding ---

    def _solve_root(self, req: ProblemRequest, method: str) -> SolverResult:
        if not req.expression:
            raise ValueError("expression is required for root-finding methods.")

        expr_sym, f = parse_function_x(req.expression)

        if method == "newton_raphson":
            x0 = req.x0 if req.x0 is not None else req.a
            if x0 is None:
                raise ValueError("x0 (or a) must be supplied for Newton-Raphson.")
            _, df = differentiate_x(expr_sym)
            return newton_raphson(f, df, x0, req.tol, req.max_iter)

        # bracketing methods
        if req.a is None or req.b is None:
            raise ValueError("a and b (bracket) are required for bracketing methods.")

        if method == "bisection":
            return bisection(f, req.a, req.b, req.tol, req.max_iter)
        else:
            return false_position(f, req.a, req.b, req.tol, req.max_iter)

    # --- linear systems ---

    def _solve_linear(self, req: ProblemRequest, method: str) -> SolverResult:
        if not req.A or not req.b_vec:
            raise ValueError("A and b_vec are required for linear system methods.")
        if method == "gauss_elimination":
            return gauss_elimination(req.A, req.b_vec)
        else:
            return gauss_jordan(req.A, req.b_vec)

    # --- ODE ---

    def _solve_ode(self, req: ProblemRequest, method: str) -> SolverResult:
        if not req.expression:
            raise ValueError("expression (f(x,y)) is required for ODE methods.")
        for name, val in [
            ("ode_x0", req.ode_x0),
            ("ode_y0", req.ode_y0),
            ("ode_h", req.ode_h),
            ("ode_x_end", req.ode_x_end),
        ]:
            if val is None:
                raise ValueError(f"{name} is required for ODE methods.")

        _, f = parse_function_xy(req.expression)

        if method == "euler":
            return euler(f, req.ode_x0, req.ode_y0, req.ode_h, req.ode_x_end)
        elif method == "modified_euler":
            return modified_euler(f, req.ode_x0, req.ode_y0, req.ode_h, req.ode_x_end)
        else:
            return rk4(f, req.ode_x0, req.ode_y0, req.ode_h, req.ode_x_end)


# ---------------------------------------------------------------------------
# Comparison engine
# ---------------------------------------------------------------------------

class ComparisonEngine:
    """Run multiple compatible methods on the same problem and collect results."""

    def __init__(self) -> None:
        self._engine = SolverEngine()

    def compare(self, methods: list[str], req: ProblemRequest) -> dict[str, SolverResult]:
        """
        Run each method in *methods* against *req* and return a dict of results.

        All methods must belong to the same problem family (root, linear, or ODE).
        """
        # determine family from first method
        m0 = methods[0].strip().lower()
        if m0 in ROOT_FINDING_METHODS:
            family = ROOT_FINDING_METHODS
        elif m0 in LINEAR_SYSTEM_METHODS:
            family = LINEAR_SYSTEM_METHODS
        elif m0 in ODE_METHODS:
            family = ODE_METHODS
        else:
            raise ValueError(f"Unknown method '{m0}'.")

        for m in methods:
            if m.strip().lower() not in family:
                raise ValueError(
                    f"Method '{m}' is not compatible with '{m0}' "
                    "(they belong to different problem families)."
                )

        results: dict[str, SolverResult] = {}
        for m in methods:
            cloned = ProblemRequest(**req.__dict__.copy())
            cloned.method = m
            results[m] = self._engine.solve(cloned)
        return results
