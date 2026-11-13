# NUMERIX — Product & UI Implementation Specification

> **Purpose:** Build NUMERIX as a distinctive, polished numerical-methods learning desktop application. Use the supplied UI reference PDF for broad interaction inspiration only. Do not reproduce its branding, layout pixel-for-pixel, colors, copy, icons, or proprietary visual identity.
>
> **Product identity:** NUMERIX  
> **Tagline:** Understand the Mathematics. Visualize the Process. Verify the Results.  
> **Primary platform:** Python desktop application  
> **Primary audience:** Students learning numerical methods in a university laboratory  
> **Design direction:** Premium glassmorphism, scientific workspace, calm and precise, highly readable.

---

## 1. Product vision

NUMERIX is an interactive numerical-methods workbench, not a generic calculator. A student should be able to:

1. Choose a topic from the Numerical Methods Laboratory.
2. Enter an equation, matrix, or differential equation using a friendly math-entry experience.
3. Select a numerical method and configure its parameters.
4. Run the calculation.
5. Inspect the mathematical process step by step.
6. Explore interactive graphs and numerical tables.
7. Compare methods on the same problem.
8. Save, revisit, and export the work.

The reference PDF suggests useful interaction patterns: a prominent problem-entry area, mathematical symbol controls, topic navigation, expandable worked steps, a graph view, and contextual help. Reinterpret these as a cohesive NUMERIX experience with its own information architecture and glass visual language.

## 2. Product principles

- **Learning before answer:** Show how a result is obtained, not only the final number.
- **Transparent computation:** Every iteration, row operation, or ODE stage must be inspectable.
- **One consistent workspace:** All numerical modules share familiar input, result, graph, and comparison patterns.
- **Accurate and honest:** Clearly distinguish approximate error, residual, exact error (when an exact solution is known), and execution time.
- **Progressive disclosure:** Keep the initial view calm; reveal advanced parameters and detailed derivations when requested.
- **Responsive desktop layout:** Prioritize desktop use, but adapt gracefully to smaller windows.
- **Accessible glassmorphism:** Translucency is decorative; text, controls, focus states, and charts must remain high contrast.

## 3. Core feature scope

### 3.1 Required numerical modules

#### A. Root Finding

Implement:
- Bisection Method
- False Position (Regula Falsi) Method
- Newton–Raphson Method

Inputs:
- Function `f(x)`
- Interval `[a, b]` for bracketing methods
- Initial guess `x0` for Newton–Raphson
- Tolerance
- Maximum iterations
- Optional display range for plotting

Results:
- Approximate root
- Function value at the approximate root
- Iteration count
- Convergence status and termination reason
- Approximate absolute error and relative approximate error where defined
- Execution time
- Full iteration history

Iteration details:
- Bisection: `a`, `b`, midpoint, `f(a)`, `f(b)`, `f(mid)`, updated interval, error.
- False Position: `a`, `b`, `f(a)`, `f(b)`, estimated root, `f(root)`, updated interval, error.
- Newton–Raphson: `x_n`, `f(x_n)`, `f'(x_n)`, `x_(n+1)`, error.

Validation:
- Bracketing methods must verify a valid sign change, with a clear explanation if the interval does not bracket a root.
- Newton–Raphson must detect a zero or near-zero derivative.
- Detect invalid expressions, non-finite values, and iteration-limit termination.

Visualizations:
- Function curve and x-axis
- Root marker
- Initial bracket / interval evolution where applicable
- Newton tangent and iteration markers where practical
- Error versus iteration chart

#### B. Linear Systems

Implement:
- Gaussian Elimination with partial pivoting
- Gauss–Jordan Elimination

Inputs:
- Matrix dimension
- Coefficient matrix `A`
- Right-hand-side vector `b`
- Optional pivoting configuration if supported

Results:
- Solution vector when a unique solution exists
- Transformed / augmented matrices
- Every elementary row operation
- Pivot information
- Residual vector and residual norm
- Execution time
- Clear status for singular or underdetermined systems

