"""
NUMERIX MetricCard + MetricsRow components.
"""
from __future__ import annotations

import tkinter as tk
from typing import Any

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    BG_ELEVATED,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    FONT_MONO,
    FONT_UI,
    FONT_UI_BOLD,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
    ERROR,
)


def _fmt(val: Any) -> str:
    """Format a numeric value for display."""
    if val is None:
        return "—"
    if isinstance(val, float):
        if abs(val) < 1e-3 or abs(val) > 1e6:
            return f"{val:.6e}"
        return f"{val:.8g}"
    return str(val)


class MetricCard(tk.Frame):
    """A single elevated card displaying a label and a value."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        value: str = "—",
        value_color: str = TEXT_PRIMARY,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            bg=BG_ELEVATED,
            padx=12,
            pady=8,
            **kwargs,
        )
        self._value_color = value_color

        self._lbl = tk.Label(
            self,
            text=label,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_ELEVATED,
        )
        self._lbl.pack(anchor="w")

        self._val_var = tk.StringVar(value=value)
        self._val_lbl = tk.Label(
            self,
            textvariable=self._val_var,
            font=FONT_MONO,
            fg=value_color,
            bg=BG_ELEVATED,
        )
        self._val_lbl.pack(anchor="w")

    def set_value(self, value: Any, color: str | None = None) -> None:
        self._val_var.set(_fmt(value))
        if color:
            self._val_lbl.configure(fg=color)
        else:
            self._val_lbl.configure(fg=self._value_color)

    def reset(self) -> None:
        self._val_var.set("—")
        self._val_lbl.configure(fg=self._value_color)


class MetricsRow(tk.Frame):
    """Horizontal strip of MetricCards updated from a SolverResult."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, **kwargs)
        self._build()

    def _build(self) -> None:
        self._card_root = MetricCard(self, "Root", value_color=ACCENT_CYAN)
        self._card_root.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self._card_iter = MetricCard(self, "Iterations")
        self._card_iter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self._card_err = MetricCard(self, "Final Error")
        self._card_err.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self._card_time = MetricCard(self, "Time (s)")
        self._card_time.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self._card_status = MetricCard(self, "Status")
        self._card_status.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

    def update_from_result(self, result: Any) -> None:
        """Populate cards from a SolverResult object."""
        # Root
        self._card_root.set_value(result.root, ACCENT_CYAN)

        # Iterations
        self._card_iter.set_value(result.metrics.iterations)

        # Error
        self._card_err.set_value(result.metrics.final_approximate_error)

        # Time
        t = result.metrics.execution_time_seconds
        if t is not None:
            self._card_time.set_value(f"{t:.4f}")
        else:
            self._card_time.set_value(None)

        # Status
        status_str = result.status.value if hasattr(result.status, "value") else str(result.status)
        color = SUCCESS if "converge" in status_str.lower() or "success" in status_str.lower() else WARNING
        if "error" in status_str.lower() or "invalid" in status_str.lower() or "singular" in status_str.lower():
            color = ERROR
        self._card_status.set_value(status_str, color)

    def reset(self) -> None:
        """Reset all cards to placeholder dash."""
        for card in (
            self._card_root,
            self._card_iter,
            self._card_err,
            self._card_time,
            self._card_status,
        ):
            card.reset()
