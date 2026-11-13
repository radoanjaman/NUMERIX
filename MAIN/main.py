"""
NUMERIX — Desktop Application Entry Point.

Launch:
    python main.py
"""
import os
import sys

# Ensure repository root is on sys.path
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from numerix.gui.app import NumerixApp


def main() -> None:
    if "--test-import" in sys.argv:
        print("NUMERIX Desktop Application imported successfully.")
        sys.exit(0)

    app = NumerixApp()
    app.mainloop()


if __name__ == "__main__":
    main()
