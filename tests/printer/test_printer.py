from pretty_printer import Printer
from AST import *


def test_print_int_literal():
    """1"""
    ast = IntLiteral(1)
    printer = Printer()
    expected = "IntLiteral(1)"
    result = printer.print(ast)
    assert expected == result


def test_print_float_literal():
    """1.2"""
    ast = FloatLiteral(1.2)
    printer = Printer()
    expected = "FloatLiteral(1.2)"
    result = printer.print(ast)
    assert expected == result


def test_print_str_literal():
    """'abc'"""
    ast = StrLiteral("abc")
    printer = Printer()
    expected = "StrLiteral('abc')"
    result = printer.print(ast)
    assert expected == result


def test_print_null():
    """null"""
    ast = NullLiteral()
    printer = Printer()
    expected = "NullLiteral()"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_int():
    """-1"""
    ast = UnaryExpr(IntLiteral(1))
    printer = Printer()
    expected = "UnaryExpr(IntLiteral(1))"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_float():
    """-1.2"""
    ast = UnaryExpr(FloatLiteral(1.2))
    printer = Printer()
    expected = "UnaryExpr(FloatLiteral(1.2))"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_str_literal_not_interpretable():
    """-'abc'"""
    ast = UnaryExpr(StrLiteral("abc"))
    printer = Printer()
    expected = "UnaryExpr(StrLiteral('abc'))"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_str_literal_interpretable_as_int():
    """-'1'"""
    ast = UnaryExpr(StrLiteral("1"))
    printer = Printer()
    expected = "UnaryExpr(StrLiteral('1'))"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_str_literal_interpretable_as_float():
    """-'1.2'"""
    ast = UnaryExpr(StrLiteral("1.2"))
    printer = Printer()
    expected = "UnaryExpr(StrLiteral('1.2'))"
    result = printer.print(ast)
    assert expected == result


