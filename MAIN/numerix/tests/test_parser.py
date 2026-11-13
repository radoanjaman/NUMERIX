"""
Tests for the safe expression parser.
"""
import math
import pytest

from numerix.core.expression_parser import (
    parse_function_x,
    parse_function_xy,
    differentiate_x,
    ParseError,
)


class TestParseFunctionX:
    def test_polynomial(self):
        _, f = parse_function_x("x**3 - x - 2")
        assert abs(f(2.0) - 4.0) < 1e-10

    def test_trig(self):
        _, f = parse_function_x("sin(x)")
        assert abs(f(0.0)) < 1e-10
        assert abs(f(math.pi / 2) - 1.0) < 1e-10

    def test_exp(self):
        _, f = parse_function_x("exp(x)")
        assert abs(f(0.0) - 1.0) < 1e-10
        assert abs(f(1.0) - math.e) < 1e-8

    def test_sqrt(self):
        _, f = parse_function_x("sqrt(x)")
        assert abs(f(4.0) - 2.0) < 1e-10

    def test_pi_constant(self):
        _, f = parse_function_x("sin(pi)")
        assert abs(f(0.0)) < 1e-10  # sin(pi) ≈ 0

    def test_log(self):
        _, f = parse_function_x("log(x)")
        assert abs(f(math.e) - 1.0) < 1e-8

    def test_illegal_symbol_raises(self):
        with pytest.raises(ParseError, match="Unsupported symbol"):
            parse_function_x("x + z")

    def test_empty_expression_raises(self):
        with pytest.raises(ParseError):
            parse_function_x("")

    def test_invalid_syntax_raises(self):
        with pytest.raises(ParseError):
            parse_function_x("x + + +")

    def test_no_import_injection(self):
        with pytest.raises(ParseError):
            parse_function_x("__import__('os').system('dir')")


class TestParseFunctionXY:
    def test_simple(self):
        _, f = parse_function_xy("x + y")
        assert abs(f(1.0, 2.0) - 3.0) < 1e-10

    def test_mixed(self):
        _, f = parse_function_xy("x * y + sin(x)")
        assert abs(f(0.0, 5.0) - 0.0) < 1e-10

    def test_illegal_z_raises(self):
        with pytest.raises(ParseError, match="Unsupported symbol"):
            parse_function_xy("x + y + z")


class TestDifferentiate:
    def test_polynomial_derivative(self):
        expr, _ = parse_function_x("x**3 - x - 2")
        _, df = differentiate_x(expr)
        # d/dx (x^3 - x - 2) = 3x^2 - 1
        assert abs(df(2.0) - 11.0) < 1e-8
        assert abs(df(0.0) - (-1.0)) < 1e-8

    def test_sin_derivative(self):
        expr, _ = parse_function_x("sin(x)")
        _, df = differentiate_x(expr)
        assert abs(df(0.0) - 1.0) < 1e-8   # cos(0) = 1

    def test_exp_derivative(self):
        expr, _ = parse_function_x("exp(x)")
        _, df = differentiate_x(expr)
        assert abs(df(1.0) - math.e) < 1e-7
