"""
Gaussian Elimination with partial pivoting — linear systems.

Reduces [A | b] to row-echelon form with column-maximum pivot selection,
then back-substitutes to find x such that Ax = b.

Records every row-operation for the UI's step-by-step display.
"""
from __future__ import annotations

import time
from copy import deepcopy
from typing import Any

import numpy as np

from numerix.core.result_models import (
    IterationRecord,
    SolverMetrics,
    SolverResult,
    SolverStatus,
)
from numerix.core.validators import validate_matrix

_PIVOT_EPS = 1e-14  # treat pivots smaller than this as zero


def gauss_elimination(
    A: list[list[float]],
    b: list[float],
) -> SolverResult:
    """
    Gaussian Elimination with partial pivoting.

    Parameters
    ----------
    A : n×n coefficient matrix (list of lists)
    b : right-hand-side vector (length n)

    Returns
    -------
    SolverResult with solution_vector, full row-operation history, and residual.
    """
    validate_matrix(A, b)
    n = len(b)

    # work on float numpy arrays; keep the original for residual check
    A_orig = np.array(A, dtype=float)
    b_orig = np.array(b, dtype=float)
    aug = np.hstack([A_orig.copy(), b_orig.reshape(-1, 1)])  # augmented [A|b]

    history: list[IterationRecord] = []
    op_n = 0
    t0 = time.perf_counter()

    # ---- Forward elimination with partial pivoting ----
    for col in range(n):
        # find row with max absolute value in this column (from col downward)
        pivot_row = int(np.argmax(np.abs(aug[col:, col]))) + col

        if abs(aug[pivot_row, col]) < _PIVOT_EPS:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Gauss Elimination",
                problem_type="linear_system",
                status=SolverStatus.SINGULAR_MATRIX,
                termination_reason="singular_or_near_singular_matrix",
                iterations=history,
                metrics=SolverMetrics(
                    iterations=op_n,
                    execution_time_seconds=elapsed,
                ),
                warnings=[f"Zero pivot encountered at column {col}; matrix may be singular."],
            )

        # swap rows
        if pivot_row != col:
            aug[[col, pivot_row]] = aug[[pivot_row, col]]
            op_n += 1
            history.append(
                IterationRecord(
                    n=op_n,
                    values={"type": "swap", "row1": col, "row2": pivot_row},  # type: ignore[dict-item]
                    extra={
                        "description": f"R{col+1} ↔ R{pivot_row+1}  (partial pivot)",
                        "matrix_snapshot": aug.tolist(),
                    },
                )
            )

        pivot_val = aug[col, col]
        for row in range(col + 1, n):
            factor = aug[row, col] / pivot_val
            if factor == 0.0:
                continue
            aug[row] -= factor * aug[col]
            op_n += 1
            history.append(
                IterationRecord(
                    n=op_n,
                    values={"type": "eliminate", "target_row": row, "pivot_row": col, "factor": factor},  # type: ignore[dict-item]
                    extra={
                        "description": f"R{row+1} ← R{row+1} − ({factor:.6g})·R{col+1}",
                        "matrix_snapshot": aug.tolist(),
                    },
                )
            )

    # ---- Back substitution ----
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = aug[i, n]
        for j in range(i + 1, n):
            x[i] -= aug[i, j] * x[j]
        x[i] /= aug[i, i]

    residual_vec = A_orig @ x - b_orig
    residual_norm = float(np.linalg.norm(residual_vec))
    elapsed = time.perf_counter() - t0

    return SolverResult(
        method="Gauss Elimination",
        problem_type="linear_system",
        status=SolverStatus.SUCCESS,
        termination_reason="solution_found",
        solution_vector=x.tolist(),
        iterations=history,
        metrics=SolverMetrics(
            iterations=op_n,
            execution_time_seconds=elapsed,
            final_residual=residual_norm,
        ),
        extra={
            "residual_vector": residual_vec.tolist(),
            "row_echelon_matrix": aug.tolist(),
        },
    )