def test_print_add_ints():
    """1+2"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2)], ["+"])
    printer = Printer()
    expected = "AddExpr([IntLiteral(1), IntLiteral(2)], ['+'])"
    result = printer.print(ast)
    assert expected == result


def test_print_add_int_and_float():
    """1+2.3"""
    ast = AddExpr([IntLiteral(1), FloatLiteral(2.3)], ["+"])
    printer = Printer()
    expected = "AddExpr([IntLiteral(1), FloatLiteral(2.3)], ['+'])"
    result = printer.print(ast)
    assert expected == result


def test_print_add_float_and_int():
    """1.2+3"""
    ast = AddExpr([FloatLiteral(1.2), IntLiteral(3)], ["+"])
    printer = Printer()
    expected = "AddExpr([FloatLiteral(1.2), IntLiteral(3)], ['+'])"
    result = printer.print(ast)
    assert expected == result


def test_print_add_interpretable_as_int_str_and_int_minus_float():
    """'1'+2-3.4"""
    ast = AddExpr([StrLiteral("1"), IntLiteral(2), FloatLiteral(3.4)], ["+", "-"])
    printer = Printer()
    expected = (
        "AddExpr([StrLiteral('1'), IntLiteral(2), FloatLiteral(3.4)], ['+', '-'])"
    )
    result = printer.print(ast)
    assert expected == result


def test_print_add_noninterpretable_as_int_str_and_int_minus_float():
    """'abc'+2-3.4"""
    ast = AddExpr([StrLiteral("abc"), IntLiteral(2), FloatLiteral(3.4)], ["+", "-"])
    printer = Printer()
    expected = (
        "AddExpr([StrLiteral('abc'), IntLiteral(2), FloatLiteral(3.4)], ['+', '-'])"
    )
    result = printer.print(ast)
    assert expected == result


def test_print_multi_int_and_int():
    """1*2"""
    ast = MultiExpr([IntLiteral(1), IntLiteral(2)], ["*"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(1), IntLiteral(2)], ['*'])"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_int_and_zero():
    """1*0"""
    ast = MultiExpr([IntLiteral(1), IntLiteral(0)], ["*"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(1), IntLiteral(0)], ['*'])"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_zero_and_int():
    """0*1"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(1)], ["*"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(0), IntLiteral(1)], ['*'])"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_zero_and_int_divide_by_int():
    """0*1/2"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(1), IntLiteral(2)], ["*", "/"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(0), IntLiteral(1), IntLiteral(2)], ['*', '/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_int_divide_by_zero():
    """1/0"""
    ast = MultiExpr([IntLiteral(1), IntLiteral(0)], ["/"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(1), IntLiteral(0)], ['/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_times_zero():
    """0*0"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(0)], ["*"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(0), IntLiteral(0)], ['*'])"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_divided_by_zero():
    """0/0"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(0)], ["/"])
    printer = Printer()
    expected = "MultiExpr([IntLiteral(0), IntLiteral(0)], ['/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_divided_by_zero_but_floats():
    """0.0/0.0"""
    ast = MultiExpr([FloatLiteral(0.0), FloatLiteral(0.0)], ["/"])
    printer = Printer()
    expected = "MultiExpr([FloatLiteral(0.0), FloatLiteral(0.0)], ['/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_interpretable_as_int_str_divided_by_zero():
    """'1'/0"""
    ast = MultiExpr([StrLiteral("1"), IntLiteral(0)], ["/"])
    printer = Printer()
    expected = "MultiExpr([StrLiteral('1'), IntLiteral(0)], ['/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_interpretable_as_int_str_divided_by_interpretable_as_int_str_zero():
    """'1'/'0'"""
    ast = MultiExpr([StrLiteral("1"), StrLiteral("0")], ["/"])
    printer = Printer()
    expected = "MultiExpr([StrLiteral('1'), StrLiteral('0')], ['/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_interpretable_as_int_str_divided_by_interpretable_as_float_str_zero():
    """'1'/'0.0'"""
    ast = MultiExpr([StrLiteral("1"), StrLiteral("0.0")], ["/"])
    printer = Printer()
    expected = "MultiExpr([StrLiteral('1'), StrLiteral('0.0')], ['/'])"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_or_one():
    """0|1"""
    ast = OrExpr([IntLiteral(0), IntLiteral(1)])
    printer = Printer()
    expected = "OrExpr([IntLiteral(0), IntLiteral(1)])"
    result = printer.print(ast)
    assert expected == result


def test_print_one_or_zero():
    """1|0"""
    ast = OrExpr([IntLiteral(1), IntLiteral(0)])
    printer = Printer()
    expected = "OrExpr([IntLiteral(1), IntLiteral(0)])"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_or_zero_as_float_or_zero_as_int_str_or_zero_as_float_str_or_one():
    """0|0.0|'0'|'0.0'|1"""
    ast = OrExpr(
        [
            IntLiteral(0),
            FloatLiteral(0.0),
            StrLiteral("0"),
            StrLiteral("0.0"),
            IntLiteral(1),
        ]
    )
    printer = Printer()
    expected = "OrExpr([IntLiteral(0), FloatLiteral(0.0), StrLiteral('0'), StrLiteral('0.0'), IntLiteral(1)])"
    result = printer.print(ast)
    assert expected == result


def test_print_one_and_zero():
    """1&0"""
    ast = AndExpr([IntLiteral(1), IntLiteral(0)])
    printer = Printer()
    expected = "AndExpr([IntLiteral(1), IntLiteral(0)])"
    result = printer.print(ast)
    assert expected == result


def test_print_one_and_float():
    """1&1.2"""
    ast = AndExpr([IntLiteral(1), FloatLiteral(1.2)])
    printer = Printer()
    expected = "AndExpr([IntLiteral(1), FloatLiteral(1.2)])"
    result = printer.print(ast)
    assert expected == result


def test_print_one_and_float_and_one_as_int_str():
    """1&1.2&'1'"""
    ast = AndExpr([IntLiteral(1), FloatLiteral(1.2), StrLiteral("1")])
    printer = Printer()
    expected = "AndExpr([IntLiteral(1), FloatLiteral(1.2), StrLiteral('1')])"
    result = printer.print(ast)
    assert expected == result


def test_print_and_all_types_interpetable_as_true():
    """1&1.2&'1'&'1.2'"""
    ast = AndExpr(
        [IntLiteral(1), FloatLiteral(1.2), StrLiteral("1"), StrLiteral("1.2")]
    )
    printer = Printer()
    expected = "AndExpr([IntLiteral(1), FloatLiteral(1.2), StrLiteral('1'), StrLiteral('1.2')])"
    result = printer.print(ast)
    assert expected == result


def test_and_or_and():
    """0&1|2&3"""
    ast = OrExpr(
        [
            AndExpr([IntLiteral(0), IntLiteral(1)]),
            AndExpr([IntLiteral(0), IntLiteral(1)]),
        ]
    )
    printer = Printer()
    expected = "OrExpr([AndExpr([IntLiteral(0), IntLiteral(1)]), AndExpr([IntLiteral(0), IntLiteral(1)])])"
    result = printer.print(ast)
    assert expected == result


def test_or_and_or():
    """0|1&2|3"""
    ast = OrExpr(
        [IntLiteral(0), AndExpr([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)]
    )
    printer = Printer()
    expected = "OrExpr([IntLiteral(0), AndExpr([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)])"
    result = printer.print(ast)
    assert expected == result


def test_print_less_than():
    """1<2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "<")
    printer = Printer()
    expected = "RelationExpr(IntLiteral(1), IntLiteral(2), '<')"
    result = printer.print(ast)
    assert expected == result


