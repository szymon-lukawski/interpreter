"""Correct token streams. """

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck


import pytest

from lexer.token_type import TokenType
from lexer.my_token import Token
from my_parser import Parser
from lexer.lexer import Lexer
from parser.AST import *
from parser_exceptions import ParserException
from token_provider import TokenProvider




def test_sanity():
    """Test for making sure test infrastructure works"""
    # pylint: disable=C0121:singleton-comparison
    assert True == 1


id_values = [
    "MyType",
    "YourType1234567890",
    "Human",
    "A",
    "a",
    "ZX",
    "ala_ma_kota",
    "abc",
    "a1",
    "z_13",
    "ThisIsVariable",
]


@pytest.mark.parametrize("id_value", id_values)
def test_identifier_different_values(id_value):
    """identifier"""

    tokens = [
        Token(TokenType.IDENTIFIER, id_value),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_identifier()
    assert result == id_value


def test_args_no_args():
    """)"""

    tokens = [
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_args()
    assert result == []


def test_args_int_literal():
    """1)"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_args()
    assert result == [IntLiteral(1)]


def test_args_nested_int_literal():
    """(1))"""

    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_args()
    assert result == [IntLiteral(1)]


def test_args_one_multi_expr_arg():
    """(trapez.a+trapez.b)*trapez.h/2"""

    tokens = [
        Token(TokenType.LEFT_BRACKET, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "trapez", position=(1, 2)),
        Token(TokenType.DOT, position=(1, 8)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 9)),
        Token(TokenType.PLUS, position=(1, 10)),
        Token(TokenType.IDENTIFIER, "trapez", position=(1, 11)),
        Token(TokenType.DOT, position=(1, 17)),
        Token(TokenType.IDENTIFIER, "b", position=(1, 18)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 19)),
        Token(TokenType.TIMES, position=(1, 20)),
        Token(TokenType.IDENTIFIER, "trapez", position=(1, 21)),
        Token(TokenType.DOT, position=(1, 27)),
        Token(TokenType.IDENTIFIER, "h", position=(1, 28)),
        Token(TokenType.DIVIDE, position=(1, 29)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 30)),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_args()
    assert result == [
        MultiExpr(
            [
                AddExpr(
                    [ObjectAccess(["trapez", "a"]), ObjectAccess(["trapez", "b"])],
                    ["+"],
                ),
                ObjectAccess(["trapez", "h"]),
                IntLiteral(2),
            ],
            ["*", "/"],
        )
    ]


def test_args_two_diff_literals():
    """1,3.2"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.COMMA),
        Token(TokenType.FLOAT_LITERAL, 3.2),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_args()
    assert result == [IntLiteral(1), FloatLiteral(3.2)]


def test_args_four_term_arg():
    """a.b,1,'abc',3.2,null"""

    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.COMMA),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.COMMA),
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.COMMA),
        Token(TokenType.FLOAT_LITERAL, 3.2),
        Token(TokenType.COMMA),
        Token(TokenType.NULL),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_args()
    assert result == [
        ObjectAccess(["a", "b"]),
        IntLiteral(1),
        StrLiteral("abc"),
        FloatLiteral(3.2),
        NullLiteral(),
    ]


