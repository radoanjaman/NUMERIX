"""
Typed Pydantic models for NUMERIX Learning Engine solutions.
"""
from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


StepType = Literal[
    "concept",
    "formula",
    "substitution",
    "calculation",
    "evaluation",
    "decision",
    "matrix_operation",
    "convergence",
    "interpretation",
    "conclusion",
    "knowledge_check",
]


class KnowledgeCheckQuestion(BaseModel):
    """Interactive diagnostic multiple choice question."""
    id: str
    question: str
    options: list[str]
    correct_index: int
    explanation: str
    question_type: str = "conceptual"  # conceptual, calculation, prediction, interval, formula, matrix_op
    hint: str | None = None


class VariableDefinition(BaseModel):
    """Definition of a variable or parameter used in calculations."""
    symbol: str
    name: str
    description: str
    current_value: str | None = None


class FormulaCardModel(BaseModel):
    """Mathematical governing formula card."""
    name: str
    latex: str
    description: str
    variables: list[VariableDefinition] = Field(default_factory=list)


class SolutionStep(BaseModel):
    """An individual educational step in the worked numerical solution."""
    step_number: int
    step_type: StepType
    title: str
    concept: str | None = None
    explanation: str = ""
    formula_latex: str | None = None
    substitution_latex: str | None = None
    calculation_latex: str | None = None
    result_latex: str | None = None
    decision: str | None = None
    related_iteration: int | None = None
    related_operation: str | None = None
    related_plot_data: dict[str, Any] | None = None
    checkpoint_question: KnowledgeCheckQuestion | None = None
    variable_definitions: list[VariableDefinition] = Field(default_factory=list)
    matrix_snapshot: list[list[float]] | None = None
    substeps: list[str] = Field(default_factory=list)


class FinalInterpretation(BaseModel):
    """Summary and academic interpretation of the final result."""
    summary: str
    root_or_solution: str
    iterations_count: int
    stopping_reason: str
    accuracy_achieved: str
    verification: str


class SolutionDocument(BaseModel):
    """
    Complete structured educational lesson produced by the Learning Engine.
    Represents an interactive textbook chapter integrated with the solver.
    """
    method: str
    topic: str
    problem_statement: str
    learning_objectives: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    formulas: list[FormulaCardModel] = Field(default_factory=list)
    steps: list[SolutionStep] = Field(default_factory=list)
    final_interpretation: FinalInterpretation
    practice_questions: list[KnowledgeCheckQuestion] = Field(default_factory=list)
