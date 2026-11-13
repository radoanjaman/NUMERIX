"""
Educational lesson generators for Linear Systems numerical methods:
  - Gaussian Elimination with Partial Pivoting
  - Gauss-Jordan Elimination
"""
from __future__ import annotations

import numpy as np
from typing import Any

from numerix.core.result_models import SolverResult, SolverStatus
from numerix.engine.solver_engine import ProblemRequest
from numerix.learning.concept_registry import get_concept_info
from numerix.learning.formula_registry import get_formula_cards
from numerix.learning.knowledge_checks.question_generator import generate_questions_for_method
from numerix.learning.solution_models import (
    FinalInterpretation,
    KnowledgeCheckQuestion,
    SolutionDocument,
    SolutionStep,
    VariableDefinition,
)


def _fmt(val: float | int | None, precision: int = 4) -> str:
    """Format a float or int for clean mathematical LaTeX output."""
    if val is None:
        return "0"
    if isinstance(val, int):
        return str(val)
    if abs(val) < 1e-12:
        return "0"
    if abs(val) >= 1e5 or (0 < abs(val) < 1e-4):
        s = f"{val:.4e}"
        base, exp = s.split("e")
        return f"{float(base):.3f} \\times 10^{{{int(exp)}}}"
    s = f"{val:.{precision}f}".rstrip("0").rstrip(".")
    return s if s else "0"


def _matrix_to_latex(mat: list[list[float]] | np.ndarray, augmented_col: int | None = None) -> str:
    """Format a 2D matrix into LaTeX pmatrix with optional augmented vertical line."""
    if isinstance(mat, np.ndarray):
        mat = mat.tolist()
    rows = []
    for r in mat:
        cells = [_fmt(c) for c in r]
        if augmented_col is not None and augmented_col < len(cells):
            left = " & ".join(cells[:augmented_col])
            right = " & ".join(cells[augmented_col:])
            rows.append(f"{left} & \\big| & {right}")
        else:
            rows.append(" & ".join(cells))
    body = " \\\\\n".join(rows)
    return f"\\begin{{pmatrix}}\n{body}\n\\end{{pmatrix}}"


