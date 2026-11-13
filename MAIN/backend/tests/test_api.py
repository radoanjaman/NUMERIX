"""
Tests for FastAPI Backend Endpoints using TestClient.
"""
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "online"
    assert "/api/health" in data["endpoints"]


def test_health_check():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "bisection" in data["methods_supported"]


def test_methods_catalog():
    resp = client.get("/api/methods")
    assert resp.status_code == 200
    data = resp.json()
    assert "categories" in data
    cat_ids = [c["id"] for c in data["categories"]]
    assert "root_finding" in cat_ids
    assert "linear_systems" in cat_ids
    assert "differential_equations" in cat_ids


# ── Root Finding Tests ─────────────────────────────────────────────────────────

def test_solve_bisection_endpoint():
    payload = {
        "method": "bisection",
        "expression": "x**3 - x - 2",
        "a": 1.0,
        "b": 2.0,
        "tol": 1e-6,
        "max_iter": 50,
    }
    resp = client.post("/api/solve/root", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert abs(data["root"] - 1.52138) < 1e-3
    assert len(data["iterations"]) > 0
    assert len(data["curves"]) >= 1


def test_solve_false_position_endpoint():
    payload = {
        "method": "false_position",
        "expression": "x**3 - x - 2",
        "a": 1.0,
        "b": 2.0,
        "tol": 1e-6,
    }
    resp = client.post("/api/solve/root", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["root"] is not None


def test_solve_newton_raphson_endpoint():
    payload = {
        "method": "newton_raphson",
        "expression": "x**3 - x - 2",
        "x0": 1.5,
        "tol": 1e-6,
    }
    resp = client.post("/api/solve/root", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert abs(data["root"] - 1.52138) < 1e-3


def test_root_finding_validation_error():
    # Invalid bracket: a >= b
    payload = {
        "method": "bisection",
        "expression": "x**2 - 4",
        "a": 3.0,
        "b": 1.0,
    }
    resp = client.post("/api/solve/root", json=payload)
    assert resp.status_code in (422, 400)


def test_root_finding_parser_security_error():
    # Injection attempt
    payload = {
        "method": "bisection",
        "expression": "__import__('os').system('dir')",
        "a": 1.0,
        "b": 2.0,
    }
    resp = client.post("/api/solve/root", json=payload)
    assert resp.status_code in (400, 422, 500)


# ── Linear Systems Tests ──────────────────────────────────────────────────────

def test_solve_gauss_elimination_endpoint():
    payload = {
        "method": "gauss_elimination",
        "A": [[2.0, 1.0, 1.0], [1.0, 3.0, 1.0], [1.0, 1.0, 4.0]],
        "b": [8.0, 10.0, 15.0],
    }
    resp = client.post("/api/solve/linear", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["solution_vector"] is not None
    assert abs(data["solution_vector"][0] - 1.6470588) < 1e-4
    assert abs(data["solution_vector"][1] - 1.8235294) < 1e-4
    assert abs(data["solution_vector"][2] - 2.8823529) < 1e-4


def test_solve_gauss_jordan_endpoint():
    payload = {
        "method": "gauss_jordan",
        "A": [[2.0, 1.0, 1.0], [1.0, 3.0, 1.0], [1.0, 1.0, 4.0]],
        "b": [8.0, 10.0, 15.0],
    }
    resp = client.post("/api/solve/linear", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert abs(data["solution_vector"][0] - 1.6470588) < 1e-4


def test_linear_system_dimension_mismatch():
    payload = {
        "method": "gauss_elimination",
        "A": [[1.0, 2.0], [3.0, 4.0]],
        "b": [1.0, 2.0, 3.0],  # 3 items for 2x2
    }
    resp = client.post("/api/solve/linear", json=payload)
    assert resp.status_code == 422


# ── Differential Equations Tests ──────────────────────────────────────────────

def test_solve_euler_endpoint():
    payload = {
        "method": "euler",
        "expression": "x + y",
        "x0": 0.0,
        "y0": 1.0,
        "h": 0.1,
        "x_end": 0.5,
    }
    resp = client.post("/api/solve/ode", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert len(data["ode_table"]) == 6


def test_solve_modified_euler_endpoint():
    payload = {
        "method": "modified_euler",
        "expression": "x + y",
        "x0": 0.0,
        "y0": 1.0,
        "h": 0.1,
        "x_end": 0.5,
    }
    resp = client.post("/api/solve/ode", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


def test_solve_rk4_endpoint_with_exact_solution():
    payload = {
        "method": "rk4",
        "expression": "x + y",
        "x0": 0.0,
        "y0": 1.0,
        "h": 0.1,
        "x_end": 0.5,
        "exact_expression": "2*exp(x) - x - 1",
    }
    resp = client.post("/api/solve/ode", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["metrics"]["final_exact_error"] is not None
    assert data["metrics"]["final_exact_error"] < 1e-4
    # Check that both numerical and exact curves are returned
    curve_labels = [c["label"] for c in data["curves"]]
    assert any("Numerical" in l for l in curve_labels)
    assert any("Exact" in l for l in curve_labels)


# ── Comparison Endpoint Tests ─────────────────────────────────────────────────

def test_compare_root_methods():
    payload = {
        "category": "root_finding",
        "methods": ["bisection", "false_position", "newton_raphson"],
        "root_input": {
            "method": "bisection",
            "expression": "x**3 - x - 2",
            "a": 1.0,
            "b": 2.0,
            "x0": 1.5,
            "tol": 1e-6,
            "max_iter": 50,
        },
    }
    resp = client.post("/api/compare", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 3
    method_names = [item["method"] for item in data["items"]]
    assert "Bisection" in method_names


def test_compare_ode_methods():
    payload = {
        "category": "ode",
        "methods": ["euler", "modified_euler", "rk4"],
        "ode_input": {
            "method": "euler",
            "expression": "x + y",
            "x0": 0.0,
            "y0": 1.0,
            "h": 0.1,
            "x_end": 0.5,
        },
    }
    resp = client.post("/api/compare", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 3
    assert len(data["curves"]) == 3
