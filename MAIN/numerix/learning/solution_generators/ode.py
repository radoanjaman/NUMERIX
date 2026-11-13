"""
Educational lesson generators for Ordinary Differential Equations (ODEs):
  - Euler's Method
  - Modified Euler (Heun's Predictor-Corrector)
  - 4th-Order Runge-Kutta (RK4)
"""
from __future__ import annotations

import sympy
from typing import Any

from numerix.core.expression_parser import parse_function_xy
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


def _fmt(val: float | int | None, precision: int = 5) -> str:
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


def generate_euler_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for Euler's Method."""
    concept = get_concept_info("euler")
    formulas = get_formula_cards("euler")
    questions = generate_questions_for_method("euler", problem, result)

    expr_str = problem.expression.strip()
    try:
        expr_sym, _ = parse_function_xy(expr_str)
        expr_latex = sympy.latex(expr_sym)
    except Exception:
        expr_latex = expr_str

    x0 = problem.ode_x0 if problem.ode_x0 is not None else 0.0
    y0 = problem.ode_y0 if problem.ode_y0 is not None else 1.0
    h = problem.ode_h if problem.ode_h is not None else 0.1
    x_end = problem.ode_x_end if problem.ode_x_end is not None else 1.0

    problem_statement = (
        f"Solve the initial value problem (IVP) $\\frac{{dy}}{{dx}} = f(x, y) = {expr_latex}$ "
        f"with initial condition $y({_fmt(x0)}) = {_fmt(y0)}$ on the interval $[{_fmt(x0)}, {_fmt(x_end)}]$ "
        f"using Euler's method with step size $h = {_fmt(h)}$."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Initial Value Problem & First-Order Stepping Concept
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Initial Value Problem (IVP) & Tangent Line Stepping",
            concept="Forward Euler Stepping & Local Truncation Error",
            explanation=(
                f"Euler's method is the fundamental explicit single-step method for ODEs. "
                "Given the state $(x_n, y_n)$, it evaluates the instantaneous slope $f(x_n, y_n) = dy/dx$ "
                "and advances along the tangent line across step size $h$. "
                "The local truncation error is $\\mathcal{O}(h^2)$, resulting in an accumulated global error of $\\mathcal{O}(h)$."
            ),
            formula_latex=r"y_{n+1} = y_n + h \cdot f(x_n, y_n), \quad x_{n+1} = x_n + h",
            calculation_latex=(
                f"\\text{{Initial state: }} (x_0, y_0) = ({_fmt(x0)}, {_fmt(y0)}) \\\\[4pt]"
                f"\\text{{Step size: }} h = {_fmt(h)}, \\quad x_{{\\text{{target}}}} = {_fmt(x_end)}"
            ),
            decision="Begin stepwise integration from initial condition.",
            variable_definitions=[
                VariableDefinition(symbol="x_0", name="Initial x", description="Starting value of independent variable", current_value=_fmt(x0)),
                VariableDefinition(symbol="y_0", name="Initial y", description="Known state y(x_0)", current_value=_fmt(y0)),
                VariableDefinition(symbol="h", name="Step Size", description="Mesh spacing increment", current_value=_fmt(h)),
            ],
        )
    )
    step_num += 1

    # Integration Steps
    for it in result.iterations:
        n = it.n
        xn = float(it.values.get("x", 0.0))
        yn = float(it.values.get("y", 0.0))
        slope = float(it.values.get("slope", 0.0))
        ynext = float(it.values.get("y_next", 0.0))
        xnext = float(it.values.get("x_next", xn + h))
        increment = h * slope

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title=f"Step {n+1}: Advance from x = {_fmt(xn)} to x = {_fmt(xnext)}",
                concept="Euler Forward Integration Step",
                explanation=(
                    f"Evaluate slope $f({_fmt(xn)}, {_fmt(yn)}) = {_fmt(slope)}$. "
                    f"Multiply by step size $h = {_fmt(h)}$ to obtain displacement $\\Delta y = {_fmt(increment)}$. "
                    f"Add to current state $y_{{{n}}}$ to calculate $y_{{{n+1}}}$."
                ),
                formula_latex=r"y_{n+1} = y_n + h \cdot f(x_n, y_n)",
                substitution_latex=f"y_{{{n+1}}} = {_fmt(yn)} + ({_fmt(h)}) \\cdot ({_fmt(slope)})",
                calculation_latex=(
                    f"f(x_{{{n}}}, y_{{{n}}}) = f({_fmt(xn)}, {_fmt(yn)}) = {_fmt(slope)} \\\\[4pt]"
                    f"\\Delta y = h \\cdot f(x_{{{n}}}, y_{{{n}}}) = ({_fmt(h)}) \\cdot ({_fmt(slope)}) = {_fmt(increment)} \\\\[4pt]"
                    f"y_{{{n+1}}} = {_fmt(yn)} + {_fmt(increment)} = {_fmt(ynext)} \\\\[4pt]"
                    f"x_{{{n+1}}} = {_fmt(xn)} + {_fmt(h)} = {_fmt(xnext)}"
                ),
                result_latex=f"y({_fmt(xnext)}) \\approx {_fmt(ynext)}",
                decision=f"Next state computed: y({_fmt(xnext)}) = {_fmt(ynext)}.",
                related_iteration=n,
                variable_definitions=[
                    VariableDefinition(symbol=f"x_{{{n}}}", name="Current x", description="Abscissa at start of step", current_value=_fmt(xn)),
                    VariableDefinition(symbol=f"y_{{{n}}}", name="Current y", description="Ordinate at start of step", current_value=_fmt(yn)),
                    VariableDefinition(symbol=f"f(x_{{{n}}}, y_{{{n}}})", name="Slope", description="Derivative at current point", current_value=_fmt(slope)),
                    VariableDefinition(symbol=f"y_{{{n+1}}}", name="Next y", description="Integrated state at x_{n+1}", current_value=_fmt(ynext)),
                ],
                substeps=[
                    f"1. Evaluate dy/dx at ({_fmt(xn)}, {_fmt(yn)}) = {_fmt(slope)}",
                    f"2. Compute increment Δy = h · slope = {_fmt(increment)}",
                    f"3. Advance y: {_fmt(yn)} + {_fmt(increment)} = {_fmt(ynext)}",
                    f"4. Advance x: {_fmt(xn)} + {_fmt(h)} = {_fmt(xnext)}",
                ],
            )
        )
        step_num += 1

    final_row = result.ode_table[-1] if result.ode_table else {}
    final_x = final_row.get("x", x_end)
    final_y = final_row.get("y", 0.0)

    # Conclusion Step
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="conclusion",
            title=f"Integration Complete at x = {_fmt(final_x)}",
            concept="Euler Trajectory Summary",
            explanation=(
                f"Euler's method completed {len(result.iterations)} integration steps from $x_0 = {_fmt(x0)}$ to $x = {_fmt(final_x)}$. "
                f"Final numerical solution: $y({_fmt(final_x)}) \\approx {_fmt(final_y)}$."
            ),
            formula_latex=r"y(x_{\text{end}}) \approx y_N",
            calculation_latex=f"y({_fmt(final_x)}) \\approx {_fmt(final_y)}",
            result_latex=f"y({_fmt(final_x)}) \\approx {_fmt(final_y)}",
            decision="Target endpoint reached.",
        )
    )

    final_interp = FinalInterpretation(
        summary=(
            f"Euler's method solved dy/dx = {expr_str} over [{_fmt(x0)}, {_fmt(x_end)}] "
            f"in {result.metrics.iterations} steps with h = {_fmt(h)}."
        ),
        root_or_solution=f"y({_fmt(final_x)}) ≈ {_fmt(final_y)}",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Global error order O(h) = O({_fmt(h)})",
        verification=(
            f"Final state y({_fmt(final_x)}) = {_fmt(final_y)}. "
            "To improve accuracy, a smaller step size h or higher-order scheme (Modified Euler / RK4) can be employed."
        ),
    )

    # Extract worked step for Step 1
    worked_step = next((s for s in steps if s.related_iteration == 1 and s.step_type == "calculation"), None)
    if not worked_step and len(steps) > 1:
        worked_step = steps[1]

    what_changes_next = (
        "The newly calculated values become the starting point for the next step. "
        "The Euler forward step repeats across the interval until reaching $x_{\\text{end}}$."
    )
    rem_summary = (
        f"Subsequent integration steps advance from $x_1$ to $x = {_fmt(final_x)}$, "
        f"reaching the final state $y \\approx {_fmt(final_y)}$."
    )

    return SolutionDocument(
        method="Euler",
        topic=concept["topic"],
        problem_statement=problem_statement,
        one_sentence_purpose="Advances along the tangent slope $f(x_n, y_n)$ across step size $h$ to approximate the trajectory of an Initial Value Problem.",
        essential_formula=formulas[0] if formulas else None,
        worked_step=worked_step,
        what_changes_next=what_changes_next,
        remaining_iterations_summary=rem_summary,
        learning_objectives=concept["learning_objectives"],
        prerequisites=concept["prerequisites"],
        formulas=formulas,
        steps=steps,
        final_interpretation=final_interp,
        practice_questions=questions,
    )


