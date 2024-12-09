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


def test_getting_value_of_uninitialised_attr():
    """A : struct begin x : int; end a : A;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False)]),
            VariableDeclaration("a", "A", False),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    with pytest.raises(RuntimeError) as e:
        i.visit_obj_access(ObjectAccess(["a", "x"]))
    assert str(e.value) == "Variable 'a' has no value"


def test_getting_value_of_initialised_attr():
    """A : struct begin x : int; end a : mut A; a.x = 12;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False)]),
            VariableDeclaration("a", "A", True),
            AssignmentStatement(ObjectAccess(["a", "x"]), IntLiteral(12)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a", "x"])).value == 12


def test_struct_with_default_value():
    """A : struct begin x: mut int = 1; end a : A;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True, IntLiteral(1))]),
            VariableDeclaration("a", "A", True),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a", "x"])).value == 1


def test_reasigning_non_mutable_attr():
    """A : struct begin x: int = 1; end a : A; a.x = 2;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False, IntLiteral(1))]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a", "x"]), IntLiteral(2)),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Trying to reassign value to a non-mutable attribute."


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
    assert i.visit_obj_access(ObjectAccess(["a", "x"])).value == 10


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
    assert i.visit_obj_access(ObjectAccess(["b", "a", "x"])).value == 10


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
    # TODO assert i.visit_obj_access(ObjectAccess(["b", "a"])) ==


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
    assert i.visit_obj_access(ObjectAccess(["b", "x"])).value == 10


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
    assert result.type == "A"
    assert result.value["x"].value.value == 12


def test_assignment_of_complex_types_is_by_value():
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
    result = i.visit_obj_access(ObjectAccess(["b", "a"]))
    assert result.type == "A"
    assert result.value["x"].value.value == 12


def test_struct_type_factory_function():
    """A : struct begin x: mut int; end A(x : int): A begin a : mut A; a.x = x; return a; end a :mut A=A(5);"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            FuncDef(
                "A",
                [Param("x", "int", False)],
                "A",
                Program(
                    [
                        VariableDeclaration("a", "A", True),
                        AssignmentStatement(
                            ObjectAccess(["a", "x"]), ObjectAccess(["x"])
                        ),
                        ReturnStatement(ObjectAccess(["a"])),
                    ]
                ),
            ),
            VariableDeclaration(
                "a", "A", True, ObjectAccess([FunctionCall("A", [IntLiteral(5)])])
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    result = i.visit_obj_access(ObjectAccess(["a"]))
    assert result.type == "A"
    assert result.value["x"].value.value == 5


def test_struct_with_one_default_value():
    """A : struct begin x: mut int; y: mut str = 'BOOM'; end a : A;"""
    ast = Program(
        [
            StructDef(
                "A",
                [
                    VariableDeclaration("x", "int", True),
                    VariableDeclaration("y", "str", True, StrLiteral("BOOM")),
                ],
            ),
            VariableDeclaration("a", "A", False),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    result = i.visit_obj_access(ObjectAccess(["a"]))
    result.value["y"].value.value = "BOOM"


def test_asigning_int_to_struct_type():
    """A : struct begin end a : A = 1;"""
    ast = Program(
        [
            StructDef(
                "A",
                [
                    VariableDeclaration("x", "int", True),
                    VariableDeclaration("y", "str", True, StrLiteral("BOOM")),
                ],
            ),
            VariableDeclaration("a", "A", False),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)  # Type error
    assert "Type" in str(e.value)


def test_asigning_A_to_B():
    """A : struct begin x : int = 1; end B : struct begin x : int = 1; end a : mut A; b : B; a = b;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False, IntLiteral(1))]),
            StructDef("B", [VariableDeclaration("x", "int", False, IntLiteral(1))]),
            VariableDeclaration("a", "A", True),
            VariableDeclaration("b", "B", False),
            AssignmentStatement(ObjectAccess(["a"]), ObjectAccess(["b"])),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)  # Type error
    assert "Type" in str(e.value)


def test_assignment_of_nested_types_using_one_statement():
    """A : struct begin x: int; end B : struct begin a: A; end C : struct begin b: B; end c : C; c.b.a.x = 123;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False)]),
            StructDef("B", [VariableDeclaration("a", "A", False)]),
            StructDef("C", [VariableDeclaration("b", "B", False)]),
            VariableDeclaration("c", "C", False),
            AssignmentStatement(ObjectAccess(["c", "b", "a", "x"]), IntLiteral(123)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["c", "b", "a", "x"])).value == 123


def test_struct_value_has_value_when_any_attribute_has_value():
    """A : struct begin x: int; end B : struct begin a: A; end C : struct begin b: B; end c : C; c.b.a.x = 123;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False, IntLiteral(1234))]),
            StructDef("B", [VariableDeclaration("a", "A", False)]),
            StructDef("C", [VariableDeclaration("b", "B", False)]),
            VariableDeclaration("c", "C", False),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["c", "b", "a", "x"])).value == 1234
    