"""
NUMERIX Backend Server Launcher
Run this from the repository root:
    python run_backend.py
"""
import os
import sys

# Ensure MAIN is in sys.path so backend and numerix packages are resolved
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(ROOT_DIR, "MAIN")
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("  NUMERIX Numerical Engine & Learning API")
    print("  - Server:       http://127.0.0.1:8000")
    print("  - API Docs:     http://127.0.0.1:8000/docs")
    print("  - Health Check: http://127.0.0.1:8000/api/health")
    print("=" * 60 + "\n")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
