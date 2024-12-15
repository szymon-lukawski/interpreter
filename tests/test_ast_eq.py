"""Test for comparing two AST"""

from parser.AST import *


class SomeObject(ASTNode):
    pass


def test_sanity():
    assert True == 1


def test_int_not_same():
    """IntLiteral(1) != IntLiteral(2)"""
    assert IntLiteral(1) != IntLiteral(2)


def test_int_same():
    """IntLiteral(1) == IntLiteral(1)"""
    assert IntLiteral(1) == IntLiteral(1)


def test_int_same_attr_but_different_class_name():
    """IntLiteral(1) == IntLiteral(1)"""
    a = SomeObject()
    a.value = 1
    assert IntLiteral(1) != a


def test_float_same():
    """FloatLiteral(1) == FloatLiteral(1)"""
    assert FloatLiteral(1) == FloatLiteral(1)


def test_float_not_same():
    """FloatLiteral(1) == FloatLiteral(1)"""
    assert FloatLiteral(1.2) != FloatLiteral(1.02)


def test_float_same_attr_but_different_class_name():
    """FloatLiteral(1) == FloatLiteral(1)"""
    a = SomeObject()
    a.value = 1.2
    assert FloatLiteral(1.2) != a


def test_str_literal_same():
    """StrLiteral('abc') == StrLiteral('abc')"""
    assert StrLiteral("abc") == StrLiteral("abc")


def test_str_literal_not_same():
    """StrLiteral('abc') == StrLiteral('abcd')"""
    assert StrLiteral("abc") != StrLiteral("abcd")


def test_str_same_attr_but_different_class_name():
    """StrLiteral('abc') == SomeObject('abc')"""
    a = SomeObject()
    a.value = "abc"
    assert StrLiteral("abc") != a


def test_null_same():
    """NullLiteral() == NullLiteral()"""
    assert NullLiteral() == NullLiteral()


def test_unary_same():
    """-1 == -1"""
    assert UnaryExpr(IntLiteral(1)) == UnaryExpr(IntLiteral(1))


def test_unary_int_is_not_unary_float_with_same_value():
    """-1 == -1.0"""
    assert UnaryExpr(IntLiteral(1)) != UnaryExpr(FloatLiteral(1))


def test_unary_is_not_the_negated_part():
    """-1 != 1"""
    x = IntLiteral(1)
    assert UnaryExpr(x) != IntLiteral(1)


def test_multi_same_literlas_but_different_operations():
    """1 * 2 != 1 / 2"""
    assert MultiExpr([IntLiteral(1), IntLiteral(2)], ["*"]) != MultiExpr(
        [IntLiteral(1), IntLiteral(2)], ["/"]
    )


def test_multi_same():
    """1 * 2 != 1 * 2"""
    assert MultiExpr([IntLiteral(1), IntLiteral(2)], ["*"]) == MultiExpr(
        [IntLiteral(1), IntLiteral(2)], ["*"]
    )


