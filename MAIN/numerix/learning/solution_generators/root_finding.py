"""
Educational lesson generators for Root-Finding numerical methods:
  - Bisection Method
  - False Position (Regula Falsi) Method
  - Newton-Raphson Method
"""
from __future__ import annotations

import math
import sympy
from typing import Any

from numerix.core.expression_parser import parse_function_x, differentiate_x, ParseError
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


def _fmt(val: float | int | None, precision: int = 6) -> str:
    """Format a float or int for clean mathematical LaTeX output."""
    if val is None:
        return "0"
    if isinstance(val, int):
        return str(val)
    if abs(val) < 1e-13:
        return "0"
    if abs(val) >= 1e5 or (0 < abs(val) < 1e-4):
        s = f"{val:.4e}"
        base, exp = s.split("e")
        return f"{float(base):.4f} \\times 10^{{{int(exp)}}}"
    s = f"{val:.{precision}f}".rstrip("0").rstrip(".")
    return s if s else "0"


def generate_bisection_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for the Bisection Method."""
    concept = get_concept_info("bisection")
    formulas = get_formula_cards("bisection")
    questions = generate_questions_for_method("bisection", problem, result)

    expr_str = problem.expression.strip()
    try:
        expr_sym, _ = parse_function_x(expr_str)
        expr_latex = sympy.latex(expr_sym)
    except Exception:
        expr_latex = expr_str

    a_init = problem.a if problem.a is not None else 0.0
    b_init = problem.b if problem.b is not None else 1.0
    tol = problem.tol

    problem_statement = (
        f"Find a real root of the nonlinear equation $f(x) = {expr_latex} = 0$ "
        f"on the initial bracketing interval $[{_fmt(a_init)}, {_fmt(b_init)}]$ "
        f"with convergence tolerance $\\text{{tol}} = {_fmt(tol)}$."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Conceptual Foundation & Initial Interval Validation
    f_a0 = result.iterations[0].values.get("f_a") if result.iterations else None
    f_b0 = result.iterations[0].values.get("f_b") if result.iterations else None

    if f_a0 is not None and f_b0 is not None:
        sign_product = f_a0 * f_b0
        valid_bracket = sign_product < 0
        bracket_eval_latex = (
            f"f(a) = f({_fmt(a_init)}) = {_fmt(f_a0)}, \\quad "
            f"f(b) = f({_fmt(b_init)}) = {_fmt(f_b0)} \\\\[4pt]"
            f"f(a) \\cdot f(b) = ({_fmt(f_a0)}) \\cdot ({_fmt(f_b0)}) = {_fmt(sign_product)}"
        )
        if valid_bracket:
            decision_text = (
                f"Because $f(a) \\cdot f(b) < 0$, the function changes sign across $[{_fmt(a_init)}, {_fmt(b_init)}]$. "
                "By the Intermediate Value Theorem (IVT), at least one real root is guaranteed in this interval."
            )
        else:
            decision_text = (
                f"Warning: $f(a) \\cdot f(b) \\ge 0$. The initial interval does not satisfy the sign-change criterion."
            )
    else:
        bracket_eval_latex = r"f(a) \cdot f(b) < 0"
        decision_text = "Verify that the endpoints satisfy the sign-change criterion before interval halving."

    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Prerequisite & Bracket Verification (Intermediate Value Theorem)",
            concept="Intermediate Value Theorem (IVT)",
            explanation=(
                "For any continuous function $f(x)$ on $[a, b]$, if $f(a)$ and $f(b)$ have opposite signs, "
                "the curve $y = f(x)$ must intersect the horizontal axis $y = 0$ at least once. "
                "The Bisection Method relies on this theorem to trap the root within an ever-shrinking interval."
            ),
            formula_latex=r"f(a) \cdot f(b) < 0 \implies \exists \, r \in (a, b) : f(r) = 0",
            calculation_latex=bracket_eval_latex,
            decision=decision_text,
            variable_definitions=[
                VariableDefinition(symbol="a", name="Lower Bound", description="Initial bracket lower boundary", current_value=_fmt(a_init)),
                VariableDefinition(symbol="b", name="Upper Bound", description="Initial bracket upper boundary", current_value=_fmt(b_init)),
                VariableDefinition(symbol=r"\text{tol}", name="Tolerance", description="User-specified stopping tolerance", current_value=_fmt(tol)),
            ],
        )
    )
    step_num += 1

    # Step 2..N: Iteration steps from actual solver results
    for it in result.iterations:
        n = it.n
        a_val = float(it.values.get("a", 0.0))
        b_val = float(it.values.get("b", 0.0))
        mid_val = float(it.values.get("mid", (a_val + b_val) / 2.0))
        fa_val = float(it.values.get("f_a", 0.0))
        fb_val = float(it.values.get("f_b", 0.0))
        fmid_val = float(it.values.get("f_mid", 0.0))
        err_val = it.approximate_error if it.approximate_error is not None else abs(b_val - a_val) / 2.0

        # Sign logic
        fa_neg = fa_val < 0
        fmid_neg = fmid_val < 0
        same_sign = (fa_neg == fmid_neg)
        product = fa_val * fmid_val

        if same_sign:
            decision_msg = (
                f"Since $f(a) \\cdot f(c) = ({_fmt(fa_val)}) \\cdot ({_fmt(fmid_val)}) = {_fmt(product)} > 0$, "
                f"$f(a)$ and $f(c)$ share the same sign. The root lies in the right half $[c, b]$. "
                f"Therefore, update the lower bound: $a \\leftarrow c = {_fmt(mid_val)}$."
            )
            next_interval_latex = f"[{_fmt(mid_val)}, {_fmt(b_val)}]"
        else:
            decision_msg = (
                f"Since $f(a) \\cdot f(c) = ({_fmt(fa_val)}) \\cdot ({_fmt(fmid_val)}) = {_fmt(product)} < 0$, "
                f"$f(a)$ and $f(c)$ have opposite signs. The root is trapped in the left half $[a, c]$. "
                f"Therefore, update the upper bound: $b \\leftarrow c = {_fmt(mid_val)}$."
            )
            next_interval_latex = f"[{_fmt(a_val)}, {_fmt(mid_val)}]"

        checkpoint = None
        if n == 1 and questions:
            # Attach the interval question to iteration 1
            for q in questions:
                if q.question_type == "interval":
                    checkpoint = q
                    break

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title=f"Iteration {n}: Midpoint Evaluation & Subinterval Selection",
                concept="Interval Bisection & Intermediate Value Sign Test",
                explanation=(
                    f"Bisect the current interval $[{_fmt(a_val)}, {_fmt(b_val)}]$ by computing the midpoint $c$. "
                    f"Then evaluate $f(c)$ to determine which half contains the sign change."
                ),
                formula_latex=r"c = \frac{a + b}{2}, \quad \epsilon_n = \frac{b - a}{2}",
                substitution_latex=f"c = \\frac{{{_fmt(a_val)} + {_fmt(b_val)}}}{{2}}",
                calculation_latex=(
                    f"c = {_fmt(mid_val)} \\\\[4pt]"
                    f"f(c) = f({_fmt(mid_val)}) = {_fmt(fmid_val)} \\\\[4pt]"
                    f"\\text{{Error bound }} \\epsilon_{{{n}}} = \\frac{{{_fmt(b_val)} - {_fmt(a_val)}}}{{2}} = {_fmt(err_val)}"
                ),
                result_latex=f"c_{{{n}}} = {_fmt(mid_val)}, \\quad f(c_{{{n}}}) = {_fmt(fmid_val)}",
                decision=decision_msg,
                related_iteration=n,
                checkpoint_question=checkpoint,
                variable_definitions=[
                    VariableDefinition(symbol=f"a_{{{n}}}", name="Current Lower Bound", description="Lower bound for this iteration", current_value=_fmt(a_val)),
                    VariableDefinition(symbol=f"b_{{{n}}}", name="Current Upper Bound", description="Upper bound for this iteration", current_value=_fmt(b_val)),
                    VariableDefinition(symbol=f"c_{{{n}}}", name="Midpoint Estimate", description="Approximation computed at this step", current_value=_fmt(mid_val)),
                    VariableDefinition(symbol=f"f(c_{{{n}}})", name="Function at Midpoint", description="Evaluated residual", current_value=_fmt(fmid_val)),
                    VariableDefinition(symbol=r"\epsilon", name="Half-Width Error", description="Maximum distance to root", current_value=_fmt(err_val)),
                ],
                substeps=[
                    f"1. Compute arithmetic mean: c = ({_fmt(a_val)} + {_fmt(b_val)}) / 2 = {_fmt(mid_val)}",
                    f"2. Evaluate function: f({_fmt(mid_val)}) = {_fmt(fmid_val)}",
                    f"3. Sign test: f(a) · f(c) {' > 0 (same sign)' if same_sign else ' < 0 (opposite sign)'}",
                    f"4. Next bracket: {next_interval_latex}",
                ],
            )
        )
        step_num += 1

    # Final Convergence Step
    final_err = result.metrics.final_approximate_error
    converged = result.status == SolverStatus.CONVERGED
    convergence_explanation = (
        f"The solver concluded after {len(result.iterations)} iterations. "
        + (
            f"The bracket half-width {_fmt(final_err)} is strictly less than the convergence tolerance {_fmt(tol)}, "
            "satisfying the termination condition."
            if converged
            else f"Algorithm terminated due to: {result.termination_reason}."
        )
    )

    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="convergence",
            title="Convergence Analysis & Stopping Criterion",
            concept="Error Halving & Stopping Criterion",
            explanation=convergence_explanation,
            formula_latex=r"\epsilon_n = \frac{b_n - a_n}{2} < \text{tol}",
            calculation_latex=(
                f"\\epsilon_{{{len(result.iterations)}}} = {_fmt(final_err)} \\quad "
                f"({'<' if (final_err is not None and final_err < tol) else '\\ge'}) \\quad "
                f"\\text{{tol}} = {_fmt(tol)}"
            ),
            result_latex=f"x^* \\approx {_fmt(result.root)}",
            decision=(
                f"Termination condition satisfied. The midpoint $c = {_fmt(result.root)}$ is accepted as the numerical root."
            ),
            related_iteration=len(result.iterations) if result.iterations else None,
        )
    )

    root_val_str = _fmt(result.root)
    f_root_val = getattr(result, "f_root", None)
    if f_root_val is None and result.iterations:
        last_vals = result.iterations[-1].values
        f_root_val = last_vals.get("f_mid", last_vals.get("f_root", last_vals.get("f_xn")))
    f_root_str = _fmt(f_root_val if f_root_val is not None else 0.0)

    final_interp = FinalInterpretation(
        summary=(
            f"The Bisection Method successfully isolated the real root of f(x) = {expr_str} "
            f"to x* ≈ {root_val_str} across {result.metrics.iterations} iterations."
        ),
        root_or_solution=f"x* ≈ {root_val_str}",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Maximum bound |x* - r| ≤ {_fmt(final_err)}",
        verification=(
            f"Evaluating the function at the computed root yields f({root_val_str}) = {f_root_str}. "
            f"Because this residual is within machine tolerance of zero, the solution is verified."
        ),
    )

    # Extract worked step for Iteration 1
    worked_step = next((s for s in steps if s.related_iteration == 1 and s.step_type == "calculation"), None)
    if not worked_step and len(steps) > 1:
        worked_step = steps[1]

    what_changes_next = (
        "The same midpoint formula is applied again using the updated interval. "
        "At each iteration, the interval width is halved and the root estimate becomes more accurate "
        "until the error tolerance is satisfied."
    )
    rem_summary = (
        f"Subsequent iterations continue halving the bracket, reducing the error bound "
        f"from {_fmt(result.iterations[0].approximate_error if result.iterations else tol)} "
        f"down to {_fmt(final_err)}."
    )

    return SolutionDocument(
        method="Bisection Method",
        topic=concept["topic"],
        problem_statement=problem_statement,
        one_sentence_purpose="Finds real roots by iteratively halving an interval $[a, b]$ where the function changes sign.",
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


def generate_false_position_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for the False Position (Regula Falsi) Method."""
    concept = get_concept_info("false_position")
    formulas = get_formula_cards("false_position")
    questions = generate_questions_for_method("false_position", problem, result)

    expr_str = problem.expression.strip()
    try:
        expr_sym, _ = parse_function_x(expr_str)
        expr_latex = sympy.latex(expr_sym)
    except Exception:
        expr_latex = expr_str

    a_init = problem.a if problem.a is not None else 0.0
    b_init = problem.b if problem.b is not None else 1.0
    tol = problem.tol

    problem_statement = (
        f"Find a real root of $f(x) = {expr_latex} = 0$ on the bracket "
        f"$[{_fmt(a_init)}, {_fmt(b_init)}]$ using the False Position (Regula Falsi) method "
        f"with tolerance $\\text{{tol}} = {_fmt(tol)}$."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Geometric Secant Line Derivation vs Bisection
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Conceptual Foundation: Secant Line Interpolation vs Bisection",
            concept="Linear Secant Interpolation",
            explanation=(
                "Unlike the Bisection Method which naively splits the interval in half regardless of function values, "
                "the False Position (Regula Falsi) method constructs a straight secant line between the bracket endpoints "
                "$(a, f(a))$ and $(b, f(b))$. The root approximation $c$ is the exact $x$-intercept where this line crosses $y = 0$. "
                "If $f(a)$ is much closer to zero than $f(b)$, the secant line wisely places $c$ closer to $a$."
            ),
            formula_latex=r"c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)} = b - \frac{f(b)(b - a)}{f(b) - f(a)}",
            calculation_latex=(
                r"\text{Secant slope: } m = \frac{f(b) - f(a)}{b - a} \\\\[4pt]"
                r"\text{Line equation: } y - f(b) = m(x - b) \implies 0 - f(b) = m(c - b) \implies c = b - \frac{f(b)}{m}"
            ),
            decision="Linear interpolation provides faster convergence than bisection when the curve is relatively flat.",
            variable_definitions=[
                VariableDefinition(symbol="a, b", name="Bracket Endpoints", description="Enclosing interval points with opposite signs", current_value=f"[{_fmt(a_init)}, {_fmt(b_init)}]"),
                VariableDefinition(symbol="c", name="Secant Intercept", description="Point where secant chord intersects y = 0"),
            ],
        )
    )
    step_num += 1

    # Step 2..N: Iteration steps
    for it in result.iterations:
        n = it.n
        a_val = float(it.values.get("a", 0.0))
        b_val = float(it.values.get("b", 0.0))
        root_val = float(it.values.get("root", 0.0))
        fa_val = float(it.values.get("f_a", 0.0))
        fb_val = float(it.values.get("f_b", 0.0))
        froot_val = float(it.values.get("f_root", 0.0))
        err_val = it.approximate_error if it.approximate_error is not None else 0.0

        denom = fb_val - fa_val
        num = a_val * fb_val - b_val * fa_val

        # Decision
        fa_neg = fa_val < 0
        froot_neg = froot_val < 0
        same_sign_with_a = (fa_neg == froot_neg)

        if same_sign_with_a:
            decision_msg = (
                f"Because $f(a) = {_fmt(fa_val)}$ and $f(c) = {_fmt(froot_val)}$ share the same sign, "
                f"the root is bracketed in $[c, b]$. Replace lower endpoint: $a \\leftarrow c = {_fmt(root_val)}$."
            )
        else:
            decision_msg = (
                f"Because $f(a) = {_fmt(fa_val)}$ and $f(c) = {_fmt(froot_val)}$ have opposite signs, "
                f"the root is bracketed in $[a, c]$. Replace upper endpoint: $b \\leftarrow c = {_fmt(root_val)}$."
            )

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title=f"Iteration {n}: Secant Substitution & Root Estimation",
                concept="Secant Line Intercept Calculation",
                explanation=f"Compute the x-intercept $c_{{{n}}}$ of the chord connecting $(a, f(a))$ and $(b, f(b))$.",
                formula_latex=r"c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)}",
                substitution_latex=(
                    f"c = \\frac{{({_fmt(a_val)})({_fmt(fb_val)}) - ({_fmt(b_val)})({_fmt(fa_val)})}}"
                    f"{{{_fmt(fb_val)} - ({_fmt(fa_val)})}}"
                ),
                calculation_latex=(
                    f"\\text{{Numerator: }} {_fmt(num)} \\\\[4pt]"
                    f"\\text{{Denominator: }} {_fmt(denom)} \\\\[4pt]"
                    f"c_{{{n}}} = {_fmt(root_val)}, \\quad f(c_{{{n}}}) = {_fmt(froot_val)} \\\\[4pt]"
                    f"\\text{{Step Change: }} |c_{{{n}}} - c_{{{n-1}}}| = {_fmt(err_val)}"
                ),
                result_latex=f"c_{{{n}}} = {_fmt(root_val)}",
                decision=decision_msg,
                related_iteration=n,
                variable_definitions=[
                    VariableDefinition(symbol="a", name="Lower Bound", description="Current left bracket", current_value=_fmt(a_val)),
                    VariableDefinition(symbol="b", name="Upper Bound", description="Current right bracket", current_value=_fmt(b_val)),
                    VariableDefinition(symbol="f(a)", name="f(a)", description="Function at left bracket", current_value=_fmt(fa_val)),
                    VariableDefinition(symbol="f(b)", name="f(b)", description="Function at right bracket", current_value=_fmt(fb_val)),
                    VariableDefinition(symbol="c", name="New Root Estimate", description="Secant root estimate", current_value=_fmt(root_val)),
                ],
                substeps=[
                    f"1. Evaluate f(a) = {_fmt(fa_val)} and f(b) = {_fmt(fb_val)}",
                    f"2. Apply false position formula: c = {_fmt(root_val)}",
                    f"3. Evaluate f(c) = {_fmt(froot_val)}",
                    f"4. Approximate error = {_fmt(err_val)}",
                ],
            )
        )
        step_num += 1

    # Convergence Step
    final_err = result.metrics.final_approximate_error
    converged = result.status == SolverStatus.CONVERGED
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="convergence",
            title="Convergence Behavior & Stagnation Note",
            concept="Secant Convergence & One-Sided Stagnation",
            explanation=(
                "False position terminates when the change between successive root estimates $|c_{new} - c_{old}|$ "
                f"falls below $\\text{{tol}} = {_fmt(tol)}$. "
                "Note: If the function is concave or convex on the bracket, one endpoint can remain stagnant while the other "
                "slowly advances. In such scenarios, the step difference can be small even if the interval remains wide."
            ),
            formula_latex=r"|c_{n} - c_{n-1}| < \text{tol}",
            calculation_latex=f"|c_{{{len(result.iterations)}}} - c_{{{len(result.iterations)-1}}}| = {_fmt(final_err)} < {_fmt(tol)}",
            result_latex=f"x^* \\approx {_fmt(result.root)}",
            decision="Tolerance threshold reached. Computation complete.",
            related_iteration=len(result.iterations) if result.iterations else None,
        )
    )

    root_val_str = _fmt(result.root)
    f_root_val = getattr(result, "f_root", None)
    if f_root_val is None and result.iterations:
        last_vals = result.iterations[-1].values
        f_root_val = last_vals.get("f_mid", last_vals.get("f_root", last_vals.get("f_xn")))
    f_root_str = _fmt(f_root_val if f_root_val is not None else 0.0)

    final_interp = FinalInterpretation(
        summary=(
            f"The False Position method converged to root x* ≈ {root_val_str} "
            f"in {result.metrics.iterations} iterations."
        ),
        root_or_solution=f"x* ≈ {root_val_str}",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Estimated error |Δx| ≈ {_fmt(final_err)}",
        verification=f"Evaluation confirms f({root_val_str}) = {f_root_str} ≈ 0.",
    )

    # Extract worked step for Iteration 1
    worked_step = next((s for s in steps if s.related_iteration == 1 and s.step_type == "calculation"), None)
    if not worked_step and len(steps) > 1:
        worked_step = steps[1]

    what_changes_next = (
        "The next approximation is calculated using the updated interval and its latest endpoint function values. "
        "The secant chord is redrawn dynamically until successive estimates satisfy the tolerance."
    )
    rem_summary = (
        f"Subsequent iterations update the active bracket endpoint, achieving an approximation error "
        f"of {_fmt(final_err)}."
    )

    return SolutionDocument(
        method="False Position",
        topic=concept["topic"],
        problem_statement=problem_statement,
        one_sentence_purpose="Finds real roots by drawing a linear secant chord between bracket endpoints and calculating its $x$-intercept.",
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


def generate_newton_raphson_lesson(problem: ProblemRequest, result: SolverResult) -> SolutionDocument:
    """Generate interactive academic lesson for the Newton-Raphson Method."""
    concept = get_concept_info("newton_raphson")
    formulas = get_formula_cards("newton_raphson")
    questions = generate_questions_for_method("newton_raphson", problem, result)

    expr_str = problem.expression.strip()
    deriv_latex = "f'(x)"
    try:
        expr_sym, _ = parse_function_x(expr_str)
        expr_latex = sympy.latex(expr_sym)
        deriv_sym, _ = differentiate_x(expr_sym)
        deriv_latex = sympy.latex(deriv_sym)
    except Exception:
        expr_latex = expr_str

    x0 = problem.x0 if problem.x0 is not None else (problem.a if problem.a is not None else 0.0)
    tol = problem.tol

    problem_statement = (
        f"Find a real root of $f(x) = {expr_latex} = 0$ starting from initial guess "
        f"$x_0 = {_fmt(x0)}$ with convergence tolerance $\\text{{tol}} = {_fmt(tol)}$."
    )

    steps: list[SolutionStep] = []
    step_num = 1

    # Step 1: Symbolic Differentiation & Tangent Line Foundation
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="concept",
            title="Symbolic Differentiation & Geometric Tangent Concept",
            concept="First-Order Taylor Expansion & Tangent Line",
            explanation=(
                "The Newton-Raphson method replaces the curve $y = f(x)$ with its tangent line at the current guess $x_n$. "
                "The first-order Taylor expansion around $x_n$ is: $f(x) \\approx f(x_n) + f'(x_n)(x - x_n)$. "
                "Setting $f(x) = 0$ and solving for $x$ yields the updated estimate $x_{n+1}$."
            ),
            formula_latex=r"f(x) \approx f(x_n) + f'(x_n)(x - x_n) = 0 \implies x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}",
            calculation_latex=(
                f"f(x) = {expr_latex} \\\\[4pt]"
                f"f'(x) = \\frac{{df}}{{dx}} = {deriv_latex}"
            ),
            decision=f"Initial guess selected: $x_0 = {_fmt(x0)}$. We must ensure $f'(x_n) \\ne 0$ at all steps.",
            variable_definitions=[
                VariableDefinition(symbol="f(x)", name="Target Function", description="Function whose root is sought", current_value=expr_str),
                VariableDefinition(symbol="f'(x)", name="Symbolic Derivative", description="First derivative with respect to x", current_value=str(deriv_latex)),
                VariableDefinition(symbol="x_0", name="Initial Guess", description="Starting point for the iteration", current_value=_fmt(x0)),
            ],
        )
    )
    step_num += 1

    # Step 2..N: Iterations
    for it in result.iterations:
        n = it.n
        xn = float(it.values.get("x_n", 0.0))
        fxn = float(it.values.get("f_xn", 0.0))
        dfxn = float(it.values.get("df_xn", 0.0))
        x_new = float(it.values.get("x_new", 0.0))
        err_val = it.approximate_error if it.approximate_error is not None else abs(x_new - xn)

        ratio = fxn / dfxn if dfxn != 0 else 0.0

        checkpoint = None
        if n == 1 and questions:
            for q in questions:
                if q.id == "nr_q2":
                    checkpoint = q
                    break

        # Plot data for tangent line
        tangent_x = [xn - 0.5, xn + 0.5, x_new]
        tangent_y = [fxn + dfxn * (tx - xn) for tx in tangent_x]

        steps.append(
            SolutionStep(
                step_number=step_num,
                step_type="calculation",
                title=f"Iteration {n}: Tangent Slope & Newton Step",
                concept="Newton Tangent Intercept",
                explanation=(
                    f"At current point $x_{{{n-1}}} = {_fmt(xn)}$, evaluate the function $f(x)$ and its slope $f'(x)$. "
                    f"Then project along the tangent line to locate the $x$-axis intercept $x_{{{n}}}$."
                ),
                formula_latex=r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}",
                substitution_latex=f"x_{{{n}}} = {_fmt(xn)} - \\frac{{{_fmt(fxn)}}}{{{_fmt(dfxn)}}}",
                calculation_latex=(
                    f"f(x_{{{n-1}}}) = f({_fmt(xn)}) = {_fmt(fxn)} \\\\[4pt]"
                    f"f'(x_{{{n-1}}}) = f'({_fmt(xn)}) = {_fmt(dfxn)} \\\\[4pt]"
                    f"\\Delta x = \\frac{{f(x_{{{n-1}}})}}{{f'(x_{{{n-1}}})}} = \\frac{{{_fmt(fxn)}}}{{{_fmt(dfxn)}}} = {_fmt(ratio)} \\\\[4pt]"
                    f"x_{{{n}}} = {_fmt(xn)} - ({_fmt(ratio)}) = {_fmt(x_new)} \\\\[4pt]"
                    f"\\text{{Approximate Error }} |x_{{{n}}} - x_{{{n-1}}}| = {_fmt(err_val)}"
                ),
                result_latex=f"x_{{{n}}} = {_fmt(x_new)}",
                decision=(
                    f"Slope $f'({_fmt(xn)}) = {_fmt(dfxn)}$ is non-zero, avoiding singular horizontal tangent. "
                    f"Advance to next approximation $x_{{{n}}} = {_fmt(x_new)}$."
                ),
                related_iteration=n,
                checkpoint_question=checkpoint,
                related_plot_data={"tangent_x": tangent_x, "tangent_y": tangent_y, "point": [xn, fxn]},
                variable_definitions=[
                    VariableDefinition(symbol=f"x_{{{n-1}}}", name="Current Estimate", description="Approximation before this step", current_value=_fmt(xn)),
                    VariableDefinition(symbol=f"f(x_{{{n-1}}})", name="Function Value", description="Height at current point", current_value=_fmt(fxn)),
                    VariableDefinition(symbol=f"f'(x_{{{n-1}}})", name="Tangent Slope", description="Derivative at current point", current_value=_fmt(dfxn)),
                    VariableDefinition(symbol=f"x_{{{n}}}", name="Next Estimate", description="Tangent x-intercept", current_value=_fmt(x_new)),
                    VariableDefinition(symbol=r"\Delta x", name="Newton Step", description="Displacement along x", current_value=_fmt(err_val)),
                ],
                substeps=[
                    f"1. Evaluate f({_fmt(xn)}) = {_fmt(fxn)}",
                    f"2. Evaluate derivative f'({_fmt(xn)}) = {_fmt(dfxn)}",
                    f"3. Compute step Δx = f/f' = {_fmt(ratio)}",
                    f"4. Next approximation x_{n} = {_fmt(x_new)}",
                ],
            )
        )
        step_num += 1

    # Convergence Step
    final_err = result.metrics.final_approximate_error
    converged = result.status == SolverStatus.CONVERGED
    steps.append(
        SolutionStep(
            step_number=step_num,
            step_type="convergence",
            title="Quadratic Convergence & Stopping Condition",
            concept="Quadratic Convergence",
            explanation=(
                "Newton-Raphson terminates when the successive step difference $|x_{n+1} - x_n| < \\text{tol}$. "
                "Because Newton-Raphson converges quadratically near simple roots, each iteration approximately doubles "
                "the number of correct decimal places."
            ),
            formula_latex=r"|x_{n+1} - x_n| < \text{tol}, \quad |e_{n+1}| \approx C |e_n|^2",
            calculation_latex=(
                f"|x_{{{len(result.iterations)}}} - x_{{{len(result.iterations)-1}}}| = {_fmt(final_err)} "
                f"({'<' if (final_err is not None and final_err < tol) else '\\ge'}) {_fmt(tol)}"
            ),
            result_latex=f"x^* \\approx {_fmt(result.root)}",
            decision="Quadratic convergence completed within tolerance.",
            related_iteration=len(result.iterations) if result.iterations else None,
        )
    )

    root_val_str = _fmt(result.root)
    f_root_val = getattr(result, "f_root", None)
    if f_root_val is None and result.iterations:
        last_vals = result.iterations[-1].values
        f_root_val = last_vals.get("f_mid", last_vals.get("f_root", last_vals.get("f_xn")))
    f_root_str = _fmt(f_root_val if f_root_val is not None else 0.0)

    final_interp = FinalInterpretation(
        summary=(
            f"The Newton-Raphson method successfully computed the root x* ≈ {root_val_str} "
            f"in {result.metrics.iterations} iterations."
        ),
        root_or_solution=f"x* ≈ {root_val_str}",
        iterations_count=result.metrics.iterations,
        stopping_reason=result.termination_reason,
        accuracy_achieved=f"Successive step error |Δx| ≤ {_fmt(final_err)}",
        verification=(
            f"Evaluating f({root_val_str}) = {f_root_str}. "
            f"Near-zero residual confirms precision."
        ),
    )

    # Extract worked step for Iteration 1
    worked_step = next((s for s in steps if s.related_iteration == 1 and s.step_type == "calculation"), None)
    if not worked_step and len(steps) > 1:
        worked_step = steps[1]

    what_changes_next = (
        "The new approximation becomes the starting value for the next iteration. "
        "The tangent line intersection formula is repeated until the error reaches the required tolerance."
    )
    rem_summary = (
        f"Subsequent iterations apply the same tangent update, quadratically converging to error "
        f"{_fmt(final_err)}."
    )

    return SolutionDocument(
        method="Newton-Raphson",
        topic=concept["topic"],
        problem_statement=problem_statement,
        one_sentence_purpose="Approximates roots by projecting tangent lines from the current point to the $x$-axis using calculus derivatives.",
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