Interaction:
- Provide a dynamic matrix editor with add/remove row-column controls.
- Allow keyboard navigation between cells.
- Provide a small set of sample systems.
- Show row operations in an ordered, expandable operation timeline.

Visualizations:
- Matrix snapshots after each major operation
- Highlight pivot row, pivot element, and elimination target
- Optional residual/error summary

#### C. Ordinary Differential Equations (ODE)

Implement:
- Euler Method
- Modified Euler Method (Heun / predictor-corrector, with the chosen convention documented)
- Fourth-Order Runge–Kutta (RK4)

Inputs:
- Differential equation `dy/dx = f(x, y)`
- Initial values `x0`, `y0`
- Step size `h`
- Final x-value or number of steps
- Optional exact solution for comparison

Results:
- Table of `n`, `x_n`, `y_n`
- Method-specific intermediate values
- For Euler: slope and next estimate
- For Modified Euler: predictor, predicted slope, corrected estimate
- For RK4: `k1`, `k2`, `k3`, `k4`, and next estimate
- Exact value and error only when an exact solution is supplied or safely derived
- Execution time and completion status

Visualizations:
- Numerical solution curve
- Exact solution overlay when available
- Numerical sample points
- Error versus x when exact values are available
- Optional comparison of Euler, Modified Euler, and RK4 on one problem

### 3.2 Shared learning and analysis features

- Step-by-step worked solution with expandable/collapsible steps.
- A concise explanation of the purpose of each iteration or row operation.
- Formula panel showing the method's mathematical formula.
- Iteration / operation table with sortable columns where appropriate.
- Function and solution graph panels.
- Method comparison workspace.
- Error analysis panel.
- Execution-time measurement using a monotonic high-resolution timer.
- Sample problem library.
- Calculation history with reopen and duplicate actions.
- Export selected result to CSV; PDF report can be added as a follow-on feature.
- Help panel with topic overview, formula, assumptions, and common input mistakes.
- Clear empty, loading, success, warning, and error states.

### 3.3 Recommended later enhancements

Keep these out of the first milestone unless time allows:
- Secant method
- LU Decomposition
- Trapezoidal and Simpson's numerical integration
- PDF laboratory report generation
- Additional ODE systems
- User-defined exact solution comparison
- Dark/light theme toggle (the initial theme should be dark)
- Keyboard shortcuts and command palette

---

## 4. Unique NUMERIX visual identity

### 4.1 Design concept: “Glass Lab”

Create a premium scientific workspace with layered translucent surfaces, subtle depth, soft glows, and precise data typography. It should feel like a modern instrument panel or research workstation—not a clone of the reference website.

### 4.2 Color direction

Use a deep midnight blue / graphite background with restrained cyan and violet accents.

Suggested tokens (adjust for visual harmony):
- App background: `#08111F`
- Secondary background: `#0D1A2B`
- Glass surface: `rgba(20, 36, 58, 0.62)`
- Elevated glass: `rgba(31, 51, 77, 0.72)`
- Glass border: `rgba(180, 215, 245, 0.16)`
- Primary text: `#F1F6FC`
- Secondary text: `#A7B7CA`
- Muted text: `#71839A`
- Cyan accent: `#57D7E8`
- Violet accent: `#9B8CFF`
- Success: `#55D6A5`
- Warning: `#F5C36A`
- Error: `#FF7185`

Use accent gradients sparingly, for example cyan-to-violet on primary actions or active navigation. Avoid large saturated red headers.

### 4.3 Glassmorphism rules