def test_complex_same():
    """-((1.2 < 11/10 | 125 * -5 - 100 > 500 & 1 & -3*(4+7) != -17) | 9 / 3 >= -2+(-2*-2))"""
    a = UnaryExpr(
        OrExpr(
            [
                OrExpr(
                    [
                        RelationExpr(
                            FloatLiteral(1.2),
                            MultiExpr([IntLiteral(11), IntLiteral(10)], ["/"]),
                            "<",
                        ),
                        AndExpr(
                            [
                                RelationExpr(
                                    AddExpr(
                                        [
                                            MultiExpr(
                                                [
                                                    IntLiteral(125),
                                                    UnaryExpr(IntLiteral(5)),
                                                ],
                                                ["*"],
                                            ),
                                            IntLiteral(100),
                                        ],
                                        ["-"],
                                    ),
                                    IntLiteral(500),
                                    ">",
                                ),
                                IntLiteral(1),
                                RelationExpr(
                                    MultiExpr(
                                        [
                                            UnaryExpr(IntLiteral(3)),
                                            AddExpr(
                                                [IntLiteral(4), IntLiteral(7)], ["+"]
                                            ),
                                        ],
                                        ["*"],
                                    ),
                                    UnaryExpr(IntLiteral(17)),
                                    "!=",
                                ),
                            ]
                        ),
                    ]
                ),
                RelationExpr(
                    MultiExpr([IntLiteral(9), IntLiteral(3)], ["/"]),
                    AddExpr(
                        [
                            UnaryExpr(IntLiteral(2)),
                            MultiExpr(
                                [UnaryExpr(IntLiteral(2)), UnaryExpr(IntLiteral(2))],
                                ["*"],
                            ),
                        ],
                        ["+"],
                    ),
                    ">=",
                ),
            ]
        )
    )
    b = UnaryExpr(
        OrExpr(
            [
                OrExpr(
                    [
                        RelationExpr(
                            FloatLiteral(1.2),
                            MultiExpr([IntLiteral(11), IntLiteral(10)], ["/"]),
                            "<",
                        ),
                        AndExpr(
                            [
                                RelationExpr(
                                    AddExpr(
                                        [
                                            MultiExpr(
                                                [
                                                    IntLiteral(125),
                                                    UnaryExpr(IntLiteral(5)),
                                                ],
                                                ["*"],
                                            ),
                                            IntLiteral(100),
                                        ],
                                        ["-"],
                                    ),
                                    IntLiteral(500),
                                    ">",
                                ),
                                IntLiteral(1),
                                RelationExpr(
                                    MultiExpr(
                                        [
                                            UnaryExpr(IntLiteral(3)),
                                            AddExpr(
                                                [IntLiteral(4), IntLiteral(7)], ["+"]
                                            ),
                                        ],
                                        ["*"],
                                    ),
                                    UnaryExpr(IntLiteral(17)),
                                    "!=",
                                ),
                            ]
                        ),
                    ]
                ),
                RelationExpr(
                    MultiExpr([IntLiteral(9), IntLiteral(3)], ["/"]),
                    AddExpr(
                        [
                            UnaryExpr(IntLiteral(2)),
                            MultiExpr(
                                [UnaryExpr(IntLiteral(2)), UnaryExpr(IntLiteral(2))],
                                ["*"],
                            ),
                        ],
                        ["+"],
                    ),
                    ">=",
                ),
            ]
        )
    )
    assert a == b


def test_if_prog_cond_and_same_no_else():
    """if a < 10 begin a = a + 1; end"""
    ast = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
    )
    expected = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
    )
    assert ast == expected


def test_if_cond_and_prog_and_else_same():
    """if a < 10 begin a = a + 1; end else begin a = a - 3; end"""
    ast = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(3)], ["-"]),
                )
            ]
        ),
    )
    expected = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(3)], ["-"]),
                )
            ]
        ),
    )
    assert ast == expected


def test_if_cond_prog_same_else_diff():
    """if a < 10 begin a = a + 1; end [else begin end]"""
    ast = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
        Program([]),
    )
    expected = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
    )
    assert ast != expected


def test_if_prog_else_same_cond_diff():
    """if ['a < 10' | '10 > a'] begin a = a + 1; end else begin end"""
    ast = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
        Program([]),
    )
    expected = IfStatement(
        RelationExpr(IntLiteral(10), ObjectAccess(["a"]), ">"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
        Program([]),
    )
    assert ast != expected


def test_if_cond_else_same_prog_diff():
    """if a < 10 begin ['a = a + 1;' | 'a = a - 3;' end else begin end"""
    ast = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
        Program([]),
    )
    expected = IfStatement(
        RelationExpr(ObjectAccess(["a"]), IntLiteral(10), "<"),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(3)], ["-"]),
                )
            ]
        ),
        Program([]),
    )
    assert ast != expected


def test_while_cond_prog_same():
    """while b <= 12.34 begin b = b * 1.1; end"""
    ast = WhileStatement(
        RelationExpr(ObjectAccess(["b"]), FloatLiteral(12.34), "<="),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["b"]),
                    MultiExpr([ObjectAccess(["b"]), FloatLiteral(1.1)], ["*"]),
                )
            ]
        ),
    )
    expected = WhileStatement(
        RelationExpr(ObjectAccess(["b"]), FloatLiteral(12.34), "<="),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["b"]),
                    MultiExpr([ObjectAccess(["b"]), FloatLiteral(1.1)], ["*"]),
                )
            ]
        ),
    )
    assert ast == expected


