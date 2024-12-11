import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *
from interpreter_errors import InterpreterError

def test_sanity():
    """."""
    assert 1 == True


def test_empty_if():
    """if 1 begin end"""
    ast = Program([IfStatement(IntLiteral(1), Program([]))])
    i = Interpreter()
    ast.accept(i)


def test_variable_before_if_is_visable_from_inside():
    """a: mut int = 1; if 1 begin a = 2; end"""
    ast = Program(
        [
            VariableDeclaration("a", "int", True, IntLiteral(1)),
            IfStatement(
                IntLiteral(1),
                Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(2))]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 2


def test_can_create_same_name_variable_in_different_scopes():
    """a: mut int = 1; if 1 begin a: mut int = 1; end"""
    ast = Program(
        [
            VariableDeclaration("a", "int", True, IntLiteral(1)),
            IfStatement(
                IntLiteral(1),
                Program([VariableDeclaration("a", "int", True, IntLiteral(2))]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value == 1


def test_same_name_variable_in_else_as_in_main():
    """if 1 begin a: mut int = 1; end else begin a: mut int = 1; end"""
    ast = Program(
        [
            IfStatement(
                IntLiteral(1),
                Program([VariableDeclaration("a", "int", True, IntLiteral(1))]),
                Program([VariableDeclaration("a", "int", True, IntLiteral(1))]),
            )
        ]
    )
    i = Interpreter()
    ast.accept(i)


def test_same_name_variable_in_else():
    """if 0 begin end else begin a: mut int = 1; a: mut int = 1;  end"""
    ast = Program(
        [
            IfStatement(
                IntLiteral(0),
                Program([]),
                Program(
                    [
                        VariableDeclaration("a", "int", True, IntLiteral(1)),
                        VariableDeclaration("a", "int", True, IntLiteral(1), pos=(5,1)),
                    ]
                ),
            )
        ]
    )
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 5, column: 1, Variable 'a' already declared in the current scope"