- Use translucent panels with subtle background blur where the GUI framework supports it.
- Add a thin low-opacity border and soft shadow to distinguish panel edges.
- Use layered surfaces: app background, main glass panels, elevated cards, and floating overlays.
- Keep blur moderate; do not sacrifice text clarity.
- Avoid applying transparency to text or essential controls.
- Use consistent corner radii: 10–14 px for controls, 16–22 px for cards, 24 px for major panels.
- Use restrained ambient radial glows behind the main workspace, not behind every component.
- Use micro-interactions: short fades, subtle hover lift, animated progress, and smooth panel transitions. Respect reduced-motion preferences if supported.

### 4.4 Typography

- Use a clean sans-serif UI font such as Inter, Segoe UI, or a reliable system fallback.
- Use a monospaced font for numerical values, matrices, code-like expressions, and iteration data.
- Mathematical expressions should be rendered cleanly and consistently. Use SymPy LaTeX output with a suitable math renderer if practical; otherwise use a safe, readable formatted-text fallback.
- Establish clear hierarchy: page title, section title, card title, label, helper text, and numeric result.
- Use tabular numerals for aligned metrics.

### 4.5 Iconography

Use one consistent line-icon family. Icons must be paired with labels in navigation where possible. Do not use emoji as primary interface icons. Provide tooltips for icon-only controls.

---

## 5. Application information architecture

### Main application shell

Use a three-part desktop shell:

1. **Left navigation rail / sidebar** — persistent topic navigation.
2. **Central work area** — problem entry, results, worked steps, and graphs.
3. **Optional contextual inspector** — method help, parameter explanation, and selected-step details. It can collapse to give the central workspace more room.

Suggested sidebar:

- NUMERIX logo and compact product mark
- Overview
- Root Finding
  - Bisection
  - False Position
  - Newton–Raphson
- Linear Systems
  - Gauss Elimination
  - Gauss–Jordan
- Differential Equations
  - Euler
  - Modified Euler
  - RK4
- Compare Methods
- Calculation History
- Learning Center
- Settings / About

The sidebar should show active state with a subtle glass highlight and accent indicator, not a large solid color block.

### Top bar

- Current page / breadcrumb
- Global quick search or command entry (optional)
- Theme / settings access
- Help button
- Window controls handled appropriately by the desktop framework

### Dashboard

The dashboard should include:
- Greeting and concise “Start a calculation” prompt
- Three large module cards
- A “Continue recent work” area
- Recently used methods
- A small learning tip / method of the day
- Quick access to sample problems

Do not overload the dashboard with fake statistics. If there is no history yet, show a helpful empty state.

---

## 6. Main solver workspace layout

Use a distinctive NUMERIX layout inspired by scientific IDEs:

### A. Problem composer (top section)

A wide, elevated glass panel containing:
- Module and method title
- Equation / matrix input
- Math symbol helper toolbar when useful
- Parameter fields
- Sample problem selector
- Primary “Run Calculation” button
- Secondary “Reset” and “Load Example” actions

For equation input:
- Accept clear Python-style expressions such as `x**3 - x - 2`.
- Show supported syntax beside the input.
- Provide symbol buttons for common operators, powers, parentheses, pi, and common functions.
- Do not execute arbitrary Python code.
- Include inline validation and actionable error messages.

### B. Result overview

After a successful run, show a row or grid of compact metric cards:
- Approximate solution
- Iterations / steps
- Final approximate error
- Execution time
- Status

Metrics must be context-aware. For example, a matrix solver should show residual norm rather than an irrelevant root error.

### C. Worked solution panel

This is a signature NUMERIX feature.

Display each iteration as a numbered glass card or row:
- Step number and short title
- Formula used
- Substituted values
- Calculated result
- Short plain-language explanation
- Expand/collapse control for full details

Provide:
- “Expand all” / “Collapse all”
- Previous / next step navigation (optional)
- Current step highlight
- Copy value / copy equation action where useful

Do not invent explanations. The explanation templates must correspond to the actual calculation data returned by the algorithm.

### D. Visualization panel

Use tabs or segmented controls:
- Function / Solution Graph
- Error Analysis
- Iteration Data

