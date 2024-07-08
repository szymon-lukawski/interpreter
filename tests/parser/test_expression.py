"""test for expression part of grammar"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck


import pytest

from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *


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


def test_null_literal():
    """null"""
    tokens = [Token(TokenType.NULL)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == NullLiteral
    assert result.value is None


def test_int_literal():
    """1"""
    tokens = [Token(TokenType.INT_LITERAL, 1)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == IntLiteral
    assert type(result.value) == int
    assert result.value == 1


def test_float_literal():
    """1.5"""
    tokens = [Token(TokenType.FLOAT_LITERAL, 1.5)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == FloatLiteral
    assert type(result.value) == float
    assert result.value == 1.5


def test_string_literal():
    """'1'"""
    tokens = [Token(TokenType.STR_LITERAL, "1")]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == StrLiteral
    assert type(result.value) == str
    assert result.value == "1"


def test_empty_string_literal():
    """''"""
    tokens = [Token(TokenType.STR_LITERAL, "")]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == StrLiteral
    assert type(result.value) == str
    assert result.value == ""


def test_literal_parsing_when_should_not_consume():
    """str begin"""
    tokens = [Token(TokenType.STR), Token(TokenType.BEGIN)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert result is None
    assert parser.lexer.curr_token == tokens[0]


def test_object_access_only_identifiers():
    """czlowiek.adres.kod"""
    tokens = [
        Token(TokenType.IDENTIFIER, "czlowiek"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "adres"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "kod"),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_object_access()
    assert type(result) == ObjectAccess
    assert result.name_chain == ["czlowiek", "adres", "kod"]


def test_nested_expression():
    pass


def test_parse_term_str_literal():
    """''"""
    tokens = [Token(TokenType.STR_LITERAL, "")]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == StrLiteral
    assert type(result.value) == str
    assert result.value == ""


def test_parse_term_obj_access():
    """czlowiek.adres.kod"""
    tokens = [
        Token(TokenType.IDENTIFIER, "czlowiek"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "adres"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "kod"),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_term()
    assert type(result) == ObjectAccess
    assert result.name_chain == ["czlowiek", "adres", "kod"]


def test_unary_expression():
    """1"""
    tokens = [Token(TokenType.INT_LITERAL, 1)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == IntLiteral
    assert type(result.value) == int
    assert result.value == 1


def test_unary_float_literal():
    """-1.5"""
    tokens = [Token(TokenType.MINUS), Token(TokenType.FLOAT_LITERAL, 1.5)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_unary_expr()
    assert type(result) == UnaryExpr
    assert type(result.negated) == FloatLiteral
    assert type(result.negated.value) == float
    assert result.negated.value == 1.5


def test_unary_float_literal_without_minus():
    """1.5"""
    tokens = [Token(TokenType.FLOAT_LITERAL, 1.5)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_unary_expr()
    assert type(result) == FloatLiteral
    assert type(result.value) == float
    assert result.value == 1.5


def test_multi_expression():
    """suma / 2"""
    tokens = [
        Token(TokenType.IDENTIFIER, "suma"),
        Token(TokenType.DIVIDE),
        Token(TokenType.INT_LITERAL, 2),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_multi_expr()
    assert type(result) == MultiExpr
    assert len(result.children) == 2
    assert len(result.operations) == 1
    assert result.operations[0] == TokenType.DIVIDE
    assert type(result.children[0]) == ObjectAccess
    assert result.children[0].name_chain == ["suma"]
    assert type(result.children[1]) == IntLiteral
    assert result.children[1].value == 2


def test_bigger_multi_expression_with_times_and_divide():
    """Area of quater of a circle"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.TIMES),
        Token(TokenType.IDENTIFIER, "r"),
        Token(TokenType.TIMES),
        Token(TokenType.IDENTIFIER, "r"),
        Token(TokenType.DIVIDE),
        Token(TokenType.INT_LITERAL, 4),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_multi_expr()
    assert type(result) == MultiExpr
    assert len(result.children) == 4
    assert len(result.operations) == 3
    assert result.operations[0] == TokenType.TIMES
    assert result.operations[1] == TokenType.TIMES
    assert result.operations[2] == TokenType.DIVIDE
    assert type(result.children[0]) == FloatLiteral
    assert type(result.children[1]) == ObjectAccess
    assert type(result.children[2]) == ObjectAccess
    assert type(result.children[3]) == IntLiteral
    assert result.children[1].name_chain == ["r"]
    assert result.children[2].name_chain == ["r"]
    assert result.children[3].value == 4


