import pytest
from lexer.token_type import TokenType
from interpreter.interpreter import Interpreter
from parser.AST import *
from interpreter.interpreter import InterpreterError


def test_variant_should_have_more_than_zero_options():
    """A : variant begin end; a : A;"""
    ast = Program([VariantDef("A", [], pos=(1, 1))])
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "InterpreterError: row: 1, column: 1, Variant 'A' should have more than 1 variant options"
    )


def test_variant_with_one_named_type():
    """A : variant begin x : int; end; a : A;"""
    ast = Program([VariantDef("A", [NamedType("x", "int")], pos=(0, 1))])
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "InterpreterError: row: 0, column: 1, Variant 'A' should have more than 1 variant options"
    )


def test_variant_with_2_named_types():
    """A : variant begin x : int; y : float; end; a : A;"""
    ast = Program([VariantDef("A", [NamedType("x", "int"), NamedType("y", "float")])])
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_named_types_for_("A", pos=(1,1)) == [
        NamedType("x", "int"),
        NamedType("y", "float"),
    ]


def test_variant_with_variant_option():
    """A : variant begin x : A; y : float; end a : A;"""
    ast = Program([VariantDef("A", [NamedType("x", "A", pos=(2,1)), NamedType("y", "float")],pos=(1,1))])
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 2, column: 1, Variant option 'x' can no be of type variant"


def test_can_not_use_variant_type_before_it_was_defined():
    """a : A; A : variant begin x : int; y : float; end"""
    ast = Program(
        [
            VariableDeclaration("a", "A", False, pos=(1,1)),
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "float")]),
        ]
    )
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 1, column: 1, Type 'A' not found"


def test_declarations_in_inner_scope_not_visable_in_outer():
    """a: int = 1; if a begin A : variant begin x : A; y : float; end end b : A;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(1)),
            IfStatement(
                ObjectAccess(
                    [
                        "a",
                    ]
                ),
                Program(
                    [VariantDef("A", [NamedType("x", "int"), NamedType("y", "float")])]
                ),
            ),
            VariableDeclaration("b", "A", False, pos=(43,1)),
        ]
    )
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 43, column: 1, Type 'A' not found"


def test_variant_as_param_type():
    """A : struct begin x : int; end V : variant begin a : A;  y : float; end ret(v : V): int begin return v.x; end al : A; al.x = 7; y : int = ret(al);"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", True)]),
            VariantDef("V", [NamedType("a", "A"), NamedType("y", "float")]),
            FuncDef(
                "ret",
                [Param("v", "V", True)],
                "int",
                Program([ReturnStatement(ObjectAccess(["v", "x"]))]),
            ),
            VariableDeclaration("al", "A", True),
            AssignmentStatement(ObjectAccess(["al", "x"]), IntLiteral(7)),
            VariableDeclaration(
                "y",
                "int",
                True,
                ObjectAccess([FunctionCall("ret", [ObjectAccess(["al"])])]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["y"])).value == 7


