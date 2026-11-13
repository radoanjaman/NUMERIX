"""
Health check route.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "NUMERIX Numerical API",
        "version": "2.0.0",
        "methods_supported": [
            "bisection",
            "false_position",
            "newton_raphson",
            "gauss_elimination",
            "gauss_jordan",
            "euler",
            "modified_euler",
            "rk4",
        ],
    }
