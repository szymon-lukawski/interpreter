import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *


def test_new_struct_is_visable():
    """A : struct begin end; a : A;"""
    ast = Program([StructDef('A', [])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_type_definition('A') == []


def test_struct_with_one_attribte():
    """A : struct begin x : int; end; a : A;"""
    ast = ast = Program([StructDef('A', [VariableDeclaration('x', 'int', False)])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_type_definition('A') == [VariableDeclaration('x', 'int', False, None)]


