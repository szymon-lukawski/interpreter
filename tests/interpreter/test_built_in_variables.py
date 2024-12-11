import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *
from interpreter_errors import InterpreterError

def test_sanity():
    """."""
    assert 1 == True


def test_getting_value_of_not_initialised_variable():
    """a : int;"""
    ast = Program([VariableDeclaration("a", "int", False, pos=(1,1))])
    i = Interpreter()
    ast.accept(i)
    with pytest.raises(InterpreterError) as e:
        i.visit_obj_access(ObjectAccess(["a"], pos=(2,1)))

    assert str(e.value) == "InterpreterError: row: 2, column: 1, Variable 'a' has no value"


def test_getting_value_of_initialised_variable_int():
    """a : int = 1;"""
    ast = Program([VariableDeclaration("a", "int", False, IntLiteral(1))])
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 1


def test_getting_value_of_initialised_variable_float():
    """a : int = 1.2;"""
    ast = Program([VariableDeclaration("a", "int", False, FloatLiteral(1.2))])
    i = Interpreter()
    ast.accept(i)
    assert 1 == i.visit_obj_access(ObjectAccess(["a"])).value


def test_getting_value_of_initialised_variable_str():
    """a : int = 'Ala';"""
    ast = Program([VariableDeclaration("a", "int", False, StrLiteral("Ala"), pos=(2,1))])
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 2, column: 1, Can not convert 'Ala' str into int"

def test_setting_value_of_non_mutable_variable_int():
    """a : int; a = 1;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert 1 == i.visit_obj_access(ObjectAccess(["a"])).value


def test_setting_value_of_non_mutable_but_initialised_variable_int():
    """a : int = 2; a = 1;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(2), pos=(1,1)),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1),pos=(1,17)),
        ]
    )
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 1, column: 17, Trying to reassign value to non mutable variable"