def test_parse_func_or_name_ala_name():
    """ala"""
    tokens = [
        Token(TokenType.IDENTIFIER, "ala"),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_func_or_name()
    assert result == "ala"


def test_parse_func_or_name_ala_func_no_args():
    """ala()"""
    tokens = [
        Token(TokenType.IDENTIFIER, "ala", (1,1)),
        Token(TokenType.LEFT_BRACKET, position=(1,4)),
        Token(TokenType.RIGHT_BRACKET, position=(1,5)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_func_or_name()
    assert result == FunctionCall("ala", [])


def test_parse_func_or_name_ala_func_with_args():
    """ala(a.b,1,'abc',3.2,null)"""
    tokens = [
        Token(TokenType.IDENTIFIER, "ala"),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.COMMA),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.COMMA),
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.COMMA),
        Token(TokenType.FLOAT_LITERAL, 3.2),
        Token(TokenType.COMMA),
        Token(TokenType.NULL),
        Token(TokenType.RIGHT_BRACKET),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_func_or_name()
    assert result == FunctionCall(
        "ala",
        [
            ObjectAccess(["a", "b"]),
            IntLiteral(1),
            StrLiteral("abc"),
            FloatLiteral(3.2),
            NullLiteral(),
        ],
    )


built_in_types = [
    (TokenType.INT, "int"),
    (TokenType.FLOAT, "float"),
    (TokenType.STR, "str"),
    (TokenType.NULL_TYPE, "null_type"),
]


@pytest.mark.parametrize("tt, t_str", built_in_types)
def test_type_built_in(tt, t_str):
    """int | float | str"""

    tokens = [
        Token(tt),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._shall(parser._parse_type())
    assert result == t_str


other_types = [
    (Token(TokenType.IDENTIFIER, "MyType"), "MyType"),
    (Token(TokenType.IDENTIFIER, "YourType1234567890"), "YourType1234567890"),
    (Token(TokenType.IDENTIFIER, "Car_"), "Car_"),
]


@pytest.mark.parametrize("t, t_str", other_types)
def test_type_other(t, t_str):
    """MyType | YourType1234567890 | Car_"""

    tokens = [
        t,
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._shall(parser._parse_type())
    assert result == t_str


@pytest.mark.parametrize("t, t_str", other_types)
def test_named_type_name_and_type_the_same(t, t_str):
    """SomeName : SomeName;"""
    tokens = [
        t,
        Token(TokenType.COLON),
        t,
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._shall(parser._try_parse_named_type())
    assert result == NamedType(t_str, t_str)


def test_named_type_ala_of_type_human():
    """ala : Human;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "ala"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._shall(parser._try_parse_named_type())
    assert result == NamedType("ala", "Human")


def test_named_types_zero():
    """Empty"""
    tokens = [
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_named_types()
    assert result == []


def test_named_types_one():
    """ala : Human;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "ala"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_named_types()
    assert result == [NamedType("ala", "Human")]


def test_named_types_two():
    """a : int; b : float;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.COLON),
        Token(TokenType.INT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.COLON),
        Token(TokenType.FLOAT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_named_types()
    assert result == [NamedType("a", "int"), NamedType("b", "float")]


def test_named_types_two_self_two_built_in():
    """a : Human; b : float; c : int; d : Car;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.COLON),
        Token(TokenType.FLOAT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "c"),
        Token(TokenType.COLON),
        Token(TokenType.INT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "d"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Car"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_named_types()
    assert result == [
        NamedType("a", "Human"),
        NamedType("b", "float"),
        NamedType("c", "int"),
        NamedType("d", "Car"),
    ]


def test_if_empty_no_else():
    """if 1 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 4)),
        Token(TokenType.BEGIN, position=(1, 6)),
        Token(TokenType.END, position=(1, 12)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([IfStatement(IntLiteral(1), Program([]))])
    assert result == expected


def test_if_empty_with_empty_else():
    """if 1 begin end else begin end"""
    tokens = [
        Token(TokenType.IF),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.ELSE),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([IfStatement(IntLiteral(1), Program([]), Program([]))])
    assert result == expected


def test_while_empty():
    """while 1 begin end"""
    tokens = [
        Token(TokenType.WHILE),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([WhileStatement(IntLiteral(1), Program([]))])
    assert result == expected


def test_block_empty():
    """begin end"""
    tokens = [
        Token(TokenType.BEGIN),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([Program([])])
    assert result == expected


def test_struct_empty():
    """a : struct begin end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.STRUCT, position=(1, 5)),
        Token(TokenType.BEGIN, position=(1, 12)),
        Token(TokenType.END, position=(1, 18)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([StructDef("a", [])])
    assert result == expected


def test_variant_empty():
    """v : variant begin end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "v", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.VARIANT, position=(1, 5)),
        Token(TokenType.BEGIN, position=(1, 13)),
        Token(TokenType.END, position=(1, 19)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariantDef("v", [])])
    assert result == expected


def test_variant_4_different_named_types():
    """v : variant begin a : Human; b : float; c : int; d : Car; end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "v"),
        Token(TokenType.COLON),
        Token(TokenType.VARIANT),
        Token(TokenType.BEGIN),
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.COLON),
        Token(TokenType.FLOAT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "c"),
        Token(TokenType.COLON),
        Token(TokenType.INT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "d"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Car"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program(
        [
            VariantDef(
                "v",
                [
                    NamedType("a", "Human"),
                    NamedType("b", "float"),
                    NamedType("c", "int"),
                    NamedType("d", "Car"),
                ],
            )
        ]
    )
    assert result == expected


def test_return_int_literal():
    """return 1;"""
    tokens = [
        Token(TokenType.RETURN),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.SEMICOLON),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([ReturnStatement(IntLiteral(1))])
    assert result == expected


def test_case_sections_empty():
    """Empty"""
    tokens = []

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_case_sections()
    expected = []
    assert result == expected


def test_case_sections_one_empty():
    """case int begin end"""
    tokens = [
        Token(TokenType.CASE),
        Token(TokenType.INT),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_case_sections()
    expected = [CaseSection("int", Program([]))]
    assert result == expected


def test_case_sections_2_my_types_2_built_in_all_empty():
    """case int begin end case Car begin end case float begin end case Human begin end"""
    tokens = [
        Token(TokenType.CASE),
        Token(TokenType.INT),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Car"),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.FLOAT),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_case_sections()
    expected = [
        CaseSection("int", Program([])),
        CaseSection("Car", Program([])),
        CaseSection("float", Program([])),
        CaseSection("Human", Program([])),
    ]
    assert result == expected


def test_case_sections_2_my_types_2_built_in_not_empty():
    """case int begin begin end end
    case Car begin return 'Car'; end
    case float begin return 3.14; end
    case Human begin return 'Human'; end"""
    tokens = [
        Token(TokenType.CASE),
        Token(TokenType.INT),
        Token(TokenType.BEGIN),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Car"),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.STR_LITERAL, "Car"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.FLOAT),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.STR_LITERAL, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_case_sections()
    expected = [
        CaseSection("int", Program([Program([])])),
        CaseSection("Car", Program([ReturnStatement(StrLiteral("Car"))])),
        CaseSection("float", Program([ReturnStatement(FloatLiteral(3.14))])),
        CaseSection("Human", Program([ReturnStatement(StrLiteral("Human"))])),
    ]
    assert result == expected


def test_visit_empty():
    """visit ala begin end"""
    tokens = [
        Token(TokenType.VISIT),
        Token(TokenType.IDENTIFIER, "ala"),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_visit_statement()
    expected = VisitStatement(ObjectAccess(["ala"]), [])
    assert result == expected


def test_visit_2_other_types_2_built_in_parse_visit():
    """visit ala begin end"""
    tokens = [
        Token(TokenType.VISIT),
        Token(TokenType.IDENTIFIER, "ala"),
        Token(TokenType.BEGIN),
        Token(TokenType.CASE),
        Token(TokenType.INT),
        Token(TokenType.BEGIN),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Car"),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.STR_LITERAL, "Car"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.FLOAT),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.STR_LITERAL, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.END),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_visit_statement()
    expected = VisitStatement(
        ObjectAccess(["ala"]),
        [
            CaseSection("int", Program([Program([])])),
            CaseSection("Car", Program([ReturnStatement(StrLiteral("Car"))])),
            CaseSection("float", Program([ReturnStatement(FloatLiteral(3.14))])),
            CaseSection("Human", Program([ReturnStatement(StrLiteral("Human"))])),
        ],
    )
    assert result == expected


def test_visit_2_other_types_2_built_in_parse_program():
    """visit ala begin end"""
    tokens = [
        Token(TokenType.VISIT),
        Token(TokenType.IDENTIFIER, "ala"),
        Token(TokenType.BEGIN),
        Token(TokenType.CASE),
        Token(TokenType.INT),
        Token(TokenType.BEGIN),
        Token(TokenType.BEGIN),
        Token(TokenType.END),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Car"),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.STR_LITERAL, "Car"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.FLOAT),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.CASE),
        Token(TokenType.IDENTIFIER, "Human"),
        Token(TokenType.BEGIN),
        Token(TokenType.RETURN),
        Token(TokenType.STR_LITERAL, "Human"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.END),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program(
        [
            VisitStatement(
                ObjectAccess(["ala"]),
                [
                    CaseSection("int", Program([Program([])])),
                    CaseSection("Car", Program([ReturnStatement(StrLiteral("Car"))])),
                    CaseSection(
                        "float", Program([ReturnStatement(FloatLiteral(3.14))])
                    ),
                    CaseSection(
                        "Human", Program([ReturnStatement(StrLiteral("Human"))])
                    ),
                ],
            )
        ]
    )
    assert result == expected


def test_variable_decl_not_mutable_no_initial_value():
    """a : int;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.INT, position=(1, 5)),
        Token(TokenType.SEMICOLON, position=(1, 8)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariableDeclaration("a", "int", False)])
    assert result == expected


def test_variable_decl_mutable_no_initial_value():
    """a : mut int;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.MUT, position=(1, 5)),
        Token(TokenType.INT, position=(1, 9)),
        Token(TokenType.SEMICOLON, position=(1, 12)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariableDeclaration("a", "int", True)])
    assert result == expected


def test_var_decl_mutable_with_initial_value():
    """a : mut int = 1;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.MUT, position=(1, 5)),
        Token(TokenType.INT, position=(1, 9)),
        Token(TokenType.ASSIGNMENT, position=(1, 13)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 15)),
        Token(TokenType.SEMICOLON, position=(1, 16)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariableDeclaration("a", "int", True, IntLiteral(1))])
    assert result == expected


def test_var_decl_non_mutable_with_initial_value():
    """a : int = 1;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.INT, position=(1, 5)),
        Token(TokenType.ASSIGNMENT, position=(1, 9)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 11)),
        Token(TokenType.SEMICOLON, position=(1, 12)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariableDeclaration("a", "int", False, IntLiteral(1))])
    assert result == expected


def test_var_decl_non_mutable_my_type():
    """b : my_type;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "b", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.IDENTIFIER, "my_type", position=(1, 5)),
        Token(TokenType.SEMICOLON, position=(1, 12)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariableDeclaration("b", "my_type", False)])
    assert result == expected


def test_struct_populated_with_several_variables():
    """a : struct begin a:int; b:mut float; c:mut my_type; d : str = 'ala'; e:mut str = 'e';  end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.STRUCT, position=(1, 5)),
        Token(TokenType.BEGIN, position=(1, 12)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 18)),
        Token(TokenType.COLON, position=(1, 19)),
        Token(TokenType.INT, position=(1, 20)),
        Token(TokenType.SEMICOLON, position=(1, 23)),
        Token(TokenType.IDENTIFIER, "b", position=(1, 25)),
        Token(TokenType.COLON, position=(1, 26)),
        Token(TokenType.MUT, position=(1, 27)),
        Token(TokenType.FLOAT, position=(1, 31)),
        Token(TokenType.SEMICOLON, position=(1, 36)),
        Token(TokenType.IDENTIFIER, "c", position=(1, 38)),
        Token(TokenType.COLON, position=(1, 39)),
        Token(TokenType.MUT, position=(1, 40)),
        Token(TokenType.IDENTIFIER, "my_type", position=(1, 44)),
        Token(TokenType.SEMICOLON, position=(1, 51)),
        Token(TokenType.IDENTIFIER, "d", position=(1, 53)),
        Token(TokenType.COLON, position=(1, 55)),
        Token(TokenType.STR, position=(1, 57)),
        Token(TokenType.ASSIGNMENT, position=(1, 61)),
        Token(TokenType.STR_LITERAL, "ala", position=(1, 63)),
        Token(TokenType.SEMICOLON, position=(1, 68)),
        Token(TokenType.IDENTIFIER, "e", position=(1, 70)),
        Token(TokenType.COLON, position=(1, 71)),
        Token(TokenType.MUT, position=(1, 72)),
        Token(TokenType.STR, position=(1, 76)),
        Token(TokenType.ASSIGNMENT, position=(1, 80)),
        Token(TokenType.STR_LITERAL, "e", position=(1, 82)),
        Token(TokenType.SEMICOLON, position=(1, 85)),
        Token(TokenType.END, position=(1, 88)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program(
        [
            StructDef(
                "a",
                [
                    VariableDeclaration("a", "int", False),
                    VariableDeclaration("b", "float", True),
                    VariableDeclaration("c", "my_type", True),
                    VariableDeclaration("d", "str", False, StrLiteral("ala")),
                    VariableDeclaration("e", "str", True, StrLiteral("e")),
                ],
            )
        ]
    )
    assert result == expected


def test_func_empty_no_params():
    """a() : int begin end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 2)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 3)),
        Token(TokenType.COLON, position=(1, 5)),
        Token(TokenType.INT, position=(1, 7)),
        Token(TokenType.BEGIN, position=(1, 11)),
        Token(TokenType.END, position=(1, 17)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([FuncDef("a", [], "int", Program([]))])
    assert result == expected


def test_func_call_no_args():
    """a();"""
    tokens = [
        Token(TokenType.IDENTIFIER, "a", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 2)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 3)),
        Token(TokenType.SEMICOLON, position=(1, 4)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([FunctionCall("a", [])])
    assert result == expected


def test_func_def_with_params():
    """add(arg1 : int, arg2 : float) : int begin return arg1 + arg2; end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "add", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.IDENTIFIER, "arg1", position=(1, 5)),
        Token(TokenType.COLON, position=(1, 10)),
        Token(TokenType.INT, position=(1, 12)),
        Token(TokenType.COMMA, position=(1, 15)),
        Token(TokenType.IDENTIFIER, "arg2", position=(1, 17)),
        Token(TokenType.COLON, position=(1, 22)),
        Token(TokenType.FLOAT, position=(1, 24)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 29)),
        Token(TokenType.COLON, position=(1, 31)),
        Token(TokenType.INT, position=(1, 33)),
        Token(TokenType.BEGIN, position=(1, 37)),
        Token(TokenType.RETURN, position=(1, 43)),
        Token(TokenType.IDENTIFIER, "arg1", position=(1, 50)),
        Token(TokenType.PLUS, position=(1, 55)),
        Token(TokenType.IDENTIFIER, "arg2", position=(1, 57)),
        Token(TokenType.SEMICOLON, position=(1, 61)),
        Token(TokenType.END, position=(1, 63)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program(
        [
            FuncDef(
                "add",
                [Param("arg1", "int", False), Param("arg2", "float", False)],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr(
                                [ObjectAccess(["arg1"]), ObjectAccess(["arg2"])], ["+"]
                            )
                        )
                    ]
                ),
            )
        ]
    )
    assert result == expected


