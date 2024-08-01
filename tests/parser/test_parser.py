"""Correct token streams"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck


import pytest

from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *
from parser_exceptions import ParserException


class TokenProvider(Lexer):
    """Mocks lexer."""

    def __init__(self, _, list_of_tokens) -> None:
        self.tokens = list_of_tokens
        self.idx = -1
        self._EOT_token_in_place = False
        super().__init__(_)

    def _next_token(self):
        if self._EOT_token_in_place:
            return
        if self._is_end_of_file():
            self.curr_token = Token(TokenType.EOT)
            self._EOT_token_in_place = True
            return
        self.idx += 1
        self.curr_token = self.tokens[self.idx]

    def _is_end_of_file(self):
        return self.idx + 2 > len(self.tokens)


def test_sanity():
    """Test for making sure test infrastructure works"""
    # pylint: disable=C0121:singleton-comparison
    assert True == 1


def test_token_int_shall_parse_literal():
    """int"""

    tokens = [
        Token(TokenType.INT),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ParserException):  # TODO change to better exception
        result = parser._shall(parser._parse_literal())


literal_parse_funcs = [
    Parser._parse_literal,
    Parser._parse_term,
    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize("func", literal_parse_funcs)
def test_token_int_literal(func):
    """1"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = IntLiteral(1)
    assert result == expected


@pytest.mark.parametrize("func", literal_parse_funcs)
def test_token_str_literal(func):
    """'ala ma kota'"""

    tokens = [
        Token(TokenType.STR_LITERAL, "ala ma kota"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = StrLiteral("ala ma kota")
    assert result == expected


@pytest.mark.parametrize("func", literal_parse_funcs)
def test_token_float_literal(func):
    """1.2"""

    tokens = [
        Token(TokenType.FLOAT_LITERAL, 1.2),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = FloatLiteral(1.2)
    assert result == expected


@pytest.mark.parametrize("func", literal_parse_funcs)
def test_token_null_literal(func):
    """null"""

    tokens = [
        Token(TokenType.NULL),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = NullLiteral()
    assert result == expected


@pytest.mark.parametrize("func", literal_parse_funcs)
def test_token_int_parse_literal_shoul_not_advance(func):
    """int"""

    tokens = [
        Token(TokenType.INT),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    assert result is None
    assert parser.lexer.curr_token == tokens[0]


obj_access_parse_funcs = [
    Parser._parse_object_access,
    Parser._parse_term,
    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize("func", obj_access_parse_funcs)
def test_parse_object_access_a(func):
    """a"""

    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = ObjectAccess(["a"])
    assert result == expected


@pytest.mark.parametrize("func", obj_access_parse_funcs)
def test_parse_object_access_a_dot_b(func):
    """a.b"""

    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = ObjectAccess(["a", "b"])
    assert result == expected


@pytest.mark.parametrize("func", obj_access_parse_funcs)
def test_parse_object_access_a_dot_a(func):
    """a.a"""

    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = ObjectAccess(["a", "a"])
    assert result == expected


@pytest.mark.parametrize("func", obj_access_parse_funcs)
def test_parse_object_access_a_dot_b_dot_c(func):
    """a.b.c"""

    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "c"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = ObjectAccess(["a", "b", "c"])
    assert result == expected


nested_expr_funcs = [
    Parser._parse_term,
    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize("func", nested_expr_funcs)
def test_parse_nested_int_literal(func):
    """(1)"""

    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = IntLiteral(1)
    assert result == expected


@pytest.mark.parametrize("func", nested_expr_funcs)
def test_10x_nested_literal(func):
    """((((((((((1))))))))))"""
    tokens = [
        Token(TokenType.LEFT_BRACKET, position=(1, 2)),
        Token(TokenType.LEFT_BRACKET, position=(1, 3)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.LEFT_BRACKET, position=(1, 5)),
        Token(TokenType.LEFT_BRACKET, position=(1, 6)),
        Token(TokenType.LEFT_BRACKET, position=(1, 7)),
        Token(TokenType.LEFT_BRACKET, position=(1, 8)),
        Token(TokenType.LEFT_BRACKET, position=(1, 9)),
        Token(TokenType.LEFT_BRACKET, position=(1, 10)),
        Token(TokenType.LEFT_BRACKET, position=(1, 11)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 12)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 13)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 14)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 15)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 16)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 17)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 18)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 19)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 20)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 21)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 22)),
    ]
    expected = IntLiteral(1)
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    assert expected == result