def test_bigger_multi_expression_with_unary_expression():
    """Multiplicative_Expression without brackets. Natural priority of unary operation"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.TIMES),
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "r"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_multi_expr()
    assert type(result) == MultiExpr
    assert len(result.children) == 2
    assert len(result.operations) == 1
    assert result.operations[0] == TokenType.TIMES
    assert type(result.children[0]) == FloatLiteral
    assert type(result.children[1]) == UnaryExpr
    assert type(result.children[1].negated) == ObjectAccess
    assert result.children[1].negated.name_chain == ["r"]


def test_add_expr_minus():
    """-3.14 * - r - - q"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.TIMES),
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "r"),
        Token(TokenType.MINUS),  # <-----
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "q"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_add_expr()
    assert type(result) == AddExpr
    assert len(result.children) == 2
    assert type(result.children[0]) == MultiExpr
    assert len(result.children[0].operations) == 1
    assert result.children[0].operations[0] == TokenType.TIMES
    assert type(result.children[0].children[0]) == UnaryExpr
    assert type(result.children[0].children[0].negated) == FloatLiteral
    assert result.children[0].children[0].negated.value == 3.14

    assert type(result.children[0].children[1]) == UnaryExpr
    assert type(result.children[0].children[1].negated) == ObjectAccess
    assert result.children[0].children[1].negated.name_chain == ["r"]

    assert len(result.operations) == 1
    assert result.operations[0] == TokenType.MINUS

    assert type(result.children[1]) == UnaryExpr
    assert type(result.children[1].negated) == ObjectAccess
    assert result.children[1].negated.name_chain == ["q"]


