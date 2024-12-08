import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *
from scopes import Scopes


def test_new_struct_is_visable():
    """A : struct begin end; a : A;"""
    ast = Program([StructDef("A", [])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_var_defs_for_("A") == []


def test_struct_with_one_attribute():
    """A : struct begin x : int; end; a : A;"""
    ast = ast = Program([StructDef("A", [VariableDeclaration("x", "int", False)])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_var_defs_for_("A") == [
        VariableDeclaration("x", "int", False, None)
    ]


def test_struct_with_2_attributes():
    """A : struct begin x : int; y : float; end; a : A;"""
    variables = [
        VariableDeclaration("x", "int", False),
        VariableDeclaration("y", "float", False),
    ]
    ast = Program([StructDef("A", variables)])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_var_defs_for_("A") == variables


def test_can_not_use_struct_type_before_it_was_defined():
    """a : A; A : struct begin x : int; y : float; end"""
    ast = Program(
        [
            VariableDeclaration("a", "A", False),
            StructDef(
                "A",
                [
                    VariableDeclaration("x", "int", False),
                    VariableDeclaration("y", "float", False),
                ],
            ),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Type 'A' not found in any scope"


def test_declarations_in_inner_scope_not_visable_in_outer():
    """a: int = 1; if a begin A : struct begin end end b : A;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(1)),
            IfStatement(
                ObjectAccess(
                    [
                        "a",
                    ]
                ),
                Program([StructDef("A", [])]),
            ),
            VariableDeclaration("b", "A", False),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Type 'A' not found in any scope"


def test_assign_value_to_struct_instance_attr():
    """A : mut struct begin x: mut int; end a : A; a.x = 10;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            VariableDeclaration("a", "A", True),
            AssignmentStatement(ObjectAccess(["a", "x"]), IntLiteral(10)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a", "x"])) == 10


def test_struct_inside_struct():
    """A : struct begin x: mut int; end B : struct begin a : mut A; end b : mut B; b.a.x = 10;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            StructDef("B", [VariableDeclaration("a", "A", True)]),
            VariableDeclaration("b", "B", True),
            AssignmentStatement(ObjectAccess(["b", "a", "x"]), IntLiteral(10)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["b", "a", "x"])) == 10


def test_struct_inside_struct_retriving_value_of_struct():
    """A : struct begin x: mut int; end B : struct begin a : mut A; end b : mut B; b.a.x = 10;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            StructDef("B", [VariableDeclaration("a", "A", True)]),
            VariableDeclaration("b", "B", True),
            AssignmentStatement(ObjectAccess(["b", "a", "x"]), IntLiteral(10)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["b", "a"])) == Scopes.StructSymbol(
        "A", True, {"x": Scopes.BuiltInSymbol("int", True, 10)}
    )


def test_assignment_simple_struct_to_another_variable_of_the_same_type():
    """A : struct begin x: mut int; end a : mut A; a.x = 10; b:mutA; b = a;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            VariableDeclaration("a", "A", True),
            AssignmentStatement(ObjectAccess(["a", "x"]), IntLiteral(10)),
            VariableDeclaration("b", "A", True),
            AssignmentStatement(ObjectAccess(["b"]), ObjectAccess(["a"])),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["b", "x"])) == 10


def test_assignment_of_complex_type():
    """A : struct begin x: mut int; end B : struct begin a : mut A; end c : mut A; c.x = 12; b : mut  B; b.a = c;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            StructDef("B", [VariableDeclaration("a", "A", True)]),
            VariableDeclaration("c", "A", True),
            AssignmentStatement(ObjectAccess(["c", "x"]), IntLiteral(12)),
            VariableDeclaration("b", "B", True),
            AssignmentStatement(ObjectAccess(["b", "a"]), ObjectAccess(["c"])),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    result = i.visit_obj_access(ObjectAccess(["b", "a"]))
    assert result == Scopes.StructSymbol(
        "A", True, {"x": Scopes.BuiltInSymbol("int", True, 12)}
    )


def test_assignment_of_comlex_types_is_by_value():
    """A : struct begin x: mut int; end B : struct begin a : mut A; end c : mut A; c.x = 12; b : mut B; b.a = c; c.x = 10;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            StructDef("B", [VariableDeclaration("a", "A", True)]),
            VariableDeclaration("c", "A", True),
            AssignmentStatement(ObjectAccess(["c", "x"]), IntLiteral(12)),
            VariableDeclaration("b", "B", True),
            AssignmentStatement(ObjectAccess(["b", "a"]), ObjectAccess(["c"])),
            AssignmentStatement(ObjectAccess(["c", "x"]), IntLiteral(10)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["b", "a"])) == Scopes.StructSymbol(
        "A", True, {"x": Scopes.BuiltInSymbol("int", True, 12)}
    )