@pytest.mark.parametrize("func", nested_expr_funcs)
def test_parse_nested_object_access(func):
    """(a.b.c)"""

    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "c"),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = ObjectAccess(["a", "b", "c"])
    assert result == expected


# TODO test function call

unary_parse_funcs = [
    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize("func", unary_parse_funcs)
def test_unary_10x_nested_literal(func):
    """-((((((((((1))))))))))"""
    tokens = [
        Token(TokenType.MINUS, position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 2)),
        Token(TokenType.LEFT_BRACKET, position=(1, 3)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.LEFT_BRACKET, position=(1, 5)),
        Token(TokenType.LEFT_BRACKET, position=(1, 6)),
        Token(TokenType.LEFT_BRACKET, position=(1, 7)),
        Token(TokenType.LEFT_BRACKET, position=(1, 8)),
        Token(TokenType.LEFT_BRACKET, position=(1, 9)),
        Token(TokenType.LEFT_BRACKET, position=(1, 10)),
        Token(TokenType.LEFT_BRACKET, position=(1, 11)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 12)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 13)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 14)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 15)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 16)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 17)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 18)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 19)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 20)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 21)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 22)),
    ]
    expected = UnaryExpr(IntLiteral(1))
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    assert expected == result


token_ast_pair_literals = [
    (Token(TokenType.INT_LITERAL, 1), IntLiteral(1)),
    (Token(TokenType.FLOAT_LITERAL, 1.2), FloatLiteral(1.2)),
    (Token(TokenType.STR_LITERAL, "abc"), StrLiteral("abc")),
    (Token(TokenType.NULL), NullLiteral()),
]


@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", unary_parse_funcs)
def test_parse_unary_literals(func, literal_token, ast):
    """-[1 | 1.2 | 'abc' | null]"""

    tokens = [
        Token(TokenType.MINUS),
        literal_token,
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = UnaryExpr(ast)
    assert result == expected


@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", unary_parse_funcs)
def test_parse_unary_nested_literals(func, literal_token, ast):
    """- ( [1 | 1.2 | 'abc' | null] )"""

    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = UnaryExpr(ast)
    assert result == expected


@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", unary_parse_funcs)
def test_parse_unary_of_nested_unary_literals(func, literal_token, ast):
    """- ( -[1 | 1.2 | 'abc' | null] )"""

    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = UnaryExpr(UnaryExpr(ast))
    assert result == expected


multi_parse_funcs = [
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize(
    "multi_op, multi_op_token",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize("literal_token1,ast1", token_ast_pair_literals)
@pytest.mark.parametrize("literal_token2,ast2", token_ast_pair_literals)
@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_two(
    func, literal_token1, ast1, literal_token2, ast2, multi_op, multi_op_token
):
    """literal1 * literal2"""

    tokens = [
        literal_token1,
        multi_op_token,
        literal_token2,
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr([ast1, ast2], [multi_op])
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_three_literals(func):
    """2 * 2.5 * 'abc' <=> 5 * 'abc' => typeError can not interpret 'abc' as number"""

    tokens = [
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.TIMES),
        Token(TokenType.FLOAT_LITERAL, 2.5),
        Token(TokenType.TIMES),
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [IntLiteral(2), FloatLiteral(2.5), StrLiteral("abc")], ["*", "*"]
    )
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_three_literals_different_order(func):
    """'abc' * 2 * 2.5 <=> 'abcabc' * 2.5 => 'abcabc' * 2 <=> 'abcabcabcabc'"""

    tokens = [
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.TIMES),
        Token(TokenType.FLOAT_LITERAL, 2.5),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [StrLiteral("abc"), IntLiteral(2), FloatLiteral(2.5)], ["*", "*"]
    )
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_three_literals_divide_times(func):
    """'abc' / 2 * 2.5 => not supported"""

    tokens = [
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.DIVIDE),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.TIMES),
        Token(TokenType.FLOAT_LITERAL, 2.5),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [StrLiteral("abc"), IntLiteral(2), FloatLiteral(2.5)], ["/", "*"]
    )
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_three_literals_times_divide(func):
    """'abc' / 2 * 2.5 => not supported"""

    tokens = [
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.DIVIDE),
        Token(TokenType.FLOAT_LITERAL, 2.5),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [StrLiteral("abc"), IntLiteral(2), FloatLiteral(2.5)], ["*", "/"]
    )
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_three_literals_divide_divide(func):
    """'abc' / 2 / 2.5 => not supported"""

    tokens = [
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.DIVIDE),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.DIVIDE),
        Token(TokenType.FLOAT_LITERAL, 2.5),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [StrLiteral("abc"), IntLiteral(2), FloatLiteral(2.5)], ["/", "/"]
    )
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_parse_multi_unary_literals_times_before_and_after(func):
    """1 * -2 * 1"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.TIMES),
        Token(TokenType.MINUS),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [IntLiteral(1), UnaryExpr(IntLiteral(2)), IntLiteral(1)], ["*", "*"]
    )
    assert result == expected


@pytest.mark.parametrize(
    "multi_op1, multi_op_token1",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize(
    "multi_op2, multi_op_token2",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", multi_parse_funcs)
def test_all_comb_multi_op_before_and_after_unary_literal(
    func, literal_token, ast, multi_op1, multi_op_token1, multi_op2, multi_op_token2
):
    """1 [* | /] - [literal] [* | /] 1"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        multi_op_token1,
        Token(TokenType.MINUS),
        literal_token,
        multi_op_token2,
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [IntLiteral(1), UnaryExpr(ast), IntLiteral(1)], [multi_op1, multi_op2]
    )
    assert result == expected


