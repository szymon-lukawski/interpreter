import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *


def test_new_variant_is_visable():
    """A : variant begin end; a : A;"""
    ast = Program([VariantDef("A", [])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variant_definition("A") == []


def test_variant_with_one_named_type():
    """A : variant begin x : int; end; a : A;"""
    ast = Program([VariantDef("A", [NamedType("x", "int")])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variant_definition("A") == [NamedType("x", "int")]


def test_variant_with_2_named_types():
    """A : variant begin x : int; y : float; end; a : A;"""
    ast = Program([VariantDef("A", [NamedType("x", "int"), NamedType("y", "float")])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variant_definition("A") == [
        NamedType("x", "int"),
        NamedType("y", "float"),
    ]


def test_can_not_use_variant_type_before_it_was_defined():
    """a : A; A : variant begin x : int; y : float; end"""
    ast = Program(
        [
            VariableDeclaration("a", "A", False),
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "float")]),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Type 'A' not found in any scope"


def test_declarations_in_inner_scope_not_visable_in_outer():
    """a: int = 1; if a begin A : variant begin end end b : A;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(1)),
            IfStatement(
                ObjectAccess(
                    [
                        "a",
                    ]
                ),
                Program([VariantDef("A", [])]),
            ),
            VariableDeclaration("b", "A", False),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Type 'A' not found in any scope"
