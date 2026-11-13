"""
Deterministic Knowledge Check Question Generator for NUMERIX.
Generates method-specific and calculation-specific multiple choice questions.
"""
from __future__ import annotations

from typing import Any
from numerix.core.result_models import SolverResult
from numerix.engine.solver_engine import ProblemRequest
from numerix.learning.solution_models import KnowledgeCheckQuestion


def generate_questions_for_method(
    method_id: str,
    problem: ProblemRequest,
    result: SolverResult,
) -> list[KnowledgeCheckQuestion]:
    """Generate high-quality deterministic practice questions tailored to the current method and solution."""
    method = method_id.lower().replace("-", "_").replace(" ", "_")
    questions: list[KnowledgeCheckQuestion] = []

    if method == "bisection":
        # Question 1: Conceptual / IVT
        questions.append(
            KnowledgeCheckQuestion(
                id="bis_q1",
                question="What is the necessary condition for the Bisection Method to guarantee convergence to a root on an interval [a, b]?",
                options=[
                    "The function f(x) must be continuous and f(a) · f(b) < 0.",
                    "The function f(x) must have a non-zero derivative everywhere on [a, b].",
                    "The interval [a, b] must contain an even number of roots.",
                    "The function f(x) must be concave upward across [a, b].",
                ],
                correct_index=0,
                explanation="By the Intermediate Value Theorem, a continuous function that changes sign between a and b (i.e. f(a) · f(b) < 0) must have at least one real zero between a and b.",
                question_type="conceptual",
                hint="Recall the Intermediate Value Theorem for continuous functions.",
            )
        )
        # Question 2: Calculation / Interval selection based on actual values if available
        if result.iterations and len(result.iterations) >= 1:
            it0 = result.iterations[0]
            fa = it0.values.get("f_a", -1.0)
            fmid = it0.values.get("f_mid", 1.0)
            if isinstance(fa, (int, float)) and isinstance(fmid, (int, float)):
                fa_neg = fa < 0
                fmid_neg = fmid < 0
                same_sign = (fa_neg == fmid_neg)
                correct_sub = "[mid, b]" if same_sign else "[a, mid]"
                wrong_sub = "[a, mid]" if same_sign else "[mid, b]"
                questions.append(
                    KnowledgeCheckQuestion(
                        id="bis_q2",
                        question=f"In iteration 1, f(a) = {fa:.4g} and f(mid) = {fmid:.4g}. Which subinterval must be retained for the next iteration?",
                        options=[
                            f"The subinterval {correct_sub}, because the function values at its endpoints have opposite signs.",
                            f"The subinterval {wrong_sub}, because the function values at its endpoints have the same sign.",
                            "Both subintervals, because roots exist in both halves.",
                            "Neither subinterval; the initial bracket must be discarded.",
                        ],
                        correct_index=0,
                        explanation=f"A root is guaranteed in the subinterval where the sign changes. Here f(a) has sign {'negative' if fa_neg else 'positive'} and f(mid) has sign {'negative' if fmid_neg else 'positive'}, so the sign change is in {correct_sub}.",
                        question_type="interval",
                        hint="Check which pair of endpoint values has opposite signs.",
                    )
                )

        # Question 3: Convergence / Error bound
        questions.append(
            KnowledgeCheckQuestion(
                id="bis_q3",
                question="How does the maximum error bound change with each iteration in the Bisection Method?",
                options=[
                    "It is halved at every iteration: error_{n+1} = error_n / 2.",
                    "It decreases quadratically: error_{n+1} ≈ (error_n)².",
                    "It decreases by a fixed constant amount independent of interval width.",
                    "It depends on the magnitude of the derivative f'(c).",
                ],
                correct_index=0,
                explanation="Because the interval width (b - a) is divided by 2 each time, the maximum possible distance from the midpoint to the root is exactly halved at every step.",
                question_type="prediction",
                hint="Think about how the bracket interval is subdivided.",
            )
        )

    elif method == "false_position":
        questions.append(
            KnowledgeCheckQuestion(
                id="fp_q1",
                question="How does the False Position (Regula Falsi) method choose the new root approximation c?",
                options=[
                    "As the x-intercept of the secant line connecting (a, f(a)) and (b, f(b)).",
                    "As the exact arithmetic midpoint c = (a + b) / 2.",
                    "As the x-intercept of the tangent line at the midpoint.",
                    "By taking the average of the function values f(a) and f(b).",
                ],
                correct_index=0,
                explanation="Regula Falsi connects (a, f(a)) and (b, f(b)) with a straight line (secant) and finds where that line crosses the horizontal axis y = 0.",
                question_type="conceptual",
                hint="Think of linear interpolation between the two endpoints.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="fp_q2",
                question="What is a known disadvantage of the False Position method compared to the Bisection method?",
                options=[
                    "On convex or concave curves, one endpoint can remain stagnant, slowing convergence to a slow linear rate.",
                    "It can diverge to infinity even if the bracket is valid.",
                    "It requires evaluating the second derivative f''(x).",
                    "It cannot solve polynomial equations.",
                ],
                correct_index=0,
                explanation="On functions with strong curvature, one bracket endpoint often remains fixed throughout all iterations while the other creeps slowly, losing the rapid progress secant lines normally offer.",
                question_type="conceptual",
                hint="Consider what happens when one endpoint never changes sign.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="fp_q3",
                question="Which formula correctly computes the false position estimate c?",
                options=[
                    r"c = [a·f(b) - b·f(a)] / [f(b) - f(a)]",
                    r"c = [a·f(a) - b·f(b)] / [f(b) - f(a)]",
                    r"c = (a + b) / 2",
                    r"c = a - f(a) / f'(a)",
                ],
                correct_index=0,
                explanation="The x-intercept of the line through (a, f(a)) and (b, f(b)) is c = [a·f(b) - b·f(a)] / [f(b) - f(a)].",
                question_type="formula",
                hint="Derived by setting y = 0 in the two-point point-slope line equation.",
            )
        )

    elif method == "newton_raphson":
        questions.append(
            KnowledgeCheckQuestion(
                id="nr_q1",
                question="What order of convergence does the Newton-Raphson method exhibit near a simple root (where f'(r) ≠ 0)?",
                options=[
                    "Quadratic convergence (Order 2), doubling correct digits each iteration.",
                    "Linear convergence (Order 1), adding a constant number of digits.",
                    "Cubic convergence (Order 3), tripling correct digits.",
                    "Sublinear convergence.",
                ],
                correct_index=0,
                explanation="Near a simple root where f'(r) ≠ 0, Taylor series analysis shows e_{n+1} ≈ [f''(r)/(2 f'(r))] (e_n)², which is quadratic convergence.",
                question_type="conceptual",
                hint="Notice the power of the error in the Taylor series expansion.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="nr_q2",
                question="What critical failure occurs if f'(x_n) = 0 at the current iteration?",
                options=[
                    "The tangent line is horizontal and never intersects the x-axis, causing division by zero.",
                    "The method converges immediately to an exact root.",
                    "The next estimate defaults to x = 0.",
                    "The algorithm switches automatically to Bisection.",
                ],
                correct_index=0,
                explanation="In x_{n+1} = x_n - f(x_n)/f'(x_n), a zero derivative leads to division by zero because a horizontal tangent has no finite x-intercept.",
                question_type="prediction",
                hint="Consider the slope of a horizontal line.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="nr_q3",
                question="Which of the following is NOT a requirement for using the Newton-Raphson method?",
                options=[
                    "Knowing two bracket endpoints that change sign: f(a) · f(b) < 0.",
                    "An initial guess x₀ reasonably close to the root.",
                    "The ability to evaluate the derivative f'(x).",
                    "A non-zero derivative at the root: f'(r) ≠ 0.",
                ],
                correct_index=0,
                explanation="Newton-Raphson is an open method requiring only a single initial point x₀; it does not require a bracketing interval with a sign change.",
                question_type="conceptual",
                hint="Is Newton-Raphson a bracketing method or an open method?",
            )
        )

    elif method == "gauss_elimination":
        questions.append(
            KnowledgeCheckQuestion(
                id="ge_q1",
                question="Why is partial pivoting performed during Gaussian Elimination?",
                options=[
                    "To swap the largest absolute value in the current column to the pivot position, avoiding division by zero and reducing roundoff error.",
                    "To make the coefficient matrix diagonally symmetric.",
                    "To invert the matrix before calculating determinants.",
                    "To turn the matrix into reduced row echelon form in a single pass.",
                ],
                correct_index=0,
                explanation="Partial pivoting chooses the row with max |A_{k,i}| to prevent small pivot denominators, which would amplify floating-point rounding errors and cause catastrophic cancellation.",
                question_type="conceptual",
                hint="Think about what happens when dividing by numbers close to zero.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="ge_q2",
                question="What matrix structure is produced after forward elimination in Gaussian Elimination?",
                options=[
                    "Upper triangular matrix (zeros below the main diagonal).",
                    "Diagonal matrix (zeros everywhere except the main diagonal).",
                    "Lower triangular matrix (zeros above the main diagonal).",
                    "Identity matrix I.",
                ],
                correct_index=0,
                explanation="Forward elimination systematically zeros out all entries below the diagonal, leaving an upper triangular system Ux = c that is easily solved via back-substitution.",
                question_type="matrix_op",
                hint="Where are the zeros placed during the forward pass?",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="ge_q3",
                question="How is the solution vector obtained once the upper triangular system is formed?",
                options=[
                    "Via back substitution starting from the bottom row (x_n) up to the top row (x_1).",
                    "By taking the square root of the diagonal elements.",
                    "By multiplying the matrix by its transpose.",
                    "By inverting the right-hand-side vector directly.",
                ],
                correct_index=0,
                explanation="Back substitution solves the last equation first (which has only one unknown x_n), and then substitutes known values upward to solve x_{n-1}, ..., x_1.",
                question_type="conceptual",
                hint="Notice which equation has only one unknown.",
            )
        )

    elif method == "gauss_jordan":
        questions.append(
            KnowledgeCheckQuestion(
                id="gj_q1",
                question="How does Gauss-Jordan elimination differ from standard Gaussian elimination?",
                options=[
                    "It eliminates entries both above and below each pivot, producing the identity matrix [I | x].",
                    "It only works on symmetric positive-definite matrices.",
                    "It requires back-substitution after completing row operations.",
                    "It uses fewer total arithmetic operations than Gaussian elimination.",
                ],
                correct_index=0,
                explanation="Gauss-Jordan diagonalizes the system matrix completely into Reduced Row Echelon Form [I | x], eliminating the need for back-substitution at the cost of ~50% more arithmetic operations.",
                question_type="conceptual",
                hint="Look at which entries are eliminated (above vs below).",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="gj_q2",
                question="What is the result in the augmented vector column once [A | b] is transformed to [I | x] in Gauss-Jordan?",
                options=[
                    "It contains the exact solution vector x directly with no back-substitution required.",
                    "It contains the eigenvalues of matrix A.",
                    "It contains the determinant of matrix A.",
                    "It contains the residual vector r.",
                ],
                correct_index=0,
                explanation="Because the left block is the identity matrix I, the system reads 1·x_i = b'_i, so each component of the solution vector is directly visible.",
                question_type="interpretation",
                hint="If I · x = b', what is x?",
            )
        )

    elif method == "euler":
        questions.append(
            KnowledgeCheckQuestion(
                id="eu_q1",
                question="In Euler's method for solving dy/dx = f(x, y), what is the formula to advance from y_n to y_{n+1}?",
                options=[
                    r"y_{n+1} = y_n + h · f(x_n, y_n)",
                    r"y_{n+1} = y_n + (h/2) · [f(x_n, y_n) + f(x_{n+1}, y_{n+1})]",
                    r"y_{n+1} = y_n + h · f'(x_n, y_n)",
                    r"y_{n+1} = y_n + (1/6) · (k_1 + 2k_2 + 2k_3 + k_4)",
                ],
                correct_index=0,
                explanation="Euler's forward method advances along the tangent line evaluated at the beginning of the step: y_{n+1} = y_n + h · f(x_n, y_n).",
                question_type="formula",
                hint="Think of the simplest linear tangent extrapolation: Δy ≈ slope · Δx.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="eu_q2",
                question="If you halve the step size h in Euler's method, how does the global truncation error behave approximately?",
                options=[
                    "The global error is approximately halved, because Euler's method is first-order O(h).",
                    "The global error is reduced by a factor of 4, because Euler's method is second-order O(h²).",
                    "The global error is reduced by a factor of 16.",
                    "The error remains unchanged.",
                ],
                correct_index=0,
                explanation="Euler's method has a global truncation error of O(h). Reducing h by 2 approximately reduces the accumulated error by 2.",
                question_type="prediction",
                hint="Consider the order of the method.",
            )
        )

    elif method == "modified_euler":
        questions.append(
            KnowledgeCheckQuestion(
                id="me_q1",
                question="What role does the 'predictor' step play in the Modified Euler (Heun) method?",
                options=[
                    "It calculates a preliminary trial value y*_{n+1} using standard Euler so the slope at x_{n+1} can be estimated.",
                    "It predicts the exact analytical solution using symbolic calculus.",
                    "It checks whether the step size h is small enough for convergence.",
                    "It calculates the second derivative y''(x).",
                ],
                correct_index=0,
                explanation="The predictor step y*_{n+1} = y_n + h·f(x_n, y_n) provides an approximate state at x_{n+1}, allowing the corrector to evaluate slope f(x_{n+1}, y*_{n+1}).",
                question_type="conceptual",
                hint="Why do we need a preliminary estimate before taking the average slope?",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="me_q2",
                question="Why is the Modified Euler method considered a second-order method O(h²)?",
                options=[
                    "Because it averages the slopes at the beginning and predicted end of the interval, analogous to the Trapezoidal rule.",
                    "Because it evaluates the second derivative y''(x) directly.",
                    "Because it takes two integration steps per iteration.",
                    "Because it squares the step size h at each iteration.",
                ],
                correct_index=0,
                explanation="By averaging the initial slope f_1 and end slope f_2, the O(h) error terms in the Taylor series cancel out, yielding O(h²) global accuracy.",
                question_type="conceptual",
                hint="Think of numerical quadrature: which integration rule averages the two endpoints?",
            )
        )

    elif method == "rk4":
        questions.append(
            KnowledgeCheckQuestion(
                id="rk_q1",
                question="How many slope evaluations per step does the classical 4th-Order Runge-Kutta (RK4) method perform?",
                options=[
                    "4 evaluations: k₁ at start, k₂ and k₃ at midpoint, k₄ at end.",
                    "1 evaluation: slope at the midpoint.",
                    "2 evaluations: predictor and corrector.",
                    "8 evaluations: two for each order.",
                ],
                correct_index=0,
                explanation="RK4 evaluates four distinct slopes: k₁ at x_n, k₂ at midpoint using k₁/2, k₃ at midpoint using k₂/2, and k₄ at x_n + h using k₃.",
                question_type="conceptual",
                hint="Recall the definitions of k₁, k₂, k₃, and k₄.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="rk_q2",
                question="What numerical integration weighting does the RK4 scheme resemble?",
                options=[
                    "Simpson's 1/3 rule with weights 1/6 · (k₁ + 2k₂ + 2k₃ + k₄).",
                    "The Trapezoidal rule with weights 1/2 · (k₁ + k₂).",
                    "The Midpoint rule with weight 1 · k₂.",
                    "Monte Carlo uniform sampling.",
                ],
                correct_index=0,
                explanation="The combination (k₁ + 2k₂ + 2k₃ + k₄)/6 mirrors Simpson's 1/3 rule, putting double weight on the two midpoint slope estimates.",
                question_type="conceptual",
                hint="Notice the weights 1, 2, 2, 1 divided by 6.",
            )
        )
        questions.append(
            KnowledgeCheckQuestion(
                id="rk_q3",
                question="What is the global truncation error order of the RK4 method?",
                options=[
                    "O(h⁴) — reducing h by half reduces error by roughly a factor of 16.",
                    "O(h²) — reducing h by half reduces error by roughly a factor of 4.",
                    "O(h) — reducing h by half reduces error by half.",
                    "O(h⁵) — reducing h by half reduces error by roughly a factor of 32.",
                ],
                correct_index=0,
                explanation="RK4 has a local truncation error of O(h⁵) and an accumulated global truncation error of O(h⁴). 2⁴ = 16 times error reduction upon halving h.",
                question_type="prediction",
                hint="Check the relationship between local error O(h⁵) and global error over 1/h steps.",
            )
        )

    return questions
