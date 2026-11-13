"""
NUMERIX FastAPI Application Entry Point.
"""
from __future__ import annotations

import os
import sys

# Ensure repository root is on sys.path so numerix core modules can be imported
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.routes import comparison, health, learning, linear_systems, methods, ode, root_finding

app = FastAPI(
    title="NUMERIX Numerical Engine API",
    description="REST API for the NUMERIX numerical methods platform supporting root finding, linear systems, and ODEs.",
    version="2.0.0",
)

# ── CORS Configuration ─────────────────────────────────────────────────────────
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Safe Exception Handler (Never leak stack traces to client) ────────────────
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal numerical engine error occurred. Check input values."},
    )

# ── Mount API Routers ──────────────────────────────────────────────────────────
app.include_router(health.router, prefix="/api")
app.include_router(methods.router, prefix="/api")
app.include_router(root_finding.router, prefix="/api")
app.include_router(linear_systems.router, prefix="/api")
app.include_router(ode.router, prefix="/api")
app.include_router(comparison.router, prefix="/api")
app.include_router(learning.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "NUMERIX Numerical Engine API",
        "version": "2.0.0",
        "status": "online",
        "docs_url": "/docs",
        "endpoints": [
            "/api/health",
            "/api/methods",
            "/api/solve/root",
            "/api/solve/linear",
            "/api/solve/ode",
            "/api/compare",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