def test_print_less_eq_than():
    """1<=2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "<=")
    printer = Printer()
    expected = "RelationExpr(IntLiteral(1), IntLiteral(2), '<=')"
    result = printer.print(ast)
    assert expected == result


def test_print_greater_than():
    """1>2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), ">")
    printer = Printer()
    expected = "RelationExpr(IntLiteral(1), IntLiteral(2), '>')"
    result = printer.print(ast)
    assert expected == result


def test_print_greater_eq_than():
    """1>=2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), ">=")
    printer = Printer()
    expected = "RelationExpr(IntLiteral(1), IntLiteral(2), '>=')"
    result = printer.print(ast)
    assert expected == result


def test_print_not_eq_than():
    """1!=2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "!=")
    printer = Printer()
    expected = "RelationExpr(IntLiteral(1), IntLiteral(2), '!=')"
    result = printer.print(ast)
    assert expected == result


def test_print_eq_than():
    """1==2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "==")
    printer = Printer()
    expected = "RelationExpr(IntLiteral(1), IntLiteral(2), '==')"
    result = printer.print(ast)
    assert expected == result


def test_print_complex_logical_expr():
    """-(1 < 2 & 3 >= 4) |
    (5!=6 & (7 == 8 | 9 > 10)) & ((11 <= 12 | 13 > 14) & (-15 < 16) | (17 == 18 & -19 >= 20)) |
    ((21 != 22) & (23 < 24 | 25 >= 26)) |
    (-(27 == 28) & (29 != 30 | 31 <= 32))"""
    ast = OrExpr(
        [
            UnaryExpr(
                AndExpr(
                    [
                        RelationExpr(IntLiteral(1), IntLiteral(2), "<"),
                        RelationExpr(IntLiteral(3), IntLiteral(4), ">="),
                    ]
                )
            ),
            AndExpr(
                [
                    AndExpr(
                        [
                            RelationExpr(IntLiteral(5), IntLiteral(6), "!="),
                            OrExpr(
                                [
                                    RelationExpr(IntLiteral(7), IntLiteral(8), "=="),
                                    RelationExpr(IntLiteral(9), IntLiteral(10), ">"),
                                ]
                            ),
                        ]
                    ),
                    OrExpr(
                        [
                            AndExpr(
                                [
                                    OrExpr(
                                        [
                                            RelationExpr(
                                                IntLiteral(11), IntLiteral(12), "<="
                                            ),
                                            RelationExpr(
                                                IntLiteral(13), IntLiteral(14), ">"
                                            ),
                                        ]
                                    ),
                                    RelationExpr(
                                        UnaryExpr(IntLiteral(15)), IntLiteral(16), "<"
                                    ),
                                ]
                            ),
                            AndExpr(
                                [
                                    RelationExpr(IntLiteral(17), IntLiteral(18), "=="),
                                    RelationExpr(
                                        UnaryExpr(IntLiteral(19)), IntLiteral(20), ">="
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            AndExpr(
                [
                    RelationExpr(IntLiteral(21), IntLiteral(22), "!="),
                    OrExpr(
                        [
                            RelationExpr(IntLiteral(23), IntLiteral(24), "<"),
                            RelationExpr(IntLiteral(25), IntLiteral(26), ">="),
                        ]
                    ),
                ]
            ),
            AndExpr(
                [
                    UnaryExpr(RelationExpr(IntLiteral(27), IntLiteral(28), "==")),
                    OrExpr(
                        [
                            RelationExpr(IntLiteral(29), IntLiteral(30), "!="),
                            RelationExpr(IntLiteral(31), IntLiteral(32), "<="),
                        ]
                    ),
                ]
            ),
        ]
    )
    printer = Printer()
    expected = "OrExpr([UnaryExpr(AndExpr([RelationExpr(IntLiteral(1), IntLiteral(2), '<'), RelationExpr(IntLiteral(3), IntLiteral(4), '>=')])), AndExpr([AndExpr([RelationExpr(IntLiteral(5), IntLiteral(6), '!='), OrExpr([RelationExpr(IntLiteral(7), IntLiteral(8), '=='), RelationExpr(IntLiteral(9), IntLiteral(10), '>')])]), OrExpr([AndExpr([OrExpr([RelationExpr(IntLiteral(11), IntLiteral(12), '<='), RelationExpr(IntLiteral(13), IntLiteral(14), '>')]), RelationExpr(UnaryExpr(IntLiteral(15)), IntLiteral(16), '<')]), AndExpr([RelationExpr(IntLiteral(17), IntLiteral(18), '=='), RelationExpr(UnaryExpr(IntLiteral(19)), IntLiteral(20), '>=')])])]), AndExpr([RelationExpr(IntLiteral(21), IntLiteral(22), '!='), OrExpr([RelationExpr(IntLiteral(23), IntLiteral(24), '<'), RelationExpr(IntLiteral(25), IntLiteral(26), '>=')])]), AndExpr([UnaryExpr(RelationExpr(IntLiteral(27), IntLiteral(28), '==')), OrExpr([RelationExpr(IntLiteral(29), IntLiteral(30), '!='), RelationExpr(IntLiteral(31), IntLiteral(32), '<=')])])])"
    result = printer.print(ast)
    assert expected == result


def test_object_access_simple_identifier():
    """a"""
    ast = ObjectAccess(["a"])
    expected = "ObjectAccess(['a'])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_object_access_one_dot():
    """a.b"""
    ast = ObjectAccess(["a", "b"])
    expected = "ObjectAccess(['a', 'b'])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_object_access_one_dot_same_name():
    """a.a"""
    ast = ObjectAccess(["a", "a"])
    expected = "ObjectAccess(['a', 'a'])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_object_access_4_dots():
    """a.b.c.d.e"""
    ast = ObjectAccess(["a", "b", "c", "d", "e"])
    expected = "ObjectAccess(['a', 'b', 'c', 'd', 'e'])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_assignment_simple():
    """a=1"""
    ast = AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1))
    expected = "AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_assignment_object_access_chained():
    """a.b.c.d=1"""
    ast = AssignmentStatement(ObjectAccess(["a", "b", "c", "d"]), IntLiteral(1))
    expected = "AssignmentStatement(ObjectAccess(['a', 'b', 'c', 'd']), IntLiteral(1))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_assignment_more_complicated_expr():
    """a=(1+2*3)/4"""
    ast = AssignmentStatement(
        ObjectAccess(["a"]),
        MultiExpr(
            [
                AddExpr(
                    [IntLiteral(1), MultiExpr([IntLiteral(2), IntLiteral(3)], ["*"])],
                    ["+"],
                ),
                IntLiteral(4),
            ],
            ["/"],
        ),
    )
    expected = "AssignmentStatement(ObjectAccess(['a']), MultiExpr([AddExpr([IntLiteral(1), MultiExpr([IntLiteral(2), IntLiteral(3)], ['*'])], ['+']), IntLiteral(4)], ['/']))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_empty_program():
    # TODO can empty program even exist?
    """<Empty>"""
    ast = Program([])
    expected = "Program([])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_program_with_assignment():
    """a=1;"""
    ast = Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1))])
    expected = "Program([AssignmentStatement(ObjectAccess(['a']), IntLiteral(1))])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_variable_declaration():
    """a: int;"""
    ast = VariableDeclaration("a", "int", False)
    expected = "VariableDeclaration('a', 'int', False)"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_mutable_variable_declaration():
    """a: mut int;"""
    ast = VariableDeclaration("a", "int", True)
    expected = "VariableDeclaration('a', 'int', True)"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_mutable_variable_declaration_float():
    """a: mut float;"""
    ast = VariableDeclaration("a", "float", True)
    expected = "VariableDeclaration('a', 'float', True)"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_mutable_variable_declaration_MyType():
    """a: mut MyType;"""
    ast = VariableDeclaration("a", "MyType", True)
    expected = "VariableDeclaration('a', 'MyType', True)"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected

def test_simple_if_empty_program():
    """if 1 begin end"""
    ast = IfStatement(IntLiteral(1), Program([]))
    expected = "IfStatement(IntLiteral(1), Program([]))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_simple_if_assignment():
    """if 1 begin a = 12; end"""
    ast = IfStatement(
        IntLiteral(1),
        Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(12))]),
    )
    expected = "IfStatement(IntLiteral(1), Program([AssignmentStatement(ObjectAccess(['a']), IntLiteral(12))]))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_if_assignment_else_assignment():
    """if 1 begin a = 12; end else begin a = 123; end"""
    ast = IfStatement(
        IntLiteral(1),
        Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(12))]),
        Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(123))]),
    )
    expected = "IfStatement(IntLiteral(1), Program([AssignmentStatement(ObjectAccess(['a']), IntLiteral(12))]), Program([AssignmentStatement(ObjectAccess(['a']), IntLiteral(123))]))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected

def test_simple_while():
    """while 1 begin a = a + 1; end"""
    ast = WhileStatement(IntLiteral(1), Program([AssignmentStatement(ObjectAccess(['a']), AddExpr([ObjectAccess(['a']), IntLiteral(1)], ['+']))]))
    expected = "WhileStatement(IntLiteral(1), Program([AssignmentStatement(ObjectAccess(['a']), AddExpr([ObjectAccess(['a']), IntLiteral(1)], ['+']))]))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_named_type():
    """p2d : Punkt2D"""
    ast = NamedType("p2d", "Punkt2D")
    expected = "NamedType('p2d', 'Punkt2D')"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_variant_def():
    """
    Punkt : variant
    begin
        p2d : Punkt2D;
        p3d : Punkt3D;
    end
    """
    ast = VariantDef(
        "Punkt", [NamedType("p2d", "Punkt2D"), NamedType("p3d", "Punkt3D")]
    )
    expected = "VariantDef('Punkt', [NamedType('p2d', 'Punkt2D'), NamedType('p3d', 'Punkt3D')])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected


def test_case_section():
    """
    case Punkt2D
    begin
        wiadmosc = '[' + p2d.x + '; ' +p2d.y + ']';
    end
    """
    ast = CaseSection(
        "Punkt2D",
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["wiadomosc"]),
                    AddExpr(
                        [
                            StrLiteral("["),
                            ObjectAccess(["p2d", "x"]),
                            StrLiteral("; "),
                            ObjectAccess(["p2d", "y"]),
                            StrLiteral("]"),
                        ],
                        ["+", "+", "+"],
                    ),
                )
            ]
        ),
    )
    expected = "CaseSection('Punkt2D', Program([AssignmentStatement(ObjectAccess(['wiadomosc']), AddExpr([StrLiteral('['), ObjectAccess(['p2d', 'x']), StrLiteral('; '), ObjectAccess(['p2d', 'y']), StrLiteral(']')], ['+', '+', '+']))]))"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected

def test_visit_punkt_example():
    """
    visit punkt
    begin
        case Punkt2D
        begin
            wiadmosc = '[' + p2d.x + '; ' + p2d.y + ']';
        end
        case Punkt3D
        begin
            wiadmosc = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';
        end
    end
    """
    ast = VisitStatement(ObjectAccess(['punkt']), [CaseSection('Punkt2D', Program([AssignmentStatement(ObjectAccess(['wiadomosc']), AddExpr([StrLiteral('['), ObjectAccess(['p2d', 'x']), StrLiteral('; '), ObjectAccess(['p2d', 'y']), StrLiteral(']')], ['+', '+', '+']))])), CaseSection('Punkt3D', Program([AssignmentStatement(ObjectAccess(['wiadomosc']), AddExpr([StrLiteral('['), ObjectAccess(['p3d', 'x']), StrLiteral('; '), ObjectAccess(['p3d', 'y']), StrLiteral('; '), ObjectAccess(['p3d', 'z']), StrLiteral(']')], ['+', '+', '+', '+']))]))])
    
    expected = "VisitStatement(ObjectAccess(['punkt']), [CaseSection('Punkt2D', Program([AssignmentStatement(ObjectAccess(['wiadomosc']), AddExpr([StrLiteral('['), ObjectAccess(['p2d', 'x']), StrLiteral('; '), ObjectAccess(['p2d', 'y']), StrLiteral(']')], ['+', '+', '+']))])), CaseSection('Punkt3D', Program([AssignmentStatement(ObjectAccess(['wiadomosc']), AddExpr([StrLiteral('['), ObjectAccess(['p3d', 'x']), StrLiteral('; '), ObjectAccess(['p3d', 'y']), StrLiteral('; '), ObjectAccess(['p3d', 'z']), StrLiteral(']')], ['+', '+', '+', '+']))]))])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected

def test_struct_example():
    """
    Point1D : struct
    begin
    x : mut int = 0; @ wartość domyślna wynosi 0
    end
    """
    ast = StructDef('Point1D', [VariableDeclaration('x', 'int', True, IntLiteral(0))])
    expected = "StructDef('Point1D', [VariableDeclaration('x', 'int', True, IntLiteral(0))])"
    printer = Printer()
    result = printer.print(ast)
    assert result == expected