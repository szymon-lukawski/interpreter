import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *


def test_sanity():
    """."""
    assert 1 == True


def test_getting_value_of_not_initialised_variable():
    """a : int;"""
    ast = Program([VariableDeclaration('a', 'int', False)])
    i = Interpreter()
    ast.accept(i)
    with pytest.raises(RuntimeError) as e:
        i.scopes.get_variable_value('a')

    assert str(e.value) == "Variable 'a' has no value"

def test_getting_value_of_initialised_variable_int():
    """a : int = 1;"""
    ast = Program([VariableDeclaration('a', 'int', False, IntLiteral(1))])
    i = Interpreter()
    ast.accept(i)
    assert 1 == i.scopes.get_variable_value('a')

def test_getting_value_of_initialised_variable_float():
    """a : int = 1.2;"""
    ast = Program([VariableDeclaration('a', 'int', False, FloatLiteral(1.2))])
    i = Interpreter()
    ast.accept(i)
    assert 1.2 == i.scopes.get_variable_value('a')

def test_getting_value_of_initialised_variable_str():
    """a : int = 'Ala';"""
    ast = Program([VariableDeclaration('a', 'int', False, StrLiteral('Ala'))])
    i = Interpreter()
    ast.accept(i)
    assert 'Ala' == i.scopes.get_variable_value('a')

def test_setting_value_of_non_mutable_variable_int():
    """a : int; a = 1;"""
    ast = Program([VariableDeclaration('a', 'int', False), AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))])
    i = Interpreter()
    ast.accept(i)
    assert 1 == i.scopes.get_variable_value('a')

def test_setting_value_of_non_mutable_but_initialised_variable_int():
    """a : int = 2; a = 1;"""
    ast = Program([VariableDeclaration('a', 'int', False, IntLiteral(2)), AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))])
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Trying to reassign value to non mutable variable 'a'"