def test_assignment_of_two_different_types_to_variant():
    """int_or_float : variant begin x : int; y : float; end a : int_or_float = 1; b : int_or_float = 1.2;"""
    ast = Program(
        [
            VariantDef(
                "int_or_float", [NamedType("x", "int"), NamedType("y", "float")]
            ),
            VariableDeclaration("a", "int_or_float", True, IntLiteral(1)),
            VariableDeclaration("b", "int_or_float", True, FloatLiteral(1.2)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value.value == 1
    assert i.visit_obj_access(ObjectAccess(["a"])).name == "x"
    assert i.visit_obj_access(ObjectAccess(["b"])).value.value == 1.2
    assert i.visit_obj_access(ObjectAccess(["b"])).name == "y"


def test_assignment_of_two_different_types_to_same_variable():
    """int_or_float : variant begin x : int; y : float; end a : int_or_float = 1; a = 1.2;"""
    ast = Program(
        [
            VariantDef(
                "int_or_float", [NamedType("x", "int"), NamedType("y", "float")]
            ),
            VariableDeclaration("a", "int_or_float", True, IntLiteral(1)),
            AssignmentStatement(ObjectAccess(["a"]), FloatLiteral(1.2)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["a"])).value.value == 1.2


def test_recurrent_variant_def():
    """VariantList : variant begin vl : VariantList; x : int; end l : VariantList; l = 1;"""
    ast = Program(
        [
            VariantDef(
                "VariantList", [NamedType("vl", "VariantList", pos=(91,1)), NamedType("x", "int")]
            ),
            VariableDeclaration("l", "VariantList", True),
            AssignmentStatement(ObjectAccess(["l"]), IntLiteral(1)),
        ]
    )
    i = Interpreter()

    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "InterpreterError: row: 91, column: 1, Variant option 'vl' can no be of type variant"


def test_binary_tree():
    """Leaf : struct begin value : int; end Node : struct begin left : Tree; right : Tree; end Tree : variant begin leaf : Leaf; node : Node; end sumTree(tree : Tree) : int begin visit tree begin case leaf begin return leaf.value; end case node begin return sumTree(node.left)+sumTree(node.right); end end end l : Leaf; l.value = 5; sum : int = sumTree(l);"""
    ast = Program(
        [
            StructDef("Leaf", [VariableDeclaration("value", "int", True)]),
            StructDef(
                "Node",
                [
                    VariableDeclaration("left", "Tree", True),
                    VariableDeclaration("right", "Tree", True),
                ],
            ),
            VariantDef("Tree", [NamedType("leaf", "Leaf"), NamedType("node", "Node")]),
            FuncDef(
                "sumTree",
                [Param("tree", "Tree", True)],
                "int",
                Program(
                    [
                        VisitStatement(
                            ObjectAccess(["tree"]),
                            [
                                CaseSection(
                                    "leaf",
                                    Program(
                                        [
                                            ReturnStatement(
                                                ObjectAccess(["leaf", "value"])
                                            )
                                        ]
                                    ),
                                ),
                                CaseSection(
                                    "node",
                                    Program(
                                        [
                                            ReturnStatement(
                                                AddExpr(
                                                    [
                                                        ObjectAccess(
                                                            [
                                                                FunctionCall(
                                                                    "sumTree",
                                                                    [
                                                                        ObjectAccess(
                                                                            [
                                                                                "node",
                                                                                "left",
                                                                            ]
                                                                        )
                                                                    ],
                                                                )
                                                            ]
                                                        ),
                                                        ObjectAccess(
                                                            [
                                                                FunctionCall(
                                                                    "sumTree",
                                                                    [
                                                                        ObjectAccess(
                                                                            [
                                                                                "node",
                                                                                "right",
                                                                            ]
                                                                        )
                                                                    ],
                                                                )
                                                            ]
                                                        ),
                                                    ],
                                                    ["+"],
                                                )
                                            )
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ]
                ),
            ),
            VariableDeclaration("l", "Leaf", True),
            AssignmentStatement(ObjectAccess(["l", "value"]), IntLiteral(5)),
            VariableDeclaration(
                "sum",
                "int",
                True,
                ObjectAccess([FunctionCall("sumTree", [ObjectAccess(["l"])])]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["sum"])).value == 5


def test_assignment_to_not_initialised_variant_sub_attr_sub_attribute_matches():
    """A: struct begin x: int; end V : variant begin a : A; x : int; end v : V; v.x = 123;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False)]),
            VariantDef("V", [NamedType("a", "A"), NamedType("x", "int")]),
            VariableDeclaration("v", "V", False),
            AssignmentStatement(ObjectAccess(["v", "x"]), IntLiteral(123)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["v", "x"])).value == 123


def test_complex_assignment_both_coukd_match_matched_first():
    """A: struct begin x: int; end B: struct begin x: int; end V : variant begin a : A; b : B; end v : V; v.x = 123;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False)]),
            StructDef("B", [VariableDeclaration("x", "int", False)]),
            VariantDef("V", [NamedType("a", "A"), NamedType("b", "B")]),
            VariableDeclaration("v", "V", False),
            AssignmentStatement(ObjectAccess(["v", "x"]), IntLiteral(123)),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["v", "x"])).value == 123
    assert i.visit_obj_access(ObjectAccess(["v"])).get_concrete_type() == "A"
