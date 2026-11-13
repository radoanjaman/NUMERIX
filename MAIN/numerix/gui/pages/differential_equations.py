"""
NUMERIX Differential Equations Page — interactive initial value problem solver.
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from typing import Any

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
from numerix.gui.visualization.ode_plots import ODEPlotPanel


_METHOD_MAP = {
    "Euler": "euler",
    "Modified Euler (Heun)": "modified_euler",
    "Runge-Kutta 4 (RK4)": "rk4",
}

_FORMULAS = {
    "Euler": "Euler (Order 1): y_{n+1} = y_n + h·f(x_n, y_n)",
    "Modified Euler (Heun)": "Heun (Order 2): Predictor y* = y_n + h·f_n, Corrector y_{n+1} = y_n + (h/2)·[f_n + f(x_{n+1}, y*)]",
    "Runge-Kutta 4 (RK4)": "RK4 (Order 4): y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4)/6, evaluates 4 intermediate slopes per step",
}


class DifferentialEquationsPage(tk.Frame):
    """ODE workspace: IVP parameters on left, step table and trajectory plot on right."""

    def __init__(self, parent: tk.Widget, status_bar=None, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, padx=16, pady=12, **kwargs)
        self._status_bar = status_bar
        self._engine = SolverEngine()
        self._is_running = False
        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=0, minsize=380)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ── Left Pane (Inputs & Controls) ──────────────────────────────────────
        left = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Title & Method Selection
        tk.Label(left, text="ODE Method", font=FONT_SUBHEADING, fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w")
        self._method_var = tk.StringVar(value="Euler")
        self._method_combo = ttk.Combobox(
            left,
            textvariable=self._method_var,
            values=["Euler", "Modified Euler (Heun)", "Runge-Kutta 4 (RK4)"],
            state="readonly",
            font=FONT_UI,
        )
        self._method_combo.pack(fill=tk.X, pady=(4, 10))
        self._method_combo.bind("<<ComboboxSelected>>", self._on_method_change)

        # Formula banner
        self._formula_var = tk.StringVar(value=_FORMULAS["Euler"])
        tk.Label(
            left,
            textvariable=self._formula_var,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_ELEVATED,
            wraplength=340,
            justify=tk.LEFT,
            padx=8,
            pady=6,
        ).pack(fill=tk.X, pady=(0, 12))

        # Equation dy/dx = f(x, y)
        tk.Label(left, text="Equation:  dy/dx = f(x, y)", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w")
        self._expr_var = tk.StringVar(value="x + y")
        tk.Entry(
            left, textvariable=self._expr_var, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(fill=tk.X, pady=(4, 12), ipady=4)

        # Initial values: x0 and y0
        iv_row = tk.Frame(left, bg=BG_PANEL)
        iv_row.pack(fill=tk.X, pady=(0, 8))
        tk.Label(iv_row, text="Initial x0:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._x0_var = tk.StringVar(value="0.0")
        tk.Entry(
            iv_row, textvariable=self._x0_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=6)
        tk.Label(iv_row, text="Initial y0:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT, padx=(10, 0))
        self._y0_var = tk.StringVar(value="1.0")
        tk.Entry(
            iv_row, textvariable=self._y0_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=6)

        # Step size h and End x
        step_row = tk.Frame(left, bg=BG_PANEL)
        step_row.pack(fill=tk.X, pady=(0, 10))
        tk.Label(step_row, text="Step size h:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        self._h_var = tk.StringVar(value="0.1")
        tk.Entry(
            step_row, textvariable=self._h_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=6)
        tk.Label(step_row, text="End x:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT, padx=(10, 0))
        self._xend_var = tk.StringVar(value="0.5")
        tk.Entry(
            step_row, textvariable=self._xend_var, width=8, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(side=tk.LEFT, padx=6)

        # Optional exact solution for overlay
        tk.Label(left, text="Optional Exact y(x) [e.g. 2*exp(x)-x-1]:", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(anchor="w")
        self._exact_var = tk.StringVar(value="2*exp(x) - x - 1")
        tk.Entry(
            left, textvariable=self._exact_var, font=FONT_MONO,
            bg=BG_ELEVATED, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat", highlightbackground=BORDER, highlightthickness=1
        ).pack(fill=tk.X, pady=(4, 12), ipady=3)

        # Validation message
        self._val_msg_var = tk.StringVar(value="")
        self._val_lbl = tk.Label(
            left, textvariable=self._val_msg_var, font=FONT_UI, fg=ERROR, bg=BG_PANEL, wraplength=340, justify=tk.LEFT
        )
        self._val_lbl.pack(fill=tk.X, pady=(0, 6))

        # Action Buttons
        btn_box = tk.Frame(left, bg=BG_PANEL)
        btn_box.pack(fill=tk.X, pady=(0, 14))
        self._btn_run = ttk.Button(btn_box, text="▶ Solve ODE", style="Accent.NX.TButton", command=self._on_run)
        self._btn_run.pack(side=tk.LEFT, padx=(0, 6))
        self._btn_reset = ttk.Button(btn_box, text="Reset", style="NX.TButton", command=self._on_reset)
        self._btn_reset.pack(side=tk.LEFT, padx=6)
        self._btn_example = ttk.Button(btn_box, text="Load Example", style="NX.TButton", command=self._on_load_example)
        self._btn_example.pack(side=tk.LEFT, padx=6)

        # Metrics row
        self._metrics_row = MetricsRow(left)
        self._metrics_row.pack(fill=tk.X, pady=(6, 0))

        # ── Right Pane (Notebook: Step Table & Trajectory Plot) ───────────────
        right = tk.Frame(self, bg=BG_SECONDARY)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self._notebook = ttk.Notebook(right)
        self._notebook.grid(row=0, column=0, sticky="nsew")

        # Tab 1: Step Table
        self._table = IterationTable(self._notebook)
        self._notebook.add(self._table, text="  Step Table  ")

        # Tab 2: Trajectory Plot
        self._plot_panel = ODEPlotPanel(self._notebook)
        self._notebook.add(self._plot_panel, text="  Trajectory Plot  ")

    def _on_method_change(self, _event=None) -> None:
        m = self._method_var.get()
        self._formula_var.set(_FORMULAS.get(m, ""))

    def _on_load_example(self) -> None:
        self._expr_var.set("x + y")
        self._x0_var.set("0.0")
        self._y0_var.set("1.0")
        self._h_var.set("0.1")
        self._xend_var.set("0.5")
        self._exact_var.set("2*exp(x) - x - 1")
        self._val_msg_var.set("")

    def _on_reset(self) -> None:
        self._on_load_example()
        self._metrics_row.reset()
        self._table.clear()
        self._plot_panel.clear()
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
            self._val_msg_var.set("Please enter dy/dx expression.")
            return

        try:
            x0 = float(self._x0_var.get())
            y0 = float(self._y0_var.get())
            h = float(self._h_var.get())
            x_end = float(self._xend_var.get())
            req = ProblemRequest(
                method=method_id,
                expression=expr,
                ode_x0=x0,
                ode_y0=y0,
                ode_h=h,
                ode_x_end=x_end,
            )
        except ValueError as exc:
            self._val_msg_var.set(f"Input error: {exc}")
            return

        self._is_running = True
        self._btn_run.configure(state="disabled")
        if self._status_bar:
            self._status_bar.set_running(method_name)

        exact_str = self._exact_var.get().strip()

        def worker():
            try:
                res = self._engine.solve(req)
                self.after(0, lambda: self._on_solve_done(res, method_id, method_name, exact_str))
            except Exception as exc:
                self.after(0, lambda: self._on_solve_error(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_solve_done(self, res: SolverResult, method_id: str, method_name: str, exact_str: str) -> None:
        self._is_running = False
        self._btn_run.configure(state="normal")

        # In ODE, res.root is None, but final y is in res.ode_table[-1]["y"]
        if res.ode_table:
            final_y = res.ode_table[-1]["y"]
            res.root = final_y  # allow metric card to show final y

        self._metrics_row.update_from_result(res)
        self._table.load_ode(res.ode_table or [], res.iterations, method_id)
        self._plot_panel.plot_ode(res.ode_table or [], method_name, exact_str)

        if self._status_bar:
            self._status_bar.set_done(f"Completed {res.metrics.iterations} steps ({res.metrics.execution_time_seconds:.4f}s)")

    def _on_solve_error(self, err_msg: str) -> None:
        self._is_running = False
        self._btn_run.configure(state="normal")
        self._val_msg_var.set(f"Solver Error: {err_msg}")
        if self._status_bar:
            self._status_bar.set_error(err_msg)