def test_while_cond_same_prog_diff():
    """while b <= 12.34 begin ['b = b * 1.1;' | 'c = c * 1.1;'] end"""
    ast = WhileStatement(
        RelationExpr(ObjectAccess(["b"]), FloatLiteral(12.34), "<="),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["c"]),
                    MultiExpr([ObjectAccess(["c"]), FloatLiteral(1.1)], ["*"]),
                )
            ]
        ),
    )
    expected = WhileStatement(
        RelationExpr(ObjectAccess(["b"]), FloatLiteral(12.34), "<="),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["b"]),
                    MultiExpr([ObjectAccess(["b"]), FloatLiteral(1.1)], ["*"]),
                )
            ]
        ),
    )
    assert ast != expected


def test_while_prog_same_cond_diff():
    """while ['b <= 12.34' | '12.34 >= b'] begin c = c * 1.1; end"""
    ast = WhileStatement(
        RelationExpr(ObjectAccess(["b"]), FloatLiteral(12.34), "<="),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["c"]),
                    MultiExpr([ObjectAccess(["c"]), FloatLiteral(1.1)], ["*"]),
                )
            ]
        ),
    )
    expected = WhileStatement(
        RelationExpr(FloatLiteral(12.34), ObjectAccess(["b"]), ">="),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["c"]),
                    MultiExpr([ObjectAccess(["c"]), FloatLiteral(1.1)], ["*"]),
                )
            ]
        ),
    )
    assert ast != expected


def test_obj_access_name_chain_one_element_same():
    """a"""
    ast = ObjectAccess(["a"])
    expected = ObjectAccess(["a"])
    assert ast == expected


def test_obj_access_name_chain_two_elements_same():
    """a.b"""
    ast = ObjectAccess(["a", "b"])
    expected = ObjectAccess(["a", "b"])
    assert ast == expected


def test_obj_access_name_chain_two_elements_first_diff():
    """[a|c].b"""
    ast = ObjectAccess(["c", "b"])
    expected = ObjectAccess(["a", "b"])
    assert ast != expected


def test_obj_access_name_chain_two_elements_second_diff():
    """a.[b|c]"""
    ast = ObjectAccess(["a", "c"])
    expected = ObjectAccess(["a", "b"])
    assert ast != expected


def test_case_section_type_program_same():
    """case int begin end"""
    ast = CaseSection("int", Program([]))
    expected = CaseSection("int", Program([]))
    assert ast == expected


def test_case_section_program_same_type_diff():
    """case int[1] begin end"""
    ast = CaseSection("int", Program([]))
    expected = CaseSection("int1", Program([]))
    assert ast != expected


def test_case_section_type_same_program_diff():
    """case int begin [a = a + 1;] end"""
    ast = CaseSection(
        "int",
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
    )
    expected = CaseSection("int", Program([]))
    assert ast != expected


def test_visit_obj_case_sections_same():
    """visit a.c begin case int begin n = n + 1; end case float begin n = n - 2.5; end end"""
    ast = VisitStatement(
        ObjectAccess(["a", "c"]),
        [
            CaseSection(
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), IntLiteral(1)], ["+"]),
                        )
                    ]
                ),
            ),
            CaseSection(
                "float",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), FloatLiteral(2.5)], ["-"]),
                        )
                    ]
                ),
            ),
        ],
    )
    expected = VisitStatement(
        ObjectAccess(["a", "c"]),
        [
            CaseSection(
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), IntLiteral(1)], ["+"]),
                        )
                    ]
                ),
            ),
            CaseSection(
                "float",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), FloatLiteral(2.5)], ["-"]),
                        )
                    ]
                ),
            ),
        ],
    )
    assert ast == expected


