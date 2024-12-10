import pytest
from interpreter import Interpreter
from AST import *


def test_assignment_defore_definition():
    """a = 1;"""
    ast = Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1))])
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Variable 'a' not found in any scope"



def test_assigment_converts_int_to_int():
    """a : int; a = 7;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(7)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 7

def test_assigment_converts_float_to_float():
    """a : float; a = 3.14;"""
    ast = Program(
        [
            VariableDeclaration("a", "float", False),
            AssignmentStatement(ObjectAccess(["a"]), FloatLiteral(3.14)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 3.14

def test_assigment_converts_str_to_str():
    """a : str; a = 'BOOM';"""
    ast = Program(
        [
            VariableDeclaration("a", "str", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral("BOOM")),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == "BOOM"



def test_assigment_converts_float_to_str():
    """a : str; a = 1.2;"""
    ast = Program(
        [
            VariableDeclaration("a", "str", False),
            AssignmentStatement(ObjectAccess(["a"]), FloatLiteral(1.2)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == "1.2000"


def test_assigment_converts_int_to_str():
    """a : str; a = 123;"""
    ast = Program(
        [
            VariableDeclaration("a", "str", False),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(123)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == "123"


def test_assigment_converts_float_to_int():
    """a : int; a = 1.2;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False),
            AssignmentStatement(ObjectAccess(["a"]), FloatLiteral(1.2)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 1


def test_assigment_converts_int_to_float():
    """a : float; a = 67;"""
    ast = Program(
        [
            VariableDeclaration("a", "float", False),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(67)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    rv = i.visit_obj_access(ObjectAccess(["a"]))
    assert rv.value == 67.0
    assert rv.type == 'float'


def test_assigment_converts_str_to_float():
    """a : float; a = '67';"""
    ast = Program(
        [
            VariableDeclaration("a", "float", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral('67')),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    rv = i.visit_obj_access(ObjectAccess(["a"]))
    assert rv.value == 67.0
    assert rv.type == 'float'

def test_assigment_converts_str_to_int_float_repr():
    """a : int; a = '67.12123';"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral('67.12123')),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    rv = i.visit_obj_access(ObjectAccess(["a"]))
    assert rv.value == 67
    assert rv.type == "int"


def test_assigment_converts_str_to_int():
    """a : int; a = '67';"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral('67')),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    rv = i.visit_obj_access(ObjectAccess(["a"]))
    assert rv.value == 67
    assert rv.type == "int"