Graph requirements:
- Axis labels, units where relevant, legend, and grid
- Zoom and pan where supported
- Hover / cursor readout where supported
- Clear markers for numerical points and roots
- Responsive resizing
- A reset-view control
- Avoid decorative chart effects that obscure numerical meaning

### E. Contextual learning inspector

A collapsible right-side panel can show:
- Method description
- Formula
- When to use it
- Convergence notes
- Common failure cases
- Selected iteration explanation

The inspector is a learning aid, not an AI chatbot dependency. The app must work fully offline without a network connection.

---

## 7. Method comparison workspace

Create a dedicated comparison page.

Workflow:
1. Choose a problem type.
2. Enter one shared problem.
3. Select two or more compatible methods.
4. Run methods with shared stopping conditions where meaningful.
5. Display a side-by-side result table.
6. Overlay solution/convergence graphs where meaningful.
7. Explain differences in convergence and accuracy.

Comparison table fields:
- Method
- Approximate solution
- Iterations / steps
- Final approximate error
- Residual or exact error when applicable
- Execution time
- Convergence status

Important:
- Do not compare incompatible metrics as if they were equivalent.
- Explain that execution time can vary with machine load and should be interpreted as an approximate measurement.
- Use the same problem and equivalent stopping conditions for fair comparisons.
- For methods with different iteration structures, label the count accurately.

---

## 8. Input and parsing requirements

### Safe expression parsing

- Never use unrestricted `eval()` or `exec()` on user-entered expressions.
- Prefer a restricted SymPy parser or a custom allowlisted parser.
- Permit only supported symbols, constants, operators, and mathematical functions.
- Validate the expression before computation and before plotting.
- Handle domain errors and non-finite values.
- For root finding, use `x` as the independent variable.
- For ODEs, use only `x` and `y` as declared variables.
- Provide clear examples of supported syntax.

### Matrix input

- Validate dimensions and numeric cells.
- Detect incomplete cells.
- Distinguish singular, inconsistent, and potentially underdetermined systems where the implementation can establish this reliably.
- Preserve the original matrix and each transformed matrix in the result history.

### Parameter validation

- Tolerance must be positive.
- Maximum iteration count must be a positive integer.
- Step size must be nonzero and have a direction consistent with the integration interval.
- Validate all initial values and interval bounds.
- Prevent application freezes from extreme input sizes or excessive iteration counts.

---

## 9. Technical architecture

Keep algorithms independent of the GUI.

Recommended architecture:

```text
NUMERIX/
├── main.py
├── requirements.txt
├── README.md
├── config/
│   └── theme.py
├── core/
│   ├── expression_parser.py
│   ├── validators.py
│   ├── result_models.py
│   ├── error_metrics.py
│   └── timing.py
├── algorithms/
│   ├── root_finding/
│   │   ├── bisection.py
│   │   ├── false_position.py
│   │   └── newton_raphson.py
│   ├── linear_systems/
│   │   ├── gauss_elimination.py
│   │   └── gauss_jordan.py
│   └── ode/
│       ├── euler.py
│       ├── modified_euler.py
│       └── rk4.py
├── services/
│   ├── solver_service.py
│   ├── comparison_service.py
│   ├── history_service.py
│   └── export_service.py
├── ui/
│   ├── app_shell.py
│   ├── navigation.py
│   ├── dashboard.py
│   ├── components/
│   │   ├── glass_card.py
│   │   ├── math_input.py
│   │   ├── parameter_form.py
│   │   ├── metric_card.py
│   │   ├── step_card.py
│   │   ├── data_table.py
│   │   └── graph_panel.py
│   └── pages/
│       ├── root_finding_page.py
│       ├── linear_systems_page.py
│       ├── ode_page.py
│       ├── comparison_page.py
│       ├── history_page.py
│       └── learning_page.py
├── visualization/
│   ├── root_plot.py
│   ├── convergence_plot.py
│   ├── matrix_visualizer.py
│   └── ode_plot.py
├── storage/
│   └── history.json
├── tests/
│   ├── test_root_finding.py
│   ├── test_linear_systems.py
│   ├── test_ode.py
│   ├── test_parser.py
│   └── test_validation.py
└── docs/
    └── algorithms.md
```

