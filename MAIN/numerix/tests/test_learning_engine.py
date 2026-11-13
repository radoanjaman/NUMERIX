"""
Unit tests for NUMERIX Learning Engine, solution generators, and knowledge checks.
"""
from __future__ import annotations

import pytest

from numerix.core.result_models import SolverResult, SolverStatus, IterationRecord, SolverMetrics
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.learning.learning_engine import LearningEngine
from numerix.learning.solution_models import SolutionDocument, SolutionStep
from numerix.learning.knowledge_checks.question_generator import generate_questions_for_method
from numerix.learning.concept_registry import get_concept_info
from numerix.learning.formula_registry import get_formula_cards


@pytest.fixture
def solver():
    return SolverEngine()


@pytest.fixture
def learning():
    return LearningEngine()


class TestLearningEngineAllMethods:
    """Verify that all 8 numerical methods produce valid typed SolutionDocuments."""

    def test_bisection_lesson(self, solver, learning):
        req = ProblemRequest(method="bisection", expression="x**3 - x - 2", a=1.0, b=2.0, tol=1e-5)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "Bisection Method"
        assert doc.topic == "Root Finding"
        assert len(doc.learning_objectives) >= 3
        assert len(doc.prerequisites) >= 2
        assert len(doc.formulas) >= 2
        assert len(doc.steps) > 5
        assert len(doc.practice_questions) >= 2
        assert doc.final_interpretation.iterations_count == res.metrics.iterations

        # Verify numerical consistency with solver
        step_midpoints = [s.result_latex for s in doc.steps if s.result_latex and "c_" in s.result_latex]
        assert len(step_midpoints) == len(res.iterations)

        # Verify step types
        step_types = {s.step_type for s in doc.steps}
        assert "concept" in step_types
        assert "calculation" in step_types
        assert "convergence" in step_types

    def test_false_position_lesson(self, solver, learning):
        req = ProblemRequest(method="false_position", expression="x**3 - x - 2", a=1.0, b=2.0, tol=1e-5)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "False Position"
        assert len(doc.steps) > 5
        assert doc.steps[0].step_type == "concept"
        assert "secant" in doc.steps[0].explanation.lower()
        assert len(doc.practice_questions) >= 2

    def test_newton_raphson_lesson(self, solver, learning):
        req = ProblemRequest(method="newton_raphson", expression="x**3 - x - 2", x0=1.5, tol=1e-5)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "Newton-Raphson"
        assert len(doc.steps) >= 3
        # Check symbolic derivative step
        assert "3*x**2 - 1" in doc.steps[0].calculation_latex or "3 x^{2} - 1" in doc.steps[0].calculation_latex
        assert len(doc.practice_questions) >= 2

    def test_gauss_elimination_lesson(self, solver, learning):
        A = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
        b = [8.0, -11.0, -3.0]
        req = ProblemRequest(method="gauss_elimination", A=A, b_vec=b)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "Gauss Elimination"
        assert doc.topic == "Linear Systems"
        assert len(doc.steps) >= len(res.iterations) + 2
        # Verify matrix snapshots are captured
        matrix_steps = [s for s in doc.steps if s.matrix_snapshot is not None]
        assert len(matrix_steps) >= len(res.iterations)
        assert len(doc.practice_questions) >= 2

    def test_gauss_jordan_lesson(self, solver, learning):
        A = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
        b = [8.0, -11.0, -3.0]
        req = ProblemRequest(method="gauss_jordan", A=A, b_vec=b)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "Gauss-Jordan"
        assert len(doc.steps) >= len(res.iterations) + 1
        assert len(doc.practice_questions) >= 2

    def test_euler_lesson(self, solver, learning):
        req = ProblemRequest(method="euler", expression="x + y", ode_x0=0.0, ode_y0=1.0, ode_h=0.1, ode_x_end=0.4)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "Euler"
        assert doc.topic == "Differential Equations"
        assert len(doc.steps) == len(res.iterations) + 2
        assert len(doc.practice_questions) >= 2

    def test_modified_euler_lesson(self, solver, learning):
        req = ProblemRequest(method="modified_euler", expression="x + y", ode_x0=0.0, ode_y0=1.0, ode_h=0.1, ode_x_end=0.4)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "Modified Euler"
        assert len(doc.steps) == len(res.iterations) + 2
        assert len(doc.practice_questions) >= 2

    def test_rk4_lesson(self, solver, learning):
        req = ProblemRequest(method="rk4", expression="x + y", ode_x0=0.0, ode_y0=1.0, ode_h=0.1, ode_x_end=0.4)
        res = solver.solve(req)
        doc = learning.generate(req, res)

        assert isinstance(doc, SolutionDocument)
        assert doc.method == "RK4"
        assert len(doc.steps) == len(res.iterations) + 2
        # Check that k1, k2, k3, k4 are present in calculations
        rk4_steps = [s for s in doc.steps if s.step_type == "calculation"]
        assert len(rk4_steps) == len(res.iterations)
        for s in rk4_steps:
            assert "k_1" in s.calculation_latex
            assert "k_4" in s.calculation_latex
        assert len(doc.practice_questions) >= 2


class TestLearningEdgeCases:
    """Test robustness against singular matrices, zero derivatives, empty histories, and failures."""

    def test_zero_derivative_newton(self, solver, learning):
        # f(x) = x^2 + 1 has derivative 2x, which is 0 at x0=0
        req = ProblemRequest(method="newton_raphson", expression="x**2 + 1", x0=0.0, tol=1e-5)
        res = solver.solve(req)
        assert res.status == SolverStatus.ZERO_DERIVATIVE
        doc = learning.generate(req, res)
        assert isinstance(doc, SolutionDocument)
        assert doc.steps[0].step_type == "concept"

    def test_singular_matrix_gauss(self, solver, learning):
        A = [[1.0, 2.0], [2.0, 4.0]]  # linearly dependent rows
        b = [3.0, 6.0]
        req = ProblemRequest(method="gauss_elimination", A=A, b_vec=b)
        res = solver.solve(req)
        assert res.status == SolverStatus.SINGULAR_MATRIX
        doc = learning.generate(req, res)
        assert isinstance(doc, SolutionDocument)

    def test_empty_iterations(self, learning):
        req = ProblemRequest(method="bisection", expression="x", a=0.0, b=1.0)
        res = SolverResult(
            method="Bisection",
            problem_type="root_finding",
            status=SolverStatus.INVALID_BRACKET,
            termination_reason="Invalid bracket",
            iterations=[],
        )
        doc = learning.generate(req, res)
        assert isinstance(doc, SolutionDocument)
        assert len(doc.steps) >= 1

    def test_unknown_method_graceful(self, learning):
        req = ProblemRequest(method="unknown_algo", expression="x")
        res = SolverResult(
            method="unknown_algo",
            problem_type="root_finding",
            status=SolverStatus.INVALID_INPUT,
            termination_reason="Unknown method",
        )
        doc = learning.generate(req, res)
        assert isinstance(doc, SolutionDocument)
        assert len(doc.steps) >= 1
