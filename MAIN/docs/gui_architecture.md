# GUI Architecture — NUMERIX Phase 2

## Overview

The NUMERIX Phase 2 desktop application is a **dark glass-inspired UI** built on
Python-native libraries that require no additional system installation beyond the
`requirements.txt` packages.

---

## Framework Stack

| Layer | Technology |
|---|---|
| Window / widgets | **Tkinter + ttk** (Python built-in) |
| Plots / charts | **Matplotlib** (TkAgg backend embedded in frames) |
| Numerical engine | NUMERIX Phase 1 `SolverEngine` |
| Safe math parser | SymPy-based `expression_parser` |

### Why Tkinter?

- Proposal-aligned: the original spec targets a "Glass Lab desktop" with no browser dependency.
- Zero extra install: Tkinter ships with CPython on all platforms.
- `ttk` provides themed widgets that accept full CSS-like style overrides for the dark theme.
- `matplotlib` integrates cleanly via `FigureCanvasTkAgg` and `NavigationToolbar2Tk`.

---

## Application Architecture

```
NumerixApp  (numerix/gui/app.py)
│
├── Sidebar  (components/sidebar.py)
│   └── navigation buttons → page routing
│
├── PageHeader  (components/header.py)
│
├── Page container  (tk.Frame, swapped on navigation)
│   ├── DashboardPage  (pages/dashboard.py)       — lazy-loaded
│   ├── RootFindingPage  (pages/root_finding.py)  — lazy-loaded
│   ├── LinearSystemsPage  (pages/linear.py)      — lazy-loaded
│   ├── ODEPage  (pages/ode.py)                   — lazy-loaded
│   ├── ComparisonPage  (pages/comparison.py)     — lazy-loaded
│   └── AboutPage  (pages/about.py)               — lazy-loaded
│
└── StatusBar  (components/status_bar.py)
```

### Page internals (root-finding example)

```
RootFindingPage
├── InputPanel (left)
│   ├── MethodSelector  (ttk.Combobox)
│   ├── ExpressionEntry  (ttk.Entry)
│   ├── ParameterFields  (a, b, x0, tol, max_iter)
│   └── RunButton → SolverController.run_async()
│
├── ResultPanel (right, ttk.Notebook)
│   ├── Tab: Metrics  (MetricsRow of MetricCards)
│   ├── Tab: Iterations  (IterationTable)
│   └── Tab: Charts  (RootPlotPanel)
│
└── SolverController
    ├── Builds ProblemRequest
    ├── Submits to worker thread
    └── On done → root.after(0, _on_result)
```

---

## Threading Model

All solver calls run on a **daemon worker thread** to keep the UI responsive:

```
Main thread (Tkinter event loop)
    │
    └─ RunButton pressed → SolverController.run_async()
            │
            └─ threading.Thread(target=_worker).start()
                    │
                    └─ SolverEngine.solve(req)   ← blocking
                            │
                            └─ result / exception
                                    │
                                    └─ root.after(0, _on_result)  ← back on main thread
                                            │
                                            └─ update widgets
```

`root.after(0, callback)` is the **only** safe way to update Tkinter widgets from a
non-main thread.  No shared state is mutated without this indirection.

---

## Visualization

Charts are **Matplotlib figures embedded in Tkinter frames** via `FigureCanvasTkAgg`:

```python
fig, ax = plt.subplots(facecolor=BG_MAIN)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill="both", expand=True)
```

The `RootPlotPanel` hosts a `ttk.Notebook` with two tabs:
- **Function Plot** — f(x) curve, zero-line, root marker, bracket shading
- **Error Plot** — approximate error per iteration (log scale)

The `ODEPlotPanel` hosts a single tab:
- **Solution Curve** — (x, y) values across the integration interval

All figure backgrounds match `BG_MAIN = "#0B1020"` for the seamless dark look.

---

## Theme System

`gui/theme/colors.py` — design tokens (hex strings + font tuples)  
`gui/theme/styles.py` — `apply_theme(root)` configures `ttk.Style` globally

Key style names:

| ttk Style | Purpose |
|---|---|
| `NX.TButton` | Standard dark button |
| `Accent.NX.TButton` | Cyan call-to-action button |
| `Danger.NX.TButton` | Red destructive action |
| `NX.Treeview` | Iteration table rows |

---

## Parser Security

The expression parser (`numerix/core/expression_parser.py`) uses a layered defence:

1. **Length limit** — rejects strings > 500 characters.
2. **Character blocklist** — rejects `.`, `[`, `]`, `;` before SymPy sees the string.
3. **Newline guard** — rejects `\n` / `\r`.
4. **Token blocklist** — rejects `__`, `import`, `eval`, `exec`, `open`, `compile`,
   `globals`, `locals`, `lambda`.
5. **SymPy parse** — `parse_expr` with an explicit `local_dict` of allowed names only.
6. **Type check** — result must be an instance of `sympy.Basic`.
7. **Symbol allowlist** — only `x` (or `x, y` for ODE) may appear as free symbols.

No `eval()` or `exec()` is ever called on user input.
