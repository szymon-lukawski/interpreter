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
    assert i.visit_obj_access(ObjectAccess(["a"])).value == "1.2"


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