### Framework recommendation

Preferred option for a highly polished glassmorphism desktop UI:
- **PySide6 (Qt)** for the desktop interface, custom widgets, layouts, animation, and native desktop behavior.
- **Matplotlib** embedded for scientific plots.
- **NumPy** for numerical arrays and matrix operations.
- **SymPy** for safe symbolic parsing, differentiation, and optional exact solutions.
- **pytest** for testing.
- **JSON / CSV** for local history and export.

If the existing project is already committed to Tkinter, preserve Tkinter rather than silently rewriting the entire stack. However, PySide6 is the recommended choice if the visual design quality and custom glass-like surfaces are a priority. Confirm the existing repository structure before changing frameworks.

### Common result contract

Each algorithm should return structured data rather than print to the console.

Example contract (adapt fields to each problem type):

```python
{
    "method": "Bisection",
    "problem_type": "root_finding",
    "solution": 1.52138,
    "iterations": [],
    "converged": True,
    "termination_reason": "tolerance_reached",
    "approximate_error": 0.00001,
    "residual": None,
    "exact_error": None,
    "execution_time_seconds": 0.0005,
    "warnings": []
}
```

Each iteration should include raw numeric values and method-specific details. The UI layer formats them for display; the algorithm layer must not contain UI code.

---

## 10. Data and numerical correctness requirements

- Use a high-resolution monotonic timer such as `time.perf_counter()` for elapsed time.
- Keep unrounded floating-point values internally; round only for display.
- Clearly define the approximate error formula used by each method.
- Avoid division by zero when computing relative approximate error.
- For linear systems, calculate and report residual `r = A x - b` and an appropriate norm.
- For ODEs, calculate exact error only if an exact reference solution is genuinely available.
- Do not label residual as exact error.
- Do not claim convergence unless the stopping condition has actually been met.
- Return termination reasons such as tolerance reached, maximum iterations, invalid bracket, derivative too small, singular matrix, or invalid input.
- Add unit tests for standard examples and edge cases.
- Compare matrix solutions against trusted NumPy results in tests, not as a replacement for teaching implementations.
- Keep the educational algorithm implementation explicit; do not call a black-box solver for the main method being demonstrated.

Suggested verification examples:
- Root finding: `f(x) = x**3 - x - 2`, bracket `[1, 2]`, known root approximately `1.52138`.
- Linear system: use a small nonsingular 3×3 system with a known solution and verify `A @ x` is close to `b`.
- ODE: `dy/dx = x + y`, `y(0) = 1`, compare Euler, Modified Euler, and RK4 with the exact solution when configured.

---

## 11. Interaction and motion design

- Sidebar navigation changes should be smooth and immediate.
- Primary action has a clear hover, pressed, disabled, and loading state.
- While a calculation runs, show progress or a lightweight busy state without freezing the interface.
- Worked steps expand and collapse smoothly.
- Graph tabs switch without losing the calculation result.
- Tooltips explain specialist terms.
- Keyboard focus must be visible.
- Enter may submit a focused equation form; Escape should close transient overlays.
- Provide confirmation before clearing unsaved work.
- Use non-blocking notifications for success and recoverable errors.
- Keep animations short and subtle; do not animate numerical data in a way that makes it difficult to read.

---

## 12. Accessibility and usability

- Maintain readable contrast on every glass surface.
- Never use color alone to communicate success, failure, or convergence.
- Pair status colors with labels and icons.
- Support keyboard navigation across forms, tables, and navigation.
- Provide descriptive labels and validation messages.
- Ensure the layout remains usable at common laptop resolutions.
- Allow panels to collapse when screen width is limited.
- Use clear numeric formatting and consistent significant digits.
- Include units or variable labels wherever applicable.