@pytest.mark.parametrize(
    "multi_op1, multi_op_token1",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize(
    "multi_op2, multi_op_token2",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", multi_parse_funcs)
def test_all_comb_multi_op_before_and_after_unary_nested_literal(
    func, literal_token, ast, multi_op1, multi_op_token1, multi_op2, multi_op_token2
):
    """1 [* | /] - ([literal]) [* | /] 1"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        multi_op_token1,
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        multi_op_token2,
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [IntLiteral(1), UnaryExpr(ast), IntLiteral(1)], [multi_op1, multi_op2]
    )
    assert result == expected


@pytest.mark.parametrize(
    "multi_op1, multi_op_token1",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize(
    "multi_op2, multi_op_token2",
    [("*", Token(TokenType.TIMES)), ("/", Token(TokenType.DIVIDE))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", multi_parse_funcs)
def test_all_comb_multi_op_before_and_after_unary_nested_unary_literal(
    func, literal_token, ast, multi_op1, multi_op_token1, multi_op2, multi_op_token2
):
    """1 [* | /] - ([literal]) [* | /] 1"""

    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        multi_op_token1,
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        multi_op_token2,
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [IntLiteral(1), UnaryExpr(UnaryExpr(ast)), IntLiteral(1)],
        [multi_op1, multi_op2],
    )
    assert result == expected


@pytest.mark.parametrize("func", multi_parse_funcs)
def test_unary_one_in_3_forms(func):
    """ -1 * (-1) / -(1)"""
    tokens = [
        Token(TokenType.MINUS, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 2)),
        Token(TokenType.TIMES, position=(1, 4)),
        Token(TokenType.LEFT_BRACKET, position=(1, 6)),
        Token(TokenType.MINUS, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 8)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 9)),
        Token(TokenType.DIVIDE, position=(1, 11)),
        Token(TokenType.MINUS, position=(1, 13)),
        Token(TokenType.LEFT_BRACKET, position=(1, 14)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 15)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 16)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = MultiExpr(
        [UnaryExpr(IntLiteral(1)), UnaryExpr(IntLiteral(1)),UnaryExpr(IntLiteral(1))],
        ['*','/'],
    )
    assert result == expected


add_parse_funcs = [
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize(
    "add_op, add_op_token",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize("literal_token1,ast1", token_ast_pair_literals)
@pytest.mark.parametrize("literal_token2,ast2", token_ast_pair_literals)
@pytest.mark.parametrize("func", add_parse_funcs)
def test_parse_add_two_literals(
    func, literal_token1, ast1, literal_token2, ast2, add_op, add_op_token
):
    """literal1 [+ | -] literal2"""
    tokens = [
        literal_token1,
        add_op_token,
        literal_token2,
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr([ast1, ast2], [add_op])
    assert result == expected


@pytest.mark.parametrize(
    "add_op1, add_op_token1",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize(
    "add_op2, add_op_token2",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", add_parse_funcs)
def test_all_comb_add_op_before_and_after_literal(
    func, add_op1, add_op_token1, add_op2, add_op_token2, literal_token, ast
):
    """3.21 [ + | - ] literal [ + | - ] 'abc'"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.21),
        add_op_token1,
        literal_token,
        add_op_token2,
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr([FloatLiteral(3.21), ast, StrLiteral("abc")], [add_op1, add_op2])
    assert result == expected


@pytest.mark.parametrize(
    "add_op1, add_op_token1",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize(
    "add_op2, add_op_token2",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", add_parse_funcs)
def test_all_comb_add_op_before_and_after_unary_literal(
    func, add_op1, add_op_token1, add_op2, add_op_token2, literal_token, ast
):
    """3.21 [ + | - ] -literal [ + | - ] 'abc'"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.21),
        add_op_token1,
        Token(TokenType.MINUS),
        literal_token,
        add_op_token2,
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr(
        [FloatLiteral(3.21), UnaryExpr(ast), StrLiteral("abc")], [add_op1, add_op2]
    )
    assert result == expected


@pytest.mark.parametrize(
    "add_op1, add_op_token1",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize(
    "add_op2, add_op_token2",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", add_parse_funcs)
def test_all_comb_add_op_before_and_after_nested_literal(
    func, add_op1, add_op_token1, add_op2, add_op_token2, literal_token, ast
):
    """3.21 [ + | - ] (literal) [ + | - ] 'abc'"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.21),
        add_op_token1,
        Token(TokenType.LEFT_BRACKET),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        add_op_token2,
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr([FloatLiteral(3.21), ast, StrLiteral("abc")], [add_op1, add_op2])
    assert result == expected


@pytest.mark.parametrize(
    "add_op1, add_op_token1",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize(
    "add_op2, add_op_token2",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", add_parse_funcs)
def test_all_comb_add_op_before_and_after_unary_nested_literal(
    func, add_op1, add_op_token1, add_op2, add_op_token2, literal_token, ast
):
    """3.21 [ + | - ] -(literal) [ + | - ] 'abc'"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.21),
        add_op_token1,
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        add_op_token2,
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr(
        [FloatLiteral(3.21), UnaryExpr(ast), StrLiteral("abc")], [add_op1, add_op2]
    )
    assert result == expected


@pytest.mark.parametrize(
    "add_op1, add_op_token1",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize(
    "add_op2, add_op_token2",
    [("+", Token(TokenType.PLUS)), ("-", Token(TokenType.MINUS))],
)
@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", add_parse_funcs)
def test_all_comb_add_op_before_and_after_unary_nested_unary_literal(
    func, add_op1, add_op_token1, add_op2, add_op_token2, literal_token, ast
):
    """3.21 [ + | - ] -(-literal) [ + | - ] 'abc'"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.21),
        add_op_token1,
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        literal_token,
        Token(TokenType.RIGHT_BRACKET),
        add_op_token2,
        Token(TokenType.STR_LITERAL, "abc"),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr(
        [FloatLiteral(3.21), UnaryExpr(UnaryExpr(ast)), StrLiteral("abc")],
        [add_op1, add_op2],
    )
    assert result == expected


@pytest.mark.parametrize("func", add_parse_funcs)
def test_subtraction_of_two_multi_expr(func):
    """-1 * -2 / -3 - -4 / -5 * -6"""
    tokens = [
        Token(TokenType.MINUS, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 2)),
        Token(TokenType.TIMES, position=(1, 4)),
        Token(TokenType.MINUS, position=(1, 6)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 7)),
        Token(TokenType.DIVIDE, position=(1, 9)),
        Token(TokenType.MINUS, position=(1, 11)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 12)),
        Token(TokenType.MINUS, position=(1, 14)),
        Token(TokenType.MINUS, position=(1, 16)),
        Token(TokenType.INT_LITERAL, 4, position=(1, 17)),
        Token(TokenType.DIVIDE, position=(1, 19)),
        Token(TokenType.MINUS, position=(1, 21)),
        Token(TokenType.INT_LITERAL, 5, position=(1, 22)),
        Token(TokenType.TIMES, position=(1, 24)),
        Token(TokenType.MINUS, position=(1, 26)),
        Token(TokenType.INT_LITERAL, 6, position=(1, 27)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr(
        [
            MultiExpr(
                [
                    UnaryExpr(IntLiteral(1)),
                    UnaryExpr(IntLiteral(2)),
                    UnaryExpr(IntLiteral(3)),
                ],
                ["*", "/"],
            ),
            MultiExpr(
                [
                    UnaryExpr(IntLiteral(4)),
                    UnaryExpr(IntLiteral(5)),
                    UnaryExpr(IntLiteral(6)),
                ],
                ["/", "*"],
            ),
        ],
        ["-"],
    )
    assert result == expected


@pytest.mark.parametrize("func", add_parse_funcs)
def test_add_expr_nested_chain(func):
    """1+(2+(3+(4+(5))))"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1, position=(1, 1)),
        Token(TokenType.PLUS, position=(1, 2)),
        Token(TokenType.LEFT_BRACKET, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 4)),
        Token(TokenType.PLUS, position=(1, 5)),
        Token(TokenType.LEFT_BRACKET, position=(1, 6)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 7)),
        Token(TokenType.PLUS, position=(1, 8)),
        Token(TokenType.LEFT_BRACKET, position=(1, 9)),
        Token(TokenType.INT_LITERAL, 4, position=(1, 10)),
        Token(TokenType.PLUS, position=(1, 11)),
        Token(TokenType.LEFT_BRACKET, position=(1, 12)),
        Token(TokenType.INT_LITERAL, 5, position=(1, 13)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 14)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 15)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 16)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 17)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr(
        [
            IntLiteral(1),
            AddExpr(
                [
                    IntLiteral(2),
                    AddExpr(
                        [
                            IntLiteral(3),
                            AddExpr(
                                [IntLiteral(4), IntLiteral(5)],
                                ["+"],
                            ),
                        ],
                        ["+"],
                    ),
                ],
                ["+"],
            ),
        ],
        ["+"],
    )
    assert result == expected


@pytest.mark.parametrize("func", add_parse_funcs)
def test_add_expr_nested_chain_start_from_left(func):
    """((((1)+2)+3)+4)+5"""
    tokens = [
        Token(TokenType.LEFT_BRACKET, position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 2)),
        Token(TokenType.LEFT_BRACKET, position=(1, 3)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 5)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 6)),
        Token(TokenType.PLUS, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 8)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 9)),
        Token(TokenType.PLUS, position=(1, 10)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 11)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 12)),
        Token(TokenType.PLUS, position=(1, 13)),
        Token(TokenType.INT_LITERAL, 4, position=(1, 14)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 15)),
        Token(TokenType.PLUS, position=(1, 16)),
        Token(TokenType.INT_LITERAL, 5, position=(1, 17)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AddExpr(
        [
            AddExpr(
                [
                    AddExpr(
                        [
                            AddExpr(
                                [
                                    IntLiteral(1),
                                    IntLiteral(2),
                                ],
                                ["+"],
                            ),
                            IntLiteral(3),
                        ],
                        ["+"],
                    ),
                    IntLiteral(4),
                ],
                ["+"],
            ),
            IntLiteral(5),
        ],
        ["+"],
    )
    assert result == expected



rel_operators = [
    (TokenType.LESS, '<'),
    (TokenType.LESS_EQUAL, '<='),
    (TokenType.EQUAL, '=='),
    (TokenType.INEQUAL, '!='),
    (TokenType.GREATER, '>'),
    (TokenType.GREATER_EQUAL, '>='),
]

rel_parse_funcs = [
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr
]

@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)
@pytest.mark.parametrize("func", rel_parse_funcs)
def test_rel_literals(func, rel_token_type, rel_str):
    """1 rel_op 2"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1, position=(1, 1)),
        Token(rel_token_type, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = RelationExpr(IntLiteral(1), IntLiteral(2), rel_str)
    assert result == expected


@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)
@pytest.mark.parametrize("func", rel_parse_funcs)
def test_rel_(func,rel_token_type,rel_str):
    """1+2*-3 rel_op 4""" # TODO after adding position to AST then two-letter rel operators will not pass
    tokens = [
        Token(TokenType.INT_LITERAL, 1, position=(1, 1)),
        Token(TokenType.PLUS, position=(1, 2)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 3)),
        Token(TokenType.TIMES, position=(1, 4)),
        Token(TokenType.MINUS, position=(1, 5)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 6)),
        Token(rel_token_type, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 4, position=(1, 8)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = RelationExpr(AddExpr([IntLiteral(1), MultiExpr([IntLiteral(2), UnaryExpr(IntLiteral(3))], ['*'])], ['+']), IntLiteral(4), rel_str)
    assert result == expected



@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)
@pytest.mark.parametrize("func", rel_parse_funcs)
def test_rel_sum_beofre_multi(func,rel_token_type,rel_str):
    """(1+2)*-3 rel_op 4"""
    tokens = [
        Token(TokenType.LEFT_BRACKET, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 2)),
        Token(TokenType.PLUS, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 4)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 5)),
        Token(TokenType.TIMES, position=(1, 6)),
        Token(TokenType.MINUS, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 8)),
        Token(rel_token_type, position=(1, 9)),
        Token(TokenType.INT_LITERAL, 4, position=(1, 10)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = RelationExpr(MultiExpr([AddExpr([IntLiteral(1), IntLiteral(2)], ['+']), UnaryExpr(IntLiteral(3))], ['*']), IntLiteral(4), rel_str)
    assert result == expected

@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)
@pytest.mark.parametrize("func", rel_parse_funcs)
def test_rel_not_correct_relation_negation(func,rel_token_type,rel_str):
    """- 1<2"""
    tokens = [
        Token(TokenType.MINUS, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 3)),
        Token(rel_token_type, position=(1, 4)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = RelationExpr(UnaryExpr(IntLiteral(1)), IntLiteral(2), rel_str)
    assert result == expected

@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)
@pytest.mark.parametrize("func", rel_parse_funcs)
def test_rel_correct_relation_negation(func,rel_token_type,rel_str):
    """- (1<2)"""
    tokens = [
        Token(TokenType.MINUS, position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 4)),
        Token(rel_token_type, position=(1, 5)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 6)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 7)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = UnaryExpr(RelationExpr(IntLiteral(1), IntLiteral(2), rel_str))
    assert result == expected


