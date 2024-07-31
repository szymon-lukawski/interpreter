"""Parser tests"""

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
    expected = ObjectAccess(['a','b','c'])
    assert result == expected


unary_parse_funcs = [    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,]


token_ast_pair_literals = [(Token(TokenType.INT_LITERAL, 1), IntLiteral(1)),(Token(TokenType.FLOAT_LITERAL, 1.2), FloatLiteral(1.2)),(Token(TokenType.STR_LITERAL, 'abc'), StrLiteral('abc')),(Token(TokenType.NULL), NullLiteral())]

@pytest.mark.parametrize("literal_token,ast", token_ast_pair_literals)
@pytest.mark.parametrize("func", unary_parse_funcs)
def test_parse_unary_int_literal(func, literal_token, ast):
    """-1"""

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