def test_func_call_arg_starting_with_identifier():
    """add(arg1);"""
    tokens = [
        Token(TokenType.IDENTIFIER, "add", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.IDENTIFIER, "arg1", position=(1, 5)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 9)),
        Token(TokenType.SEMICOLON, position=(1, 10)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([FunctionCall("add", [ObjectAccess(["arg1"])])])
    assert result == expected


def test_func_func_call_arg_starting_with_chained_identifier():
    """area(obj.sqare);"""
    tokens = [
        Token(TokenType.IDENTIFIER, "area", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 5)),
        Token(TokenType.IDENTIFIER, "obj", position=(1, 6)),
        Token(TokenType.DOT, position=(1, 9)),
        Token(TokenType.IDENTIFIER, "sqare", position=(1, 10)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 15)),
        Token(TokenType.SEMICOLON, position=(1, 16)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([FunctionCall("area", [ObjectAccess(["obj", "sqare"])])])
    assert result == expected


def test_func_call_with_3_int_literals_args():
    """area(1,2,3);"""
    tokens = [
        Token(TokenType.IDENTIFIER, "area", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 5)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 6)),
        Token(TokenType.COMMA, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 8)),
        Token(TokenType.COMMA, position=(1, 9)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 10)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 11)),
        Token(TokenType.SEMICOLON, position=(1, 12)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program(
        [FunctionCall("area", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])]
    )
    assert result == expected
