"""
NUMERIX Learning Engine — single entry point to transform numerical solver output
into an interactive academic learning document.
"""
from __future__ import annotations

import logging
from typing import Callable

from numerix.core.result_models import SolverResult, SolverStatus
from numerix.engine.solver_engine import ProblemRequest
from numerix.learning.solution_models import (
    FinalInterpretation,
    SolutionDocument,
    SolutionStep,
)
from numerix.learning.concept_registry import get_concept_info
from numerix.learning.formula_registry import get_formula_cards
from numerix.learning.knowledge_checks.question_generator import generate_questions_for_method
from numerix.learning.solution_generators.root_finding import (
    generate_bisection_lesson,
    generate_false_position_lesson,
    generate_newton_raphson_lesson,
)
from numerix.learning.solution_generators.linear_systems import (
    generate_gauss_elimination_lesson,
    generate_gauss_jordan_lesson,
)
from numerix.learning.solution_generators.ode import (
    generate_euler_lesson,
    generate_modified_euler_lesson,
    generate_rk4_lesson,
)

logger = logging.getLogger("numerix.learning_engine")


class LearningEngine:
    """
    Learning subsystem engine that turns numerical solver execution histories
    into complete structured educational solutions.
    """

    _GENERATORS: dict[str, Callable[[ProblemRequest, SolverResult], SolutionDocument]] = {
        "bisection": generate_bisection_lesson,
        "false_position": generate_false_position_lesson,
        "newton_raphson": generate_newton_raphson_lesson,
        "gauss_elimination": generate_gauss_elimination_lesson,
        "gauss_jordan": generate_gauss_jordan_lesson,
        "euler": generate_euler_lesson,
        "modified_euler": generate_modified_euler_lesson,
        "rk4": generate_rk4_lesson,
    }

    @classmethod
    def normalize_method_id(cls, method_name: str) -> str:
        """Normalize method names to canonical registry keys."""
        norm = method_name.lower().strip().replace("-", "_").replace(" ", "_")
        # Handle variations like "rk_4", "newton", "gauss"
        if norm in ("newton", "newtonraphson"):
            return "newton_raphson"
        if norm in ("falseposition", "regula_falsi"):
            return "false_position"
        if norm in ("rk_4", "runge_kutta", "runge_kutta_4"):
            return "rk4"
        if norm in ("gauss", "gaussian_elimination"):
            return "gauss_elimination"
        if norm in ("gaussjordan", "gauss_gordan"):
            return "gauss_jordan"
        if norm in ("modifiedeuler", "heun"):
            return "modified_euler"
        return norm

    def generate(self, problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
        """
        Generate a typed SolutionDocument from the original problem request and solver result.

        Parameters
        ----------
        problem : ProblemRequest
            The parameters passed to the solver.
        result  : SolverResult
            The actual execution result, iteration records, and metrics from the engine.

        Returns
        -------
        SolutionDocument
            A structured interactive textbook lesson populated with the actual numerical values.
        """
        method_key = self.normalize_method_id(problem.method or result.method)

        generator = self._GENERATORS.get(method_key)
        if generator is None:
            # Fallback for unexpected or missing generator
            return self._generate_generic_fallback(method_key, problem, result)

        try:
            doc = generator(problem, result)
            return doc
        except Exception as exc:
            logger.warning(f"Error in {method_key} lesson generator: {exc}", exc_info=True)
            return self._generate_generic_fallback(method_key, problem, result, error=str(exc))

    def _generate_generic_fallback(
        self,
        method_key: str,
        problem: ProblemRequest,
        result: SolverResult,
        error: str | None = None,
    ) -> SolutionDocument:
        """Graceful fallback if a generator encounters an unhandled edge case or invalid input."""
        concept = get_concept_info(method_key)
        formulas = get_formula_cards(method_key)
        questions = generate_questions_for_method(method_key, problem, result)

        steps: list[SolutionStep] = [
            SolutionStep(
                step_number=1,
                step_type="concept",
                title=f"Mathematical Concept: {concept.get('method_name', method_key)}",
                concept=concept.get("topic"),
                explanation=concept.get("concept_summary", ""),
            )
        ]

        if error:
            steps.append(
                SolutionStep(
                    step_number=2,
                    step_type="conclusion",
                    title="Educational Processing Notice",
                    explanation=f"A specialized educational derivation could not be completed: {error}",
                    decision=f"Status: {result.status.value}. Reason: {result.termination_reason}",
                )
            )

        final_interp = FinalInterpretation(
            summary=f"Analysis of {method_key} execution. Status: {result.status.value}.",
            root_or_solution=str(result.root if result.root is not None else result.solution_vector),
            iterations_count=result.metrics.iterations,
            stopping_reason=result.termination_reason,
            accuracy_achieved=f"Iterations: {result.metrics.iterations}",
            verification="Check solver iteration records and termination status.",
        )

        return SolutionDocument(
            method=concept.get("method_name", method_key),
            topic=concept.get("topic", "Numerical Methods"),
            problem_statement=f"Problem input for {method_key}: {problem.expression}",
            learning_objectives=concept.get("learning_objectives", []),
            prerequisites=concept.get("prerequisites", []),
            formulas=formulas,
            steps=steps,
            final_interpretation=final_interp,
            practice_questions=questions,
        )
