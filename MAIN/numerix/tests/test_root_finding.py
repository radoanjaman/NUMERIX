"""
Tests for root-finding algorithms.

Known root used throughout: f(x) = x**3 - x - 2  →  root ≈ 1.52138
"""
import math
import pytest

from numerix.algorithms.root_finding.bisection import bisection
from numerix.algorithms.root_finding.false_position import false_position
from numerix.algorithms.root_finding.newton_raphson import newton_raphson
from numerix.core.result_models import SolverStatus


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

def f(x):
    return x**3 - x - 2

def df(x):
    return 3 * x**2 - 1

KNOWN_ROOT = 1.5213797068045676
TOL = 1e-6


# ---------------------------------------------------------------------------
# Bisection
# ---------------------------------------------------------------------------

class TestBisection:
    def test_converges_to_known_root(self):
        res = bisection(f, 1.0, 2.0, tol=TOL)
        assert res.status == SolverStatus.CONVERGED
        assert res.root is not None
        assert abs(res.root - KNOWN_ROOT) < 1e-5

    def test_history_populated(self):
        res = bisection(f, 1.0, 2.0, tol=TOL)
        assert len(res.iterations) > 0

    def test_iteration_fields_present(self):
        res = bisection(f, 1.0, 2.0, tol=1e-3)
        rec = res.iterations[0]
        assert "a" in rec.values
        assert "b" in rec.values
        assert "mid" in rec.values
        assert "f_mid" in rec.values
        assert rec.approximate_error is not None

    def test_exact_root_terminates(self):
        # f(x) = x, root at 0
        res = bisection(lambda x: x, -1.0, 1.0, tol=TOL)
        assert res.root is not None
        assert abs(res.root) < TOL + 1e-10

    def test_invalid_bracket_raises(self):
        with pytest.raises(ValueError, match="same sign"):
            bisection(f, 3.0, 4.0)

    def test_invalid_bracket_order_raises(self):
        with pytest.raises(ValueError, match="a < b"):
            bisection(f, 2.0, 1.0)

    def test_negative_tolerance_raises(self):
        with pytest.raises(ValueError):
            bisection(f, 1.0, 2.0, tol=-1.0)

    def test_max_iterations_respected(self):
        res = bisection(f, 1.0, 2.0, tol=1e-30, max_iter=5)
        assert res.status == SolverStatus.MAX_ITERATIONS
        assert len(res.iterations) == 5

    def test_metrics_timing_positive(self):
        res = bisection(f, 1.0, 2.0)
        assert res.metrics.execution_time_seconds >= 0.0

    def test_simple_quadratic(self):
        # f(x) = x**2 - 4, root at 2
        res = bisection(lambda x: x**2 - 4, 1.0, 3.0, tol=1e-7)
        assert abs(res.root - 2.0) < 1e-6


# ---------------------------------------------------------------------------
# False Position
# ---------------------------------------------------------------------------

class TestFalsePosition:
    def test_converges_to_known_root(self):
        res = false_position(f, 1.0, 2.0, tol=TOL)
        assert res.status == SolverStatus.CONVERGED
        assert abs(res.root - KNOWN_ROOT) < 1e-5

    def test_history_populated(self):
        res = false_position(f, 1.0, 2.0, tol=TOL)
        assert len(res.iterations) > 0

    def test_iteration_fields_present(self):
        res = false_position(f, 1.0, 2.0, tol=1e-3)
        rec = res.iterations[0]
        assert "root" in rec.values
        assert "f_root" in rec.values

    def test_invalid_bracket_raises(self):
        with pytest.raises(ValueError, match="same sign"):
            false_position(f, 3.0, 4.0)

    def test_max_iterations(self):
        res = false_position(f, 1.0, 2.0, tol=1e-30, max_iter=5)
        assert res.status == SolverStatus.MAX_ITERATIONS

    def test_quadratic(self):
        res = false_position(lambda x: x**2 - 9, 2.0, 4.0, tol=1e-7)
        assert abs(res.root - 3.0) < 1e-5


# ---------------------------------------------------------------------------
# Newton-Raphson
# ---------------------------------------------------------------------------

class TestNewtonRaphson:
    def test_converges_to_known_root(self):
        res = newton_raphson(f, df, x0=1.5, tol=TOL)
        assert res.status == SolverStatus.CONVERGED
        assert abs(res.root - KNOWN_ROOT) < 1e-8

    def test_history_fields(self):
        res = newton_raphson(f, df, x0=1.5, tol=1e-3)
        rec = res.iterations[0]
        assert "x_n" in rec.values
        assert "f_xn" in rec.values
        assert "df_xn" in rec.values
        assert "x_new" in rec.values

    def test_zero_derivative_detected(self):
        # f(x) = x**2, f'(0) = 0 — derivative zero at root
        res = newton_raphson(lambda x: x**2, lambda x: 2 * x, x0=0.0)
        assert res.status == SolverStatus.ZERO_DERIVATIVE

    def test_max_iterations(self):
        res = newton_raphson(f, df, x0=1.5, tol=1e-30, max_iter=3)
        assert res.status == SolverStatus.MAX_ITERATIONS
        assert len(res.iterations) == 3

    def test_fast_convergence(self):
        # Newton-Raphson should converge much faster than bisection
        res_nr = newton_raphson(f, df, x0=1.5, tol=1e-10)
        res_bi = bisection(f, 1.0, 2.0, tol=1e-10)
        assert res_nr.metrics.iterations < res_bi.metrics.iterations

    def test_quadratic(self):
        res = newton_raphson(lambda x: x**2 - 2, lambda x: 2*x, x0=1.5, tol=1e-9)
        assert abs(res.root - math.sqrt(2)) < 1e-8
