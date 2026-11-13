# NUMERIX User Guide

## Launching the Application

```bash
cd e:\NUMERIX\MAIN
python main.py
```

The application opens a full-screen dark desktop window.

---

## Dashboard

The **Dashboard** is the home screen. It shows six module cards:

| Card | Description |
|---|---|
| Root Finding | Find roots of f(x) = 0 |
| Linear Systems | Solve Ax = b |
| Differential Equations | Solve dy/dx = f(x, y) |
| Comparison | Compare methods side-by-side |
| About | Project information |

**Click any card** to navigate to that module. You can also use the sidebar on the
left at any time.

---

## Root Finding

### Supported methods
- **Bisection** — bracket method, guaranteed convergence
- **False Position** (Regula Falsi) — bracket method, faster convergence
- **Newton-Raphson** — open method, requires initial guess, very fast near root

### Steps
1. Select a method from the **Method** drop-down.
2. Enter `f(x)` in the **Expression** field (e.g. `x**3 - x - 2`).
3. Set parameters:
   - **a, b** — bracket endpoints (bisection / false position)
   - **x₀** — initial guess (Newton-Raphson)
   - **Tolerance** — convergence criterion (default `1e-6`)
   - **Max iterations** — safety cap (default `100`)
4. Click **Run**.

### Reading results
- **Metrics row** — Root value, iteration count, final error, execution time, status
- **Iterations tab** — table of every step (columns depend on method)
- **Function Plot** — f(x) curve with root marker; bracket shown for bracketing methods
- **Error Plot** — approximate error vs. iteration (log scale)

### Expression syntax
```
x**2 - 4          polynomial
sin(x) - x/2      trigonometric
exp(x) - 3        exponential
log(x) - 1        logarithmic
sqrt(x) - 2       square root
pi * x - 1        using π constant
```

Allowed symbols: `x`, `+`, `-`, `*`, `/`, `**`, `sin`, `cos`, `tan`, `exp`,
`log`, `sqrt`, `abs`, `pi`, `e`.

---

## Linear Systems

### Supported methods
- **Gauss Elimination** — forward elimination + back substitution (partial pivoting)
- **Gauss-Jordan** — full elimination to reduced row echelon form (partial pivoting)

### Steps
1. Set **N** (system dimension, 2–10).
2. The matrix entry grid resizes automatically.
3. Fill in the **coefficient matrix A** and **right-hand-side vector b**.
4. Click **Run**.

### Reading results
- **Solution vector** — values x₁, x₂, … xₙ
- **Residual** — ‖Ax − b‖ (should be near zero)
- **Operations tab** — row operations performed (pivot selections, eliminations)

---

## Ordinary Differential Equations

### Supported methods
- **Euler** — first-order forward Euler
- **Modified Euler** (Heun) — predictor-corrector, second-order accurate
- **RK4** — Runge-Kutta 4th order, high accuracy

### Steps
1. Select a method.
2. Enter `dy/dx = f(x, y)` in the **Expression** field (e.g. `x + y`).
3. Set initial value problem (IVP):
   - **x₀** — initial x
   - **y₀** — initial y (y at x₀)
   - **h** — step size
   - **x end** — integration endpoint
4. Click **Run**.

### Reading results
- **Solution table** — x, y, and intermediate slopes (k values for RK4, predictors for Modified Euler)
- **Solution Curve** — y vs. x plot

---

## Comparison

Compare multiple methods on the same problem simultaneously.

### Steps
1. Select the **problem type** (Root Finding / Linear Systems / ODE).
2. Check the **methods** you want to compare (2 or more).
3. Enter shared inputs (expression, parameters) — same fields as the individual pages.
4. Click **Run Comparison**.

### Reading results
- One **result card** per method, showing root/solution/table
- **Metrics table** — iterations, final error, execution time for each method side-by-side

---

## Reading Iteration Tables

Each row in an iteration table represents one algorithm step.

### Root finding columns

| Method | Columns |
|---|---|
| Bisection | n, a, b, midpoint, f(mid), error |
| False Position | n, a, b, root, f(root), error |
| Newton-Raphson | n, xₙ, f(xₙ), f′(xₙ), x_new, error |

### ODE columns

| Method | Columns |
|---|---|
| Euler | n, x, y, slope, y_next |
| Modified Euler | n, x, y, f₁ (slope), y_pred, f₂ (corrected slope), y_corr |
| RK4 | n, x, y, k₁, k₂, k₃, k₄, y_next |

### Linear systems columns

| Column | Meaning |
|---|---|
| Op | Operation type (Pivot, Eliminate, etc.) |
| Description | Human-readable description of the row operation |

Numeric values are displayed to **8 significant figures**.

---

## Charts

### Function Plot (root finding)
- **Blue curve** — f(x) evaluated over the interval
- **Cyan dashed line** — y = 0 (zero axis)
- **Red dot** — found root
- **Shaded region** — current bracket (bisection / false position)

### Error Plot (root finding)
- X axis — iteration number
- Y axis — approximate error (log scale)
- Shows quadratic convergence of Newton-Raphson vs. linear for bracketing methods

### Solution Curve (ODE)
- X axis — independent variable x
- Y axis — y(x) solution
- Each point is one step of the numerical integration

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` (in any input field) | Run solver |
| `Escape` | Clear results |
| `Ctrl+C` | Copy selected table rows |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "Expression too long" | > 500 characters | Shorten expression |
| "Forbidden character" | `.`, `[`, `]`, or `;` in expression | Use valid math syntax |
| "Unsupported symbol" | Used a variable other than `x` (or `x, y`) | Only `x` is allowed in root finding |
| "Invalid bracket" | f(a) and f(b) have the same sign | Choose a, b so the root is bracketed |
| "Singular matrix" | Matrix has no unique solution | Check the system for linear dependence |
| "Zero derivative" | f′(x₀) = 0 at starting point | Choose a different x₀ |
| Import error on launch | Missing dependency | Run `pip install -r requirements.txt` |
