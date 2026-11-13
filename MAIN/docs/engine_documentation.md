# Engine Documentation

## SolverEngine

Single entry point for all eight NUMERIX algorithms.

```python
from numerix.engine.solver_engine import SolverEngine, ProblemRequest

engine = SolverEngine()
result = engine.solve(request)
```

### ProblemRequest fields

| Field | Type | Used by |
|---|---|---|
| `method` | `str` | All — one of the method IDs below |
| `expression` | `str` | Root finding, ODE — f(x) or f(x,y) string |
| `a` | `float` | Bisection, False Position — left bracket |
| `b` | `float` | Bisection, False Position — right bracket |
| `x0` | `float` | Newton-Raphson — initial guess |
| `tol` | `float` | Root finding — convergence tolerance (default 1e-6) |
| `max_iter` | `int` | Root finding — iteration limit (default 100) |
| `A` | `list[list[float]]` | Linear systems — coefficient matrix |
| `b_vec` | `list[float]` | Linear systems — RHS vector |
| `ode_x0` | `float` | ODE — initial x |
| `ode_y0` | `float` | ODE — initial y(x0) |
| `ode_h` | `float` | ODE — step size |
| `ode_x_end` | `float` | ODE — integration end point |

### Method IDs

| ID | Algorithm |
|---|---|
| `bisection` | Bisection Method |
| `false_position` | False Position (Regula Falsi) |
| `newton_raphson` | Newton-Raphson |
| `gauss_elimination` | Gauss Elimination with partial pivoting |
| `gauss_jordan` | Gauss-Jordan Elimination |
| `euler` | Euler Method |
| `modified_euler` | Modified Euler (Heun) |
| `rk4` | Runge-Kutta 4th Order |

---

## ComparisonEngine

Run multiple compatible methods on the same problem.

```python
from numerix.engine.solver_engine import ComparisonEngine, ProblemRequest

compare = ComparisonEngine()
results = compare.compare(
    methods=["bisection", "false_position", "newton_raphson"],
    req=ProblemRequest(
        expression="x**3 - x - 2",
        a=1.0, b=2.0, x0=1.5,
    ),
)
# results is dict[method_id -> SolverResult]
```

Methods must belong to the same family (root / linear / ODE).

---

## Expression Parser

```python
from numerix.core.expression_parser import (
    parse_function_x,   # single-variable f(x)
    parse_function_xy,  # two-variable f(x, y) for ODEs
    differentiate_x,    # symbolic derivative → numeric callable
)

expr, f = parse_function_x("x**3 - x - 2")
deriv_expr, df = differentiate_x(expr)
print(f(1.5), df(1.5))
```

### Allowed syntax

- Variables: `x` (root finding), `x` and `y` (ODE)
- Operators: `+  -  *  /  **`
- Functions: `sin  cos  tan  exp  log  sqrt  abs`
- Constants: `pi  e`
- Parentheses: `()`

### Rejected

- Any symbol other than the declared variables
- `__import__`, `eval`, `exec`, `open`, `compile`, `globals`, `locals`
- Empty strings, non-string inputs

---

## Validation

`numerix/core/validators.py` provides:

| Function | Validates |
|---|---|
| `validate_root_finding_bracket(a, b, fa, fb)` | a < b, sign change exists |
| `validate_tolerance(tol)` | tol > 0 and finite |
| `validate_max_iterations(max_iter)` | positive integer |
| `validate_matrix(A, b)` | square, matching dimensions, all finite |
| `validate_ode_params(x0, x_end, y0, h)` | all finite, h ≠ 0, h direction consistent |

All raise `ValueError` with a descriptive message.

---

## SolverStatus enum

| Status | Meaning |
|---|---|
| `CONVERGED` | Root-finding tolerance met |
| `SUCCESS` | Linear system solved |
| `MAX_ITERATIONS` | Iteration limit reached without convergence |
| `SINGULAR_MATRIX` | Pivot too small; system may have no unique solution |
| `ZERO_DERIVATIVE` | f'(x) ≈ 0 in Newton-Raphson |
| `INVALID_BRACKET` | Bracket does not contain a sign change |
| `INVALID_INPUT` | Input failed validation |
| `NON_FINITE` | Computation produced inf or NaN |