def test_add_expr_plus():
    """- 3.14 * - r + - q"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.TIMES),
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "r"),
        Token(TokenType.PLUS),  # <-----
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "q"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_add_expr()
    assert type(result) == AddExpr
    assert len(result.children) == 2
    assert type(result.children[0]) == MultiExpr
    assert len(result.children[0].operations) == 1
    assert result.children[0].operations[0] == TokenType.TIMES
    assert type(result.children[0].children[0]) == UnaryExpr
    assert type(result.children[0].children[0].negated) == FloatLiteral
    assert result.children[0].children[0].negated.value == 3.14

    assert type(result.children[0].children[1]) == UnaryExpr
    assert type(result.children[0].children[1].negated) == ObjectAccess
    assert result.children[0].children[1].negated.name_chain == ["r"]

    assert len(result.operations) == 1
    assert result.operations[0] == TokenType.PLUS

    assert type(result.children[1]) == UnaryExpr
    assert type(result.children[1].negated) == ObjectAccess
    assert result.children[1].negated.name_chain == ["q"]


rel_operators = [
    TokenType.LESS,
    TokenType.LESS_EQUAL,
    TokenType.EQUAL,
    TokenType.INEQUAL,
    TokenType.GREATER,
    TokenType.GREATER_EQUAL,
]


@pytest.mark.parametrize("operator", rel_operators)
def test_rel_expr(operator):
    """3.14 {operator} r"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(operator),
        Token(TokenType.IDENTIFIER, "r"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_rel_expr()
    assert type(result) == RelationExpr
    assert type(result.left) == FloatLiteral
    assert result.left.value == 3.14
    assert result.operator == operator
    assert type(result.right) == ObjectAccess
    assert result.right.name_chain == ["r"]


def test_and_expr_one_arg():
    """3.14"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.14),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_and_expr()
    assert type(result) == FloatLiteral
    assert result.value == 3.14


def test_and_expr_2_arg():
    """3.14 & 5"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.AND),
        Token(TokenType.INT_LITERAL, 5),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_and_expr()
    assert type(result) == AndExpr
    assert type(result.children[0]) == FloatLiteral
    assert type(result.children[1]) == IntLiteral
    assert result.children[0].value == 3.14
    assert result.children[1].value == 5


def test_and_expr_3_args():
    """3.14 & 5 & 'Ala'"""
    tokens = [
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.AND),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_and_expr()
    assert type(result) == AndExpr
    assert type(result.children[0]) == FloatLiteral
    assert type(result.children[1]) == IntLiteral
    assert type(result.children[2]) == StrLiteral
    assert result.children[0].value == 3.14
    assert result.children[1].value == 5
    assert result.children[2].value == "Ala"


def test_and_expr_rel_args():
    """- 3.14 < 'Ala1' * 5 + 4 & 5 & 'Ala2'"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.LESS),
        Token(TokenType.STR_LITERAL, "Ala1"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.AND),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala2"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_and_expr()
    assert type(result) == AndExpr
    assert type(result.children[0]) == RelationExpr
    assert type(result.children[1]) == IntLiteral
    assert type(result.children[2]) == StrLiteral

    assert type(result.children[0].left) == UnaryExpr
    assert type(result.children[0].left.negated) == FloatLiteral
    assert result.children[0].left.negated.value == 3.14

    assert type(result.children[0].right) == AddExpr
    assert type(result.children[0].right.children[0]) == MultiExpr
    assert type(result.children[0].right.children[0].children[0]) == StrLiteral
    assert type(result.children[0].right.children[0].children[1]) == IntLiteral
    assert result.children[0].right.children[0].children[0].value == "Ala1"
    assert result.children[0].right.children[0].children[1].value == 5
    assert type(result.children[0].right.children[1]) == IntLiteral
    assert result.children[0].right.children[1].value == 4

    assert result.children[1].value == 5
    assert result.children[2].value == "Ala2"


def test_and_expr_rel_args_order_does_not_matter():
    """5 & - 3.14 < 'Ala1' * 5 + 4 & 'Ala2'"""
    tokens = [
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.LESS),
        Token(TokenType.STR_LITERAL, "Ala1"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala2"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_and_expr()
    assert type(result) == AndExpr
    assert type(result.children[1]) == RelationExpr
    assert type(result.children[0]) == IntLiteral
    assert type(result.children[2]) == StrLiteral

    assert type(result.children[1].left) == UnaryExpr
    assert type(result.children[1].left.negated) == FloatLiteral
    assert result.children[1].left.negated.value == 3.14

    assert type(result.children[1].right) == AddExpr
    assert type(result.children[1].right.children[0]) == MultiExpr
    assert type(result.children[1].right.children[0].children[0]) == StrLiteral
    assert type(result.children[1].right.children[0].children[1]) == IntLiteral
    assert result.children[1].right.children[0].children[0].value == "Ala1"
    assert result.children[1].right.children[0].children[1].value == 5
    assert type(result.children[1].right.children[1]) == IntLiteral
    assert result.children[1].right.children[1].value == 4

    assert result.children[0].value == 5
    assert result.children[2].value == "Ala2"


def test_or_expr_2_args():
    """5 & - 3.14 < 'Ala1' * 5 + 4 & 'Ala2' | 1"""
    tokens = [
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.LESS),
        Token(TokenType.STR_LITERAL, "Ala1"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala2"),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 1),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_or_expr()
    assert type(result) == OrExpr
    assert type(result.children[0].children[1]) == RelationExpr
    assert type(result.children[0].children[0]) == IntLiteral
    assert type(result.children[0].children[2]) == StrLiteral

    assert type(result.children[0].children[1].left) == UnaryExpr
    assert type(result.children[0].children[1].left.negated) == FloatLiteral
    assert result.children[0].children[1].left.negated.value == 3.14

    assert type(result.children[0].children[1].right) == AddExpr
    assert type(result.children[0].children[1].right.children[0]) == MultiExpr
    assert (
        type(result.children[0].children[1].right.children[0].children[0]) == StrLiteral
    )
    assert (
        type(result.children[0].children[1].right.children[0].children[1]) == IntLiteral
    )
    assert result.children[0].children[1].right.children[0].children[0].value == "Ala1"
    assert result.children[0].children[1].right.children[0].children[1].value == 5
    assert type(result.children[0].children[1].right.children[1]) == IntLiteral
    assert result.children[0].children[1].right.children[1].value == 4

    assert result.children[0].children[0].value == 5
    assert result.children[0].children[2].value == "Ala2"

    assert len(result.children) == 2
    assert type(result.children[1]) == IntLiteral
    assert result.children[1].value == 1


def test_or_expr_2_args_switched_order():
    """1 | 5 & - 3.14 < 'Ala1' * 5 + 4 & 'Ala2'"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.LESS),
        Token(TokenType.STR_LITERAL, "Ala1"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala2"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_or_expr()
    assert type(result) == OrExpr
    assert type(result.children[1].children[1]) == RelationExpr
    assert type(result.children[1].children[0]) == IntLiteral
    assert type(result.children[1].children[2]) == StrLiteral

    assert type(result.children[1].children[1].left) == UnaryExpr
    assert type(result.children[1].children[1].left.negated) == FloatLiteral
    assert result.children[1].children[1].left.negated.value == 3.14

    assert type(result.children[1].children[1].right) == AddExpr
    assert type(result.children[1].children[1].right.children[0]) == MultiExpr
    assert (
        type(result.children[1].children[1].right.children[0].children[0]) == StrLiteral
    )
    assert (
        type(result.children[1].children[1].right.children[0].children[1]) == IntLiteral
    )
    assert result.children[1].children[1].right.children[0].children[0].value == "Ala1"
    assert result.children[1].children[1].right.children[0].children[1].value == 5
    assert type(result.children[1].children[1].right.children[1]) == IntLiteral
    assert result.children[1].children[1].right.children[1].value == 4

    assert result.children[1].children[0].value == 5
    assert result.children[1].children[2].value == "Ala2"

    assert len(result.children) == 2
    assert type(result.children[0]) == IntLiteral
    assert result.children[0].value == 1


def test_or_expr_3_args():
    """1 | 0 | 5 & - 3.14 < 'Ala1' * 5 + 4 & 'Ala2'"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 0),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.LESS),
        Token(TokenType.STR_LITERAL, "Ala1"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala2"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_or_expr()
    assert type(result) == OrExpr
    assert type(result.children[2].children[1]) == RelationExpr
    assert type(result.children[2].children[0]) == IntLiteral
    assert type(result.children[2].children[2]) == StrLiteral

    assert type(result.children[2].children[1].left) == UnaryExpr
    assert type(result.children[2].children[1].left.negated) == FloatLiteral
    assert result.children[2].children[1].left.negated.value == 3.14

    assert type(result.children[2].children[1].right) == AddExpr
    assert type(result.children[2].children[1].right.children[0]) == MultiExpr
    assert (
        type(result.children[2].children[1].right.children[0].children[0]) == StrLiteral
    )
    assert (
        type(result.children[2].children[1].right.children[0].children[1]) == IntLiteral
    )
    assert result.children[2].children[1].right.children[0].children[0].value == "Ala1"
    assert result.children[2].children[1].right.children[0].children[1].value == 5
    assert type(result.children[2].children[1].right.children[1]) == IntLiteral
    assert result.children[2].children[1].right.children[1].value == 4

    assert result.children[2].children[0].value == 5
    assert result.children[2].children[2].value == "Ala2"

    assert len(result.children) == 3
    assert type(result.children[0]) == IntLiteral
    assert result.children[0].value == 1
    assert type(result.children[1]) == IntLiteral
    assert result.children[1].value == 0


def test_or_expr_3_args_switched():
    """1 | 5 & - 3.14 < 'Ala1' * 5 + 4 & 'Ala2' | 0"""
    tokens = [
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.AND),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.LESS),
        Token(TokenType.STR_LITERAL, "Ala1"),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.AND),
        Token(TokenType.STR_LITERAL, "Ala2"),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 0),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_logical_or_expr()
    assert type(result) == OrExpr
    assert type(result.children[1].children[1]) == RelationExpr
    assert type(result.children[1].children[0]) == IntLiteral
    assert type(result.children[1].children[2]) == StrLiteral

    assert type(result.children[1].children[1].left) == UnaryExpr
    assert type(result.children[1].children[1].left.negated) == FloatLiteral
    assert result.children[1].children[1].left.negated.value == 3.14

    assert type(result.children[1].children[1].right) == AddExpr
    assert type(result.children[1].children[1].right.children[0]) == MultiExpr
    assert (
        type(result.children[1].children[1].right.children[0].children[0]) == StrLiteral
    )
    assert (
        type(result.children[1].children[1].right.children[0].children[1]) == IntLiteral
    )
    assert result.children[1].children[1].right.children[0].children[0].value == "Ala1"
    assert result.children[1].children[1].right.children[0].children[1].value == 5
    assert type(result.children[1].children[1].right.children[1]) == IntLiteral
    assert result.children[1].children[1].right.children[1].value == 4

    assert result.children[1].children[0].value == 5
    assert result.children[1].children[2].value == "Ala2"

    assert len(result.children) == 3
    assert type(result.children[0]) == IntLiteral
    assert result.children[0].value == 1
    assert type(result.children[2]) == IntLiteral
    assert result.children[2].value == 0


parse__expr_funcs = [
    Parser._parse_term,
    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize("parse_func", parse__expr_funcs)
def test_bracket_parse_funcs_hierarchy(parse_func):
    """(1)"""
    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parse_func(parser)
    assert type(result) == IntLiteral
    assert result.value == 1


@pytest.mark.parametrize("parse_func", parse__expr_funcs)
def test_bracket_parse_funcs_hierarchy_minus_1(parse_func):
    """(-1)"""
    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parse_func(parser)
    assert type(result) == UnaryExpr
    assert type(result.negated) == IntLiteral
    assert result.negated.value == 1


unary_up_funcs = [
    Parser._parse_unary_expr,
    Parser._parse_multi_expr,
    Parser._parse_add_expr,
    Parser._parse_rel_expr,
    Parser._parse_logical_and_expr,
    Parser._parse_logical_or_expr,
    Parser._parse_expr,
]


@pytest.mark.parametrize("parse_func", unary_up_funcs)
def test_bracket_minus_minus_1(parse_func):
    """-(-1)"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parse_func(parser)
    assert type(result) == UnaryExpr
    assert type(result.negated) == UnaryExpr
    assert type(result.negated.negated) == IntLiteral
    assert result.negated.negated.value == 1


@pytest.mark.parametrize("parse_func", unary_up_funcs)
def test_bracket_minus_minus_minus_1(parse_func):
    """-(-(-1))"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.MINUS),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.RIGHT_BRACKET),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parse_func(parser)
    assert type(result) == UnaryExpr
    assert type(result.negated) == UnaryExpr
    assert type(result.negated.negated) == UnaryExpr
    assert type(result.negated.negated.negated) == IntLiteral
    assert result.negated.negated.negated.value == 1


@pytest.mark.parametrize("parse_func", unary_up_funcs)
def test_bracket_multiply_before_unary(parse_func):
    """-(1*2)"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.TIMES),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.RIGHT_BRACKET),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parse_func(parser)
    assert type(result) == UnaryExpr
    assert type(result.negated) == MultiExpr
    assert len(result.negated.children) == 2
    assert type(result.negated.children[0]) == IntLiteral
    assert result.negated.children[0].value == 1
    assert type(result.negated.children[1]) == IntLiteral
    assert result.negated.children[1].value == 2


@pytest.mark.parametrize("parse_func", unary_up_funcs)
def test_bracket_plus_before_multiply(parse_func):
    """-((1+2)*(3+4))"""
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.TIMES),
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 4),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.RIGHT_BRACKET),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parse_func(parser)
    assert type(result) == UnaryExpr
    assert type(result.negated) == MultiExpr
    assert len(result.negated.children) == 2
    assert type(result.negated.children[0]) == AddExpr
    assert len(result.negated.children[0].children) == 2
    assert type(result.negated.children[0].children[0]) == IntLiteral
    assert type(result.negated.children[0].children[1]) == IntLiteral
    assert result.negated.children[0].children[0].value == 1
    assert result.negated.children[0].children[1].value == 2
    assert type(result.negated.children[1]) == AddExpr
    assert len(result.negated.children[1].children) == 2
    assert type(result.negated.children[1].children[0]) == IntLiteral
    assert type(result.negated.children[1].children[1]) == IntLiteral
    assert result.negated.children[1].children[0].value == 3
    assert result.negated.children[1].children[1].value == 4


