"""
NUMERIX Desktop Application Launcher
Run this from the repository root:
    python run_desktop.py
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(ROOT_DIR, "MAIN")
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

if __name__ == "__main__":
    if "--test-import" in sys.argv:
        from numerix.gui.app import NumerixApp
        print("NUMERIX Desktop Application imported successfully.")
        sys.exit(0)

    from numerix.gui.app import NumerixApp
    app = NumerixApp()
    app.mainloop()
