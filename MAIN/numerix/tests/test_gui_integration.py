"""
Integration tests for SolverEngine, ComparisonEngine, and Tkinter GUI workflows.
"""
import os
import pytest
import tkinter as tk

from numerix.engine.solver_engine import (
    SolverEngine,
    ComparisonEngine,
    ProblemRequest,
)
from numerix.core.result_models import SolverResult, SolverStatus
from numerix.core.expression_parser import ParseError
from numerix.gui.app import NumerixApp
from numerix.gui.pages.root_finding import RootFindingPage
from numerix.gui.pages.linear_systems import LinearSystemsPage
from numerix.gui.pages.differential_equations import DifferentialEquationsPage
from numerix.gui.pages.comparison import ComparisonPage
from numerix.gui.pages.about import AboutPage
from numerix.gui.pages.dashboard import DashboardPage


# ---------------------------------------------------------------------------
# Shared fixtures / helpers
# ---------------------------------------------------------------------------

ENGINE = SolverEngine()
COMPARISON = ComparisonEngine()

# A simple root-finding problem: x**3 - x - 2 on [1, 2]
_ROOT_REQ = ProblemRequest(
    expression="x**3 - x - 2",
    a=1.0, b=2.0, x0=1.5,
    tol=1e-7, max_iter=100,
)

# ODE: dy/dx = x + y, y(0)=1, x in [0, 0.5], h=0.1
_ODE_REQ = ProblemRequest(
    expression="x + y",
    ode_x0=0.0, ode_y0=1.0,
    ode_h=0.1, ode_x_end=0.5,
)

# Linear system: 2x+y+z=8, x+3y+z=10, x+y+4z=15
_LINEAR_REQ = ProblemRequest(
    A=[[2.0, 1.0, 1.0], [1.0, 3.0, 1.0], [1.0, 1.0, 4.0]],
    b_vec=[8.0, 10.0, 15.0],
)


