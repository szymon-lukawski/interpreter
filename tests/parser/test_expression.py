from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *


class TokenProvider(Lexer):
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
    assert True == 1


def test_null_literal():
    tokens = [Token(TokenType.NULL)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == NullLiteral
    assert result.value == None


def test_int_literal():
    tokens = [Token(TokenType.INT_LITERAL, 1)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == IntLiteral
    assert type(result.value) == int
    assert result.value == 1


def test_float_literal():
    tokens = [Token(TokenType.FLOAT_LITERAL, 1.5)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == FloatLiteral
    assert type(result.value) == float
    assert result.value == 1.5


def test_string_literal():
    tokens = [Token(TokenType.STR_LITERAL, "1")]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == StrLiteral
    assert type(result.value) == str
    assert result.value == "1"


def test_empty_string_literal():
    tokens = [Token(TokenType.STR_LITERAL, "")]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == StrLiteral
    assert type(result.value) == str
    assert result.value == ""


def test_literal_parsing_when_should_not_consume():
    tokens = [Token(TokenType.STR), Token(TokenType.BEGIN)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert result is None
    assert parser.lexer.curr_token == tokens[0]


def test_object_access_only_identifiers():
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
    assert type(result.nested_objects[0]) == Identifier
    assert result.nested_objects[0].name == "czlowiek"
    assert type(result.nested_objects[1]) == Identifier
    assert result.nested_objects[1].name == "adres"
    assert type(result.nested_objects[2]) == Identifier
    assert result.nested_objects[2].name == "kod"

    assert len(result.nested_objects) == 3


def test_nested_expression():
    pass


def test_parse_term_str_literal():
    tokens = [Token(TokenType.STR_LITERAL, "")]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == StrLiteral
    assert type(result.value) == str
    assert result.value == ""


def test_parse_term_obj_access():
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
    assert type(result.nested_objects[0]) == Identifier
    assert result.nested_objects[0].name == "czlowiek"
    assert type(result.nested_objects[1]) == Identifier
    assert result.nested_objects[1].name == "adres"
    assert type(result.nested_objects[2]) == Identifier
    assert result.nested_objects[2].name == "kod"

    assert len(result.nested_objects) == 3


def test_unary_expression():
    tokens = [Token(TokenType.INT_LITERAL, 1)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_literal()
    assert type(result) == IntLiteral
    assert type(result.value) == int
    assert result.value == 1


def test_unary_float_literal():
    tokens = [Token(TokenType.MINUS), Token(TokenType.FLOAT_LITERAL, 1.5)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_unary_expr()
    assert type(result) == UnaryExpr
    assert type(result.negated) == FloatLiteral
    assert type(result.negated.value) == float
    assert result.negated.value == 1.5


def test_unary_float_literal_without_minus():
    tokens = [Token(TokenType.FLOAT_LITERAL, 1.5)]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_unary_expr()
    assert type(result) == FloatLiteral
    assert type(result.value) == float
    assert result.value == 1.5


def test_multi_expression():
    tokens = [
        Token(TokenType.IDENTIFIER, "suma"),
        Token(TokenType.DIVIDE),
        Token(TokenType.INT_LITERAL, 2),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_multi_expr()
    assert type(result) == MultiExpr
    assert len(result.children) == 3
    assert type(result.children[0]) == Identifier
    assert result.children[0].name == "suma"
    assert result.children[1] == TokenType.DIVIDE
    assert type(result.children[2]) == IntLiteral
    assert result.children[2].value == 2


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
    assert len(result.children) == 7
    assert type(result.children[0]) == FloatLiteral
    assert result.children[1] == TokenType.TIMES
    assert type(result.children[2]) == Identifier
    assert result.children[3] == TokenType.TIMES
    assert type(result.children[4]) == Identifier
    assert result.children[5] == TokenType.DIVIDE
    assert type(result.children[6]) == IntLiteral
    assert result.children[2].name == "r"
    assert result.children[4].name == "r"
    assert result.children[6].value == 4


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
    assert len(result.children) == 3
    assert type(result.children[0]) == FloatLiteral
    assert result.children[1] == TokenType.TIMES
    assert type(result.children[2]) == UnaryExpr
    assert type(result.children[2].negated) == Identifier
    assert result.children[2].negated.name == 'r'


def test_add_expr():
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT_LITERAL, 3.14),
        Token(TokenType.TIMES),
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "r"),
        Token(TokenType.MINUS), # <-----
        Token(TokenType.MINUS),
        Token(TokenType.IDENTIFIER, "q"),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_add_expr()
    assert type(result) == AddExpr
    assert len(result.children) == 3
    assert type(result.children[0]) == MultiExpr

    assert type(result.children[0].children[0]) == UnaryExpr
    assert type(result.children[0].children[0].negated) == FloatLiteral
    assert result.children[0].children[0].negated.value == 3.14

    assert result.children[0].children[1] == TokenType.TIMES

    assert type(result.children[0].children[2]) == UnaryExpr
    assert type(result.children[0].children[2].negated) == Identifier
    assert result.children[0].children[2].negated.name == 'r'

    assert result.children[1] == TokenType.MINUS

    assert type(result.children[2]) == UnaryExpr
    assert type(result.children[2].negated) == Identifier
    assert result.children[2].negated.name == 'q'