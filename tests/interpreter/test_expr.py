"""test interpretation of expression part of language"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck

import pytest
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


