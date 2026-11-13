"""
Gauss-Jordan Elimination — linear systems.

Extends Gaussian elimination: after forward elimination, also eliminates
entries *above* each pivot to reach reduced row-echelon form.
Each pivot row is normalised to a leading 1 before elimination.

Records every row operation for the UI's step-by-step display.
"""
from __future__ import annotations

import time

import numpy as np

from numerix.core.result_models import (
    IterationRecord,
    SolverMetrics,
    SolverResult,
    SolverStatus,
)
from numerix.core.validators import validate_matrix

_PIVOT_EPS = 1e-14


def gauss_jordan(
    A: list[list[float]],
    b: list[float],
) -> SolverResult:
    """
    Gauss-Jordan Elimination with partial pivoting.

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

    A_orig = np.array(A, dtype=float)
    b_orig = np.array(b, dtype=float)
    aug = np.hstack([A_orig.copy(), b_orig.reshape(-1, 1)])

    history: list[IterationRecord] = []
    op_n = 0
    t0 = time.perf_counter()

    for col in range(n):
        # partial pivot: find row with largest absolute value in this column
        pivot_row = int(np.argmax(np.abs(aug[col:, col]))) + col

        if abs(aug[pivot_row, col]) < _PIVOT_EPS:
            elapsed = time.perf_counter() - t0
            return SolverResult(
                method="Gauss-Jordan",
                problem_type="linear_system",
                status=SolverStatus.SINGULAR_MATRIX,
                termination_reason="singular_or_near_singular_matrix",
                iterations=history,
                metrics=SolverMetrics(
                    iterations=op_n,
                    execution_time_seconds=elapsed,
                ),
                warnings=[f"Zero pivot at column {col}; matrix may be singular."],
            )

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

        # normalise pivot row
        pivot_val = aug[col, col]
        aug[col] /= pivot_val
        op_n += 1
        history.append(
            IterationRecord(
                n=op_n,
                values={"type": "scale", "row": col, "scale": pivot_val},  # type: ignore[dict-item]
                extra={
                    "description": f"R{col+1} ← R{col+1} / {pivot_val:.6g}",
                    "matrix_snapshot": aug.tolist(),
                },
            )
        )

        # eliminate all other rows (above AND below)
        for row in range(n):
            if row == col:
                continue
            factor = aug[row, col]
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

    x = aug[:, n]
    residual_vec = A_orig @ x - b_orig
    residual_norm = float(np.linalg.norm(residual_vec))
    elapsed = time.perf_counter() - t0

    return SolverResult(
        method="Gauss-Jordan",
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
            "reduced_row_echelon_matrix": aug.tolist(),
        },
    )