def test_visit_case_sections_same_obj_diff():
    """visit [a.c|a.d] begin case int begin n = n + 1; end case float begin n = n - 2.5; end end"""
    ast = VisitStatement(
        ObjectAccess(["a", "c"]),
        [
            CaseSection(
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), IntLiteral(1)], ["+"]),
                        )
                    ]
                ),
            ),
            CaseSection(
                "float",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), FloatLiteral(2.5)], ["-"]),
                        )
                    ]
                ),
            ),
        ],
    )
    expected = VisitStatement(
        ObjectAccess(["a", "d"]),
        [
            CaseSection(
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), IntLiteral(1)], ["+"]),
                        )
                    ]
                ),
            ),
            CaseSection(
                "float",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), FloatLiteral(2.5)], ["-"]),
                        )
                    ]
                ),
            ),
        ],
    )
    assert ast != expected


def test_visit_obj_same_case_sections_diff():
    """visit a.c begin case int begin n = n + 1; end case float begin n = n - 2.5[1]; end end"""
    ast = VisitStatement(
        ObjectAccess(["a", "c"]),
        [
            CaseSection(
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), IntLiteral(1)], ["+"]),
                        )
                    ]
                ),
            ),
            CaseSection(
                "float",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), FloatLiteral(2.5)], ["-"]),
                        )
                    ]
                ),
            ),
        ],
    )
    expected = VisitStatement(
        ObjectAccess(["a", "c"]),
        [
            CaseSection(
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), IntLiteral(1)], ["+"]),
                        )
                    ]
                ),
            ),
            CaseSection(
                "float",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["n"]),
                            AddExpr([ObjectAccess(["n"]), FloatLiteral(2.51)], ["-"]),
                        )
                    ]
                ),
            ),
        ],
    )
    assert ast != expected


def test_assignment_obj_expr_same():
    """a = 1;"""
    ast = AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))
    expected = AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))
    assert ast == expected

def test_assignment_expr_same_obj_diff():
    """[a | b] = 1;"""
    ast = AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))
    expected = AssignmentStatement(ObjectAccess(['b']), IntLiteral(1))
    assert ast != expected

def test_assignment_obj_same_expr_diff():
    """a = [1 | 2];"""
    ast = AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))
    expected = AssignmentStatement(ObjectAccess(['a']), IntLiteral(2))
    assert ast != expected


def test_var_decl_non_mutable_no_initial_value_1():
    """a : int;"""
    ast = VariableDeclaration('a', 'int', False)
    expected = VariableDeclaration('a', 'int', False)
    assert ast == expected

def test_var_decl_non_mutable_no_initial_value_2():
    """[a | b] : int;"""
    ast = VariableDeclaration('a', 'int', False)
    expected = VariableDeclaration('b', 'int', False)
    assert ast != expected

def test_var_decl_non_mutable_no_initial_value_3():
    """a : [int | float];"""
    ast = VariableDeclaration('a', 'int', False)
    expected = VariableDeclaration('a', 'float', False)
    assert ast != expected

def test_var_decl_non_mutable_no_initial_value_4():
    """a : int; | b : float;"""
    ast = VariableDeclaration('a', 'int', False)
    expected = VariableDeclaration('b', 'float', False)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_1():
    """a : mut int;"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('a', 'int', True)
    assert ast == expected

def test_var_decl_mutable_no_initial_value_2():
    """[a | b] : mut int;"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('b', 'int', True)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_3():
    """a : [mut] int;"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('a', 'int', False)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_4():
    """a : mut [int | float];"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('a', 'float', True)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_5():
    """[a | b] : [mut] int;"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('b', 'int', False)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_6():
    """[a | b] : mut [int | float];"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('b', 'float', True)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_7():
    """a : [mut] [int | float];"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('a', 'float', False)
    assert ast != expected

def test_var_decl_mutable_no_initial_value_8():
    """[a | b] : [mut] [int | float];"""
    ast = VariableDeclaration('a', 'int', True)
    expected = VariableDeclaration('b', 'float', False)
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_1():
    """a : int = 1;"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('a', 'int', False, IntLiteral(1))
    assert ast == expected

def test_var_decl_non_mutable_with_initial_value_2():
    """[a | b] : int = 1;"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('b', 'int', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_3():
    """a : [int | float] = 1;"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('a', 'float', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_4():
    """a : int = [1 | 2] ;"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('a', 'int', False, IntLiteral(2))
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_5():
    """[a | b] : [int | float] = 1;"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('b', 'float', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_6():
    """[a | b] : int = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('b', 'int', False, IntLiteral(2))
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_7():
    """a : [int | float] = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('a', 'float', False, IntLiteral(2))
    assert ast != expected

