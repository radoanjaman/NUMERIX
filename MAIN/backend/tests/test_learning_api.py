"""
Tests for Learning API routes.
"""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_learning_topics_endpoint():
    res = client.get("/api/learning/topics")
    assert res.status_code == 200
    data = res.json()
    assert "topics" in data
    assert "bisection" in data["topics"]
    assert "rk4" in data["topics"]
    assert len(data["topics"]["bisection"]["formulas"]) >= 2


def test_learning_generate_endpoint_bisection():
    payload = {
        "method": "bisection",
        "expression": "x**3 - x - 2",
        "a": 1.0,
        "b": 2.0,
        "tol": 1e-5,
    }
    res = client.post("/api/learning/generate", json=payload)
    assert res.status_code == 200
    doc = res.json()
    assert doc["method"] == "Bisection Method"
    assert len(doc["steps"]) > 5
    assert len(doc["practice_questions"]) >= 2


def test_solve_root_includes_solution_document():
    payload = {
        "method": "bisection",
        "expression": "x**3 - x - 2",
        "a": 1.0,
        "b": 2.0,
        "tol": 1e-5,
        "max_iter": 50,
    }
    res = client.post("/api/solve/root", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "solution_document" in data
    assert data["solution_document"] is not None
    assert data["solution_document"]["method"] == "Bisection Method"
    assert len(data["solution_document"]["steps"]) > 0


def test_solve_linear_includes_solution_document():
    payload = {
        "method": "gauss_elimination",
        "A": [[2.0, 1.0], [1.0, -1.0]],
        "b": [3.0, 0.0],
    }
    res = client.post("/api/solve/linear", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["solution_document"] is not None
    assert data["solution_document"]["method"] == "Gauss Elimination"


def test_solve_ode_includes_solution_document():
    payload = {
        "method": "rk4",
        "expression": "x + y",
        "x0": 0.0,
        "y0": 1.0,
        "h": 0.1,
        "x_end": 0.3,
    }
    res = client.post("/api/solve/ode", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["solution_document"] is not None
    assert data["solution_document"]["method"] == "RK4"