def generate_modified_euler_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for Modified Euler (Heun's Predictor-Corrector)."""
    concept = get_concept_info("modified_euler")
    formulas = get_formula_cards("modified_euler")
    questions = generate_questions_for_method("modified_euler", problem, result)

    expr_str = problem.expression.strip()
    try:
        expr_sym, _ = parse_function_xy(expr_str)
        expr_latex = sympy.latex(expr_sym)
    except Exception:
        expr_latex = expr_str

    x0 = problem.ode_x0 if problem.ode_x0 is not None else 0.0
    y0 = problem.ode_y0 if problem.ode_y0 is not None else 1.0
    h = problem.ode_h if problem.ode_h is not None else 0.1
    x_end = problem.ode_x_end if problem.ode_x_end is not None else 1.0

    problem_statement = (
        f"Solve the initial value problem $\\frac{{dy}}{{dx}} = {expr_latex}$ "
        f"with $y({_fmt(x0)}) = {_fmt(y0)}$ on $[{_fmt(x0)}, {_fmt(x_end)}]$ "
        f"using the Modified Euler (Heun's) method with step size $h = {_fmt(h)}$."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Predictor-Corrector Foundation
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Predictor-Corrector Concept & Average Slope (Heun's Method)",
            concept="Two-Stage Predictor-Corrector & Trapezoidal Integration",
            explanation=(
                "Standard Euler assumes the slope is constant throughout the interval. "
                "Modified Euler (Heun's method) resolves this limitation in two stages: "
                "1. **Predictor:** Takes an initial Euler trial step to predict $y^*_{n+1}$. "
                "2. **Corrector:** Evaluates slope at the predicted point $f(x_{n+1}, y^*_{n+1})$, "
                "and uses the average of the initial and predicted slopes to compute the corrected state $y_{n+1}$. "
                "This achieves second-order global accuracy $\\mathcal{O}(h^2)$."
            ),
            formula_latex=(
                r"\text{Predictor: } y^*_{n+1} = y_n + h \cdot f(x_n, y_n) \\\\[4pt]"
                r"\text{Corrector: } y_{n+1} = y_n + \frac{h}{2} \left[ f(x_n, y_n) + f(x_{n+1}, y^*_{n+1}) \right]"
            ),
            calculation_latex=f"(x_0, y_0) = ({_fmt(x0)}, {_fmt(y0)}), \\quad h = {_fmt(h)}",
            decision="Initialize two-stage integration scheme.",
            variable_definitions=[
                VariableDefinition(symbol="f_1", name="Initial Slope", description="Slope at beginning of interval"),
                VariableDefinition(symbol="y^*_{n+1}", name="Predictor Value", description="Trial value from standard Euler step"),
                VariableDefinition(symbol="f_2", name="Corrector Slope", description="Slope at predicted state"),
                VariableDefinition(symbol="y_{n+1}", name="Corrected Value", description="Final second-order estimate"),
            ],
        )
    )
    step_num += 1

    # Integration Steps
    for it in result.iterations:
        n = it.n
        xn = float(it.values.get("x", 0.0))
        yn = float(it.values.get("y", 0.0))
        f1 = float(it.values.get("f1_slope", 0.0))
        ypred = float(it.values.get("y_predictor", 0.0))
        xnext = float(it.values.get("x_next", xn + h))
        f2 = float(it.values.get("f2_slope", 0.0))
        ycorr = float(it.values.get("y_corrector", 0.0))
        avg_slope = 0.5 * (f1 + f2)

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title=f"Step {n+1}: Predictor-Corrector Cycle over [{_fmt(xn)}, {_fmt(xnext)}]",
                concept="Predictor Step followed by Corrector Slope Averaging",
                explanation=(
                    f"First compute predictor slope $f_1 = {_fmt(f1)}$ to predict $y^*_{{{n+1}}} = {_fmt(ypred)}$. "
                    f"Then evaluate corrector slope $f_2 = f({_fmt(xnext)}, {_fmt(ypred)}) = {_fmt(f2)}$. "
                    f"Finally, average the two slopes $\\bar{{f}} = {_fmt(avg_slope)}$ to calculate the corrected $y_{{{n+1}}}$."
                ),
                formula_latex=(
                    r"y^*_{n+1} = y_n + h \cdot f_1 \\\\[4pt]"
                    r"y_{n+1} = y_n + \frac{h}{2}(f_1 + f_2)"
                ),
                substitution_latex=(
                    f"y^*_{{{n+1}}} = {_fmt(yn)} + ({_fmt(h)})({_fmt(f1)}) = {_fmt(ypred)} \\\\[4pt]"
                    f"y_{{{n+1}}} = {_fmt(yn)} + \\frac{{{_fmt(h)}}}{{2}} ({_fmt(f1)} + {_fmt(f2)})"
                ),
                calculation_latex=(
                    f"\\text{{Initial slope: }} f_1 = f({_fmt(xn)}, {_fmt(yn)}) = {_fmt(f1)} \\\\[4pt]"
                    f"\\text{{Predictor: }} y^*_{{{n+1}}} = {_fmt(ypred)} \\\\[4pt]"
                    f"\\text{{Corrector slope: }} f_2 = f({_fmt(xnext)}, {_fmt(ypred)}) = {_fmt(f2)} \\\\[4pt]"
                    f"\\text{{Average slope: }} \\bar{{f}} = \\frac{{{_fmt(f1)} + {_fmt(f2)}}}{{2}} = {_fmt(avg_slope)} \\\\[4pt]"
                    f"\\text{{Corrected value: }} y_{{{n+1}}} = {_fmt(yn)} + ({_fmt(h)})({_fmt(avg_slope)}) = {_fmt(ycorr)}"
                ),
                result_latex=f"y({_fmt(xnext)}) \\approx {_fmt(ycorr)}",
                decision=f"Prediction refined with corrector slope: y({_fmt(xnext)}) = {_fmt(ycorr)}.",
                related_iteration=n,
                variable_definitions=[
                    VariableDefinition(symbol="f_1", name="Slope at (x_n, y_n)", description="Initial slope", current_value=_fmt(f1)),
                    VariableDefinition(symbol="y^*", name="Predictor y", description="Uncorrected trial value", current_value=_fmt(ypred)),
                    VariableDefinition(symbol="f_2", name="Slope at (x_{n+1}, y^*)", description="Corrector slope", current_value=_fmt(f2)),
                    VariableDefinition(symbol=r"\bar{f}", name="Average Slope", description="Mean slope across interval", current_value=_fmt(avg_slope)),
                    VariableDefinition(symbol="y_{n+1}", name="Corrected y", description="Final state", current_value=_fmt(ycorr)),
                ],
                substeps=[
                    f"1. Slope f1 = {_fmt(f1)}",
                    f"2. Predictor y* = {_fmt(ypred)}",
                    f"3. Slope f2 = {_fmt(f2)}",
                    f"4. Mean slope = {_fmt(avg_slope)}",
                    f"5. Corrected y = {_fmt(ycorr)}",
                ],
            )
        )
        step_num += 1

    final_row = result.ode_table[-1] if result.ode_table else {}
    final_x = final_row.get("x", x_end)
    final_y = final_row.get("y", 0.0)

    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="conclusion",
            title=f"Integration Complete at x = {_fmt(final_x)}",
            concept="Modified Euler Trajectory Summary",
            explanation=(
                f"Completed {len(result.iterations)} predictor-corrector cycles. "
                f"Final state: $y({_fmt(final_x)}) \\approx {_fmt(final_y)}$."
            ),
            formula_latex=r"y(x_{\text{end}}) \approx y_N",
            calculation_latex=f"y({_fmt(final_x)}) \\approx {_fmt(final_y)}",
            result_latex=f"y({_fmt(final_x)}) \\approx {_fmt(final_y)}",
            decision="Endpoint reached with second-order accuracy.",
        )
    )

    final_interp = FinalInterpretation(
        summary=(
            f"Modified Euler solved dy/dx = {expr_str} over [{_fmt(x0)}, {_fmt(x_end)}] "
            f"with h = {_fmt(h)} across {result.metrics.iterations} steps."
        ),
        root_or_solution=f"y({_fmt(final_x)}) ≈ {_fmt(final_y)}",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Second-order global accuracy O(h²) = O({_fmt(h**2)})",
        verification=(
            f"Final state y({_fmt(final_x)}) = {_fmt(final_y)}. "
            "Predictor-corrector averaging substantially suppresses truncation error compared to first-order Euler."
        ),
    )

    # Extract worked step for Step 1
    worked_step = next((s for s in steps if s.related_iteration == 1 and s.step_type == "calculation"), None)
    if not worked_step and len(steps) > 1:
        worked_step = steps[1]

    what_changes_next = (
        "The prediction and correction process repeats using the latest $x$ and $y$ values "
        "to advance along the curve with second-order accuracy."
    )
    rem_summary = (
        f"Subsequent predictor-corrector cycles advance the state to $x = {_fmt(final_x)}$, "
        f"reaching $y \\approx {_fmt(final_y)}$."
    )

    return SolutionDocument(
        method="Modified Euler",
        topic=concept["topic"],
        problem_statement=problem_statement,
        one_sentence_purpose="Uses a predictor-corrector strategy that averages slopes at the beginning and predicted end of each step for second-order $\\mathcal{O}(h^2)$ accuracy.",
        essential_formula=formulas[0] if formulas else None,
        worked_step=worked_step,
        what_changes_next=what_changes_next,
        remaining_iterations_summary=rem_summary,
        learning_objectives=concept["learning_objectives"],
        prerequisites=concept["prerequisites"],
        formulas=formulas,
        steps=steps,
        final_interpretation=final_interp,
        practice_questions=questions,
    )