def test_var_decl_non_mutable_with_initial_value_8():
    """a : int = 1; | b : float = 2;"""
    ast = VariableDeclaration('a', 'int', False, IntLiteral(1))
    expected = VariableDeclaration('b', 'float', False, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_1():
    """a : mut int = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'int', True, IntLiteral(1))
    assert ast == expected


def test_var_decl_mutable_with_initial_value_2():
    """[a | b]  : mut int = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'int', True, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_3():
    """a  : [mut] int = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'int', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_4():
    """a : mut [int | float] = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'float', True, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_5():
    """a  : mut int = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'int', True, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_6():
    """[a | b]  : [mut] int = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'int', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_7():
    """[a | b]  : mut [int | float] = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'float', True, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_8():
    """[a | b]  : mut int = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'int', True, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_9():
    """a  : [mut] [int | float] = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'float', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_10():
    """a  : [mut] int = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'int',False,  IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_11():
    """a  : mut [int | float] = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'float', True, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_12():
    """[a | b]  : [mut] [int | float] = 1;"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'float', False, IntLiteral(1))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_13():
    """[a | b]  : [mut] int = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'int', False, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_14():
    """[a | b]  : mut [int | float] = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'float', True, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_15():
    """a  : [mut] [int | float] = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('a', 'float', False, IntLiteral(2))
    assert ast != expected

def test_var_decl_mutable_with_initial_value_16():
    """[a | b]  :[mut] [int | float] = [1 | 2];"""
    ast = VariableDeclaration('a', 'int', True, IntLiteral(1))
    expected = VariableDeclaration('b', 'float', False, IntLiteral(2))
    assert ast != expected


def test_struct_name_attrs_same():
    """MyType : struct begin a : int; end"""
    ast = StructDef('MyType', [VariableDeclaration('a', 'int', False)])
    expected = StructDef('MyType', [VariableDeclaration('a', 'int', False)])
    assert ast == expected



def test_struct_attrs_same_name_diff():
    """[MyType | YourType] : struct begin a : int; end"""
    ast = StructDef('MyType', [VariableDeclaration('a', 'int', False)])
    expected = StructDef('YourType', [VariableDeclaration('a', 'int', False)])
    assert ast != expected

def test_struct_name_same_attrs_diff():
    """MyType : struct begin b : int; end"""
    ast = StructDef('MyType', [VariableDeclaration('a', 'int', False)])
    expected = StructDef('MyType', [VariableDeclaration('b', 'int', False)])
    assert ast != expected


def test_named_type_name_type_same():
    """a : int"""
    ast = NamedType('a', 'int')
    expected = NamedType('a', 'int')
    assert ast == expected

def test_named_type_type_same_name_diff():
    """[a | b] : int"""
    ast = NamedType('a', 'int')
    expected = NamedType('b', 'int')
    assert ast != expected

def test_named_type_name_same_type_diff():
    """a : int"""
    ast = NamedType('a', 'int')
    expected = NamedType('a', 'float')
    assert ast != expected

def test_named_type_name_type_diff():
    """a : int | b : float"""
    ast = NamedType('a', 'int')
    expected = NamedType('b', 'float')
    assert ast != expected

def test_variant_name_named_types_same():
    """A : variant begin a : int; b : float end"""
    ast = VariantDef('A', [NamedType('a', 'int'), NamedType('b', 'float')])
    expected = VariantDef('A', [NamedType('a', 'int'), NamedType('b', 'float')])
    assert ast == expected

def test_variant_named_types_same_name_diff():
    """[A | B] : variant begin a : int; b : float end"""
    ast = VariantDef('A', [NamedType('a', 'int'), NamedType('b', 'float')])
    expected = VariantDef('B', [NamedType('a', 'int'), NamedType('b', 'float')])
    assert ast != expected

def test_variant_name_same_named_types_diff():
    """A : variant begin [a | c] : int; b : float end"""
    ast = VariantDef('A', [NamedType('a', 'int'), NamedType('b', 'float')])
    expected = VariantDef('A', [NamedType('c', 'int'), NamedType('b', 'float')])
    assert ast != expected

def test_variant_name_named_types_diff():
    """[A | B] : variant begin [a | c] : int; b : float end"""
    ast = VariantDef('A', [NamedType('a', 'int'), NamedType('b', 'float')])
    expected = VariantDef('B', [NamedType('c', 'int'), NamedType('b', 'float')])
    assert ast != expected

def test_return_expr_same():
    """return 1;"""
    ast = ReturnStatement(IntLiteral(1))
    expected = ReturnStatement(IntLiteral(1))
    assert ast == expected


def test_return_expr_diff():
    """return [1 | 2];"""
    ast = ReturnStatement(IntLiteral(1))
    expected = ReturnStatement(IntLiteral(2))
    assert ast != expected




def test_param_non_mutable_no_initial_value_1():
    """a : int;"""
    ast = Param('a', 'int', False)
    expected = Param('a', 'int', False)
    assert ast == expected

def test_param_non_mutable_no_initial_value_2():
    """[a | b] : int;"""
    ast = Param('a', 'int', False)
    expected = Param('b', 'int', False)
    assert ast != expected

def test_param_non_mutable_no_initial_value_3():
    """a : [int | float];"""
    ast = Param('a', 'int', False)
    expected = Param('a', 'float', False)
    assert ast != expected

def test_param_non_mutable_no_initial_value_4():
    """a : int; | b : float;"""
    ast = Param('a', 'int', False)
    expected = Param('b', 'float', False)
    assert ast != expected

def test_param_mutable_no_initial_value_1():
    """a : mut int;"""
    ast = Param('a', 'int', True)
    expected = Param('a', 'int', True)
    assert ast == expected

def test_param_mutable_no_initial_value_2():
    """[a | b] : mut int;"""
    ast = Param('a', 'int', True)
    expected = Param('b', 'int', True)
    assert ast != expected

def test_param_mutable_no_initial_value_3():
    """a : [mut] int;"""
    ast = Param('a', 'int', True)
    expected = Param('a', 'int', False)
    assert ast != expected

def test_param_mutable_no_initial_value_4():
    """a : mut [int | float];"""
    ast = Param('a', 'int', True)
    expected = Param('a', 'float', True)
    assert ast != expected

def test_param_mutable_no_initial_value_5():
    """[a | b] : [mut] int;"""
    ast = Param('a', 'int', True)
    expected = Param('b', 'int', False)
    assert ast != expected

def test_param_mutable_no_initial_value_6():
    """[a | b] : mut [int | float];"""
    ast = Param('a', 'int', True)
    expected = Param('b', 'float', True)
    assert ast != expected

def test_param_mutable_no_initial_value_7():
    """a : [mut] [int | float];"""
    ast = Param('a', 'int', True)
    expected = Param('a', 'float', False)
    assert ast != expected

def test_param_mutable_no_initial_value_8():
    """[a | b] : [mut] [int | float];"""
    ast = Param('a', 'int', True)
    expected = Param('b', 'float', False)
    assert ast != expected

def test_param_non_mutable_with_initial_value_1():
    """a : int = 1;"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('a', 'int', False, IntLiteral(1))
    assert ast == expected

def test_param_non_mutable_with_initial_value_2():
    """[a | b] : int = 1;"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('b', 'int', False, IntLiteral(1))
    assert ast != expected

def test_param_non_mutable_with_initial_value_3():
    """a : [int | float] = 1;"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('a', 'float', False, IntLiteral(1))
    assert ast != expected

def test_param_non_mutable_with_initial_value_4():
    """a : int = [1 | 2] ;"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('a', 'int', False, IntLiteral(2))
    assert ast != expected

def test_param_non_mutable_with_initial_value_5():
    """[a | b] : [int | float] = 1;"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('b', 'float', False, IntLiteral(1))
    assert ast != expected

def test_param_non_mutable_with_initial_value_6():
    """[a | b] : int = [1 | 2];"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('b', 'int', False, IntLiteral(2))
    assert ast != expected

def test_param_non_mutable_with_initial_value_7():
    """a : [int | float] = [1 | 2];"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('a', 'float', False, IntLiteral(2))
    assert ast != expected

def test_param_non_mutable_with_initial_value_8():
    """a : int = 1; | b : float = 2;"""
    ast = Param('a', 'int', False, IntLiteral(1))
    expected = Param('b', 'float', False, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_1():
    """a : mut int = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'int', True, IntLiteral(1))
    assert ast == expected


def test_param_mutable_with_initial_value_2():
    """[a | b]  : mut int = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'int', True, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_3():
    """a  : [mut] int = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'int', False, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_4():
    """a : mut [int | float] = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'float', True, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_5():
    """a  : mut int = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'int', True, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_6():
    """[a | b]  : [mut] int = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'int', False, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_7():
    """[a | b]  : mut [int | float] = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'float', True, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_8():
    """[a | b]  : mut int = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'int', True, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_9():
    """a  : [mut] [int | float] = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'float', False, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_10():
    """a  : [mut] int = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'int',False,  IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_11():
    """a  : mut [int | float] = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'float', True, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_12():
    """[a | b]  : [mut] [int | float] = 1;"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'float', False, IntLiteral(1))
    assert ast != expected

def test_param_mutable_with_initial_value_13():
    """[a | b]  : [mut] int = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'int', False, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_14():
    """[a | b]  : mut [int | float] = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'float', True, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_15():
    """a  : [mut] [int | float] = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('a', 'float', False, IntLiteral(2))
    assert ast != expected

def test_param_mutable_with_initial_value_16():
    """[a | b]  :[mut] [int | float] = [1 | 2];"""
    ast = Param('a', 'int', True, IntLiteral(1))
    expected = Param('b', 'float', False, IntLiteral(2))
    assert ast != expected


def test_func_def_name_params_type_prog_same():
    """
    add(arg1: int, arg2: int) : int
    begin
        return arg1 + arg2;
    end
    """
    ast = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    expected = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    assert ast == expected


def test_func_def_params_type_prog_same_name_diff():
    """
    [add | sum](arg1: int, arg2: int) : int
    begin
        return arg1 + arg2;
    end
    """
    ast = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    expected = FuncDef('sum', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    assert ast != expected
    
def test_func_def_name_type_prog_same_params_diff():
    """
    add(arg1: int, [arg2 | arg12]: int) : int
    begin
        return arg1 + arg2;
    end
    """
    ast = FuncDef('add', [Param('arg1', 'int', False),Param('arg1', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    expected = FuncDef('add', [Param('arg1', 'int', False),Param('arg12', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    assert ast != expected
    

def test_func_def_name_params_prog_same_type_diff():
    """
    add(arg1: int, arg2: int) : [int | float]
    begin
        return arg1 + arg2;
    end
    """
    ast = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    expected = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'float', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    assert ast != expected

def test_func_def_name_params_type_same_prog_diff():
    """
    add(arg1: int, arg2: int) : int
    begin
        return arg1 + arg2 [- 1];
    end
    """
    ast = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2'])],['+'])]))
    expected = FuncDef('add', [Param('arg1', 'int', False),Param('arg2', 'int', False) ], 'int', Program([AddExpr([ObjectAccess(['arg1']), ObjectAccess(['arg2']), IntLiteral(1)],['+', '-'])]))
    assert ast != expected


def test_function_call_name_args_same():
    """add(1, 2)"""
    ast = FunctionCall('add', [IntLiteral(1), IntLiteral(2)])
    expected = FunctionCall('add', [IntLiteral(1), IntLiteral(2)])
    assert ast == expected

def test_function_call_args_same_name_diff():
    """add(1, 2)"""
    ast = FunctionCall('add', [IntLiteral(1), IntLiteral(2)])
    expected = FunctionCall('sum', [IntLiteral(1), IntLiteral(2)])
    assert ast != expected

def test_function_call_name_same_args_diff():
    """add(1, [1 | 3])"""
    ast = FunctionCall('add', [IntLiteral(1), IntLiteral(2)])
    expected = FunctionCall('add', [IntLiteral(1), IntLiteral(3)])
    assert ast != expected