@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)
@pytest.mark.parametrize("func", rel_parse_funcs)
def test_rel_negation_right_is_more_complex_than_left(func,rel_token_type,rel_str):
    """-(-4 < -1+-2/-3)"""
    tokens = [
        Token(TokenType.MINUS, position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 2)),
        Token(TokenType.MINUS, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 4, position=(1, 4)),
        Token(rel_token_type, position=(1, 6)),
        Token(TokenType.MINUS, position=(1, 8)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 9)),
        Token(TokenType.PLUS, position=(1, 10)),
        Token(TokenType.MINUS, position=(1, 11)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 12)),
        Token(TokenType.DIVIDE, position=(1, 13)),
        Token(TokenType.MINUS, position=(1, 14)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 15)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 16)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = UnaryExpr(RelationExpr(UnaryExpr(IntLiteral(4)), AddExpr([UnaryExpr(IntLiteral(1)), MultiExpr([UnaryExpr(IntLiteral(2)), UnaryExpr(IntLiteral(3))], ['/'])], ['+']), rel_str))
    assert result == expected


and_parse_funcs = [
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr
]

@pytest.mark.parametrize("func", and_parse_funcs)
def test_and_two_literals(func):
    """1 & 2"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1, position=(1, 1)),
        Token(TokenType.AND, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AndExpr([IntLiteral(1), IntLiteral(2)])
    assert result == expected

@pytest.mark.parametrize("func", and_parse_funcs)
def test_and_three_literals(func):
    """1 & 2 & 0"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1, position=(1, 1)),
        Token(TokenType.AND, position=(1, 3)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 5)),
        Token(TokenType.AND, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 0, position=(1, 9)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = func(parser)
    expected = AndExpr([IntLiteral(1), IntLiteral(2), IntLiteral(0)])
    assert result == expected