def generate_rk4_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for 4th-Order Runge-Kutta (RK4)."""
    concept = get_concept_info("rk4")
    formulas = get_formula_cards("rk4")
    questions = generate_questions_for_method("rk4", problem, result)

    expr_str = problem.expression.strip()
    try:
        expr_sym, _ = parse_function_xy(expr_str)
        expr_latex = sympy.latex(expr_sym)
    except Exception:
        expr_latex = expr_str

    x0 = problem.ode_x0 if problem.ode_x0 is not None else 0.0
    y0 = problem.ode_y0 if problem.ode_y0 is not None else 1.0
    h = problem.ode_h if problem.ode_h is not None else 0.1
    x_end = problem.ode_x_end if problem.ode_x_end is not None else 1.0

    problem_statement = (
        f"Solve the initial value problem $\\frac{{dy}}{{dx}} = {expr_latex}$ "
        f"with $y({_fmt(x0)}) = {_fmt(y0)}$ on $[{_fmt(x0)}, {_fmt(x_end)}]$ "
        f"using the Fourth-Order Runge-Kutta (RK4) method with step size $h = {_fmt(h)}$."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Classical RK4 Foundation & Simpson's Rule Analogy
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="4th-Order Runge-Kutta Scheme & Four-Stage Slope Sampling",
            concept="Simpson's Quadrature Analogy & Fourth-Order Accuracy",
            explanation=(
                "The classical Runge-Kutta 4th-order method (RK4) samples four strategically chosen slope increments per step: "
                "1. $k_1$: Slope at the beginning of the step. "
                "2. $k_2$: Slope at the midpoint, projected using $k_1/2$. "
                "3. $k_3$: Refined midpoint slope, projected using $k_2/2$. "
                "4. $k_4$: Slope at the full endpoint, projected using $k_3$. "
                "These four slopes are combined in a weighted average with weights 1:2:2:1 (mirroring Simpson's 1/3 rule), "
                "yielding a fourth-order global error of $\\mathcal{O}(h^4)$."
            ),
            formula_latex=(
                r"y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4) \\\\[4pt]"
                r"k_1 = h \cdot f(x_n, y_n), \quad k_2 = h \cdot f\left(x_n + \frac{h}{2}, y_n + \frac{k_1}{2}\right) \\\\[4pt]"
                r"k_3 = h \cdot f\left(x_n + \frac{h}{2}, y_n + \frac{k_2}{2}\right), \quad k_4 = h \cdot f(x_n + h, y_n + k_3)"
            ),
            calculation_latex=f"(x_0, y_0) = ({_fmt(x0)}, {_fmt(y0)}), \\quad h = {_fmt(h)}",
            decision="Initialize 4th-order multi-stage integration scheme.",
            variable_definitions=[
                VariableDefinition(symbol="k_1", name="Initial Slope Increment", description="h · f(x_n, y_n)"),
                VariableDefinition(symbol="k_2", name="Midpoint Slope 1", description="h · f(x_n + h/2, y_n + k_1/2)"),
                VariableDefinition(symbol="k_3", name="Midpoint Slope 2", description="h · f(x_n + h/2, y_n + k_2/2)"),
                VariableDefinition(symbol="k_4", name="Endpoint Slope", description="h · f(x_n + h, y_n + k_3)"),
                VariableDefinition(symbol=r"\Delta y", name="Weighted Increment", description="1/6 · (k_1 + 2k_2 + 2k_3 + k_4)"),
            ],
        )
    )
    step_num += 1

    # Integration Steps
    for it in result.iterations:
        n = it.n
        xn = float(it.values.get("x", 0.0))
        yn = float(it.values.get("y", 0.0))
        k1 = float(it.values.get("k1", 0.0))
        k2 = float(it.values.get("k2", 0.0))
        k3 = float(it.values.get("k3", 0.0))
        k4 = float(it.values.get("k4", 0.0))
        ynext = float(it.values.get("y_next", 0.0))
        xnext = float(it.values.get("x_next", xn + h))
        dy = (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title=f"Step {n+1}: Four-Stage RK4 Evaluation over [{_fmt(xn)}, {_fmt(xnext)}]",
                concept="RK4 Four Slope Increments & Weighted Combination",
                explanation=(
                    f"Evaluate all four slope increments across $[{_fmt(xn)}, {_fmt(xnext)}]$. "
                    f"Then apply the Simpson weighting $\\Delta y = \\frac{{1}}{{6}}(k_1 + 2k_2 + 2k_3 + k_4)$."
                ),
                formula_latex=r"y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)",
                substitution_latex=(
                    f"\\Delta y = \\frac{{1}}{{6}} \\left[ ({_fmt(k1)}) + 2({_fmt(k2)}) + 2({_fmt(k3)}) + ({_fmt(k4)}) \\right] \\\\[4pt]"
                    f"y_{{{n+1}}} = {_fmt(yn)} + \\Delta y"
                ),
                calculation_latex=(
                    f"k_1 = ({_fmt(h)}) \\cdot f({_fmt(xn)}, {_fmt(yn)}) = {_fmt(k1)} \\\\[4pt]"
                    f"k_2 = ({_fmt(h)}) \\cdot f({_fmt(xn + h/2)}, {_fmt(yn + k1/2)}) = {_fmt(k2)} \\\\[4pt]"
                    f"k_3 = ({_fmt(h)}) \\cdot f({_fmt(xn + h/2)}, {_fmt(yn + k2/2)}) = {_fmt(k3)} \\\\[4pt]"
                    f"k_4 = ({_fmt(h)}) \\cdot f({_fmt(xnext)}, {_fmt(yn + k3)}) = {_fmt(k4)} \\\\[4pt]"
                    f"\\Delta y = {_fmt(dy)} \\\\[4pt]"
                    f"y_{{{n+1}}} = {_fmt(yn)} + {_fmt(dy)} = {_fmt(ynext)}"
                ),
                result_latex=f"y({_fmt(xnext)}) \\approx {_fmt(ynext)}",
                decision=f"RK4 step completed: y({_fmt(xnext)}) = {_fmt(ynext)}.",
                related_iteration=n,
                variable_definitions=[
                    VariableDefinition(symbol="k_1", name="Slope 1", description="Initial slope", current_value=_fmt(k1)),
                    VariableDefinition(symbol="k_2", name="Slope 2", description="Trial midpoint 1", current_value=_fmt(k2)),
                    VariableDefinition(symbol="k_3", name="Slope 3", description="Trial midpoint 2", current_value=_fmt(k3)),
                    VariableDefinition(symbol="k_4", name="Slope 4", description="Trial endpoint", current_value=_fmt(k4)),
                    VariableDefinition(symbol=r"\Delta y", name="Increment", description="Weighted Simpson average", current_value=_fmt(dy)),
                ],
                substeps=[
                    f"1. k1 = {_fmt(k1)}",
                    f"2. k2 = {_fmt(k2)}",
                    f"3. k3 = {_fmt(k3)}",
                    f"4. k4 = {_fmt(k4)}",
                    f"5. Δy = (k1 + 2k2 + 2k3 + k4)/6 = {_fmt(dy)}",
                    f"6. Next state: y = {_fmt(ynext)}",
                ],
            )
        )
        step_num += 1

    final_row = result.ode_table[-1] if result.ode_table else {}
    final_x = final_row.get("x", x_end)
    final_y = final_row.get("y", 0.0)

    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="conclusion",
            title=f"Integration Complete at x = {_fmt(final_x)}",
            concept="RK4 High-Accuracy Trajectory Summary",
            explanation=(
                f"RK4 successfully integrated the differential equation across {len(result.iterations)} steps. "
                f"Final state: $y({_fmt(final_x)}) \\approx {_fmt(final_y)}$."
            ),
            formula_latex=r"y(x_{\text{end}}) \approx y_N",
            calculation_latex=f"y({_fmt(final_x)}) \\approx {_fmt(final_y)}",
            result_latex=f"y({_fmt(final_x)}) \\approx {_fmt(final_y)}",
            decision="High-order integration concluded.",
        )
    )

    final_interp = FinalInterpretation(
        summary=(
            f"RK4 solved dy/dx = {expr_str} over [{_fmt(x0)}, {_fmt(x_end)}] "
            f"with h = {_fmt(h)} across {result.metrics.iterations} steps."
        ),
        root_or_solution=f"y({_fmt(final_x)}) ≈ {_fmt(final_y)}",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Fourth-order global accuracy O(h⁴) = O({_fmt(h**4)})",
        verification=(
            f"Final state y({_fmt(final_x)}) = {_fmt(final_y)}. "
            "RK4 provides industrial-grade accuracy with minimal step-accumulation drift."
        ),
    )

    # Extract worked step for Step 1
    worked_step = next((s for s in steps if s.related_iteration == 1 and s.step_type == "calculation"), None)
    if not worked_step and len(steps) > 1:
        worked_step = steps[1]

    what_changes_next = (
        "RK4 combines four slope estimates across each interval to calculate a fourth-order accurate next value. "
        "The same four-slope procedure is repeated at each subsequent step."
    )
    rem_summary = (
        f"Subsequent RK4 steps advance across the domain with fourth-order precision to final state "
        f"$y({_fmt(final_x)}) \\approx {_fmt(final_y)}$."
    )

    return SolutionDocument(
        method="RK4",
        topic=concept["topic"],
        problem_statement=problem_statement,
        one_sentence_purpose="Computes four exploratory slopes across each subinterval to produce a fourth-order $\\mathcal{O}(h^4)$ weighted average step.",
        essential_formula=formulas[0] if formulas else None,
        worked_step=worked_step,
        what_changes_next=what_changes_next,
        remaining_iterations_summary=rem_summary,
        learning_objectives=concept["learning_objectives"],
        prerequisites=concept["prerequisites"],
        formulas=formulas,
        steps=steps,
        final_interpretation=final_interp,
        practice_questions=questions,
    )
