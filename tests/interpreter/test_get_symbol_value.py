import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *
from scopes import Scopes
from interpreter_types import StructValue
from interpreter_errors import InterpreterError


def test_getting_value_of_uninitialised_int():
    """a : int;"""
    ast = Program([VariableDeclaration("a", "int", False, pos = (1,1))])
    i = Interpreter()
    ast.accept(i)
    with pytest.raises(InterpreterError) as e:
        i.visit_obj_access(ObjectAccess(["a"], pos=(2,1))).value
    assert str(e.value) == "InterpreterError: row: 2, column: 1, Variable 'a' has no value"


def test_getting_value_of_initialised_int():
    """a : int = 123;"""
    ast = Program([VariableDeclaration("a", "int", False, IntLiteral(123))])
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 123


def test_getting_value_of_initialised_float():
    """a : float = 123.4;"""
    ast = Program([VariableDeclaration("a", "float", False, FloatLiteral(123.4))])
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 123.4


def test_getting_value_of_initialised_str():
    """a : str = 'BOOM';"""
    ast = Program([VariableDeclaration("a", "str", False, StrLiteral("BOOM"))])
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == "BOOM"


def test_empty_struct():
    """A : struct begin end a : A;"""
    ast = Program([StructDef("A", []), VariableDeclaration("a", "A", False)])
    i = Interpreter()
    ast.accept(i)
    with pytest.raises(InterpreterError) as e:
        i.visit_obj_access(ObjectAccess(["a"], pos=(3,1)))
    assert str(e.value) == "InterpreterError: row: 3, column: 1, Variable 'a' has no value"
