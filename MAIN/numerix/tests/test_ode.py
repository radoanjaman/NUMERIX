"""
Tests for ODE algorithms.

Reference problem: dy/dx = x + y,  y(0) = 1
Exact solution:    y(x) = 2*exp(x) - x - 1

We verify that all three methods reach approximately correct values,
and that RK4 is significantly more accurate than Euler at the same step size.
"""
import math
import pytest

from numerix.algorithms.ode.euler import euler
from numerix.algorithms.ode.modified_euler import modified_euler
from numerix.algorithms.ode.rk4 import rk4
from numerix.core.result_models import SolverStatus
from numerix.core.validators import validate_ode_params


def f(x, y):
    return x + y

def exact(x):
    return 2 * math.exp(x) - x - 1

X_END = 0.5
H = 0.1
X0, Y0 = 0.0, 1.0


# ---------------------------------------------------------------------------
# Euler
# ---------------------------------------------------------------------------

class TestEuler:
    def test_runs_to_completion(self):
        res = euler(f, X0, Y0, H, X_END)
        assert res.status == SolverStatus.SUCCESS
        assert res.ode_table is not None

    def test_correct_step_count(self):
        res = euler(f, X0, Y0, H, X_END)
        # 5 steps for [0, 0.5] with h=0.1 → 6 rows (step 0 … 5)
        assert len(res.ode_table) == 6

    def test_initial_point_preserved(self):
        res = euler(f, X0, Y0, H, X_END)
        row0 = res.ode_table[0]
        assert abs(row0["x"] - X0) < 1e-14
        assert abs(row0["y"] - Y0) < 1e-14

    def test_history_slope_present(self):
        res = euler(f, X0, Y0, H, X_END)
        rec = res.iterations[0]
        assert "slope" in rec.values
        assert "y_next" in rec.values

    def test_approximate_correctness(self):
        res = euler(f, X0, Y0, H, X_END)
        y_final = res.ode_table[-1]["y"]
        y_exact = exact(X_END)
        # Euler has O(h) error; allow 5 % relative
        assert abs(y_final - y_exact) / y_exact < 0.05

    def test_invalid_step_direction_raises(self):
        with pytest.raises(ValueError):
            euler(f, 0.0, 1.0, -0.1, 0.5)

    def test_zero_step_raises(self):
        with pytest.raises(ValueError):
            euler(f, 0.0, 1.0, 0.0, 0.5)


# ---------------------------------------------------------------------------
# Modified Euler (Heun)
# ---------------------------------------------------------------------------

class TestModifiedEuler:
    def test_runs_to_completion(self):
        res = modified_euler(f, X0, Y0, H, X_END)
        assert res.status == SolverStatus.SUCCESS

    def test_correct_step_count(self):
        res = modified_euler(f, X0, Y0, H, X_END)
        assert len(res.ode_table) == 6

    def test_history_predictor_corrector_present(self):
        res = modified_euler(f, X0, Y0, H, X_END)
        rec = res.iterations[0]
        assert "y_predictor" in rec.values
        assert "y_corrector" in rec.values
        assert "f1_slope" in rec.values
        assert "f2_slope" in rec.values

    def test_more_accurate_than_euler(self):
        res_e = euler(f, X0, Y0, H, X_END)
        res_me = modified_euler(f, X0, Y0, H, X_END)
        y_exact = exact(X_END)
        err_e = abs(res_e.ode_table[-1]["y"] - y_exact)
        err_me = abs(res_me.ode_table[-1]["y"] - y_exact)
        assert err_me < err_e, "Modified Euler should be more accurate than Euler"

    def test_approximate_correctness(self):
        res = modified_euler(f, X0, Y0, H, X_END)
        y_final = res.ode_table[-1]["y"]
        y_exact = exact(X_END)
        assert abs(y_final - y_exact) / y_exact < 0.01


# ---------------------------------------------------------------------------
# RK4
# ---------------------------------------------------------------------------

class TestRK4:
    def test_runs_to_completion(self):
        res = rk4(f, X0, Y0, H, X_END)
        assert res.status == SolverStatus.SUCCESS

    def test_correct_step_count(self):
        res = rk4(f, X0, Y0, H, X_END)
        assert len(res.ode_table) == 6

    def test_history_k_values_present(self):
        res = rk4(f, X0, Y0, H, X_END)
        rec = res.iterations[0]
        for k in ("k1", "k2", "k3", "k4"):
            assert k in rec.values, f"Missing {k} in RK4 iteration record"

    def test_highly_accurate(self):
        res = rk4(f, X0, Y0, H, X_END)
        y_final = res.ode_table[-1]["y"]
        y_exact = exact(X_END)
        # RK4 O(h^4) — expect < 0.01% error at h=0.1
        assert abs(y_final - y_exact) / y_exact < 0.0001

    def test_more_accurate_than_modified_euler(self):
        res_me = modified_euler(f, X0, Y0, H, X_END)
        res_rk = rk4(f, X0, Y0, H, X_END)
        y_exact = exact(X_END)
        err_me = abs(res_me.ode_table[-1]["y"] - y_exact)
        err_rk = abs(res_rk.ode_table[-1]["y"] - y_exact)
        assert err_rk < err_me, "RK4 should be more accurate than Modified Euler"

    def test_initial_point_preserved(self):
        res = rk4(f, X0, Y0, H, X_END)
        assert abs(res.ode_table[0]["y"] - Y0) < 1e-14

    def test_simple_dy_dx_equals_x(self):
        # dy/dx = x, y(0) = 0  → exact: y = x^2 / 2
        res = rk4(lambda x, y: x, 0.0, 0.0, 0.1, 1.0)
        y_final = res.ode_table[-1]["y"]
        assert abs(y_final - 0.5) < 1e-8
