"""
Concept registry providing learning objectives, prerequisites, conceptual explanations,
and convergence behavior for all numerical methods.
"""
from __future__ import annotations


METHOD_CONCEPTS: dict[str, dict] = {
    "bisection": {
        "topic": "Root Finding",
        "method_name": "Bisection Method",
        "learning_objectives": [
            "Understand the Intermediate Value Theorem and the sign-change criterion f(a) · f(b) < 0.",
            "Learn how interval halving systematically brackets the true root.",
            "Understand how to evaluate f(c) and choose the appropriate subinterval [a, c] or [c, b].",
            "Trace the linear convergence rate O(1/2^n) and calculate theoretical error bounds.",
            "Understand termination criteria based on interval width and tolerance.",
        ],
        "prerequisites": [
            "Continuous functions and the Intermediate Value Theorem (IVT).",
            "Basic functional evaluation and interval notation [a, b].",
            "Concept of absolute error |b - a| / 2 and convergence tolerance ε.",
        ],
        "concept_summary": (
            "The Bisection Method is a guaranteed bracketing algorithm for finding real roots of continuous functions. "
            "By repeatedly dividing an interval [a, b] in half and selecting the subinterval where the function changes sign, "
            "it traps the root in a shrinking bracket whose width decreases by a factor of 2 at every step."
        ),
        "convergence_notes": (
            "Convergence is strictly linear with a convergence ratio of 1/2. Every 10 iterations reduces the bracket "
            "width by a factor of 2^10 ≈ 1024 (gaining roughly 3 decimal digits of precision). It is robust and cannot diverge, "
            "provided f is continuous and the initial bracket satisfies f(a) · f(b) < 0."
        ),
    },
    "false_position": {
        "topic": "Root Finding",
        "method_name": "False Position Method (Regula Falsi)",
        "learning_objectives": [
            "Understand linear interpolation (secant line) as an improvement over pure interval midpoint halving.",
            "Derive the Regula Falsi formula from the equation of the secant line intersecting y = 0.",
            "Trace how endpoint selection maintains the sign-change bracket f(a) · f(b) < 0.",
            "Recognize one-sided stagnation on concave/convex curves and compare speed with Bisection.",
            "Analyze termination conditions based on successive root difference |c_{new} - c_{old}|.",
        ],
        "prerequisites": [
            "Equation of a line through two points (point-slope form).",
            "Intermediate Value Theorem for continuous functions.",
            "Concept of secant lines and linear interpolation.",
        ],
        "concept_summary": (
            "The False Position (Regula Falsi) method improves upon Bisection by taking into account the magnitudes "
            "of f(a) and f(b). Instead of cutting the interval at the midpoint, it draws a straight secant line between "
            "(a, f(a)) and (b, f(b)) and takes the x-intercept of that line as the next root estimate."
        ),
        "convergence_notes": (
            "False Position usually converges faster than Bisection for well-behaved functions. However, if the function "
            "has significant curvature (e.g. convex curves), one endpoint may remain stationary while the other slowly creeps "
            "toward the root, leading to slow linear convergence. Even so, it retains the guarantee of bracketing."
        ),
    },
    "newton_raphson": {
        "topic": "Root Finding",
        "method_name": "Newton-Raphson Method",
        "learning_objectives": [
            "Understand the geometric concept of using tangent lines to approximate roots.",
            "Derive the Newton iteration formula x_{n+1} = x_n - f(x_n)/f'(x_n) from the first-order Taylor expansion.",
            "Follow the symbolic differentiation of f(x) and its numerical evaluation at each step.",
            "Observe quadratic convergence near simple roots (doubling of significant digits each step).",
            "Identify critical failure modes: zero derivatives, cycle loops, and divergence away from poor initial guesses.",
        ],
        "prerequisites": [
            "Differential calculus: derivatives, tangent lines, and first-order Taylor series.",
            "Basic root-finding concepts and iterative schemes.",
            "Limits and conditions for division by zero.",
        ],
        "concept_summary": (
            "The Newton-Raphson method is an open (non-bracketing) iterative method that replaces the curve y = f(x) with "
            "its tangent line at the current guess x_n. The intersection of this tangent line with the x-axis provides the "
            "next approximation x_{n+1}. When started near a root, it converges with remarkable quadratic speed."
        ),
        "convergence_notes": (
            "Near a simple root (where f'(r) ≠ 0), Newton's method exhibits quadratic convergence (order 2), meaning the "
            "number of correct decimal digits roughly doubles with every single iteration. However, if f'(x_n) ≈ 0, the tangent "
            "line becomes horizontal and the method fails."
        ),
    },
    "gauss_elimination": {
        "topic": "Linear Systems",
        "method_name": "Gaussian Elimination with Partial Pivoting",
        "learning_objectives": [
            "Construct the augmented matrix [A | b] representing a system of linear equations.",
            "Understand partial pivoting: identifying the column maximum entry and performing row swaps to avoid division by small pivots.",
            "Calculate elimination multipliers m_{j,i} = A_{j,i} / A_{i,i} and perform elementary row operations.",
            "Transform the matrix systematically into an upper triangular form.",
            "Execute back substitution from the bottom row up to solve for all unknown variables.",
            "Verify the solution by computing the residual vector r = Ax - b and its Euclidean norm.",
        ],
        "prerequisites": [
            "Matrix notation, dimensions, and matrix-vector multiplication Ax.",
            "Systems of linear equations with N equations and N unknowns.",
            "Elementary row operations (swapping, scaling, row addition/subtraction).",
        ],
        "concept_summary": (
            "Gaussian Elimination is a direct algorithm that converts a square linear system Ax = b into an equivalent upper "
            "triangular system Ux = c through elementary row operations. With partial pivoting, the row with the largest pivot "
            "element is swapped to the pivot position before eliminating entries below it, preventing numerical instability."
        ),
        "convergence_notes": (
            "As a direct method (not iterative), Gaussian Elimination produces the exact solution in a finite number of operations "
            "(approximately 2/3 n^3 arithmetic operations) in exact arithmetic. Partial pivoting is essential in floating-point arithmetic "
            "to suppress roundoff amplification and avoid division by zero."
        ),
    },
    "gauss_jordan": {
        "topic": "Linear Systems",
        "method_name": "Gauss-Jordan Elimination",
        "learning_objectives": [
            "Understand how Gauss-Jordan extends Gaussian elimination to eliminate entries both above and below each pivot.",
            "Normalize each pivot row so the leading diagonal element becomes exactly 1.",
            "Transform the augmented matrix [A | b] into Reduced Row-Echelon Form (RREF) [I | x].",
            "Read off the solution vector directly from the transformed right-hand side without needing back-substitution.",
            "Compare computational effort and operation count between Gauss Elimination and Gauss-Jordan.",
        ],
        "prerequisites": [
            "Elementary row operations and matrix augmentation.",
            "The concept of the identity matrix I and reduced row-echelon form (RREF).",
            "Partial pivoting principles.",
        ],
        "concept_summary": (
            "Gauss-Jordan Elimination is a variation of Gaussian elimination that diagonalizes the system matrix completely into the "
            "identity matrix [I | x]. By normalizing each pivot to 1 and eliminating entries both below and above each pivot element, "
            "the solution vector x appears directly in the augmented column, completely eliminating the need for back-substitution."
        ),
        "convergence_notes": (
            "Gauss-Jordan requires approximately n^3 operations (roughly 50% more operations than Gaussian Elimination with back-substitution). "
            "While slightly more computationally expensive for solving a single system, it offers great conceptual simplicity because the "
            "solution can be read directly from the final augmented column."
        ),
    },
    "euler": {
        "topic": "Differential Equations",
        "method_name": "Euler's Method",
        "learning_objectives": [
            "Formulate an initial value problem (IVP) dy/dx = f(x, y) with initial condition y(x_0) = y_0.",
            "Understand how the tangent line at (x_n, y_n) projects the state forward across step size h.",
            "Calculate the numerical substitution y_{n+1} = y_n + h · f(x_n, y_n).",
            "Distinguish between local truncation error O(h^2) and global accumulated error O(h).",
            "Understand the trade-off between step size h, computational effort, and numerical stability.",
        ],
        "prerequisites": [
            "First-order ordinary differential equations and Initial Value Problems (IVPs).",
            "Geometric interpretation of dy/dx as the instantaneous slope.",
            "Euler forward stepping and Taylor series approximation: y(x+h) ≈ y(x) + h y'(x).",
        ],
        "concept_summary": (
            "Euler's method is the simplest single-step numerical method for solving first-order ODEs. It assumes that the slope "
            "of the solution curve is constant over a small interval [x_n, x_n + h] and advances along the tangent line. Because "
            "curves bend away from their tangents, Euler's method accumulates truncation error linearly with h."
        ),
        "convergence_notes": (
            "Euler's method is a first-order method: halving the step size h approximately halves the global error (O(h)). "
            "For large step sizes or stiff equations, Euler's method can quickly become unstable or inaccurate."
        ),
    },
    "modified_euler": {
        "topic": "Differential Equations",
        "method_name": "Modified Euler Method (Heun's Predictor-Corrector)",
        "learning_objectives": [
            "Understand the predictor-corrector concept in numerical integration.",
            "Compute the predictor slope f_1 = f(x_n, y_n) and predictor value y^*_{n+1}.",
            "Evaluate the corrector slope f_2 = f(x_{n+1}, y^*_{n+1}) at the predicted endpoint.",
            "Calculate the average slope (f_1 + f_2)/2 to achieve second-order accuracy (Trapezoidal rule analogy).",
            "Compare accuracy and step-size efficiency against basic Euler's method.",
        ],
        "prerequisites": [
            "Standard Euler's method and slope calculation.",
            "Trapezoidal numerical integration rule.",
            "Second-order Taylor expansion.",
        ],
        "concept_summary": (
            "The Modified Euler method (also known as Heun's method) is a two-stage predictor-corrector scheme. It first uses "
            "an Euler step as a 'predictor' to estimate y at x_{n+1}. Then it evaluates the slope at this predicted point and "
            "uses the average of the initial and predicted slopes to compute the final 'corrected' y_{n+1}."
        ),
        "convergence_notes": (
            "Modified Euler is a second-order method: halving the step size h reduces the global error by approximately a factor "
            "of 4 (global error O(h^2)). It achieves much higher accuracy than standard Euler for only one extra function evaluation per step."
        ),
    },
    "rk4": {
        "topic": "Differential Equations",
        "method_name": "Runge-Kutta 4th-Order Method (RK4)",
        "learning_objectives": [
            "Understand why multi-stage slope sampling across the step interval [x_n, x_n + h] improves accuracy.",
            "Compute the initial slope k_1 at the start point (x_n, y_n).",
            "Compute the midpoint slopes k_2 and k_3 evaluated at x_n + h/2 using trial state increments.",
            "Compute the end slope k_4 evaluated at x_n + h.",
            "Apply the weighted Simpson average Δy = 1/6 (k_1 + 2k_2 + 2k_3 + k_4) to calculate y_{n+1}.",
            "Appreciate the fourth-order global accuracy O(h^4) and why RK4 is the engineering gold standard.",
        ],
        "prerequisites": [
            "Predictor-corrector methods and slope averaging.",
            "Simpson's 1/3 rule for numerical integration.",
            "Higher-order Taylor series expansions.",
        ],
        "concept_summary": (
            "The classical Fourth-Order Runge-Kutta method (RK4) is the workhorse of numerical ODE integration. By evaluating "
            "four strategic slopes—one at the beginning, two at the trial midpoint, and one at the trial end—and combining them "
            "using weights inspired by Simpson's 1/3 rule (1:2:2:1), RK4 achieves fourth-order accuracy without needing higher derivatives."
        ),
        "convergence_notes": (
            "RK4 is a fourth-order method: halving the step size h reduces the global error by approximately a factor of 16 (O(h^4)). "
            "This extraordinary balance of high accuracy, stability, and moderate computational cost makes it the preferred general-purpose solver."
        ),
    },
}


def get_concept_info(method_id: str) -> dict:
    """Retrieve concept dictionary for a method."""
    method = method_id.lower().replace("-", "_").replace(" ", "_")
    return METHOD_CONCEPTS.get(method, {
        "topic": "Numerical Methods",
        "method_name": method_id,
        "learning_objectives": ["Understand the numerical algorithm and convergence characteristics."],
        "prerequisites": ["Basic algebra and calculus."],
        "concept_summary": f"Numerical solution using {method_id}.",
        "convergence_notes": "Standard convergence properties apply.",
    })
