"""
NUMERIX Desktop Application Shell — Tkinter main window, navigation rail, and page coordinator.
"""
from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk
from typing import Any

from numerix.gui.components.header import PageHeader
from numerix.gui.components.sidebar import Sidebar
from numerix.gui.components.status_bar import StatusBar
from numerix.gui.pages.about import AboutPage
from numerix.gui.pages.comparison import ComparisonPage
from numerix.gui.pages.dashboard import DashboardPage
from numerix.gui.pages.differential_equations import DifferentialEquationsPage
from numerix.gui.pages.linear_systems import LinearSystemsPage
from numerix.gui.pages.root_finding import RootFindingPage
from numerix.gui.theme.colors import BG_MAIN, BG_SECONDARY
from numerix.gui.theme.styles import apply_theme


_PAGE_DESCRIPTIONS = {
    "Dashboard": ("Dashboard", "Overview, method categories, and quick-start presets"),
    "Root Finding": ("Root Finding", "Solve nonlinear equations f(x) = 0 with bracketing and open methods"),
    "Linear Systems": ("Linear Systems", "Solve Ax = b with partial pivoting and inspect row operations"),
    "Diff. Equations": ("Differential Equations", "Integrate initial-value problems dy/dx = f(x, y)"),
    "Comparison": ("Method Comparison", "Benchmark multiple numerical algorithms on identical problems"),
    "About": ("About NUMERIX", "Algorithm specifications, architecture, and educational documentation"),
}


class NumerixApp(tk.Tk):
    """Main NUMERIX application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title("NUMERIX — Numerical Methods Simulator")
        self.geometry("1280x820")
        self.minsize(920, 600)
        self.configure(bg=BG_MAIN)

        # Apply dark theme
        apply_theme(self)

        self._active_page_name = "Dashboard"
        self._pages: dict[str, tk.Widget] = {}

        self._build_layout()
        self.navigate("Dashboard")

    def _build_layout(self) -> None:
        # Window grid: Col 0 = Sidebar (fixed width), Col 1 = Main Content (expand)
        self.columnconfigure(0, weight=0, minsize=200)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ── Sidebar ────────────────────────────────────────────────────────────
        self._sidebar = Sidebar(self, on_navigate=self.navigate)
        self._sidebar.grid(row=0, column=0, sticky="nsew")

        # ── Right / Main Container ─────────────────────────────────────────────
        main_container = tk.Frame(self, bg=BG_SECONDARY)
        main_container.grid(row=0, column=1, sticky="nsew")
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)  # Page content row expands

        # Top Header Bar
        self._header = PageHeader(main_container)
        self._header.grid(row=0, column=0, sticky="ew")

        # Content Area Frame (holds pages)
        self._content_area = tk.Frame(main_container, bg=BG_SECONDARY)
        self._content_area.grid(row=1, column=0, sticky="nsew")
        self._content_area.rowconfigure(0, weight=1)
        self._content_area.columnconfigure(0, weight=1)

        # Bottom Status Bar
        self._status_bar = StatusBar(main_container)
        self._status_bar.grid(row=2, column=0, sticky="ew")

    def _get_or_create_page(self, name: str) -> tk.Widget:
        if name not in self._pages:
            if name == "Dashboard":
                p = DashboardPage(self._content_area, on_navigate=self.navigate)
            elif name == "Root Finding":
                p = RootFindingPage(self._content_area, status_bar=self._status_bar)
            elif name == "Linear Systems":
                p = LinearSystemsPage(self._content_area, status_bar=self._status_bar)
            elif name == "Diff. Equations":
                p = DifferentialEquationsPage(self._content_area, status_bar=self._status_bar)
            elif name == "Comparison":
                p = ComparisonPage(self._content_area, status_bar=self._status_bar)
            elif name == "About":
                p = AboutPage(self._content_area)
            else:
                p = tk.Frame(self._content_area, bg=BG_SECONDARY)
            self._pages[name] = p
            p.grid(row=0, column=0, sticky="nsew")
        return self._pages[name]

    def navigate(self, page_name: str) -> None:
        """Switch visible page, update header, and highlight sidebar item."""
        if page_name not in _PAGE_DESCRIPTIONS:
            return

        self._active_page_name = page_name

        # Update sidebar and header
        self._sidebar.set_active(page_name)
        title, subtitle = _PAGE_DESCRIPTIONS[page_name]
        self._header.update(title, subtitle)

        # Raise requested page
        page_widget = self._get_or_create_page(page_name)
        page_widget.tkraise()
        self._status_bar.set_ready()


def main() -> None:
    if "--test-import" in sys.argv:
        print("Import check successful.")
        sys.exit(0)

    app = NumerixApp()
    app.mainloop()


if __name__ == "__main__":
    main()
