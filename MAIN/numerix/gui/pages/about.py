"""
NUMERIX About Page — project identity, algorithm specifications, and verification credits.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    ACCENT_VIOLET,
    BG_ELEVATED,
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


class AboutPage(tk.Frame):
    """About & Educational Help View for NUMERIX."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_SECONDARY, padx=30, pady=24, **kwargs)
        self._build()

    def _build(self) -> None:
        # Title
        tk.Label(self, text="NUMERIX", font=FONT_LARGE, fg=ACCENT_CYAN, bg=BG_SECONDARY).pack(anchor="w")
        tk.Label(
            self,
            text="Understand the Mathematics. Visualize the Process. Verify the Results.",
            font=FONT_SUBHEADING,
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY,
        ).pack(anchor="w", pady=(2, 6))

        tk.Label(
            self,
            text="Interactive Numerical Methods Simulator — Built for University Laboratory Learning",
            font=FONT_UI,
            fg=TEXT_SECONDARY,
            bg=BG_SECONDARY,
        ).pack(anchor="w", pady=(0, 20))

        # Main Info Box
        box = tk.LabelFrame(
            self,
            text=" Supported Numerical Methods (Phase 1 & Phase 2) ",
            font=FONT_SUBHEADING,
            fg=ACCENT_CYAN,
            bg=BG_PANEL,
            padx=16,
            pady=14,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        box.pack(fill=tk.BOTH, expand=True)

        sections = [
            ("Root Finding", [
                "Bisection Method — interval halving with guaranteed bracket convergence",
                "False Position (Regula Falsi) — linear interpolation with bracket retention",
                "Newton-Raphson Method — quadratic tangent convergence with auto-differentiation",
            ]),
            ("Linear Systems", [
                "Gauss Elimination — forward elimination with partial pivoting & back-substitution",
                "Gauss-Jordan Elimination — full reduction to reduced row-echelon form (RREF)",
            ]),
            ("Differential Equations (ODEs)", [
                "Euler Method — 1st-order forward finite difference integration",
                "Modified Euler (Heun) — 2nd-order predictor-corrector scheme",
                "Runge-Kutta 4 (RK4) — 4th-order multi-stage classical method",
            ]),
        ]

        for title, items in sections:
            tk.Label(box, text=f"■  {title}", font=FONT_UI_BOLD, fg=ACCENT_VIOLET, bg=BG_PANEL).pack(anchor="w", pady=(6, 2))
            for item in items:
                tk.Label(box, text=f"    •  {item}", font=FONT_UI, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=1)

        # Technical details footer
        tech = tk.Label(
            self,
            text=(
                "Architecture: Python 3 · Tkinter (ttk) · Matplotlib (TkAgg) · NumPy · SymPy\n"
                "Computation Engine: 118 automated tests passing · High-resolution monotonic timers · Fully offline"
            ),
            font=FONT_MONO,
            fg=TEXT_SECONDARY,
            bg=BG_SECONDARY,
            justify=tk.LEFT,
        )
        tech.pack(anchor="w", pady=(16, 0))
