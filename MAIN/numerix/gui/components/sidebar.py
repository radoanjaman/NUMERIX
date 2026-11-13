"""
NUMERIX Sidebar navigation component.
"""
from __future__ import annotations

import tkinter as tk
from typing import Callable

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    BG_ELEVATED,
    BG_MAIN,
    BORDER,
    FONT_LARGE,
    FONT_UI,
    FONT_UI_BOLD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

_NAV_ITEMS = [
    ("Dashboard",       "Dashboard"),
    ("Root Finding",    "Root Finding"),
    ("Linear Systems",  "Linear Systems"),
    ("Diff. Equations", "Diff. Equations"),
    ("Comparison",      "Comparison"),
    ("About",           "About"),
]


class _NavItem(tk.Frame):
    """A single sidebar navigation row."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        page: str,
        on_click: Callable[[str], None],
    ) -> None:
        super().__init__(parent, bg=BG_MAIN, cursor="hand2")
        self._page = page
        self._on_click = on_click
        self._active = False

        # Left accent bar (shown only when active)
        self._accent = tk.Frame(self, bg=BG_MAIN, width=3)
        self._accent.pack(side=tk.LEFT, fill=tk.Y)
        self._accent.pack_propagate(False)

        # Label
        self._label = tk.Label(
            self,
            text=label,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_MAIN,
            anchor="w",
            padx=14,
            pady=10,
        )
        self._label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind clicks on every child widget
        for widget in (self, self._label, self._accent):
            widget.bind("<Button-1>", self._clicked)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _clicked(self, _event: tk.Event) -> None:
        self._on_click(self._page)

    def _on_enter(self, _event: tk.Event) -> None:
        if not self._active:
            self._label.configure(fg=TEXT_PRIMARY)
            self.configure(bg=BG_ELEVATED)
            self._label.configure(bg=BG_ELEVATED)

    def _on_leave(self, _event: tk.Event) -> None:
        if not self._active:
            self._label.configure(fg=TEXT_SECONDARY)
            self.configure(bg=BG_MAIN)
            self._label.configure(bg=BG_MAIN)

    def set_active(self, active: bool) -> None:
        self._active = active
        if active:
            self._accent.configure(bg=ACCENT_CYAN)
            self._label.configure(
                fg=ACCENT_CYAN,
                bg=BG_ELEVATED,
                font=FONT_UI_BOLD,
            )
            self.configure(bg=BG_ELEVATED)
        else:
            self._accent.configure(bg=BG_MAIN)
            self._label.configure(
                fg=TEXT_SECONDARY,
                bg=BG_MAIN,
                font=FONT_UI,
            )
            self.configure(bg=BG_MAIN)


class Sidebar(tk.Frame):
    """Fixed-width dark sidebar with logo and navigation."""

    WIDTH = 200

    def __init__(
        self,
        parent: tk.Widget,
        on_navigate: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=BG_MAIN, width=self.WIDTH, **kwargs)
        self.pack_propagate(False)
        self._on_navigate = on_navigate
        self._items: dict[str, _NavItem] = {}

        self._build()

    def _build(self) -> None:
        # ── Logo ──────────────────────────────────────────────────────────
        logo_frame = tk.Frame(self, bg=BG_MAIN)
        logo_frame.pack(fill=tk.X, pady=(20, 10))

        tk.Label(
            logo_frame,
            text="NUMERIX",
            font=FONT_LARGE,
            fg=ACCENT_CYAN,
            bg=BG_MAIN,
        ).pack(padx=16, anchor="w")

        tk.Label(
            logo_frame,
            text="Numerical Methods",
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_MAIN,
        ).pack(padx=16, anchor="w")

        # ── Separator ─────────────────────────────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X, padx=12, pady=8)

        # ── Nav items ─────────────────────────────────────────────────────
        for label, page in _NAV_ITEMS:
            item = _NavItem(self, label, page, self._on_navigate)
            item.pack(fill=tk.X)
            self._items[page] = item

        # ── Bottom spacer ─────────────────────────────────────────────────
        tk.Frame(self, bg=BG_MAIN).pack(fill=tk.BOTH, expand=True)

        # ── Version badge ─────────────────────────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X, padx=12, pady=(0, 4))
        tk.Label(
            self,
            text="v2.0  |  Phase 2",
            font=("Segoe UI", 8),
            fg=TEXT_SECONDARY,
            bg=BG_MAIN,
        ).pack(padx=16, pady=(0, 12), anchor="w")

    def set_active(self, page_name: str) -> None:
        """Highlight *page_name* and unhighlight all others."""
        for page, item in self._items.items():
            item.set_active(page == page_name)
