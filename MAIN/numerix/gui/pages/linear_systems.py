"""
NUMERIX Linear Systems Page — interactive matrix solver with step-by-step row operations.
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from typing import Any

from numerix.core.result_models import SolverResult, SolverStatus
from numerix.engine.solver_engine import ProblemRequest, SolverEngine
from numerix.gui.components.iter_table import IterationTable
from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    ACCENT_VIOLET,
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
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)


_DEFAULT_3X3_A = [
    [2.0, 1.0, 1.0],
    [1.0, 3.0, 1.0],
    [1.0, 1.0, 4.0],
]
_DEFAULT_3X3_B = [8.0, 10.0, 15.0]


class LinearSystemsPage(tk.Frame):
    """Linear systems workspace: dynamic matrix grid editor and row-operation viewer."""

    def __init__(self, parent: tk.Widget, status_bar=None, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, padx=16, pady=12, **kwargs)
        self._status_bar = status_bar
        self._engine = SolverEngine()
        self._is_running = False
        self._n_dim = 3
        self._cell_entries: list[list[tk.Entry]] = []
        self._b_entries: list[tk.Entry] = []
        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=0, minsize=420)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ── Left Pane (Matrix Inputs & Controls) ──────────────────────────────
        left = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Title & Method Selection
        tk.Label(left, text="Linear System Solver", font=FONT_SUBHEADING, fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w")

        method_row = tk.Frame(left, bg=BG_PANEL)
        method_row.pack(fill=tk.X, pady=(4, 10))
        self._method_var = tk.StringVar(value="Gauss Elimination")
        self._method_combo = ttk.Combobox(
            method_row,
            textvariable=self._method_var,
            values=["Gauss Elimination", "Gauss-Jordan"],
            state="readonly",
            font=FONT_UI,
            width=18,
        )
        self._method_combo.pack(side=tk.LEFT)

        # Dimension selector
        dim_box = tk.Frame(method_row, bg=BG_PANEL)
        dim_box.pack(side=tk.RIGHT)
        tk.Label(dim_box, text="Size (n):", font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT, padx=4)
        self._n_var = tk.IntVar(value=3)
        self._dim_spin = tk.Spinbox(
            dim_box,
            from_=2,
            to=6,
            textvariable=self._n_var,
            width=4,
            font=FONT_MONO,
            bg=BG_ELEVATED,
            fg=TEXT_PRIMARY,
            buttonbackground=BG_PANEL,
            command=self._on_dim_change,
        )
        self._dim_spin.pack(side=tk.LEFT)

        # Matrix editor container
        tk.Label(left, text="Augmented Matrix [ A | b ]:", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(4, 2))
        self._matrix_frame = tk.Frame(left, bg=BG_PANEL)
        self._matrix_frame.pack(fill=tk.X, pady=(0, 10))
        self._render_matrix_grid(3)

        # Validation message
        self._val_msg_var = tk.StringVar(value="")
        self._val_lbl = tk.Label(
            left, textvariable=self._val_msg_var, font=FONT_UI, fg=ERROR, bg=BG_PANEL, wraplength=380, justify=tk.LEFT
        )
        self._val_lbl.pack(fill=tk.X, pady=(0, 6))

        # Buttons
        btn_box = tk.Frame(left, bg=BG_PANEL)
        btn_box.pack(fill=tk.X, pady=(0, 12))
        self._btn_run = ttk.Button(btn_box, text="▶ Solve System", style="Accent.NX.TButton", command=self._on_run)
        self._btn_run.pack(side=tk.LEFT, padx=(0, 6))
        self._btn_reset = ttk.Button(btn_box, text="Reset", style="NX.TButton", command=self._on_reset)
        self._btn_reset.pack(side=tk.LEFT, padx=6)
        self._btn_example = ttk.Button(btn_box, text="Load Example", style="NX.TButton", command=self._on_load_example)
        self._btn_example.pack(side=tk.LEFT, padx=6)

        # Solution summary card
        self._sol_card = tk.LabelFrame(
            left,
            text=" Solution Vector x ",
            font=FONT_SUBHEADING,
            fg=ACCENT_CYAN,
            bg=BG_ELEVATED,
            padx=10,
            pady=8,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self._sol_card.pack(fill=tk.X, pady=(6, 0))

        self._sol_text_var = tk.StringVar(value="x = —")
        self._sol_lbl = tk.Label(
            self._sol_card,
            textvariable=self._sol_text_var,
            font=FONT_MONO,
            fg=SUCCESS,
            bg=BG_ELEVATED,
            justify=tk.LEFT,
        )
        self._sol_lbl.pack(anchor="w")

        self._resid_var = tk.StringVar(value="Residual Norm: —")
        tk.Label(self._sol_card, textvariable=self._resid_var, font=FONT_UI, fg=TEXT_SECONDARY, bg=BG_ELEVATED).pack(anchor="w", pady=(4, 0))

        # ── Right Pane (Notebook: Row Operations Table & Snapshots) ───────────
        right = tk.Frame(self, bg=BG_SECONDARY)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self._notebook = ttk.Notebook(right)
        self._notebook.grid(row=0, column=0, sticky="nsew")

        # Tab: Row Operations
        self._table = IterationTable(self._notebook)
        self._notebook.add(self._table, text="  Row Operations History  ")

    def _render_matrix_grid(self, n: int) -> None:
        """Clear and regenerate N x (N+1) entry widgets."""
        for widget in self._matrix_frame.winfo_children():
            widget.destroy()

        self._n_dim = n
        self._cell_entries = []
        self._b_entries = []

        grid_inner = tk.Frame(self._matrix_frame, bg=BG_PANEL)
        grid_inner.pack()

        # Headers
        for j in range(n):
            tk.Label(grid_inner, text=f"x{j+1}", font=FONT_UI_BOLD, fg=TEXT_SECONDARY, bg=BG_PANEL, width=6).grid(row=0, column=j, padx=2, pady=2)
        tk.Label(grid_inner, text="|", font=FONT_UI_BOLD, fg=ACCENT_CYAN, bg=BG_PANEL).grid(row=0, column=n, padx=2)
        tk.Label(grid_inner, text="b", font=FONT_UI_BOLD, fg=ACCENT_CYAN, bg=BG_PANEL, width=6).grid(row=0, column=n+1, padx=2, pady=2)

        # Rows
        for i in range(n):
            row_entries = []
            for j in range(n):
                val = str(_DEFAULT_3X3_A[i][j]) if (n == 3 and i < 3 and j < 3) else ("1.0" if i == j else "0.0")
                e = tk.Entry(
                    grid_inner,
                    width=6,
                    font=FONT_MONO,
                    bg=BG_ELEVATED,
                    fg=TEXT_PRIMARY,
                    insertbackground=TEXT_PRIMARY,
                    justify=tk.CENTER,
                    relief="flat",
                    highlightbackground=BORDER,
                    highlightthickness=1,
                )
                e.insert(0, val)
                e.grid(row=i+1, column=j, padx=2, pady=2)
                row_entries.append(e)
            self._cell_entries.append(row_entries)

            # Separator bar
            tk.Label(grid_inner, text="|", font=FONT_UI_BOLD, fg=ACCENT_CYAN, bg=BG_PANEL).grid(row=i+1, column=n, padx=2)

            # b entry
            b_val = str(_DEFAULT_3X3_B[i]) if (n == 3 and i < 3) else "1.0"
            eb = tk.Entry(
                grid_inner,
                width=6,
                font=FONT_MONO,
                bg=BG_ELEVATED,
                fg=TEXT_PRIMARY,
                insertbackground=TEXT_PRIMARY,
                justify=tk.CENTER,
                relief="flat",
                highlightbackground=BORDER,
                highlightthickness=1,
            )
            eb.insert(0, b_val)
            eb.grid(row=i+1, column=n+1, padx=2, pady=2)
            self._b_entries.append(eb)

    def _on_dim_change(self) -> None:
        try:
            val = int(self._n_var.get())
            if 2 <= val <= 6 and val != self._n_dim:
                self._render_matrix_grid(val)
        except Exception:
            pass

    def _on_load_example(self) -> None:
        self._n_var.set(3)
        self._render_matrix_grid(3)
        self._val_msg_var.set("")

    def _on_reset(self) -> None:
        self._on_load_example()
        self._table.clear()
        self._sol_text_var.set("x = —")
        self._resid_var.set("Residual Norm: —")
        self._val_msg_var.set("")
        if self._status_bar:
            self._status_bar.set_ready()

    def _on_run(self) -> None:
        if self._is_running:
            return

        self._val_msg_var.set("")
        n = self._n_dim
        A: list[list[float]] = []
        b: list[float] = []

        try:
            for i in range(n):
                row = []
                for j in range(n):
                    raw = self._cell_entries[i][j].get().strip()
                    row.append(float(raw))
                A.append(row)
                b.append(float(self._b_entries[i].get().strip()))
        except ValueError as exc:
            self._val_msg_var.set(f"Invalid matrix value: {exc}")
            return

        method_name = self._method_var.get()
        method_id = "gauss_elimination" if method_name == "Gauss Elimination" else "gauss_jordan"
        req = ProblemRequest(method=method_id, A=A, b_vec=b)

        self._is_running = True
        self._btn_run.configure(state="disabled")
        if self._status_bar:
            self._status_bar.set_running(method_name)

        def worker():
            try:
                res = self._engine.solve(req)
                self.after(0, lambda: self._on_solve_done(res, method_name))
            except Exception as exc:
                self.after(0, lambda: self._on_solve_error(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_solve_done(self, res: SolverResult, method_name: str) -> None:
        self._is_running = False
        self._btn_run.configure(state="normal")

        # Load row operations into table
        self._table.load_linear(res.iterations)

        if res.status == SolverStatus.SUCCESS and res.solution_vector:
            sol_lines = [f"x{i+1} = {val:.8g}" for i, val in enumerate(res.solution_vector)]
            self._sol_text_var.set("\n".join(sol_lines))
            resid = res.metrics.final_residual
            if resid is not None:
                self._resid_var.set(f"Residual Norm ||Ax - b||: {resid:.6e}")
            else:
                self._resid_var.set("Residual Norm: 0.0")

            if self._status_bar:
                self._status_bar.set_done(f"Solved in {res.metrics.iterations} operations ({res.metrics.execution_time_seconds:.4f}s)")
        else:
            self._sol_text_var.set("No unique solution found.")
            self._resid_var.set(f"Reason: {res.termination_reason}")
            self._val_msg_var.set(f"{res.status.value}: {res.termination_reason}")
            if self._status_bar:
                self._status_bar.set_error(res.termination_reason)

    def _on_solve_error(self, err_msg: str) -> None:
        self._is_running = False
        self._btn_run.configure(state="normal")
        self._val_msg_var.set(f"Solver Error: {err_msg}")
        if self._status_bar:
            self._status_bar.set_error(err_msg)
