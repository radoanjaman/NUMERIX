"""
Tests for the SolverEngine and ComparisonEngine.
"""
import pytest

from numerix.engine.solver_engine import (
    SolverEngine,
    ComparisonEngine,
    ProblemRequest,
)
from numerix.core.result_models import SolverStatus


engine = SolverEngine()
compare = ComparisonEngine()

ROOT_REQ = ProblemRequest(
    method="bisection",
    expression="x**3 - x - 2",
    a=1.0,
    b=2.0,
)

ODE_REQ = ProblemRequest(
    method="euler",
    expression="x + y",
    ode_x0=0.0,
    ode_y0=1.0,
    ode_h=0.1,
    ode_x_end=0.5,
)

LINEAR_REQ = ProblemRequest(
    method="gauss_elimination",
    A=[[2.0, 1.0, 1.0], [1.0, 3.0, 1.0], [1.0, 1.0, 4.0]],
    b_vec=[8.0, 10.0, 15.0],
)


class TestSolverEngine:
    def test_bisection_via_engine(self):
        res = engine.solve(ROOT_REQ)
        assert res.status == SolverStatus.CONVERGED
        assert abs(res.root - 1.5214) < 1e-3

    def test_false_position_via_engine(self):
        req = ProblemRequest(method="false_position", expression="x**3 - x - 2", a=1.0, b=2.0)
        res = engine.solve(req)
        assert res.status == SolverStatus.CONVERGED

    def test_newton_raphson_via_engine(self):
        req = ProblemRequest(method="newton_raphson", expression="x**3 - x - 2", x0=1.5)
        res = engine.solve(req)
        assert res.status == SolverStatus.CONVERGED

    def test_gauss_elimination_via_engine(self):
        res = engine.solve(LINEAR_REQ)
        assert res.status == SolverStatus.SUCCESS
        assert res.solution_vector is not None

    def test_gauss_jordan_via_engine(self):
        req = ProblemRequest(
            method="gauss_jordan",
            A=[[2.0, 1.0], [1.0, 3.0]],
            b_vec=[5.0, 10.0],
        )
        res = engine.solve(req)
        assert res.status == SolverStatus.SUCCESS

    def test_euler_via_engine(self):
        res = engine.solve(ODE_REQ)
        assert res.status == SolverStatus.SUCCESS

    def test_modified_euler_via_engine(self):
        req = ProblemRequest(method="modified_euler", expression="x + y",
                             ode_x0=0.0, ode_y0=1.0, ode_h=0.1, ode_x_end=0.5)
        res = engine.solve(req)
        assert res.status == SolverStatus.SUCCESS

    def test_rk4_via_engine(self):
        req = ProblemRequest(method="rk4", expression="x + y",
                             ode_x0=0.0, ode_y0=1.0, ode_h=0.1, ode_x_end=0.5)
        res = engine.solve(req)
        assert res.status == SolverStatus.SUCCESS

    def test_unknown_method_raises(self):
        req = ProblemRequest(method="secant")
        with pytest.raises(ValueError, match="Unknown method"):
            engine.solve(req)

    def test_missing_expression_raises(self):
        req = ProblemRequest(method="bisection", a=1.0, b=2.0)
        with pytest.raises(ValueError):
            engine.solve(req)

    def test_missing_bracket_raises(self):
        req = ProblemRequest(method="bisection", expression="x**2 - 2")
        with pytest.raises(ValueError):
            engine.solve(req)

    def test_invalid_expression_raises(self):
        req = ProblemRequest(method="bisection", expression="x + z", a=0.0, b=2.0)
        with pytest.raises(Exception):
            engine.solve(req)


class TestComparisonEngine:
    def test_compare_root_finding(self):
        req = ProblemRequest(expression="x**3 - x - 2", a=1.0, b=2.0, x0=1.5)
        results = compare.compare(["bisection", "false_position"], req)
        assert "bisection" in results
        assert "false_position" in results
        assert results["bisection"].status == SolverStatus.CONVERGED

    def test_compare_ode(self):
        req = ProblemRequest(expression="x + y", ode_x0=0.0, ode_y0=1.0,
                             ode_h=0.1, ode_x_end=0.5)
        results = compare.compare(["euler", "rk4"], req)
        assert len(results) == 2

    def test_incompatible_methods_raises(self):
        req = ProblemRequest(expression="x**2 - 1", a=0.0, b=2.0)
        with pytest.raises(ValueError, match="compatible"):
            compare.compare(["bisection", "euler"], req)
