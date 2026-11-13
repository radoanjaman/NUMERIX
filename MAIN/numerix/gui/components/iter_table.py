"""
NUMERIX IterationTable component — ttk.Treeview for iteration history.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    BG_ELEVATED,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

# Column definitions per method
_ROOT_COLS: dict[str, list[tuple[str, str, int]]] = {
    # (key_in_values, display_header, width)
    "bisection": [
        ("n",     "n",       40),
        ("a",     "a",      110),
        ("b",     "b",      110),
        ("mid",   "mid",    110),
        ("f_mid", "f(mid)", 110),
        ("error", "Error",  110),
    ],
    "false_position": [
        ("n",      "n",        40),
        ("a",      "a",       110),
        ("b",      "b",       110),
        ("root",   "root",    110),
        ("f_root", "f(root)", 110),
        ("error",  "Error",   110),
    ],
    "newton_raphson": [
        ("n",    "n",     40),
        ("x_n",  "xₙ",   110),
        ("f_xn", "f(xₙ)",110),
        ("df_xn","f'(xₙ)",110),
        ("x_new","x_{n+1}",110),
        ("error","Error", 110),
    ],
}

_ODE_COLS: dict[str, list[tuple[str, str, int]]] = {
    "euler": [
        ("n",      "n",      40),
        ("x",      "x",     100),
        ("y",      "y",     110),
        ("slope",  "slope", 110),
        ("y_next", "y_next",110),
    ],
    "modified_euler": [
        ("n",           "n",          40),
        ("x",           "x",         100),
        ("y",           "y",         100),
        ("f1_slope",    "f1(slope)", 110),
        ("y_predictor", "y_pred",    110),
        ("f2_slope",    "f2(slope)", 110),
        ("y_corrector", "y_corr",   110),
    ],
    "rk4": [
        ("n",      "n",    40),
        ("x",      "x",   100),
        ("y",      "y",   100),
        ("k1",     "k1",  100),
        ("k2",     "k2",  100),
        ("k3",     "k3",  100),
        ("k4",     "k4",  100),
        ("y_next", "y_next",110),
    ],
}

_LINEAR_COLS: list[tuple[str, str, int]] = [
    ("n",    "Step",        50),
    ("op",   "Operation",  120),
    ("desc", "Description",400),
]


def _fmt_val(v: Any) -> str:
    """Format a table cell value."""
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.8g}"
    return str(v)


class IterationTable(tk.Frame):
    """Scrollable Treeview for iteration history of any method."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, **kwargs)
        self._tree: ttk.Treeview | None = None
        self._scrollbar_y: ttk.Scrollbar | None = None
        self._scrollbar_x: ttk.Scrollbar | None = None
        self._build_empty()

    def _build_empty(self) -> None:
        """Build the initial (empty) treeview widget."""
        self._rebuild_tree(columns=["n", "a", "b", "mid", "f_mid", "error"],
                           headers=["n", "a", "b", "mid", "f(mid)", "Error"],
                           widths=[40, 110, 110, 110, 110, 110])

    def _rebuild_tree(
        self,
        columns: list[str],
        headers: list[str],
        widths: list[int],
    ) -> None:
        """Destroy old tree if present and build a fresh one."""
        if self._scrollbar_y:
            self._scrollbar_y.destroy()
        if self._scrollbar_x:
            self._scrollbar_x.destroy()
        if self._tree:
            self._tree.destroy()

        self._tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        for col, hdr, w in zip(columns, headers, widths):
            self._tree.heading(col, text=hdr, anchor=tk.CENTER)
            self._tree.column(col, width=w, minwidth=40, anchor=tk.CENTER)

        # Alternating row tags
        self._tree.tag_configure("odd",  background=BG_PANEL)
        self._tree.tag_configure("even", background=BG_ELEVATED)

        # Scrollbars
        self._scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tree.yview)
        self._scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._tree.xview)
        self._tree.configure(
            yscrollcommand=self._scrollbar_y.set,
            xscrollcommand=self._scrollbar_x.set,
        )

        self._scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clear(self) -> None:
        if self._tree:
            self._tree.delete(*self._tree.get_children())

    def _insert_rows(self, rows: list[list[Any]]) -> None:
        self._tree.delete(*self._tree.get_children())
        for i, row in enumerate(rows):
            tag = "odd" if i % 2 == 0 else "even"
            self._tree.insert("", tk.END, values=[_fmt_val(v) for v in row], tags=(tag,))

    def load_root_finding(self, iterations: list[Any], method_name: str) -> None:
        """Populate the table for a root-finding result."""
        key = method_name.lower().replace("-", "_").replace(" ", "_")
        col_defs = _ROOT_COLS.get(key, _ROOT_COLS["bisection"])

        columns = [c[0] for c in col_defs]
        headers = [c[1] for c in col_defs]
        widths   = [c[2] for c in col_defs]

        self._rebuild_tree(columns, headers, widths)

        rows: list[list[Any]] = []
        for rec in iterations:
            row: list[Any] = []
            for col, _, _ in col_defs:
                if col == "n":
                    row.append(rec.n)
                elif col == "error":
                    row.append(rec.approximate_error)
                else:
                    row.append(rec.values.get(col))
            rows.append(row)

        self._insert_rows(rows)

    def load_ode(self, ode_table: list[dict[str, float]], iterations: list[Any], method_name: str) -> None:
        """Populate the table for an ODE result."""
        key = method_name.lower().replace("-", "_").replace(" ", "_")
        col_defs = _ODE_COLS.get(key, _ODE_COLS["euler"])

        columns = [c[0] for c in col_defs]
        headers = [c[1] for c in col_defs]
        widths   = [c[2] for c in col_defs]

        self._rebuild_tree(columns, headers, widths)

        rows: list[list[Any]] = []
        # Try ode_table first, fall back to iteration records
        if ode_table:
            for i, row_dict in enumerate(ode_table):
                row: list[Any] = [i + 1 if "n" not in row_dict else row_dict["n"]]
                for col, _, _ in col_defs:
                    if col == "n":
                        continue
                    row.append(row_dict.get(col))
                rows.append(row)
        else:
            for rec in iterations:
                row = []
                for col, _, _ in col_defs:
                    if col == "n":
                        row.append(rec.n)
                    else:
                        row.append(rec.values.get(col))
                rows.append(row)

        self._insert_rows(rows)

    def load_linear(self, iterations: list[Any]) -> None:
        """Populate the table for a linear system result."""
        col_defs = _LINEAR_COLS
        columns = [c[0] for c in col_defs]
        headers = [c[1] for c in col_defs]
        widths   = [c[2] for c in col_defs]

        self._rebuild_tree(columns, headers, widths)

        rows: list[list[Any]] = []
        for rec in iterations:
            op = rec.values.get("type", rec.values.get("op", rec.extra.get("op", "")))
            desc = rec.extra.get("description", rec.values.get("desc", str(rec.values)))
            rows.append([rec.n, op, desc])

        self._insert_rows(rows)
