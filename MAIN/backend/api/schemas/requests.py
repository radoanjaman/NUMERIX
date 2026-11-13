"""
Pydantic Request Schemas for NUMERIX API.
"""
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, model_validator


class RootFindingRequest(BaseModel):
    method: Literal["bisection", "false_position", "newton_raphson"]
    expression: str = Field(..., min_length=1, max_length=500, description="f(x) mathematical string")
    a: float | None = Field(default=None, description="Lower bound for bracketing methods")
    b: float | None = Field(default=None, description="Upper bound for bracketing methods")
    x0: float | None = Field(default=None, description="Initial guess for Newton-Raphson")
    tol: float = Field(default=1e-6, gt=0, le=1.0, description="Convergence tolerance")
    max_iter: int = Field(default=100, ge=1, le=1000, description="Maximum iterations")

    @model_validator(mode="after")
    def validate_method_params(self) -> "RootFindingRequest":
        if self.method in ("bisection", "false_position"):
            if self.a is None or self.b is None:
                raise ValueError(f"Parameters 'a' and 'b' are required for {self.method}.")
            if self.a >= self.b:
                raise ValueError(f"Invalid bracket: 'a' must be less than 'b' (got a={self.a}, b={self.b}).")
        elif self.method == "newton_raphson":
            if self.x0 is None and self.a is None:
                raise ValueError("Parameter 'x0' (initial guess) is required for newton_raphson.")
        return self


class LinearSystemRequest(BaseModel):
    method: Literal["gauss_elimination", "gauss_jordan"]
    A: list[list[float]] = Field(..., description="Coefficient matrix A of dimension N x N")
    b: list[float] = Field(..., description="Right-hand side vector b of dimension N")

    @model_validator(mode="after")
    def validate_dimensions(self) -> "LinearSystemRequest":
        n = len(self.b)
        if n < 1 or n > 10:
            raise ValueError(f"Matrix dimension N must be between 1 and 10 (got N={n}).")
        if len(self.A) != n:
            raise ValueError(f"Matrix A has {len(self.A)} rows, but vector b has {n} elements.")
        for i, row in enumerate(self.A):
            if len(row) != n:
                raise ValueError(f"Row {i} has {len(row)} elements; expected square matrix of size {n} x {n}.")
        return self


class ODERequest(BaseModel):
    method: Literal["euler", "modified_euler", "rk4"]
    expression: str = Field(..., min_length=1, max_length=500, description="dy/dx = f(x, y) expression")
    x0: float = Field(default=0.0, description="Initial x value")
    y0: float = Field(default=1.0, description="Initial y(x0) value")
    h: float = Field(default=0.1, description="Step size h")
    x_end: float = Field(default=1.0, description="End x value")
    exact_expression: str | None = Field(default=None, max_length=500, description="Optional exact y(x) analytical function")

    @model_validator(mode="after")
    def validate_ode_steps(self) -> "ODERequest":
        if self.h == 0:
            raise ValueError("Step size h cannot be zero.")
        if (self.x_end - self.x0) * self.h <= 0:
            raise ValueError(f"Step size h={self.h} sign is inconsistent with interval [{self.x0}, {self.x_end}].")
        steps = abs((self.x_end - self.x0) / self.h)
        if steps > 10000:
            raise ValueError(f"Too many integration steps ({steps:.0f} > 10,000). Use a larger step size h.")
        return self


class ComparisonRequest(BaseModel):
    category: Literal["root_finding", "linear_systems", "ode"]
    methods: list[str] = Field(..., min_length=1, description="List of method identifiers")
    root_input: RootFindingRequest | None = None
    linear_input: LinearSystemRequest | None = None
    ode_input: ODERequest | None = None
