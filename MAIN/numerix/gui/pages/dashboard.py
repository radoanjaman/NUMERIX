"""
NUMERIX Dashboard Page — welcome, module overview cards, and quick start.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    ACCENT_VIOLET,
    BG_ELEVATED,
    BG_MAIN,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    FONT_HEADING,
    FONT_LARGE,
    FONT_MONO,
    FONT_SUBHEADING,
    FONT_UI,
    FONT_UI_BOLD,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class _ModuleCard(tk.Frame):
    """Clickable elevated card representing a topic category."""

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        tagline: str,
        methods: list[str],
        on_navigate: Callable[[str], None],
        target_page: str,
    ) -> None:
        super().__init__(
            parent,
            bg=BG_PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=18,
            pady=16,
            cursor="hand2",
        )
        self._target_page = target_page
        self._on_navigate = on_navigate

        # Title
        t_lbl = tk.Label(
            self,
            text=title,
            font=FONT_HEADING,
            fg=ACCENT_CYAN,
            bg=BG_PANEL,
        )
        t_lbl.pack(anchor="w")

        # Subtitle
        desc_lbl = tk.Label(
            self,
            text=tagline,
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_PANEL,
            wraplength=260,
            justify=tk.LEFT,
        )
        desc_lbl.pack(anchor="w", pady=(4, 10))

        # Methods list
        m_frame = tk.Frame(self, bg=BG_PANEL)
        m_frame.pack(fill=tk.X, pady=(0, 12))
        for m in methods:
            row = tk.Label(
                m_frame,
                text=f"• {m}",
                font=FONT_UI,
                fg=TEXT_PRIMARY,
                bg=BG_PANEL,
            )
            row.pack(anchor="w")

        # Action button
        btn = ttk.Button(
            self,
            text=f"Open {title} →",
            style="Accent.NX.TButton",
            command=lambda: self._on_navigate(self._target_page),
        )
        btn.pack(anchor="w")

        # Bind hover effects
        for w in (self, t_lbl, desc_lbl, m_frame):
            w.bind("<Enter>", lambda e: self.configure(bg=BG_ELEVATED))
            w.bind("<Leave>", lambda e: self.configure(bg=BG_PANEL))
            w.bind("<Button-1>", lambda e: self._on_navigate(self._target_page))


class DashboardPage(tk.Frame):
    """Dashboard view with welcome banner, module cards, and quick starts."""

    def __init__(
        self,
        parent: tk.Widget,
        on_navigate: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=BG_SECONDARY, padx=30, pady=24, **kwargs)
        self._on_navigate = on_navigate
        self._build()

    def _build(self) -> None:
        # ── Hero Banner ────────────────────────────────────────────────────────
        hero = tk.Frame(self, bg=BG_SECONDARY)
        hero.pack(fill=tk.X, pady=(0, 24))

        title = tk.Label(
            hero,
            text="NUMERIX Glass Lab",
            font=FONT_LARGE,
            fg=ACCENT_CYAN,
            bg=BG_SECONDARY,
        )
        title.pack(anchor="w")

        tagline = tk.Label(
            hero,
            text="Understand the Mathematics. Visualize the Process. Verify the Results.",
            font=FONT_SUBHEADING,
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY,
        )
        tagline.pack(anchor="w", pady=(2, 6))

        desc = tk.Label(
            hero,
            text=(
                "A modular numerical computation workbench for university laboratory study. "
                "Inspect iterations, matrix operations, trajectories, and compare algorithm behavior."
            ),
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_SECONDARY,
        )
        desc.pack(anchor="w")

        # ── Three Module Cards ─────────────────────────────────────────────────
        cards_frame = tk.Frame(self, bg=BG_SECONDARY)
        cards_frame.pack(fill=tk.X, pady=(0, 24))

        card_root = _ModuleCard(
            cards_frame,
            title="Root Finding",
            tagline="Find numerical roots of nonlinear equations f(x) = 0.",
            methods=["Bisection Method", "False Position (Regula Falsi)", "Newton-Raphson Method"],
            on_navigate=self._on_navigate,
            target_page="Root Finding",
        )
        card_root.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        card_linear = _ModuleCard(
            cards_frame,
            title="Linear Systems",
            tagline="Solve systems Ax = b and inspect step-by-step row operations.",
            methods=["Gauss Elimination (Partial Pivot)", "Gauss-Jordan (Full RREF)"],
            on_navigate=self._on_navigate,
            target_page="Linear Systems",
        )
        card_linear.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        card_ode = _ModuleCard(
            cards_frame,
            title="Diff. Equations",
            tagline="Integrate initial value problems dy/dx = f(x, y).",
            methods=["Euler Method (Order 1)", "Modified Euler (Heun Order 2)", "Runge-Kutta 4 (RK4 Order 4)"],
            on_navigate=self._on_navigate,
            target_page="Diff. Equations",
        )
        card_ode.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # ── Quick Start Section ────────────────────────────────────────────────
        qs_box = tk.LabelFrame(
            self,
            text=" Quick Starts & Presets ",
            font=FONT_SUBHEADING,
            fg=ACCENT_CYAN,
            bg=BG_PANEL,
            padx=16,
            pady=14,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        qs_box.pack(fill=tk.BOTH, expand=True)

        presets = [
            ("Root Finding: x³ - x - 2 on [1, 2]", "Root Finding"),
            ("Linear System: 3×3 Standard Well-Conditioned", "Linear Systems"),
            ("ODE: dy/dx = x + y with y(0)=1 over [0, 0.5]", "Diff. Equations"),
            ("Method Comparison: Compare Bisection vs False Position vs Newton-Raphson", "Comparison"),
        ]

        for text, target in presets:
            row = tk.Frame(qs_box, bg=BG_PANEL)
            row.pack(fill=tk.X, pady=4)

            lbl = tk.Label(row, text=f"•  {text}", font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL)
            lbl.pack(side=tk.LEFT)

            btn = ttk.Button(
                row,
                text="Load →",
                style="NX.TButton",
                command=lambda t=target: self._on_navigate(t),
            )
            btn.pack(side=tk.RIGHT)