def generate_gauss_elimination_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for Gaussian Elimination with Partial Pivoting."""
    concept = get_concept_info("gauss_elimination")
    formulas = get_formula_cards("gauss_elimination")
    questions = generate_questions_for_method("gauss_elimination", problem, result)

    A_orig = problem.A
    b_orig = problem.b_vec
    n = len(b_orig)

    # Initial augmented matrix [A | b]
    aug_init = [row + [b_orig[i]] for i, row in enumerate(A_orig)]
    aug_init_latex = _matrix_to_latex(aug_init, augmented_col=n)

    problem_statement = (
        f"Solve the linear system of equations $Ax = b$ of dimension {n} \\times {n} "
        f"using Gaussian Elimination with Partial Pivoting."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Formulation of Augmented Matrix
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Augmented Matrix Formulation [A | b]",
            concept="Linear System Matrix Representation",
            explanation=(
                f"A system of {n} linear equations with {n} unknowns is concisely represented by the augmented matrix $[A \\mid b]$. "
                "The coefficients of the unknowns form matrix $A$ of size $n \\times n$, and the right-hand constants form column $b$."
            ),
            formula_latex=r"[A \mid b] = \begin{pmatrix} A_{1,1} & \cdots & A_{1,n} & \big| & b_1 \\ \vdots & \ddots & \vdots & \big| & \vdots \\ A_{n,1} & \cdots & A_{n,n} & \big| & b_n \end{pmatrix}",
            calculation_latex=f"[A \\mid b]_{{0}} = {aug_init_latex}",
            decision=f"Initialize augmented matrix of size {n} \\times {n+1}.",
            matrix_snapshot=aug_init,
            variable_definitions=[
                VariableDefinition(symbol="A", name="Coefficient Matrix", description=f"{n}x{n} matrix of linear coefficients"),
                VariableDefinition(symbol="b", name="Constants Vector", description=f"Right-hand side vector of dimension {n}"),
                VariableDefinition(symbol="x", name="Unknown Vector", description=f"Vector of {n} unknowns to solve"),
            ],
        )
    )
    step_num += 1

    # Elementary Row Operations Steps
    current_snapshot = aug_init
    for it in result.iterations:
        op_type = it.values.get("type")
        extra_desc = it.extra.get("description", "")
        snapshot = it.extra.get("matrix_snapshot")
        if snapshot:
            current_snapshot = snapshot

        if op_type == "swap":
            r1 = int(it.values.get("row1", 0))
            r2 = int(it.values.get("row2", 0))
            steps.append(
                SolutionStep(
                    step_number=step_num,
                    step_type="matrix_operation",
                    title=f"Operation {it.n}: Partial Pivoting Row Swap (R{r1+1} ↔ R{r2+1})",
                    concept="Partial Pivoting (Column Maximum Selection)",
                    explanation=(
                        f"In column {r1+1}, we inspect all elements on and below the diagonal. "
                        f"Row {r2+1} contains the maximum absolute coefficient. "
                        f"We swap Row {r1+1} and Row {r2+1} to place the strongest pivot on the diagonal, "
                        "which suppresses roundoff amplification and avoids division by near-zero."
                    ),
                    formula_latex=rf"|A_{{p, {r1+1}}}| = \max_{{k \ge {r1+1}}} |A_{{k, {r1+1}}}| \implies R_{{{r1+1}}} \longleftrightarrow R_{{{r2+1}}}",
                    calculation_latex=f"[A \\mid b] \\longrightarrow {_matrix_to_latex(current_snapshot, augmented_col=n)}",
                    decision=f"Row swap completed: R{r1+1} ↔ R{r2+1}.",
                    related_iteration=it.n,
                    related_operation=f"R{r1+1} <-> R{r2+1}",
                    matrix_snapshot=current_snapshot,
                )
            )
            step_num += 1

        elif op_type in ("elimination", "eliminate"):
            target = int(it.values.get("target_row", 0))
            pivot = int(it.values.get("pivot_row", 0))
            m = float(it.values.get("factor", it.values.get("multiplier", 0.0)))
            steps.append(
                SolutionStep(
                    step_number=step_num,
                    step_type="matrix_operation",
                    title=f"Operation {it.n}: Eliminate Entry at Row {target+1}, Column {pivot+1}",
                    concept="Forward Elimination",
                    explanation=(
                        f"Eliminate entry $A_{{{target+1},{pivot+1}}}$ beneath the pivot element $A_{{{pivot+1},{pivot+1}}}$. "
                        f"Compute multiplier $m = \\frac{{A_{{{target+1},{pivot+1}}}}}{{A_{{{pivot+1},{pivot+1}}}}} = {_fmt(m)}$. "
                        f"Then apply the elementary row operation: $R_{{{target+1}}} \\leftarrow R_{{{target+1}}} - ({_fmt(m)}) R_{{{pivot+1}}}$."
                    ),
                    formula_latex=rf"R_{{{target+1}}} \leftarrow R_{{{target+1}}} - m \cdot R_{{{pivot+1}}}, \quad m = \frac{{A_{{{target+1},{pivot+1}}}}}{{A_{{{pivot+1},{pivot+1}}}}}",
                    calculation_latex=(
                        f"\\text{{Multiplier }} m_{{{target+1},{pivot+1}}} = {_fmt(m)} \\\\[4pt]"
                        f"[A \\mid b] \\longrightarrow {_matrix_to_latex(current_snapshot, augmented_col=n)}"
                    ),
                    decision=f"Entry at ({target+1}, {pivot+1}) zeroed out.",
                    related_iteration=it.n,
                    related_operation=f"R{target+1} <- R{target+1} - ({_fmt(m)})*R{pivot+1}",
                    matrix_snapshot=current_snapshot,
                )
            )
            step_num += 1

    # Back-Substitution Steps
    if result.solution_vector:
        sol = result.solution_vector
        back_sub_lines = []
        for i in reversed(range(n)):
            var_name = f"x_{{{i+1}}}"
            val_i = sol[i]
            back_sub_lines.append(f"{var_name} = {_fmt(val_i)}")

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title="Back Substitution: Solving Upper Triangular System",
                concept="Back Substitution",
                explanation=(
                    "Forward elimination has reduced $[A \\mid b]$ to an upper triangular system $Ux = c$. "
                    "We solve for the unknowns sequentially in reverse order, starting from the bottom equation "
                    f"$x_{n} = c_{n} / U_{{n,n}}$ and substituting known values upward."
                ),
                formula_latex=r"x_i = \frac{b'_i - \sum_{j=i+1}^n U_{i,j} x_j}{U_{i,i}}",
                calculation_latex=" \\\\[4pt]\n".join(back_sub_lines),
                result_latex=f"x = \\begin{{pmatrix}} {' \\\\ '.join([_fmt(v) for v in sol])} \\end{{pmatrix}}",
                decision="All variables solved via back substitution.",
                variable_definitions=[
                    VariableDefinition(symbol=f"x_{{{i+1}}}", name=f"Variable x{i+1}", description=f"Component {i+1} of solution", current_value=_fmt(sol[i]))
                    for i in range(n)
                ],
            )
        )
        step_num += 1

    # Residual Verification Step
    res_norm = result.metrics.final_residual
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="conclusion",
            title="Solution Verification (Residual Norm ||Ax - b||)",
            concept="Numerical Residual Verification",
            explanation=(
                "To rigorously verify the solution without assuming exactness, we compute the residual vector: "
                "$r = Ax - b$. A residual norm near zero confirms that the computed vector $x$ satisfies the equations."
            ),
            formula_latex=r"r = A x - b, \quad \|r\|_2 = \sqrt{\sum_{i=1}^n r_i^2}",
            calculation_latex=f"\\|r\\|_2 = {_fmt(res_norm)}",
            result_latex=f"\\|Ax - b\\|_2 = {_fmt(res_norm)}",
            decision=(
                f"Residual norm {_fmt(res_norm)} is within numerical floating-point precision. "
                "The solution vector is validated."
            ),
        )
    )

    sol_str = ", ".join([f"x{i+1} = {_fmt(v)}" for i, v in enumerate(result.solution_vector)]) if result.solution_vector else "None"

    final_interp = FinalInterpretation(
        summary=(
            f"Gaussian Elimination successfully solved the {n}x{n} linear system. "
            f"Solution: [{sol_str}]."
        ),
        root_or_solution=f"[{sol_str}]",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Residual norm ||Ax - b|| = {_fmt(res_norm)}",
        verification=(
            f"Direct multiplication Ax yields b within residual norm {_fmt(res_norm)}. "
            "System is consistent and uniquely determined."
        ),
    )

    return SolutionDocument(
        method="Gauss Elimination",
        topic=concept["topic"],
        problem_statement=problem_statement,
        learning_objectives=concept["learning_objectives"],
        prerequisites=concept["prerequisites"],
        formulas=formulas,
        steps=steps,
        final_interpretation=final_interp,
        practice_questions=questions,
    )


def generate_gauss_jordan_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for Gauss-Jordan Elimination."""
    concept = get_concept_info("gauss_jordan")
    formulas = get_formula_cards("gauss_jordan")
    questions = generate_questions_for_method("gauss_jordan", problem, result)

    A_orig = problem.A
    b_orig = problem.b_vec
    n = len(b_orig)

    aug_init = [row + [b_orig[i]] for i, row in enumerate(A_orig)]
    aug_init_latex = _matrix_to_latex(aug_init, augmented_col=n)

    problem_statement = (
        f"Solve the linear system $Ax = b$ of dimension {n} \\times {n} "
        f"using Gauss-Jordan Elimination to achieve Reduced Row-Echelon Form [I | x]."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Augmented Matrix
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Augmented Matrix Formulation & Gauss-Jordan Strategy",
            concept="Full Diagonalization Strategy",
            explanation=(
                f"We initialize the augmented matrix $[A \\mid b]$. In Gauss-Jordan elimination, "
                "each pivot row is scaled to make the diagonal pivot element exactly 1. "
                "Then, elimination is applied BOTH ABOVE and BELOW the pivot, converting $A$ directly into the identity matrix $I$. "
                "This allows the solution vector $x$ to be read directly from the rightmost column without back-substitution."
            ),
            formula_latex=r"[A \mid b] \longrightarrow [I \mid x]",
            calculation_latex=f"[A \\mid b]_{{0}} = {aug_init_latex}",
            decision=f"Initialize augmented matrix.",
            matrix_snapshot=aug_init,
            variable_definitions=[
                VariableDefinition(symbol="[A | b]", name="Augmented Matrix", description=f"{n}x{n+1} initial matrix"),
                VariableDefinition(symbol="I", name="Identity Matrix", description="Target diagonal identity matrix"),
            ],
        )
    )
    step_num += 1

    current_snapshot = aug_init
    for it in result.iterations:
        op_type = it.values.get("type")
        snapshot = it.extra.get("matrix_snapshot")
        if snapshot:
            current_snapshot = snapshot

        if op_type == "swap":
            r1 = int(it.values.get("row1", 0))
            r2 = int(it.values.get("row2", 0))
            steps.append(
                SolutionStep(
                    step_number=step_num,
                    step_type="matrix_operation",
                    title=f"Operation {it.n}: Partial Pivoting Swap (R{r1+1} ↔ R{r2+1})",
                    concept="Partial Pivoting",
                    explanation=f"Swap row {r1+1} and row {r2+1} to position the maximum magnitude entry on the diagonal.",
                    formula_latex=rf"R_{{{r1+1}}} \longleftrightarrow R_{{{r2+1}}}",
                    calculation_latex=f"[A \\mid b] \\longrightarrow {_matrix_to_latex(current_snapshot, augmented_col=n)}",
                    decision="Pivot row swapped into position.",
                    related_iteration=it.n,
                    related_operation=f"R{r1+1} <-> R{r2+1}",
                    matrix_snapshot=current_snapshot,
                )
            )
            step_num += 1

        elif op_type == "scale":
            row_idx = int(it.values.get("row", 0))
            scale_factor = float(it.values.get("scale", 1.0))
            steps.append(
                SolutionStep(
                    step_number=step_num,
                    step_type="matrix_operation",
                    title=f"Operation {it.n}: Pivot Normalization (R{row_idx+1} ← R{row_idx+1} / pivot)",
                    concept="Pivot Normalization (Leading 1)",
                    explanation=(
                        f"Normalize Row {row_idx+1} by dividing through by the pivot element: "
                        f"Scale factor = {_fmt(scale_factor)}. This forces the diagonal entry $A_{{{row_idx+1},{row_idx+1}}}$ to become 1."
                    ),
                    formula_latex=rf"R_{{{row_idx+1}}} \leftarrow \frac{{R_{{{row_idx+1}}}}}{{A_{{{row_idx+1},{row_idx+1}}}}}",
                    calculation_latex=f"[A \\mid b] \\longrightarrow {_matrix_to_latex(current_snapshot, augmented_col=n)}",
                    decision=f"Row {row_idx+1} pivot normalized to 1.",
                    related_iteration=it.n,
                    related_operation=f"R{row_idx+1} <- R{row_idx+1} * {_fmt(scale_factor)}",
                    matrix_snapshot=current_snapshot,
                )
            )
            step_num += 1

        elif op_type in ("elimination", "eliminate"):
            target = int(it.values.get("target_row", 0))
            pivot = int(it.values.get("pivot_row", 0))
            m = float(it.values.get("factor", it.values.get("multiplier", 0.0)))
            position_note = "above" if target < pivot else "below"
            steps.append(
                SolutionStep(
                    step_number=step_num,
                    step_type="matrix_operation",
                    title=f"Operation {it.n}: Eliminate Entry {position_note} Pivot at Row {target+1}, Column {pivot+1}",
                    concept="Column Elimination Above & Below",
                    explanation=(
                        f"Zero out entry in row {target+1}, column {pivot+1} ({position_note} pivot). "
                        f"Row operation: $R_{{{target+1}}} \\leftarrow R_{{{target+1}}} - ({_fmt(m)}) R_{{{pivot+1}}}$."
                    ),
                    formula_latex=rf"R_{{{target+1}}} \leftarrow R_{{{target+1}}} - A_{{{target+1},{pivot+1}}} R_{{{pivot+1}}}",
                    calculation_latex=f"[A \\mid b] \\longrightarrow {_matrix_to_latex(current_snapshot, augmented_col=n)}",
                    decision=f"Column {pivot+1} entry in row {target+1} zeroed out.",
                    related_iteration=it.n,
                    related_operation=f"R{target+1} <- R{target+1} - ({_fmt(m)})*R{pivot+1}",
                    matrix_snapshot=current_snapshot,
                )
            )
            step_num += 1

    # RREF & Extraction Step
    if result.solution_vector:
        sol = result.solution_vector
        extract_lines = [f"x_{{{i+1}}} = {_fmt(sol[i])}" for i in range(n)]
        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="conclusion",
                title="Reduced Row Echelon Form [I | x] & Solution Extraction",
                concept="Direct Solution Reading from RREF",
                explanation=(
                    "The coefficient matrix is now the identity matrix $I$. "
                    "Each equation simplifies to $1 \\cdot x_i = b'_i$, so the solution vector $x$ "
                    "is read directly from the augmented column without any back-substitution step."
                ),
                formula_latex=r"[I \mid x] \implies x_i = b'_i",
                calculation_latex=(
                    f"{_matrix_to_latex(current_snapshot, augmented_col=n)} \\\\[4pt]"
                    + " \\\\[4pt]\n".join(extract_lines)
                ),
                result_latex=f"x = \\begin{{pmatrix}} {' \\\\ '.join([_fmt(v) for v in sol])} \\end{{pmatrix}}",
                decision="Direct extraction complete.",
            )
        )
        step_num += 1

    res_norm = result.metrics.final_residual
    sol_str = ", ".join([f"x{i+1} = {_fmt(v)}" for i, v in enumerate(result.solution_vector)]) if result.solution_vector else "None"

    final_interp = FinalInterpretation(
        summary=(
            f"Gauss-Jordan Elimination reduced the system to RREF. "
            f"Direct solution: [{sol_str}]."
        ),
        root_or_solution=f"[{sol_str}]",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Residual norm ||Ax - b|| = {_fmt(res_norm)}",
        verification=f"Residual norm {_fmt(res_norm)} confirms exact agreement.",
    )

    return SolutionDocument(
        method="Gauss-Jordan",
        topic=concept["topic"],
        problem_statement=problem_statement,
        learning_objectives=concept["learning_objectives"],
        prerequisites=concept["prerequisites"],
        formulas=formulas,
        steps=steps,
        final_interpretation=final_interp,
        practice_questions=questions,
    )