---

## 13. Suggested implementation milestones

### Milestone 1 — Repository audit and algorithm integration
- Inspect the existing source files and dependencies.
- Preserve and refactor the existing seven lab scripts.
- Implement RK4.
- Create common result and iteration data models.
- Add tests for all eight algorithms.

### Milestone 2 — Design system and app shell
- Establish theme tokens, typography, spacing, and glass surfaces.
- Build the main window, sidebar, top bar, and dashboard.
- Implement reusable cards, buttons, fields, tabs, and notifications.

### Milestone 3 — Solver workspaces
- Build Root Finding, Linear Systems, and ODE pages.
- Add validated input forms and sample problems.
- Connect pages to the algorithm services.

### Milestone 4 — Worked solutions and visualizations
- Add iteration/row-operation cards and tables.
- Embed Matplotlib graphs.
- Add method-specific formula and explanation panels.

### Milestone 5 — Comparison, history, and export
- Add comparison workspace.
- Add local calculation history.
- Add CSV export; PDF export may follow.

### Milestone 6 — QA and polish
- Test all methods and edge cases.
- Verify responsive behavior and accessibility.
- Fix UI inconsistencies and performance problems.
- Prepare a runnable application and user guide.

---

## 14. Acceptance criteria

The first complete release is ready when:

- [ ] The application launches into a polished NUMERIX dashboard.
- [ ] The visual design consistently uses the NUMERIX Glass Lab identity.
- [ ] All eight required algorithms are accessible from the interface.
- [ ] All algorithms run from parameterized functions, not hard-coded examples.
- [ ] User expressions are parsed safely without unrestricted Python execution.
- [ ] Each solver shows a final result and full method-specific iteration history.
- [ ] Root-finding pages show the function and convergence behavior.
- [ ] Linear-system pages show row operations and residual verification.
- [ ] ODE pages show numerical values and RK4 intermediate slopes.
- [ ] Error and timing metrics are correctly defined and labeled.
- [ ] Method comparison uses the same input problem and meaningful metrics.
- [ ] Invalid inputs produce understandable messages without crashing the app.
- [ ] Calculation history can be revisited.
- [ ] Automated tests cover normal and edge cases.
- [ ] The application works without requiring an internet connection.

---

## 15. Instructions to the implementation agent

1. First inspect the entire existing project repository, including the uploaded Python scripts and dependency files.
2. Do not delete working numerical algorithms or replace them with black-box library solvers.
3. Map existing scripts to the eight required methods and identify missing functionality before coding.
4. Implement the missing RK4 method and refactor all algorithms behind a consistent service interface.
5. Confirm the current GUI framework before deciding whether to retain Tkinter or migrate to PySide6. Prefer PySide6 for the proposed polished desktop UI only if migration is practical and does not discard working project logic.
6. Build the design system and reusable components before creating every page independently.
7. Treat the supplied reference PDF as inspiration for useful workflows only. Create an original NUMERIX layout, palette, component language, labels, and visual identity.
8. Prioritize a complete working vertical slice: launch app → choose method → enter problem → solve → inspect steps → view graph.
9. Then complete the remaining methods, comparison, history, and export.
10. Run tests after each major integration. Do not mark a feature complete until it works.
11. Do not create fake result data in the real application. Sample/demo states must be clearly identified as examples.
12. Keep code modular, documented, and maintainable. Update README and requirements.
13. If a requirement is ambiguous, inspect the existing code and this specification first; make the smallest sensible decision and document it.

**Final design target:** A distinctive, dark glassmorphism scientific workspace with a compact navigation sidebar, luminous but restrained accents, a focused mathematical problem composer, elegant worked-step cards, precise tables, and interactive scientific graphs. The overall experience should feel like a premium learning instrument built specifically for numerical methods.
