"""
NUMERIX Root Finding Page — interactive solver for nonlinear equations.
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from typing import Any

from numerix.core.expression_parser import ParseError
from numerix.core.result_models import SolverResult, SolverStatus
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.gui.components.iter_table import IterationTable
from numerix.gui.components.metric_cards import MetricsRow
from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    BG_ELEVATED,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    ERROR,
    FONT_HEADING,
    FONT_MONO,
    FONT_SUBHEADING,
    FONT_UI,
    FONT_UI_BOLD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)
from numerix.gui.visualization.root_plots import RootPlotPanel


_METHOD_MAP = {
    "Bisection": "bisection",
    "False Position": "false_position",
    "Newton-Raphson": "newton_raphson",
}

_FORMULAS = {
    "Bisection": "Midpoint: c = (a + b) / 2. Stops when |b - a| / 2 < tol or f(c) = 0.",
    "False Position": "Interpolation: c = (a·f(b) - b·f(a)) / (f(b) - f(a)). Halves interval dynamically.",
    "Newton-Raphson": "Tangent: x_{n+1} = x_n - f(x_n) / f'(x_n). Symbolic derivative computed automatically.",
}


class RootFindingPage(tk.Frame):
    """Complete Root Finding workspace: controls on left, outputs/plots on right."""

    def __init__(self, parent: tk.Widget, status_bar=None, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, padx=16, pady=12, **kwargs)
        self._status_bar = status_bar
        self._engine = SolverEngine()
        self._is_running = False
        self._last_result: SolverResult | None = None
        self._build()

    def _build(self) -> None:
        # Two-column layout
        self.columnconfigure(0, weight=0, minsize=380)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ── Left Pane (Inputs & Controls) ──────────────────────────────────────
        left = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Method selection
        tk.Label(left, text="Numerical Method", font=FONT_SUBHEADING, fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w")
        self._method_var = tk.StringVar(value="Bisection")
        self._method_combo = ttk.Combobox(
            left,
            textvariable=self._method_var,
            values=["Bisection", "False Position", "Newton-Raphson"],
            state="readonly",
            font=FONT_UI,
        )
        self._method_combo.pack(fill=tk.X, pady=(4, 10))
        self._method_combo.bind("<<ComboboxSelected>>", self._on_method_change)

        # Formula / Explanation label
        self._formula_var = tk.StringVar(value=_FORMULAS["Bisection"])
        self._formula_lbl = tk.Label(
            left,
            textvariable=self._formula_var,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_ELEVATED,
            wraplength=340,
            justify=tk.LEFT,
            padx=8,
            pady=6,
        )
        self._formula_lbl.pack(fill=tk.X, pady=(0, 12))

        # Function f(x)
        tk.Label(left, text="Equation:  f(x) = 0", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w")
        self._expr_var = tk.StringVar(value="x**3 - x - 2")
        self._expr_entry = tk.Entry(
            left,
            textvariable=self._expr_var,
            font=FONT_MONO,
            bg=BG_ELEVATED,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self._expr_entry.pack(fill=tk.X, pady=(4, 12), ipady=4)

        # Dynamic parameter frames
        self._param_frame = tk.Frame(left, bg=BG_PANEL)
        self._param_frame.pack(fill=tk.X, pady=(0, 10))

        # [a, b] bracket row
        self._bracket_row = tk.Frame(self._param_frame, bg=BG_PANEL)
        self._bracket_row.pack(fill=tk.X, pady=2)
        tk.Label(self._bracket_row, text="Lower bound a:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._a_var = tk.StringVar(value="1.0")
        tk.Entry(
            self._bracket_row, textvariable=self._a_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=6)
        tk.Label(self._bracket_row, text="Upper bound b:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT, padx=(6, 0))
        self._b_var = tk.StringVar(value="2.0")
        tk.Entry(
            self._bracket_row, textvariable=self._b_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=6)

        # x0 row for Newton-Raphson
        self._x0_row = tk.Frame(self._param_frame, bg=BG_PANEL)
        tk.Label(self._x0_row, text="Initial Guess x0:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._x0_var = tk.StringVar(value="1.5")
        tk.Entry(
            self._x0_row, textvariable=self._x0_var, width=12, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=8)

        # Tolerance & Max Iterations
        common_row = tk.Frame(left, bg=BG_PANEL)
        common_row.pack(fill=tk.X, pady=(0, 12))
        tk.Label(common_row, text="Tolerance:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._tol_var = tk.StringVar(value="1e-6")
        tk.Entry(
            common_row, textvariable=self._tol_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=(4, 12))
        tk.Label(common_row, text="Max Iter:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._max_iter_var = tk.StringVar(value="100")
        tk.Entry(
            common_row, textvariable=self._max_iter_var, width=6, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=4)

        # Validation message
        self._val_msg_var = tk.StringVar(value="")
        self._val_lbl = tk.Label(
            left, textvariable=self._val_msg_var, font=FONT_UI, fg=ERROR, bg=BG_PANEL, wraplength=340, justify=tk.LEFT
        )
        self._val_lbl.pack(fill=tk.X, pady=(0, 10))

        # Action Buttons
        btn_box = tk.Frame(left, bg=BG_PANEL)
        btn_box.pack(fill=tk.X, pady=(0, 16))
        self._btn_run = ttk.Button(btn_box, text="▶ Run Calculation", style="Accent.NX.TButton", command=self._on_run)
        self._btn_run.pack(side=tk.LEFT, padx=(0, 6))
        self._btn_reset = ttk.Button(btn_box, text="Reset", style="NX.TButton", command=self._on_reset)
        self._btn_reset.pack(side=tk.LEFT, padx=6)
        self._btn_example = ttk.Button(btn_box, text="Load Example", style="NX.TButton", command=self._on_load_example)
        self._btn_example.pack(side=tk.LEFT, padx=6)

        # Metrics row
        self._metrics_row = MetricsRow(left)
        self._metrics_row.pack(fill=tk.X, pady=(10, 0))

        # ── Right Pane (Notebook: Iterations & Visualization) ─────────────────
        right = tk.Frame(self, bg=BG_SECONDARY)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self._notebook = ttk.Notebook(right)
        self._notebook.grid(row=0, column=0, sticky="nsew")

        # Tab 1: Iteration Table
        self._table = IterationTable(self._notebook)
        self._notebook.add(self._table, text="  Iteration Table  ")

        # Tab 2: Visualization
        self._plots = RootPlotPanel(self._notebook)
        self._notebook.add(self._plots, text="  Visualization  ")

    def _on_method_change(self, _event=None) -> None:
        m = self._method_var.get()
        self._formula_var.set(_FORMULAS.get(m, ""))
        if m == "Newton-Raphson":
            self._bracket_row.pack_forget()
            self._x0_row.pack(fill=tk.X, pady=2)
        else:
            self._x0_row.pack_forget()
            self._bracket_row.pack(fill=tk.X, pady=2)

    def _on_load_example(self) -> None:
        self._expr_var.set("x**3 - x - 2")
        self._a_var.set("1.0")
        self._b_var.set("2.0")
        self._x0_var.set("1.5")
        self._tol_var.set("1e-6")
        self._max_iter_var.set("100")
        self._val_msg_var.set("")

    def _on_reset(self) -> None:
        self._on_load_example()
        self._metrics_row.reset()
        self._table.clear()
        self._plots.clear()
        self._val_msg_var.set("")
        if self._status_bar:
            self._status_bar.set_ready()

    def _on_run(self) -> None:
        if self._is_running:
            return

        self._val_msg_var.set("")
        method_name = self._method_var.get()
        method_id = _METHOD_MAP[method_name]
        expr = self._expr_var.get().strip()

        if not expr:
            self._val_msg_var.set("Please enter an expression f(x).")
            return

        try:
            tol = float(self._tol_var.get())
            max_iter = int(self._max_iter_var.get())
            if method_id == "newton_raphson":
                x0 = float(self._x0_var.get())
                req = ProblemRequest(method=method_id, expression=expr, x0=x0, tol=tol, max_iter=max_iter)
            else:
                a = float(self._a_var.get())
                b = float(self._b_var.get())
                req = ProblemRequest(method=method_id, expression=expr, a=a, b=b, tol=tol, max_iter=max_iter)
        except ValueError as exc:
            self._val_msg_var.set(f"Input error: {exc}")
            return

        # Start execution in background thread
        self._is_running = True
        self._btn_run.configure(state="disabled")
        if self._status_bar:
            self._status_bar.set_running(method_name)

        def worker():
            try:
                res = self._engine.solve(req)
                self.after(0, lambda: self._on_solve_done(res, method_name, req))
            except Exception as exc:
                self.after(0, lambda: self._on_solve_error(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_solve_done(self, res: SolverResult, method_name: str, req: ProblemRequest) -> None:
        self._is_running = False
        self._btn_run.configure(state="normal")
        self._last_result = res

        # Update metrics
        self._metrics_row.update_from_result(res)

        # Update table
        self._table.load_root_finding(res.iterations, method_name)

        # Update plots
        a_val = req.a if req.a is not None else req.x0
        b_val = req.b if req.b is not None else (req.x0 + 1.0 if req.x0 is not None else 2.0)
        self._plots.plot_function(req.expression, res.root, a_val, b_val, res.iterations, method_name)
        self._plots.plot_error(res.iterations)

        # Status
        if res.status == SolverStatus.CONVERGED:
            msg = f"Converged in {res.metrics.iterations} iterations"
            if self._status_bar:
                self._status_bar.set_done(msg)
        else:
            msg = f"Status: {res.status.value}"
            self._val_msg_var.set(f"{msg}: {res.termination_reason}")
            if self._status_bar:
                self._status_bar.set_error(msg)

    def _on_solve_error(self, err_msg: str) -> None:
        self._is_running = False
        self._btn_run.configure(state="normal")
        self._val_msg_var.set(f"Error: {err_msg}")
        if self._status_bar:
            self._status_bar.set_error(err_msg)
