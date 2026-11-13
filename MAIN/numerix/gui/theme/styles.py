"""
NUMERIX ttk Style configuration — dark theme.

Call apply_theme(root) once after creating the Tk root window.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from numerix.gui.theme.colors import (
    ACCENT_CYAN,
    BG_ELEVATED,
    BG_MAIN,
    BG_PANEL,
    BG_SECONDARY,
    BORDER,
    ERROR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
    SUCCESS,
    FONT_UI,
    FONT_UI_BOLD,
    FONT_MONO,
)


def apply_theme(root: tk.Tk) -> None:
    """Configure ttk.Style globally for the NUMERIX dark theme."""
    style = ttk.Style(root)

    # Use 'clam' as the base — it allows the most colour overrides
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass  # fall back to whatever is available

    # ── TFrame ────────────────────────────────────────────────────────────
    style.configure("TFrame", background=BG_SECONDARY)

    # ── TLabel ────────────────────────────────────────────────────────────
    style.configure(
        "TLabel",
        background=BG_SECONDARY,
        foreground=TEXT_PRIMARY,
        font=FONT_UI,
    )
    style.configure(
        "Secondary.TLabel",
        background=BG_SECONDARY,
        foreground=TEXT_SECONDARY,
        font=FONT_UI,
    )
    style.configure(
        "Panel.TLabel",
        background=BG_PANEL,
        foreground=TEXT_PRIMARY,
        font=FONT_UI,
    )
    style.configure(
        "Elevated.TLabel",
        background=BG_ELEVATED,
        foreground=TEXT_PRIMARY,
        font=FONT_UI,
    )

    # ── TButton base ──────────────────────────────────────────────────────
    style.configure(
        "NX.TButton",
        background=BG_ELEVATED,
        foreground=TEXT_PRIMARY,
        font=FONT_UI_BOLD,
        borderwidth=1,
        relief="flat",
        padding=(12, 6),
        focuscolor=ACCENT_CYAN,
    )
    style.map(
        "NX.TButton",
        background=[
            ("active", ACCENT_CYAN),
            ("pressed", ACCENT_CYAN),
            ("disabled", BG_PANEL),
        ],
        foreground=[
            ("active", BG_MAIN),
            ("pressed", BG_MAIN),
            ("disabled", TEXT_SECONDARY),
        ],
    )

    # ── Accent button ─────────────────────────────────────────────────────
    style.configure(
        "Accent.NX.TButton",
        background=ACCENT_CYAN,
        foreground=BG_MAIN,
        font=FONT_UI_BOLD,
        borderwidth=0,
        relief="flat",
        padding=(12, 6),
    )
    style.map(
        "Accent.NX.TButton",
        background=[
            ("active", "#7DD3FC"),
            ("pressed", "#0EA5E9"),
            ("disabled", BG_PANEL),
        ],
        foreground=[
            ("active", BG_MAIN),
            ("disabled", TEXT_SECONDARY),
        ],
    )

    # ── Danger button ─────────────────────────────────────────────────────
    style.configure(
        "Danger.NX.TButton",
        background=ERROR,
        foreground=TEXT_PRIMARY,
        font=FONT_UI_BOLD,
        borderwidth=0,
        relief="flat",
        padding=(12, 6),
    )
    style.map(
        "Danger.NX.TButton",
        background=[
            ("active", "#F87171"),
            ("pressed", "#DC2626"),
            ("disabled", BG_PANEL),
        ],
    )

    # ── TEntry ────────────────────────────────────────────────────────────
    style.configure(
        "TEntry",
        fieldbackground=BG_PANEL,
        foreground=TEXT_PRIMARY,
        insertcolor=TEXT_PRIMARY,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        font=FONT_MONO,
        padding=4,
    )
    style.map(
        "TEntry",
        fieldbackground=[("focus", BG_ELEVATED)],
        bordercolor=[("focus", ACCENT_CYAN)],
    )

    # ── TCombobox ─────────────────────────────────────────────────────────
    style.configure(
        "TCombobox",
        fieldbackground=BG_PANEL,
        foreground=TEXT_PRIMARY,
        background=BG_ELEVATED,
        insertcolor=TEXT_PRIMARY,
        bordercolor=BORDER,
        arrowcolor=TEXT_PRIMARY,
        font=FONT_UI,
        padding=4,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", BG_PANEL), ("focus", BG_ELEVATED)],
        bordercolor=[("focus", ACCENT_CYAN)],
        foreground=[("readonly", TEXT_PRIMARY)],
    )
    # Dropdown listbox colours — set via option_add on root
    root.option_add("*TCombobox*Listbox.background", BG_ELEVATED)
    root.option_add("*TCombobox*Listbox.foreground", TEXT_PRIMARY)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT_CYAN)
    root.option_add("*TCombobox*Listbox.selectForeground", BG_MAIN)
    root.option_add("*TCombobox*Listbox.font", FONT_UI)

    # ── Treeview ──────────────────────────────────────────────────────────
    style.configure(
        "Treeview",
        background=BG_PANEL,
        foreground=TEXT_PRIMARY,
        fieldbackground=BG_PANEL,
        bordercolor=BORDER,
        font=FONT_MONO,
        rowheight=24,
    )
    style.configure(
        "Treeview.Heading",
        background=BG_ELEVATED,
        foreground=ACCENT_CYAN,
        font=FONT_UI_BOLD,
        relief="flat",
        bordercolor=BORDER,
    )
    style.map(
        "Treeview",
        background=[("selected", BG_ELEVATED)],
        foreground=[("selected", ACCENT_CYAN)],
    )
    style.map(
        "Treeview.Heading",
        background=[("active", BG_ELEVATED)],
    )

    # ── TNotebook ─────────────────────────────────────────────────────────
    style.configure(
        "TNotebook",
        background=BG_SECONDARY,
        bordercolor=BORDER,
        tabmargins=[2, 5, 2, 0],
    )
    style.configure(
        "TNotebook.Tab",
        background=BG_PANEL,
        foreground=TEXT_SECONDARY,
        font=FONT_UI,
        padding=[12, 5],
        bordercolor=BORDER,
    )
    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", BG_ELEVATED),
            ("active", BG_ELEVATED),
        ],
        foreground=[
            ("selected", ACCENT_CYAN),
            ("active", TEXT_PRIMARY),
        ],
    )

    # ── Scrollbar ─────────────────────────────────────────────────────────
    style.configure(
        "TScrollbar",
        background=BG_ELEVATED,
        troughcolor=BG_PANEL,
        bordercolor=BORDER,
        arrowcolor=TEXT_SECONDARY,
        relief="flat",
        arrowsize=12,
    )
    style.map(
        "TScrollbar",
        background=[("active", ACCENT_CYAN), ("pressed", ACCENT_CYAN)],
    )

    # ── TSeparator ────────────────────────────────────────────────────────
    style.configure("TSeparator", background=BORDER)

    # ── Root window background ────────────────────────────────────────────
    root.configure(background=BG_MAIN)
