"""
NUMERIX Method Comparison Page — side-by-side benchmark across numerical algorithms.
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from typing import Any

from numerix.core.expression_parser import parse_function_x
from numerix.core.result_models import SolverResult, SolverStatus
from numerix.engine.solver_engine import ComparisonEngine, ProblemRequest
from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    ACCENT_VIOLET,
    BG_ELEVATED,
    BG_MAIN,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    ERROR,
    FONT_HEADING,
    FONT_MONO,
    FONT_SUBHEADING,
    FONT_UI,
    FONT_UI_BOLD,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)
from numerix.gui.visualization.ode_plots import ODEPlotPanel


class ComparisonPage(tk.Frame):
    """Multi-tab workspace to compare methods for Root Finding, ODEs, and Linear Systems."""

    def __init__(self, parent: tk.Widget, status_bar=None, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, padx=16, pady=12, **kwargs)
        self._status_bar = status_bar
        self._comp_engine = ComparisonEngine()
        self._is_running = False
        self._build()

    def _build(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky="nsew")

        # Tab 1: Root Finding
        self._root_tab = tk.Frame(notebook, bg=BG_SECONDARY, padx=12, pady=12)
        notebook.add(self._root_tab, text="  Root Finding Comparison  ")
        self._build_root_tab()

        # Tab 2: Differential Equations
        self._ode_tab = tk.Frame(notebook, bg=BG_SECONDARY, padx=12, pady=12)
        notebook.add(self._ode_tab, text="  ODE Comparison  ")
        self._build_ode_tab()

        # Tab 3: Linear Systems
        self._linear_tab = tk.Frame(notebook, bg=BG_SECONDARY, padx=12, pady=12)
        notebook.add(self._linear_tab, text="  Linear Systems Comparison  ")
        self._build_linear_tab()

    # ── TAB 1: ROOT FINDING ────────────────────────────────────────────────────
    def _build_root_tab(self) -> None:
        self._root_tab.columnconfigure(0, weight=0, minsize=360)
        self._root_tab.columnconfigure(1, weight=1)
        self._root_tab.rowconfigure(0, weight=1)

        left = tk.Frame(self._root_tab, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(left, text="Compare Root Solvers", font=FONT_SUBHEADING, fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w")

        tk.Label(left, text="f(x) =", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(8, 2))
        self._r_expr_var = tk.StringVar(value="x**3 - x - 2")
        tk.Entry(
            left, textvariable=self._r_expr_var, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(fill=tk.X, pady=(0, 8), ipady=3)

        row_b = tk.Frame(left, bg=BG_PANEL)
        row_b.pack(fill=tk.X, pady=(0, 8))
        tk.Label(row_b, text="Bracket [a, b]:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._r_a_var = tk.StringVar(value="1.0")
        tk.Entry(row_b, textvariable=self._r_a_var, width=6, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=4)
        self._r_b_var = tk.StringVar(value="2.0")
        tk.Entry(row_b, textvariable=self._r_b_var, width=6, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=4)

        row_x0 = tk.Frame(left, bg=BG_PANEL)
        row_x0.pack(fill=tk.X, pady=(0, 10))
        tk.Label(row_x0, text="Newton x0:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._r_x0_var = tk.StringVar(value="1.5")
        tk.Entry(row_x0, textvariable=self._r_x0_var, width=8, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=6)

        # Checkboxes
        tk.Label(left, text="Select Methods:", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(4, 2))
        self._r_bisection_chk = tk.BooleanVar(value=True)
        self._r_falsepos_chk = tk.BooleanVar(value=True)
        self._r_newton_chk = tk.BooleanVar(value=True)

        tk.Checkbutton(left, text="Bisection", variable=self._r_bisection_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")
        tk.Checkbutton(left, text="False Position", variable=self._r_falsepos_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")
        tk.Checkbutton(left, text="Newton-Raphson", variable=self._r_newton_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")

        self._r_val_var = tk.StringVar(value="")
        tk.Label(left, textvariable=self._r_val_var, font=FONT_UI, fg=ERROR, bg=BG_PANEL, wraplength=320, justify=tk.LEFT).pack(fill=tk.X, pady=(6, 6))

        self._btn_r_run = ttk.Button(left, text="▶ Run Root Comparison", style="Accent.NX.TButton", command=self._on_run_root_comp)
        self._btn_r_run.pack(anchor="w", pady=(4, 0))

        # Right: Comparison Table
        right = tk.Frame(self._root_tab, bg=BG_SECONDARY)
        right.grid(row=0, column=1, sticky="nsew")

        cols = ["Method", "Root", "f(Root)", "Final Error", "Iterations", "Time (s)", "Status"]
        self._r_tree = ttk.Treeview(right, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            w = 120 if c not in ("Iterations", "Time (s)") else 80
            self._r_tree.heading(c, text=c, anchor=tk.CENTER)
            self._r_tree.column(c, width=w, anchor=tk.CENTER)
        self._r_tree.pack(fill=tk.BOTH, expand=True)

    def _on_run_root_comp(self) -> None:
        methods = []
        if self._r_bisection_chk.get():
            methods.append("bisection")
        if self._r_falsepos_chk.get():
            methods.append("false_position")
        if self._r_newton_chk.get():
            methods.append("newton_raphson")

        if not methods:
            self._r_val_var.set("Please select at least one method.")
            return

        try:
            req = ProblemRequest(
                expression=self._r_expr_var.get().strip(),
                a=float(self._r_a_var.get()),
                b=float(self._r_b_var.get()),
                x0=float(self._r_x0_var.get()),
                tol=1e-6,
                max_iter=100,
            )
        except ValueError as exc:
            self._r_val_var.set(f"Invalid input: {exc}")
            return

        self._r_val_var.set("")
        self._r_tree.delete(*self._r_tree.get_children())
        if self._status_bar:
            self._status_bar.set_running("Root Comparison")

        def worker():
            try:
                results = self._comp_engine.compare(methods, req)
                self.after(0, lambda: self._on_root_comp_done(results, req.expression))
            except Exception as exc:
                self.after(0, lambda: self._r_val_var.set(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_root_comp_done(self, results: dict[str, SolverResult], expr_str: str) -> None:
        try:
            _, f_eval = parse_function_x(expr_str)
        except Exception:
            f_eval = None

        for m_id, res in results.items():
            name = res.method
            root_str = f"{res.root:.8g}" if res.root is not None else "—"
            f_val = f"{f_eval(res.root):.6e}" if (f_eval and res.root is not None) else "—"
            err = f"{res.metrics.final_approximate_error:.6e}" if res.metrics.final_approximate_error is not None else "—"
            it = str(res.metrics.iterations)
            t = f"{res.metrics.execution_time_seconds:.4f}"
            st = res.status.value
            self._r_tree.insert("", tk.END, values=[name, root_str, f_val, err, it, t, st])

        if self._status_bar:
            self._status_bar.set_done("Root comparison completed")

    # ── TAB 2: ODE COMPARISON ──────────────────────────────────────────────────
    def _build_ode_tab(self) -> None:
        self._ode_tab.columnconfigure(0, weight=0, minsize=360)
        self._ode_tab.columnconfigure(1, weight=1)
        self._ode_tab.rowconfigure(0, weight=1)

        left = tk.Frame(self._ode_tab, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(left, text="Compare ODE Solvers", font=FONT_SUBHEADING, fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w")

        tk.Label(left, text="dy/dx = f(x, y)", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(8, 2))
        self._ode_expr_var = tk.StringVar(value="x + y")
        tk.Entry(left, textvariable=self._ode_expr_var, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(fill=tk.X, pady=(0, 8), ipady=3)

        r1 = tk.Frame(left, bg=BG_PANEL)
        r1.pack(fill=tk.X, pady=(0, 6))
        tk.Label(r1, text="x0:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._ode_x0_var = tk.StringVar(value="0.0")
        tk.Entry(r1, textvariable=self._ode_x0_var, width=6, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=4)
        tk.Label(r1, text="y0:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT, padx=(6, 0))
        self._ode_y0_var = tk.StringVar(value="1.0")
        tk.Entry(r1, textvariable=self._ode_y0_var, width=6, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=4)

        r2 = tk.Frame(left, bg=BG_PANEL)
        r2.pack(fill=tk.X, pady=(0, 10))
        tk.Label(r2, text="h:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._ode_h_var = tk.StringVar(value="0.1")
        tk.Entry(r2, textvariable=self._ode_h_var, width=6, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=4)
        tk.Label(r2, text="End x:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT, padx=(6, 0))
        self._ode_xend_var = tk.StringVar(value="0.5")
        tk.Entry(r2, textvariable=self._ode_xend_var, width=6, font=FONT_MONO, bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=4)

        # Checkboxes
        tk.Label(left, text="Select Methods:", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(4, 2))
        self._o_euler_chk = tk.BooleanVar(value=True)
        self._o_modeuler_chk = tk.BooleanVar(value=True)
        self._o_rk4_chk = tk.BooleanVar(value=True)

        tk.Checkbutton(left, text="Euler (Order 1)", variable=self._o_euler_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")
        tk.Checkbutton(left, text="Modified Euler (Order 2)", variable=self._o_modeuler_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")
        tk.Checkbutton(left, text="Runge-Kutta 4 (Order 4)", variable=self._o_rk4_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")

        self._ode_val_var = tk.StringVar(value="")
        tk.Label(left, textvariable=self._ode_val_var, font=FONT_UI, fg=ERROR, bg=BG_PANEL, wraplength=320, justify=tk.LEFT).pack(fill=tk.X, pady=(6, 6))

        self._btn_ode_run = ttk.Button(left, text="▶ Run ODE Comparison", style="Accent.NX.TButton", command=self._on_run_ode_comp)
        self._btn_ode_run.pack(anchor="w", pady=(4, 0))

        # Right: Notebook with Table & Comparison Plot
        right = tk.Frame(self._ode_tab, bg=BG_SECONDARY)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        ode_nb = ttk.Notebook(right)
        ode_nb.grid(row=0, column=0, sticky="nsew")

        # Table
        tab_t = tk.Frame(ode_nb, bg=BG_SECONDARY)
        ode_nb.add(tab_t, text="  Results Table  ")
        cols = ["Method", "Final y", "Total Steps", "Time (s)", "Status"]
        self._ode_tree = ttk.Treeview(tab_t, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self._ode_tree.heading(c, text=c, anchor=tk.CENTER)
            self._ode_tree.column(c, width=120, anchor=tk.CENTER)
        self._ode_tree.pack(fill=tk.BOTH, expand=True)

        # Plot
        self._ode_comp_plot = ODEPlotPanel(ode_nb)
        ode_nb.add(self._ode_comp_plot, text="  Overlay Plot  ")

    def _on_run_ode_comp(self) -> None:
        methods = []
        if self._o_euler_chk.get():
            methods.append("euler")
        if self._o_modeuler_chk.get():
            methods.append("modified_euler")
        if self._o_rk4_chk.get():
            methods.append("rk4")

        if not methods:
            self._ode_val_var.set("Please select at least one method.")
            return

        try:
            req = ProblemRequest(
                expression=self._ode_expr_var.get().strip(),
                ode_x0=float(self._ode_x0_var.get()),
                ode_y0=float(self._ode_y0_var.get()),
                ode_h=float(self._ode_h_var.get()),
                ode_x_end=float(self._ode_xend_var.get()),
            )
        except ValueError as exc:
            self._ode_val_var.set(f"Invalid input: {exc}")
            return

        self._ode_val_var.set("")
        self._ode_tree.delete(*self._ode_tree.get_children())
        if self._status_bar:
            self._status_bar.set_running("ODE Comparison")

        def worker():
            try:
                results = self._comp_engine.compare(methods, req)
                self.after(0, lambda: self._on_ode_comp_done(results))
            except Exception as exc:
                self.after(0, lambda: self._ode_val_var.set(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_ode_comp_done(self, results: dict[str, SolverResult]) -> None:
        for m_id, res in results.items():
            final_y = f"{res.ode_table[-1]['y']:.8g}" if res.ode_table else "—"
            steps = str(res.metrics.iterations)
            t = f"{res.metrics.execution_time_seconds:.4f}"
            st = res.status.value
            self._ode_tree.insert("", tk.END, values=[res.method, final_y, steps, t, st])

        self._ode_comp_plot.plot_comparison(results)
        if self._status_bar:
            self._status_bar.set_done("ODE comparison completed")

    # ── TAB 3: LINEAR SYSTEMS COMPARISON ───────────────────────────────────────
    def _build_linear_tab(self) -> None:
        self._linear_tab.columnconfigure(0, weight=0, minsize=360)
        self._linear_tab.columnconfigure(1, weight=1)
        self._linear_tab.rowconfigure(0, weight=1)

        left = tk.Frame(self._linear_tab, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(left, text="Compare Matrix Solvers", font=FONT_SUBHEADING, fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w")

        info = tk.Label(
            left,
            text="Standard 3×3 Test System:\n[ [2, 1, 1], [1, 3, 1], [1, 1, 4] ]\nb = [ 8, 10, 15 ]\nExact: x = [1, 2, 3]",
            font=FONT_MONO,
            fg=TEXT_SECONDARY,
            bg=BG_ELEVATED,
            justify=tk.LEFT,
            padx=8,
            pady=8,
        )
        info.pack(fill=tk.X, pady=(10, 12))

        self._l_ge_chk = tk.BooleanVar(value=True)
        self._l_gj_chk = tk.BooleanVar(value=True)
        tk.Checkbutton(left, text="Gauss Elimination", variable=self._l_ge_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")
        tk.Checkbutton(left, text="Gauss-Jordan", variable=self._l_gj_chk, font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL, selectcolor=BG_ELEVATED).pack(anchor="w")

        btn = ttk.Button(left, text="▶ Run Matrix Comparison", style="Accent.NX.TButton", command=self._on_run_linear_comp)
        btn.pack(anchor="w", pady=(14, 0))

        # Right: Table
        right = tk.Frame(self._linear_tab, bg=BG_SECONDARY)
        right.grid(row=0, column=1, sticky="nsew")

        cols = ["Method", "Solution Vector x", "Residual Norm", "Operations", "Time (s)", "Status"]
        self._linear_tree = ttk.Treeview(right, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            w = 160 if "Solution" in c else 110
            self._linear_tree.heading(c, text=c, anchor=tk.CENTER)
            self._linear_tree.column(c, width=w, anchor=tk.CENTER)
        self._linear_tree.pack(fill=tk.BOTH, expand=True)

    def _on_run_linear_comp(self) -> None:
        methods = []
        if self._l_ge_chk.get():
            methods.append("gauss_elimination")
        if self._l_gj_chk.get():
            methods.append("gauss_jordan")

        if not methods:
            return

        A = [[2.0, 1.0, 1.0], [1.0, 3.0, 1.0], [1.0, 1.0, 4.0]]
        b = [8.0, 10.0, 15.0]
        req = ProblemRequest(A=A, b_vec=b)

        self._linear_tree.delete(*self._linear_tree.get_children())
        if self._status_bar:
            self._status_bar.set_running("Linear Systems Comparison")

        def worker():
            try:
                results = self._comp_engine.compare(methods, req)
                self.after(0, lambda: self._on_linear_comp_done(results))
            except Exception as exc:
                pass

        threading.Thread(target=worker, daemon=True).start()

    def _on_linear_comp_done(self, results: dict[str, SolverResult]) -> None:
        for m_id, res in results.items():
            sol_str = ", ".join(f"{x:.4g}" for x in (res.solution_vector or []))
            resid = f"{res.metrics.final_residual:.4e}" if res.metrics.final_residual is not None else "0.0"
            ops = str(res.metrics.iterations)
            t = f"{res.metrics.execution_time_seconds:.4f}"
            st = res.status.value
            self._linear_tree.insert("", tk.END, values=[res.method, f"[{sol_str}]", resid, ops, t, st])

        if self._status_bar:
            self._status_bar.set_done("Matrix comparison completed")
