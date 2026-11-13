"""
NUMERIX RootPlotPanel — Matplotlib visualization embedded in a ttk.Notebook.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

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

# ── Matplotlib import (optional) ──────────────────────────────────────────
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


class _NoMplPlaceholder(tk.Frame):
    """Shown when matplotlib is not available."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=BG_SECONDARY)
        tk.Label(
            self,
            text="Matplotlib not installed.\nInstall it with:  pip install matplotlib",
            font=("Consolas", 11),
            fg=WARNING,
            bg=BG_SECONDARY,
            justify=tk.CENTER,
        ).pack(expand=True)


class RootPlotPanel(tk.Frame):
    """Embeds Matplotlib figures inside a ttk.Notebook with two tabs."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, **kwargs)
        self._build()

    def _build(self) -> None:
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        if not _MPL_AVAILABLE:
            tab1 = _NoMplPlaceholder(self._notebook)
            tab2 = _NoMplPlaceholder(self._notebook)
            self._notebook.add(tab1, text="Function Plot")
            self._notebook.add(tab2, text="Error Plot")
            return

        # ── Function plot tab ─────────────────────────────────────────────
        self._func_frame = tk.Frame(self._notebook, bg=BG_MAIN)
        self._notebook.add(self._func_frame, text="Function Plot")

        with plt.rc_context(_DARK_PARAMS):
            self._func_fig = Figure(figsize=(6, 4), dpi=96)
            self._func_ax = self._func_fig.add_subplot(111)
        _apply_dark(self._func_ax)
        self._func_fig.tight_layout(pad=1.5)

        self._func_canvas = FigureCanvasTkAgg(self._func_fig, master=self._func_frame)
        self._func_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # ── Error plot tab ────────────────────────────────────────────────
        self._err_frame = tk.Frame(self._notebook, bg=BG_MAIN)
        self._notebook.add(self._err_frame, text="Error Plot")

        with plt.rc_context(_DARK_PARAMS):
            self._err_fig = Figure(figsize=(6, 4), dpi=96)
            self._err_ax = self._err_fig.add_subplot(111)
        _apply_dark(self._err_ax)
        self._err_fig.tight_layout(pad=1.5)

        self._err_canvas = FigureCanvasTkAgg(self._err_fig, master=self._err_frame)
        self._err_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear(self) -> None:
        if not _MPL_AVAILABLE:
            return
        for ax, canvas, fig in (
            (self._func_ax, self._func_canvas, self._func_fig),
            (self._err_ax,  self._err_canvas,  self._err_fig),
        ):
            ax.cla()
            _apply_dark(ax)
            fig.tight_layout(pad=1.5)
            canvas.draw_idle()

    def plot_function(
        self,
        expr_str: str,
        root: float | None,
        a: float | None,
        b: float | None,
        iterations: list[Any],
        method_name: str,
    ) -> None:
        """Plot f(x) with root marker and bracket indicators."""
        if not _MPL_AVAILABLE:
            return
        try:
            from numerix.core.expression_parser import parse_function_x
        except ImportError:
            return

        try:
            _, f = parse_function_x(expr_str)
        except Exception:
            return

        ax = self._func_ax
        ax.cla()
        _apply_dark(ax)

        # Determine plot range
        x_lo, x_hi = -5.0, 5.0
        if a is not None and b is not None:
            margin = max(abs(b - a) * 0.5, 0.5)
            x_lo, x_hi = a - margin, b + margin
        elif root is not None:
            margin = max(abs(root) * 0.5, 1.0)
            x_lo, x_hi = root - margin, root + margin

        xs = np.linspace(x_lo, x_hi, 500)
        ys = []
        for xv in xs:
            try:
                ys.append(f(float(xv)))
            except Exception:
                ys.append(float("nan"))
        ys_arr = np.array(ys, dtype=float)

        # Mask non-finite values
        mask = np.isfinite(ys_arr)
        if not mask.any():
            ax.text(0.5, 0.5, "Cannot evaluate f(x) on this range",
                    transform=ax.transAxes, ha="center", va="center", color=WARNING)
            self._func_canvas.draw_idle()
            return

        ax.plot(xs[mask], ys_arr[mask], color=ACCENT_CYAN, linewidth=2, label="f(x)")
        ax.axhline(0, color=BORDER, linewidth=1, linestyle="-")

        # Bracket shading
        mname = method_name.lower().replace("-", "_").replace(" ", "_")
        if mname in ("bisection", "false_position") and a is not None and b is not None:
            ax.axvspan(a, b, alpha=0.12, color=ACCENT_VIOLET, label="Bracket [a,b]")
            ax.axvline(a, color=ACCENT_VIOLET, linewidth=1, linestyle="--", alpha=0.6)
            ax.axvline(b, color=ACCENT_VIOLET, linewidth=1, linestyle="--", alpha=0.6)

        # Root marker
        if root is not None:
            try:
                f_root = f(root)
            except Exception:
                f_root = 0.0
            ax.plot(root, 0.0, "o", color=SUCCESS, markersize=9, label=f"Root ≈ {root:.6g}", zorder=5)

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title(f"f(x) = {expr_str}", color=TEXT_PRIMARY, fontsize=10)
        ax.legend(fontsize=8, facecolor=BG_PANEL, edgecolor=BORDER, labelcolor=TEXT_PRIMARY)
        ax.grid(True)

        self._func_fig.tight_layout(pad=1.5)
        self._func_canvas.draw_idle()

    def plot_error(self, iterations: list[Any]) -> None:
        """Plot approximate error vs iteration number."""
        if not _MPL_AVAILABLE:
            return

        ax = self._err_ax
        ax.cla()
        _apply_dark(ax)

        ns, errs = [], []
        for rec in iterations:
            if rec.approximate_error is not None:
                try:
                    e = float(rec.approximate_error)
                    if e > 0 and np.isfinite(e):
                        ns.append(rec.n)
                        errs.append(e)
                except (TypeError, ValueError):
                    continue

        if not ns:
            ax.text(0.5, 0.5, "No error data available",
                    transform=ax.transAxes, ha="center", va="center", color=TEXT_SECONDARY)
            self._err_canvas.draw_idle()
            return

        # Use log scale if range > 3 orders of magnitude
        use_log = (max(errs) / max(min(errs), 1e-300)) > 1e3

        ax.plot(ns, errs, color=WARNING, linewidth=2, marker="o",
                markersize=4, label="Approx. Error")

        if use_log:
            ax.set_yscale("log")

        ax.set_xlabel("Iteration")
        ax.set_ylabel("Approximate Error" + (" (log)" if use_log else ""))
        ax.set_title("Convergence", color=TEXT_PRIMARY, fontsize=10)
        ax.legend(fontsize=8, facecolor=BG_PANEL, edgecolor=BORDER, labelcolor=TEXT_PRIMARY)
        ax.grid(True)

        self._err_fig.tight_layout(pad=1.5)
        self._err_canvas.draw_idle()
