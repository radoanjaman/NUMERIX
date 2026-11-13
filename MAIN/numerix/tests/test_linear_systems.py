"""
Tests for linear system algorithms.

Reference system (3×3):
    2x + y + z  = 10
    3x + 2y + 3z = 18
    x + 4y + 9z = 16
Solution: x1=7, x2=-9, x3=5   (from the original lab scripts)
Wait — let's verify with numpy and use a simple well-conditioned system.
"""
import math
import pytest
import numpy as np

from numerix.algorithms.linear_systems.gauss_elimination import gauss_elimination
from numerix.algorithms.linear_systems.gauss_jordan import gauss_jordan
from numerix.core.result_models import SolverStatus


# ---------------------------------------------------------------------------
# Well-conditioned 3×3 system with known exact solution
# ---------------------------------------------------------------------------
# 2x + y + z  = 8   → x=1, y=2, z=3
# x + 3y + z  = 10
# x + y + 4z  = 15

A3 = [[2.0, 1.0, 1.0],
      [1.0, 3.0, 1.0],
      [1.0, 1.0, 4.0]]
b3 = [8.0, 10.0, 15.0]
x3_exact = np.linalg.solve(A3, b3).tolist()   # reference solution


def _close(a, b, atol=1e-8):
    return all(abs(ai - bi) < atol for ai, bi in zip(a, b))


# ---------------------------------------------------------------------------
# Gauss Elimination
# ---------------------------------------------------------------------------

class TestGaussElimination:
    def test_3x3_system(self):
        res = gauss_elimination(A3, b3)
        assert res.status == SolverStatus.SUCCESS
        assert res.solution_vector is not None
        assert _close(res.solution_vector, x3_exact)

    def test_residual_small(self):
        res = gauss_elimination(A3, b3)
        assert res.metrics.final_residual is not None
        assert res.metrics.final_residual < 1e-10

    def test_residual_vector_present(self):
        res = gauss_elimination(A3, b3)
        assert "residual_vector" in res.extra

    def test_history_populated(self):
        res = gauss_elimination(A3, b3)
        assert len(res.iterations) > 0

    def test_singular_matrix_detected(self):
        A_sing = [[1.0, 2.0, 3.0],
                  [2.0, 4.0, 6.0],
                  [1.0, 1.0, 1.0]]
        b_sing = [1.0, 2.0, 1.0]
        res = gauss_elimination(A_sing, b_sing)
        assert res.status == SolverStatus.SINGULAR_MATRIX

    def test_1x1_system(self):
        res = gauss_elimination([[3.0]], [9.0])
        assert abs(res.solution_vector[0] - 3.0) < 1e-10

    def test_invalid_matrix_raises(self):
        with pytest.raises(ValueError):
            gauss_elimination([[1.0, 2.0]], [1.0])  # 1×2 not square

    def test_dimension_mismatch_raises(self):
        with pytest.raises(ValueError):
            gauss_elimination([[1.0, 0.0], [0.0, 1.0]], [1.0])  # b too short

    def test_original_lab_system(self):
        # from the original gauselemination.py hardcoded example
        A = [[2.0, 1.0, 1.0],
             [3.0, 2.0, 3.0],
             [1.0, 4.0, 9.0]]
        b = [10.0, 18.0, 16.0]
        res = gauss_elimination(A, b)
        assert res.status == SolverStatus.SUCCESS
        x_ref = np.linalg.solve(A, b)
        assert _close(res.solution_vector, x_ref.tolist(), atol=1e-7)


# ---------------------------------------------------------------------------
# Gauss-Jordan
# ---------------------------------------------------------------------------

class TestGaussJordan:
    def test_3x3_system(self):
        res = gauss_jordan(A3, b3)
        assert res.status == SolverStatus.SUCCESS
        assert _close(res.solution_vector, x3_exact)

    def test_residual_small(self):
        res = gauss_jordan(A3, b3)
        assert res.metrics.final_residual < 1e-10

    def test_history_populated(self):
        res = gauss_jordan(A3, b3)
        assert len(res.iterations) > 0

    def test_singular_matrix_detected(self):
        A_sing = [[0.0, 0.0], [0.0, 0.0]]
        res = gauss_jordan(A_sing, [1.0, 1.0])
        assert res.status == SolverStatus.SINGULAR_MATRIX

    def test_matches_gauss_elimination(self):
        res_ge = gauss_elimination(A3, b3)
        res_gj = gauss_jordan(A3, b3)
        assert _close(res_ge.solution_vector, res_gj.solution_vector, atol=1e-8)

    def test_identity_matrix(self):
        A = [[1.0, 0.0], [0.0, 1.0]]
        b = [5.0, 7.0]
        res = gauss_jordan(A, b)
        assert _close(res.solution_vector, [5.0, 7.0])

    def test_original_lab_system(self):
        A = [[2.0, 1.0, 1.0],
             [3.0, 2.0, 3.0],
             [1.0, 4.0, 9.0]]
        b = [10.0, 18.0, 16.0]
        res = gauss_jordan(A, b)
        assert res.status == SolverStatus.SUCCESS
        x_ref = np.linalg.solve(A, b)
        assert _close(res.solution_vector, x_ref.tolist(), atol=1e-7)
