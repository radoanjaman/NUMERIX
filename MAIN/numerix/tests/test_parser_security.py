"""
Adversarial / security tests for the safe expression parser.
"""
import math
import pytest

from numerix.core.expression_parser import (
    parse_function_x,
    ParseError,
)


class TestParserSecurity:
    """Tests that dangerous expressions are rejected."""

    def test_dunder_import_raises(self):
        """__import__('os') must be blocked (contains __)."""
        with pytest.raises(ParseError):
            parse_function_x("__import__('os')")

    def test_dot_access_raises(self):
        """Attribute access via dot must be rejected."""
        with pytest.raises(ParseError):
            parse_function_x("x.__class__")

    def test_subscript_raises(self):
        """Subscript notation must be rejected."""
        with pytest.raises(ParseError):
            parse_function_x("x[0]")

    def test_semicolon_raises(self):
        """Semicolon (statement separator) must be rejected."""
        with pytest.raises(ParseError):
            parse_function_x("x; import os")

    def test_newline_raises(self):
        """Newline in expression must be rejected."""
        with pytest.raises(ParseError):
            parse_function_x("x\nimport os")

    def test_too_long_raises(self):
        """Expressions longer than 500 chars must be rejected."""
        with pytest.raises(ParseError):
            parse_function_x("a" * 501)

    def test_lambda_raises(self):
        """Lambda keyword must be blocked."""
        with pytest.raises(ParseError):
            parse_function_x("lambda x: x")

    def test_globals_raises(self):
        """globals() must be blocked."""
        with pytest.raises(ParseError):
            parse_function_x("globals()")

    def test_open_raises(self):
        """open() must be blocked."""
        with pytest.raises(ParseError):
            parse_function_x("open('/etc/passwd')")

    def test_unsupported_symbols_raises(self):
        """Symbols not in the allowlist (z, w) must be rejected."""
        with pytest.raises(ParseError, match="Unsupported symbol"):
            parse_function_x("x + z + w")


class TestParserValid:
    """Tests that safe, well-formed expressions are accepted."""

    def test_polynomial_evaluates(self):
        """x**3 - x - 2 evaluates correctly."""
        _, f = parse_function_x("x**3 - x - 2")
        assert abs(f(2.0) - 4.0) < 1e-10
        assert abs(f(1.0) - (-2.0)) < 1e-10

    def test_sin_cos(self):
        """sin(x) + cos(x) parses and evaluates."""
        _, f = parse_function_x("sin(x) + cos(x)")
        expected = math.sin(0.5) + math.cos(0.5)
        assert abs(f(0.5) - expected) < 1e-10

    def test_exp_sqrt(self):
        """exp(x) * sqrt(x) for x > 0."""
        _, f = parse_function_x("exp(x) * sqrt(x)")
        x_val = 1.0
        expected = math.exp(x_val) * math.sqrt(x_val)
        assert abs(f(x_val) - expected) < 1e-10

    def test_log(self):
        """log(x) for x > 0."""
        _, f = parse_function_x("log(x)")
        assert abs(f(math.e) - 1.0) < 1e-8

    def test_pi_constant(self):
        """pi * x evaluates using SymPy pi."""
        _, f = parse_function_x("pi * x")
        assert abs(f(1.0) - math.pi) < 1e-10
