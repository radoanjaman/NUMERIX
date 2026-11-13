"""
NUMERIX PageHeader component — title + subtitle bar.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    BG_SECONDARY,
    BORDER,
    FONT_HEADING,
    FONT_UI,
    TEXT_SECONDARY,
)


class PageHeader(tk.Frame):
    """Horizontal header bar showing the current page title and subtitle."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, **kwargs)
        self._build()

    def _build(self) -> None:
        inner = tk.Frame(self, bg=BG_SECONDARY)
        inner.pack(fill=tk.X, padx=20, pady=12)

        self._title_var = tk.StringVar(value="Dashboard")
        self._subtitle_var = tk.StringVar(value="Welcome to NUMERIX")

        self._title_lbl = tk.Label(
            inner,
            textvariable=self._title_var,
            font=FONT_HEADING,
            fg=ACCENT_CYAN,
            bg=BG_SECONDARY,
        )
        self._title_lbl.pack(anchor="w")

        self._subtitle_lbl = tk.Label(
            inner,
            textvariable=self._subtitle_var,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_SECONDARY,
        )
        self._subtitle_lbl.pack(anchor="w")

        # Bottom border line
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X)

    def update(self, title: str, subtitle: str = "") -> None:
        """Update the displayed title and subtitle."""
        self._title_var.set(title)
        self._subtitle_var.set(subtitle)
