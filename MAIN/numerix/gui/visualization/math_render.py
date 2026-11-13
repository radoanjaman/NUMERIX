"""
Matplotlib MathText renderer for NUMERIX Tkinter GUI.
Renders LaTeX math formulas into PIL Image / PhotoImage for sharp display on dark glassmorphic panels.
"""

from io import BytesIO
from typing import Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


def render_math_to_image(
    latex_str: str,
    fontsize: int = 14,
    color: str = "#F5F7FA",
    dpi: int = 150,
    bg_color: Optional[str] = None
) -> Image.Image:
    """
    Renders a mathematical expression using Matplotlib MathText to a PIL Image.
    Works seamlessly on dark glassmorphism surfaces.
    """
    # Normalize LaTeX string
    clean_str = latex_str.strip()
    if not (clean_str.startswith("$") and clean_str.endswith("$")):
        clean_str = f"${clean_str}$"

    fig = plt.figure(figsize=(0.01, 0.01), dpi=dpi)
    if bg_color:
        fig.patch.set_facecolor(bg_color)
    else:
        fig.patch.set_alpha(0.0)

    # Render text using mathtext
    text = fig.text(
        0, 0, clean_str,
        fontsize=fontsize,
        color=color,
        ha="left",
        va="bottom"
    )

    buf = BytesIO()
    # Save with tight bbox to wrap equation exactly
    fig.savefig(
        buf,
        format="png",
        dpi=dpi,
        transparent=(bg_color is None),
        bbox_inches="tight",
        pad_inches=0.04
    )
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)


def render_math_photoimage(
    latex_str: str,
    fontsize: int = 14,
    color: str = "#F5F7FA",
    dpi: int = 150,
    bg_color: Optional[str] = None
) -> ImageTk.PhotoImage:
    """
    Convenience function returning a Tkinter-compatible PhotoImage.
    """
    img = render_math_to_image(latex_str, fontsize=fontsize, color=color, dpi=dpi, bg_color=bg_color)
    return ImageTk.PhotoImage(img)
