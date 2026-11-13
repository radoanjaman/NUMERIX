"""
NUMERIX — Root Entry Point.

Usage:
    python main.py              # Launch the Desktop GUI Application (Tkinter)
    python main.py --backend    # Launch the FastAPI Backend API
    python main.py --test-import # Verify module imports
"""
import os
import sys

# Ensure MAIN is in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(ROOT_DIR, "MAIN")
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

if __name__ == "__main__":
    if "--backend" in sys.argv:
        import uvicorn
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
    elif "--test-import" in sys.argv:
        from numerix.gui.app import NumerixApp
        from backend.main import app as fastapi_app
        print("NUMERIX Desktop & Backend imported successfully.")
        sys.exit(0)
    else:
        from numerix.gui.app import NumerixApp
        app = NumerixApp()
        app.mainloop()
