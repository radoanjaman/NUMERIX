# Algorithm Reference

## Root Finding

### Bisection

**Formula:** midpoint = (a + b) / 2

**Error metric:** (b − a) / 2 (half-width of remaining interval)

**Termination:** error < tol, or f(mid) = 0, or max iterations

**Iteration record fields:** `a, b, mid, f_a, f_b, f_mid, approximate_error`

**Limitations:** Linear convergence (≈1 bit/step). May be slow near flat roots.

---

### False Position (Regula Falsi)

**Formula:** root = (a·f(b) − b·f(a)) / (f(b) − f(a))

**Error metric:** |root_new − root_old|

**Termination:** error < tol, or f(root) = 0, or max iterations

**Iteration record fields:** `a, b, f_a, f_b, root, f_root, approximate_error`

**Limitations:** Can stagnate (Illinois variant not implemented). Requires sign change.

---

### Newton-Raphson

**Formula:** x_{n+1} = x_n − f(x_n) / f'(x_n)

**Error metric:** |x_{n+1} − x_n|

**Termination:** error < tol, |f'(x)| < 1e-14, or max iterations

**Iteration record fields:** `x_n, f_xn, df_xn, x_new, approximate_error`

**Derivative:** Computed symbolically via SymPy from the user's expression string.

**Limitations:** Requires f'(x) ≠ 0. May diverge from bad initial guesses.

---

## Linear Systems

### Gauss Elimination

**Method:** Forward elimination with partial pivoting → upper triangular form → back-substitution

**Pivot strategy:** Swap rows so the largest absolute value in the pivot column is used

**Termination:** Singular matrix (pivot < 1e-14), or solution found

**Row operation record fields:** `type (swap|eliminate), row1/row2 or target_row/pivot_row/factor`

**Extra output:** `row_echelon_matrix`, `residual_vector`

**Residual:** ||Ax − b||₂ reported in metrics

---

### Gauss-Jordan

**Method:** Forward elimination + upward elimination → reduced row-echelon form

**Pivot strategy:** Partial pivoting (same as Gauss Elimination)

**Termination:** Singular matrix, or solution found

**Row operation record fields:** `type (swap|scale|eliminate)`

**Extra output:** `reduced_row_echelon_matrix`, `residual_vector`

---

## Ordinary Differential Equations

All ODE solvers integrate dy/dx = f(x, y) over [x0, x_end] with step size h.

### Euler

**Formula:** y_{n+1} = y_n + h·f(x_n, y_n)

**Order:** 1 (O(h) global error)

**Step record fields:** `x, y, slope, y_next, x_next`

---

### Modified Euler (Heun)

**Predictor:** y\* = y_n + h·f(x_n, y_n)

**Corrector:** y_{n+1} = y_n + (h/2)·[f(x_n, y_n) + f(x_{n+1}, y\*)]

**Order:** 2 (O(h²) global error)

**Step record fields:** `x, y, f1_slope, y_predictor, x_next, f2_slope, y_corrector`

---

### Runge-Kutta 4th Order (RK4)

**Formulas:**

```
k1 = h·f(x_n,       y_n)
k2 = h·f(x_n + h/2, y_n + k1/2)
k3 = h·f(x_n + h/2, y_n + k2/2)
k4 = h·f(x_n + h,   y_n + k3)
y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4) / 6
```

**Order:** 4 (O(h⁴) global error)

**Step record fields:** `x, y, k1, k2, k3, k4, y_next, x_next`

---

## Common Result Contract

```python
SolverResult(
    method: str,
    problem_type: str,          # "root_finding" | "linear_system" | "ode"
    status: SolverStatus,       # CONVERGED | SUCCESS | MAX_ITERATIONS | ...
    termination_reason: str,
    root: float | None,
    solution_vector: list[float] | None,
    ode_table: list[dict] | None,
    iterations: list[IterationRecord],
    metrics: SolverMetrics,
    extra: dict,
    warnings: list[str],
)

SolverMetrics(
    iterations: int,
    execution_time_seconds: float,
    final_approximate_error: float | None,
    final_residual: float | None,
    final_exact_error: float | None,
)
```
