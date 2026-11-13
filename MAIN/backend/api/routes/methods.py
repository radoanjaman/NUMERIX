"""
Supported numerical methods catalog endpoint.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Methods"])


@router.get("/methods")
def get_supported_methods():
    return {
        "categories": [
            {
                "id": "root_finding",
                "name": "Root Finding",
                "description": "Find real roots of nonlinear functions f(x) = 0",
                "methods": [
                    {
                        "id": "bisection",
                        "name": "Bisection Method",
                        "type": "bracketing",
                        "order": "linear",
                        "requires": ["expression", "a", "b", "tol", "max_iter"],
                        "description": "Interval halving method with guaranteed convergence when a sign change exists.",
                    },
                    {
                        "id": "false_position",
                        "name": "False Position (Regula Falsi)",
                        "type": "bracketing",
                        "order": "linear / superlinear",
                        "requires": ["expression", "a", "b", "tol", "max_iter"],
                        "description": "Linear interpolation method maintaining opposite-sign endpoints.",
                    },
                    {
                        "id": "newton_raphson",
                        "name": "Newton-Raphson Method",
                        "type": "open",
                        "order": "quadratic",
                        "requires": ["expression", "x0", "tol", "max_iter"],
                        "description": "Tangent-line iteration with automatic symbolic derivative evaluation.",
                    },
                ],
            },
            {
                "id": "linear_systems",
                "name": "Linear Systems",
                "description": "Solve systems of linear algebraic equations A x = b",
                "methods": [
                    {
                        "id": "gauss_elimination",
                        "name": "Gauss Elimination with Partial Pivoting",
                        "requires": ["A", "b"],
                        "description": "Forward elimination to upper triangular matrix with row swaps and back-substitution.",
                    },
                    {
                        "id": "gauss_jordan",
                        "name": "Gauss-Jordan Elimination",
                        "requires": ["A", "b"],
                        "description": "Complete elimination above and below pivots yielding Reduced Row Echelon Form (RREF).",
                    },
                ],
            },
            {
                "id": "differential_equations",
                "name": "Differential Equations (ODEs)",
                "description": "Numerically integrate initial-value problems dy/dx = f(x, y)",
                "methods": [
                    {
                        "id": "euler",
                        "name": "Euler Method",
                        "order": 1,
                        "requires": ["expression", "x0", "y0", "h", "x_end"],
                        "description": "First-order forward difference stepping scheme.",
                    },
                    {
                        "id": "modified_euler",
                        "name": "Modified Euler (Heun)",
                        "order": 2,
                        "requires": ["expression", "x0", "y0", "h", "x_end"],
                        "description": "Second-order predictor-corrector averaging initial and predicted slopes.",
                    },
                    {
                        "id": "rk4",
                        "name": "Runge-Kutta 4th Order (RK4)",
                        "order": 4,
                        "requires": ["expression", "x0", "y0", "h", "x_end"],
                        "description": "Classical high-accuracy four-stage slope evaluation method.",
                    },
                ],
            },
        ]
    }
