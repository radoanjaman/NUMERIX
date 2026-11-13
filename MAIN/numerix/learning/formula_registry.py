"""
Formula registry providing canonical mathematical formulas, LaTeX representations,
and variable definitions for all eight numerical methods.
"""
from __future__ import annotations

from numerix.learning.solution_models import FormulaCardModel, VariableDefinition


def get_formula_cards(method_id: str) -> list[FormulaCardModel]:
    """Retrieve governing mathematical formula cards for a given method."""
    method = method_id.lower().replace("-", "_").replace(" ", "_")
    
    if method == "bisection":
        return [
            FormulaCardModel(
                name="Bisection Midpoint Formula",
                latex=r"c = \frac{a + b}{2}",
                description="Computes the exact arithmetic midpoint of the current bracketing interval [a, b].",
                variables=[
                    VariableDefinition(symbol="a", name="Lower Bound", description="Current lower endpoint of the interval where f(a) has known sign."),
                    VariableDefinition(symbol="b", name="Upper Bound", description="Current upper endpoint of the interval where f(b) has opposite sign."),
                    VariableDefinition(symbol="c", name="Midpoint Estimate", description="Current numerical approximation of the root."),
                ],
            ),
            FormulaCardModel(
                name="Intermediate Value / Sign-Change Theorem",
                latex=r"f(a) \cdot f(b) < 0 \implies \exists \, r \in (a, b) : f(r) = 0",
                description="Guarantees the existence of at least one real root within a continuous interval if the function values at the endpoints have opposite signs.",
                variables=[
                    VariableDefinition(symbol="f(a)", name="Function at Lower Bound", description="Value of f evaluated at x = a."),
                    VariableDefinition(symbol="f(b)", name="Function at Upper Bound", description="Value of f evaluated at x = b."),
                ],
            ),
            FormulaCardModel(
                name="Theoretical Error Bound",
                latex=r"\epsilon_n = \frac{b_n - a_n}{2} = \frac{b_0 - a_0}{2^{n}}",
                description="Maximum theoretical distance from the midpoint c_n to the true root r after n iterations.",
                variables=[
                    VariableDefinition(symbol=r"\epsilon_n", name="Error Bound", description="Maximum absolute error at iteration n."),
                    VariableDefinition(symbol="n", name="Iteration Index", description="Number of bisection steps completed."),
                ],
            ),
        ]

    elif method == "false_position":
        return [
            FormulaCardModel(
                name="Regula Falsi (False Position) Formula",
                latex=r"c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)} = b - \frac{f(b)(b - a)}{f(b) - f(a)}",
                description="Finds the x-intercept of the secant line connecting points (a, f(a)) and (b, f(b)).",
                variables=[
                    VariableDefinition(symbol="a, b", name="Bracket Endpoints", description="Endpoints enclosing a root with f(a) · f(b) < 0."),
                    VariableDefinition(symbol="f(a), f(b)", name="Endpoint Values", description="Function values at the current bracket boundaries."),
                    VariableDefinition(symbol="c", name="Secant Intercept", description="New estimated root location."),
                ],
            ),
            FormulaCardModel(
                name="Secant Line Slope",
                latex=r"m = \frac{f(b) - f(a)}{b - a}",
                description="Slope of the chord connecting the two bracket points on the curve y = f(x).",
                variables=[
                    VariableDefinition(symbol="m", name="Secant Slope", description="Average rate of change over [a, b]."),
                ],
            ),
        ]

    elif method == "newton_raphson":
        return [
            FormulaCardModel(
                name="Newton-Raphson Iteration Formula",
                latex=r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}",
                description="Uses the tangent line at (x_n, f(x_n)) to project forward onto the x-axis to find the next approximation.",
                variables=[
                    VariableDefinition(symbol=r"x_n", name="Current Estimate", description="Approximation of the root at iteration n."),
                    VariableDefinition(symbol=r"f(x_n)", name="Function Value", description="Height of the curve at x_n."),
                    VariableDefinition(symbol=r"f'(x_n)", name="First Derivative", description="Slope of the tangent line at x_n. Must be non-zero."),
                    VariableDefinition(symbol=r"x_{n+1}", name="Next Estimate", description="Updated root approximation (tangent x-intercept)."),
                ],
            ),
            FormulaCardModel(
                name="Quadratic Convergence Relation",
                latex=r"|e_{n+1}| \approx \left| \frac{f''(r)}{2 f'(r)} \right| |e_n|^2",
                description="Near a simple root where f'(r) ≠ 0, the error is approximately squared at each iteration, doubling the number of correct digits.",
                variables=[
                    VariableDefinition(symbol=r"e_n", name="Error", description="Deviation from the exact root r: e_n = x_n - r."),
                ],
            ),
        ]

    elif method == "gauss_elimination":
        return [
            FormulaCardModel(
                name="Elementary Row Operation (Forward Elimination)",
                latex=r"R_j \leftarrow R_j - m_{j,i} \cdot R_i, \quad m_{j,i} = \frac{A_{j,i}}{A_{i,i}}",
                description="Eliminates the entry in column i of row j beneath the pivot element A_{i,i}.",
                variables=[
                    VariableDefinition(symbol="A_{i,i}", name="Pivot Element", description="Diagonal pivot element in row i, column i."),
                    VariableDefinition(symbol="m_{j,i}", name="Multiplier", description="Scaling factor used to cancel out subdiagonal element A_{j,i}."),
                    VariableDefinition(symbol="R_i, R_j", name="Matrix Rows", description="Pivot row R_i and target row R_j (j > i)."),
                ],
            ),
            FormulaCardModel(
                name="Partial Pivoting Criterion",
                latex=r"|A_{p,i}| = \max_{k \ge i} |A_{k,i}| \implies \text{Swap } R_i \leftrightarrow R_p",
                description="Selects the row with the largest absolute coefficient in the pivot column to minimize roundoff error.",
                variables=[
                    VariableDefinition(symbol="p", name="Pivot Row Index", description="Index of the row with maximal magnitude in column i."),
                ],
            ),
            FormulaCardModel(
                name="Back Substitution Formula",
                latex=r"x_i = \frac{b_i - \sum_{j=i+1}^n A_{i,j} x_j}{A_{i,i}}",
                description="Solves the upper triangular system sequentially starting from row n up to row 1.",
                variables=[
                    VariableDefinition(symbol="x_i", name="Unknown Variable", description="Component i of the solution vector x."),
                ],
            ),
        ]

    elif method == "gauss_jordan":
        return [
            FormulaCardModel(
                name="Pivot Normalization",
                latex=r"R_i \leftarrow \frac{R_i}{A_{i,i}}",
                description="Scales the entire pivot row so that the pivot element on the main diagonal becomes exactly 1.",
                variables=[
                    VariableDefinition(symbol="A_{i,i}", name="Pivot Value", description="Original diagonal coefficient in row i."),
                ],
            ),
            FormulaCardModel(
                name="Full Column Elimination (Above & Below)",
                latex=r"R_j \leftarrow R_j - A_{j,i} \cdot R_i \quad \forall \, j \ne i",
                description="Eliminates all other entries in column i (both above and below the pivot), driving the matrix toward the identity matrix I.",
                variables=[
                    VariableDefinition(symbol="A_{j,i}", name="Column Entry", description="Coefficient in row j, column i to be zeroed out."),
                ],
            ),
            FormulaCardModel(
                name="Reduced Row-Echelon Form (RREF)",
                latex=r"[A \mid b] \longrightarrow [I \mid x]",
                description="When elimination is complete, the coefficient matrix is the identity matrix I, and the augmented vector is the exact solution vector x.",
                variables=[
                    VariableDefinition(symbol="I", name="Identity Matrix", description="Diagonal matrix of ones with zeros elsewhere."),
                    VariableDefinition(symbol="x", name="Solution Vector", description="Directly readable solution: x_i = b_i."),
                ],
            ),
        ]

    elif method == "euler":
        return [
            FormulaCardModel(
                name="Forward Euler Step Formula",
                latex=r"y_{n+1} = y_n + h \cdot f(x_n, y_n)",
                description="Advances the numerical solution by taking a linear step along the tangent slope f(x_n, y_n).",
                variables=[
                    VariableDefinition(symbol=r"x_n, y_n", name="Current State", description="Known independent and dependent values at step n."),
                    VariableDefinition(symbol="h", name="Step Size", description="Distance between consecutive discrete mesh points: h = x_{n+1} - x_n."),
                    VariableDefinition(symbol=r"f(x_n, y_n)", name="Slope / Derivative", description="Rate of change dy/dx evaluated at the current state."),
                    VariableDefinition(symbol=r"y_{n+1}", name="Next Estimate", description="Approximation of the solution at x_{n+1}."),
                ],
            ),
            FormulaCardModel(
                name="Grid Point Update",
                latex=r"x_{n+1} = x_n + h",
                description="Advances the independent variable by one fixed increment h.",
                variables=[
                    VariableDefinition(symbol=r"x_{n+1}", name="Next Grid Point", description="Target abscissa for the current integration step."),
                ],
            ),
        ]

    elif method == "modified_euler":
        return [
            FormulaCardModel(
                name="Predictor Step (Euler Trial)",
                latex=r"y^*_{n+1} = y_n + h \cdot f(x_n, y_n)",
                description="Computes a preliminary predicted value of y at x_{n+1} using standard forward Euler.",
                variables=[
                    VariableDefinition(symbol=r"y^*_{n+1}", name="Predicted Value", description="Initial estimation of y at x_{n+1}."),
                    VariableDefinition(symbol=r"f_1 = f(x_n, y_n)", name="Initial Slope", description="Slope evaluated at the beginning of the interval."),
                ],
            ),
            FormulaCardModel(
                name="Corrector Step (Average Slope / Trapezoidal)",
                latex=r"y_{n+1} = y_n + \frac{h}{2} \left[ f(x_n, y_n) + f(x_{n+1}, y^*_{n+1}) \right]",
                description="Refines the estimate using the arithmetic average of the initial slope and the predicted end slope.",
                variables=[
                    VariableDefinition(symbol=r"f_2 = f(x_{n+1}, y^*_{n+1})", name="Corrector Slope", description="Derivative evaluated at the predicted state."),
                    VariableDefinition(symbol=r"\bar{f} = \frac{f_1 + f_2}{2}", name="Average Slope", description="Mean slope over the interval [x_n, x_{n+1}]."),
                    VariableDefinition(symbol=r"y_{n+1}", name="Corrected Value", description="Second-order accurate approximation of y at x_{n+1}."),
                ],
            ),
        ]

    elif method == "rk4":
        return [
            FormulaCardModel(
                name="Classical 4th-Order Runge-Kutta Scheme",
                latex=r"y_{n+1} = y_n + \frac{1}{6}\left(k_1 + 2k_2 + 2k_3 + k_4\right)",
                description="Advances the solution using a weighted Simpson-rule average of four distinct slope estimates across the step.",
                variables=[
                    VariableDefinition(symbol="k_1", name="Slope at Start", description=r"k_1 = h \cdot f(x_n, y_n)"),
                    VariableDefinition(symbol="k_2", name="Midpoint Slope 1", description=r"k_2 = h \cdot f\left(x_n + \frac{h}{2}, y_n + \frac{k_1}{2}\right)"),
                    VariableDefinition(symbol="k_3", name="Midpoint Slope 2", description=r"k_3 = h \cdot f\left(x_n + \frac{h}{2}, y_n + \frac{k_2}{2}\right)"),
                    VariableDefinition(symbol="k_4", name="End Slope", description=r"k_4 = h \cdot f\left(x_n + h, y_n + k_3\right)"),
                    VariableDefinition(symbol=r"\Delta y", name="Weighted Increment", description=r"\Delta y = \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)"),
                ],
            ),
        ]

    return []
