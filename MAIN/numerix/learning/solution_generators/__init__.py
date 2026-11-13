"""Method-specific solution generators."""
from numerix.learning.solution_generators.root_finding import (
    generate_bisection_lesson,
    generate_false_position_lesson,
    generate_newton_raphson_lesson,
)
from numerix.learning.solution_generators.linear_systems import (
    generate_gauss_elimination_lesson,
    generate_gauss_jordan_lesson,
)
from numerix.learning.solution_generators.ode import (
    generate_euler_lesson,
    generate_modified_euler_lesson,
    generate_rk4_lesson,
)

__all__ = [
    "generate_bisection_lesson",
    "generate_false_position_lesson",
    "generate_newton_raphson_lesson",
    "generate_gauss_elimination_lesson",
    "generate_gauss_jordan_lesson",
    "generate_euler_lesson",
    "generate_modified_euler_lesson",
    "generate_rk4_lesson",
]