class TestEngineIntegration:

    def test_bisection_returns_solver_result(self):
        req = ProblemRequest(**{**_ROOT_REQ.__dict__, "method": "bisection"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "root_finding"
        assert res.root is not None
        assert abs(res.root - 1.5213797) < 1e-4

    def test_false_position_returns_solver_result(self):
        req = ProblemRequest(**{**_ROOT_REQ.__dict__, "method": "false_position"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "root_finding"
        assert res.root is not None

    def test_newton_raphson_returns_solver_result(self):
        req = ProblemRequest(**{**_ROOT_REQ.__dict__, "method": "newton_raphson"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "root_finding"
        assert res.root is not None
        assert abs(res.root - 1.5213797) < 1e-4

    def test_gauss_elimination_returns_solver_result(self):
        req = ProblemRequest(**{**_LINEAR_REQ.__dict__, "method": "gauss_elimination"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "linear_system"
        assert res.solution_vector is not None
        assert len(res.solution_vector) == 3

    def test_gauss_jordan_returns_solver_result(self):
        req = ProblemRequest(**{**_LINEAR_REQ.__dict__, "method": "gauss_jordan"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "linear_system"
        assert res.solution_vector is not None

    def test_euler_returns_solver_result(self):
        req = ProblemRequest(**{**_ODE_REQ.__dict__, "method": "euler"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "ode"
        assert res.ode_table is not None
        assert len(res.ode_table) > 0

    def test_modified_euler_returns_solver_result(self):
        req = ProblemRequest(**{**_ODE_REQ.__dict__, "method": "modified_euler"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "ode"
        assert res.ode_table is not None

    def test_rk4_returns_solver_result(self):
        req = ProblemRequest(**{**_ODE_REQ.__dict__, "method": "rk4"})
        res = ENGINE.solve(req)
        assert isinstance(res, SolverResult)
        assert res.problem_type == "ode"
        assert res.ode_table is not None

    def test_all_8_methods_return_solver_result(self):
        """Smoke-test every method returns a SolverResult with the right problem_type."""
        cases = [
            ("bisection",        "root_finding",  _ROOT_REQ),
            ("false_position",   "root_finding",  _ROOT_REQ),
            ("newton_raphson",   "root_finding",  _ROOT_REQ),
            ("gauss_elimination","linear_system", _LINEAR_REQ),
            ("gauss_jordan",     "linear_system", _LINEAR_REQ),
            ("euler",            "ode",           _ODE_REQ),
            ("modified_euler",   "ode",           _ODE_REQ),
            ("rk4",              "ode",           _ODE_REQ),
        ]
        for method, expected_type, base_req in cases:
            req = ProblemRequest(**{**base_req.__dict__, "method": method})
            res = ENGINE.solve(req)
            assert isinstance(res, SolverResult), f"{method}: not a SolverResult"
            assert res.problem_type == expected_type, (
                f"{method}: expected problem_type={expected_type!r}, got {res.problem_type!r}"
            )

    def test_comparison_root_finding(self):
        """ComparisonEngine on 3 root methods."""
        req = ProblemRequest(**{**_ROOT_REQ.__dict__})
        results = COMPARISON.compare(
            ["bisection", "false_position", "newton_raphson"], req
        )
        assert set(results.keys()) == {"bisection", "false_position", "newton_raphson"}
        for name, res in results.items():
            assert isinstance(res, SolverResult), f"{name}: not a SolverResult"
            assert res.problem_type == "root_finding"

    def test_comparison_ode(self):
        """ComparisonEngine on 3 ODE methods."""
        req = ProblemRequest(**{**_ODE_REQ.__dict__})
        results = COMPARISON.compare(["euler", "modified_euler", "rk4"], req)
        assert set(results.keys()) == {"euler", "modified_euler", "rk4"}
        for name, res in results.items():
            assert isinstance(res, SolverResult), f"{name}: not a SolverResult"
            assert res.problem_type == "ode"

    def test_comparison_linear(self):
        """ComparisonEngine on 2 linear methods."""
        req = ProblemRequest(**{**_LINEAR_REQ.__dict__})
        results = COMPARISON.compare(["gauss_elimination", "gauss_jordan"], req)
        assert set(results.keys()) == {"gauss_elimination", "gauss_jordan"}
        for name, res in results.items():
            assert isinstance(res, SolverResult), f"{name}: not a SolverResult"

    def test_solver_result_fields_complete(self):
        """Core SolverResult fields must be populated on a successful solve."""
        req = ProblemRequest(**{**_ROOT_REQ.__dict__, "method": "bisection"})
        res = ENGINE.solve(req)
        assert res.metrics.execution_time_seconds >= 0.0
        assert len(res.iterations) > 0
        assert isinstance(res.status, SolverStatus)

    def test_invalid_expression_through_engine(self):
        """Engine must propagate ParseError for a malicious expression."""
        req = ProblemRequest(
            method="bisection",
            expression="__import__('os')",
            a=1.0, b=2.0,
        )
        with pytest.raises(ParseError):
            ENGINE.solve(req)

    def test_singular_matrix_through_engine(self):
        """A singular matrix must yield SINGULAR_MATRIX status."""
        req = ProblemRequest(
            method="gauss_elimination",
            A=[[1.0, 2.0, 3.0],
               [2.0, 4.0, 6.0],   # row 2 = 2 * row 1
               [1.0, 1.0, 1.0]],
            b_vec=[6.0, 12.0, 3.0],
        )
        res = ENGINE.solve(req)
        assert res.status == SolverStatus.SINGULAR_MATRIX


class TestGUIAppWorkflow:
    """Verifies that the Tkinter application initializes, navigates, and handles UI events."""

    @pytest.fixture(autouse=True)
    def setup_app(self):
        # Initialize app with display
        try:
            self.app = NumerixApp()
            self.app.withdraw()  # do not show window during tests
            yield
        finally:
            if hasattr(self, "app") and self.app:
                try:
                    self.app.destroy()
                except Exception:
                    pass

    def test_app_initialization_and_dashboard(self):
        assert self.app.title() == "NUMERIX — Numerical Methods Simulator"
        assert self.app._active_page_name == "Dashboard"
        assert "Dashboard" in self.app._pages
        self.app.update_idletasks()

    def test_app_navigation_to_all_pages(self):
        pages = ["Root Finding", "Linear Systems", "Diff. Equations", "Comparison", "About", "Dashboard"]
        for p in pages:
            self.app.navigate(p)
            self.app.update_idletasks()
            assert self.app._active_page_name == p
            assert p in self.app._pages

    def test_root_finding_page_example_and_reset(self):
        self.app.navigate("Root Finding")
        page = self.app._pages["Root Finding"]
        assert isinstance(page, RootFindingPage)

        # Test example button fills variables
        page._on_load_example()
        assert page._expr_var.get() == "x**3 - x - 2"
        assert page._a_var.get() == "1.0"
        assert page._b_var.get() == "2.0"

        # Test method switch to Newton-Raphson
        page._method_var.set("Newton-Raphson")
        page._on_method_change()
        assert "Tangent" in page._formula_var.get()

        # Test reset
        page._on_reset()
        assert page._val_msg_var.get() == ""

    def test_linear_systems_page_dimension_and_reset(self):
        self.app.navigate("Linear Systems")
        page = self.app._pages["Linear Systems"]
        assert isinstance(page, LinearSystemsPage)

        # Dimension change
        page._n_var.set(4)
        page._on_dim_change()
        assert page._n_dim == 4
        assert len(page._cell_entries) == 4

        # Reset back to 3
        page._on_reset()
        assert page._n_dim == 3

    def test_differential_equations_page_load_and_reset(self):
        self.app.navigate("Diff. Equations")
        page = self.app._pages["Diff. Equations"]
        assert isinstance(page, DifferentialEquationsPage)

        page._on_load_example()
        assert page._expr_var.get() == "x + y"
        assert page._h_var.get() == "0.1"

        page._on_reset()
        assert page._val_msg_var.get() == ""

    def test_comparison_page_initialization(self):
        self.app.navigate("Comparison")
        page = self.app._pages["Comparison"]
        assert isinstance(page, ComparisonPage)
        self.app.update_idletasks()
