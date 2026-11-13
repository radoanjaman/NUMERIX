"""
NUMERIX StatusBar component — bottom strip showing solver state.
"""
from __future__ import annotations

import tkinter as tk

from numerix.gui.theme.colors import (
    BG_ELEVATED,
    BORDER,
    ERROR,
    FONT_UI,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)

_BULLET = "●"


class StatusBar(tk.Frame):
    """Bottom status strip — shows ready / running / done / error state."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_ELEVATED, **kwargs)
        self._build()

    def _build(self) -> None:
        # Top border
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X)

        inner = tk.Frame(self, bg=BG_ELEVATED)
        inner.pack(fill=tk.X, padx=12, pady=4)

        self._bullet = tk.Label(
            inner,
            text=_BULLET,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_ELEVATED,
        )
        self._bullet.pack(side=tk.LEFT)

        self._status_var = tk.StringVar(value="Ready")
        self._status_lbl = tk.Label(
            inner,
            textvariable=self._status_var,
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_ELEVATED,
        )
        self._status_lbl.pack(side=tk.LEFT, padx=(4, 0))

        # Right-aligned detail
        self._detail_var = tk.StringVar(value="")
        self._detail_lbl = tk.Label(
            inner,
            textvariable=self._detail_var,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_ELEVATED,
        )
        self._detail_lbl.pack(side=tk.RIGHT)

    def set_ready(self) -> None:
        self._bullet.configure(fg=TEXT_SECONDARY)
        self._status_var.set("Ready")
        self._status_lbl.configure(fg=TEXT_PRIMARY)
        self._detail_var.set("")

    def set_running(self, method: str = "") -> None:
        self._bullet.configure(fg=WARNING)
        self._status_var.set("Running…")
        self._status_lbl.configure(fg=WARNING)
        self._detail_var.set(method)

    def set_done(self, msg: str = "") -> None:
        self._bullet.configure(fg=SUCCESS)
        self._status_var.set("Done")
        self._status_lbl.configure(fg=SUCCESS)
        self._detail_var.set(msg)

    def set_error(self, msg: str = "") -> None:
        self._bullet.configure(fg=ERROR)
        self._status_var.set("Error")
        self._status_lbl.configure(fg=ERROR)
        self._detail_var.set(msg)
