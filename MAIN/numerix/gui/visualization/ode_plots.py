"""
NUMERIX ODEPlotPanel — Matplotlib visualization for ODE initial value problems.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from numerix.core.expression_parser import parse_function_x
from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    ACCENT_VIOLET,
    BG_MAIN,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    ERROR,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)

try:
    import numpy as np
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False


_DARK_PARAMS = {
    "figure.facecolor":    BG_MAIN,
    "axes.facecolor":      BG_PANEL,
    "axes.edgecolor":      BORDER,
    "axes.labelcolor":     TEXT_SECONDARY,
    "xtick.color":         TEXT_SECONDARY,
    "ytick.color":         TEXT_SECONDARY,
    "grid.color":          BORDER,
    "grid.linestyle":      "--",
    "grid.alpha":          0.5,
    "text.color":          TEXT_PRIMARY,
    "lines.linewidth":     2.0,
}


def _apply_dark(ax) -> None:
    ax.set_facecolor(BG_PANEL)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
    ax.tick_params(colors=TEXT_SECONDARY, which="both")
    ax.xaxis.label.set_color(TEXT_SECONDARY)
    ax.yaxis.label.set_color(TEXT_SECONDARY)
    ax.title.set_color(TEXT_PRIMARY)


class ODEPlotPanel(tk.Frame):
    """Embeds Matplotlib figures for single-method or comparison ODE trajectories."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, **kwargs)
        self._build()

    def _build(self) -> None:
        if not _MPL_AVAILABLE:
            tk.Label(
                self,
                text="Matplotlib not installed.",
                font=("Consolas", 11),
                fg=WARNING,
                bg=BG_SECONDARY,
            ).pack(expand=True)
            return

        with plt.rc_context(_DARK_PARAMS):
            self._fig = Figure(figsize=(6, 4), dpi=96)
            self._ax = self._fig.add_subplot(111)
            _apply_dark(self._ax)

        self._canvas = FigureCanvasTkAgg(self._fig, master=self)
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.clear()

    def clear(self) -> None:
        if not _MPL_AVAILABLE:
            return
        self._ax.clear()
        _apply_dark(self._ax)
        self._ax.set_title("ODE Solution Plot (run solver to display)", fontsize=10, color=TEXT_SECONDARY)
        self._ax.grid(True)
        self._canvas.draw_idle()

    def plot_ode(
        self,
        ode_table: list[dict[str, float]],
        method_name: str,
        exact_expr_str: str | None = None,
    ) -> None:
        """Plot numerical solution curve and optional exact solution."""
        if not _MPL_AVAILABLE or not ode_table:
            return

        xs = [row["x"] for row in ode_table if "x" in row and "y" in row]
        ys = [row["y"] for row in ode_table if "x" in row and "y" in row]
        if not xs or not ys:
            return

        self._ax.clear()
        _apply_dark(self._ax)

        # Plot numerical line + markers
        self._ax.plot(
            xs,
            ys,
            "o-",
            color=ACCENT_CYAN,
            label=f"{method_name} (numerical)",
            markersize=4,
            linewidth=2,
        )

        # Optional exact solution overlay
        if exact_expr_str and exact_expr_str.strip():
            try:
                _, f_exact = parse_function_x(exact_expr_str)
                x_dense = np.linspace(min(xs), max(xs), 200)
                y_dense = [f_exact(val) for val in x_dense]
                self._ax.plot(
                    x_dense,
                    y_dense,
                    "--",
                    color=SUCCESS,
                    label="Exact Solution",
                    linewidth=1.8,
                )
            except Exception:
                pass  # Ignore invalid exact expression during overlay

        self._ax.set_xlabel("x")
        self._ax.set_ylabel("y")
        self._ax.set_title(f"Numerical Trajectory: {method_name}", fontsize=11, color=TEXT_PRIMARY)
        self._ax.grid(True)
        self._ax.legend(facecolor=BG_PANEL, edgecolor=BORDER, labelcolor=TEXT_PRIMARY)
        self._fig.tight_layout()
        self._canvas.draw_idle()

    def plot_comparison(self, results_dict: dict[str, Any]) -> None:
        """Plot multiple ODE methods on the same axes."""
        if not _MPL_AVAILABLE or not results_dict:
            return

        colors = {
            "euler": ACCENT_CYAN,
            "modified_euler": ACCENT_VIOLET,
            "rk4": SUCCESS,
        }

        self._ax.clear()
        _apply_dark(self._ax)

        has_curves = False
        for method_key, res in results_dict.items():
            if not res or not res.ode_table:
                continue
            xs = [row["x"] for row in res.ode_table if "x" in row and "y" in row]
            ys = [row["y"] for row in res.ode_table if "x" in row and "y" in row]
            if not xs or not ys:
                continue

            color = colors.get(method_key.lower().replace("-", "_").replace(" ", "_"), TEXT_PRIMARY)
            label = getattr(res, "method", method_key)
            self._ax.plot(xs, ys, "o-", color=color, label=label, markersize=3, linewidth=1.8)
            has_curves = True

        if has_curves:
            self._ax.set_xlabel("x")
            self._ax.set_ylabel("y")
            self._ax.set_title("Method Comparison: ODE Trajectories", fontsize=11, color=TEXT_PRIMARY)
            self._ax.grid(True)
            self._ax.legend(facecolor=BG_PANEL, edgecolor=BORDER, labelcolor=TEXT_PRIMARY)
        else:
            self.clear()

        self._fig.tight_layout()
        self._canvas.draw_idle()