def test_bracket_rel_before_plus():
    """(1 < 2)+3"""
    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.LESS),
        Token(TokenType.INT_LITERAL, 2),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.PLUS),
        Token(TokenType.INT_LITERAL, 3),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_expr()
    assert type(result) == AddExpr
    assert len(result.children) == 2
    assert type(result.children[0]) == RelationExpr
    assert type(result.children[0].left) == IntLiteral
    assert result.children[0].left.value == 1
    assert type(result.children[0].right) == IntLiteral
    assert result.children[0].right.value == 2
    assert type(result.children[1]) == IntLiteral
    assert result.children[1].value == 3


def test_bracket_and_before_rel():
    """(1 & 0) < 3"""
    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.AND),
        Token(TokenType.INT_LITERAL, 0),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.LESS),
        Token(TokenType.INT_LITERAL, 3),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_expr()
    assert type(result) == RelationExpr
    assert type(result.left) == AndExpr
    assert len(result.left.children) == 2
    assert type(result.left.children[0]) == IntLiteral
    assert result.left.children[0].value == 1
    assert type(result.left.children[1]) == IntLiteral
    assert result.left.children[1].value == 0
    assert type(result.right) == IntLiteral
    assert result.right.value == 3


def test_bracket_or_before_and():
    """(1 or 0) & 3"""
    tokens = [
        Token(TokenType.LEFT_BRACKET),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.OR),
        Token(TokenType.INT_LITERAL, 0),
        Token(TokenType.RIGHT_BRACKET),
        Token(TokenType.AND),
        Token(TokenType.INT_LITERAL, 3),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_expr()
    assert type(result) == AndExpr
    assert len(result.children) == 2
    assert type(result.children[0]) == OrExpr
    assert len(result.children[0].children) == 2
    assert type(result.children[0].children[0]) == IntLiteral
    assert result.children[0].children[0].value == 1
    assert type(result.children[0].children[1]) == IntLiteral
    assert result.children[0].children[1].value == 0
    assert type(result.children[1]) == IntLiteral
    assert result.children[1].value == 3
