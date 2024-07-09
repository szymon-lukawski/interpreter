"""test interpretation of expression part of language"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck

import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *




def test_sanity():
    """."""
    assert 1 == True

def test_int_literal():
    """2"""
    ast = IntLiteral(2)
    i = Interpreter()
    assert 2 == ast.accept(i)


def test_float_literal():
    """2.1"""
    ast = FloatLiteral(2.1)
    i = Interpreter()
    assert abs(2.1 - ast.accept(i)) == 0


def test_str_literal():
    """'Ala ma kota.'"""
    ast = StrLiteral("Ala ma kota.")
    i = Interpreter()
    assert ast.accept(i) == "Ala ma kota."

def test_null():
    """null"""
    ast = NullLiteral()
    i = Interpreter()
    assert ast.accept(i)is None

def test_unary_integer():
    """-2"""
    ast = UnaryExpr(IntLiteral(2))
    i = Interpreter()
    assert ast.accept(i) == -2


def test_unary_float():
    """-2.1"""
    ast = UnaryExpr(FloatLiteral(2.1))
    i = Interpreter()
    assert ast.accept(i) == -2.1

def test_add_two_integers():
    """1+2"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2)],['+'])
    i = Interpreter()
    assert ast.accept(i) == 3

def test_subtract_two_integers():
    """1-2"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2)],['-'])
    i = Interpreter()
    assert ast.accept(i) == -1


def test_add_three_integers():
    """1+2+3"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)],['+', '+'])
    i = Interpreter()
    assert ast.accept(i) == 6

def test_1_plus_2_minus_3():
    """1+2-3"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)],['+', '-'])
    i = Interpreter()
    assert ast.accept(i) == 0

def test_1_minus_2_plus_3():
    """1-2+3"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)],['-', '+'])
    i = Interpreter()
    assert ast.accept(i) == 2

def test_1_minus_unary_minus_3():
    """1--3"""
    ast = AddExpr([IntLiteral(1), UnaryExpr(IntLiteral(3))],['-'])
    i = Interpreter()
    assert ast.accept(i) == 4

def test_unary_minus_3_minus_1():
    """-3-1"""
    ast = AddExpr([UnaryExpr(IntLiteral(3)), IntLiteral(1)],['-'])
    i = Interpreter()
    assert ast.accept(i) == -4

