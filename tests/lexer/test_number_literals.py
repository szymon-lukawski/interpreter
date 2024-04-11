"""."""

import pytest
from char_reader import StringReader
from lexer import Lexer
from token_type import TokenType
from my_token import MyToken

from my_token_exceptions import (
    FloatLiteralTooBig,
    IntLiteralTooBig,
    InvalidCharsInNumberLiteral,
    PrecidingZerosError,
)


def test_only_spaces():
    """EOT token does not change position after char source is dry"""
    text = 10 * " "
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    for _ in range(10):
        my_token = l.get_next_token()
        assert my_token == MyToken(TokenType.EOT, position=(1, 11))


def test_int_literal_0():
    """."""
    text = "0"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 0, position=(1, 1))


def test_int_literal_00():
    """."""
    text = "00"
    r = StringReader(text)
    l = Lexer(r)
    with pytest.raises(PrecidingZerosError):
        l.get_next_token()


def test_int_literal_1():
    """."""
    text = "1"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1, position=(1, 1))


def test_int_literal_2():
    """."""
    text = "2"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 2, position=(1, 1))


def test_int_literal_12():
    """."""
    text = "12"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 12, position=(1, 1))


def test_int_literal_123():
    """."""
    text = "123"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 123, position=(1, 1))


def test_float_literal_123_dot():
    """."""
    text = "123."
    r = StringReader(text)
    l = Lexer(r)
    with pytest.raises(InvalidCharsInNumberLiteral):
        l.get_next_token()


def test_float_literal_123_dot_some_letters():
    """."""
    text = "123.abc"
    r = StringReader(text)
    l = Lexer(r)
    with pytest.raises(InvalidCharsInNumberLiteral):
        l.get_next_token()


def test_float_literal_123_dot_0_some_letters():
    """."""
    text = "123.0abc"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(
        TokenType.FLOAT_LITERAL, 123.0, position=(1, 1)
    )
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "abc", position=(1, 6))
    assert l.get_next_token() == MyToken(TokenType.EOT, position=(1, 9))


def test_float_literal():
    """."""
    text = "123.123"
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 123.123) < 10 ** (-9)


def test_big_int_literal():
    """."""
    text = "99999999"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(
        TokenType.INT_LITERAL, 99999999, position=(1, 1)
    )


def test_to_big_int_literal():
    """."""
    text = "100000000"
    r = StringReader(text)
    l = Lexer(r)
    with pytest.raises(IntLiteralTooBig):
        l.get_next_token()


def test_big_float_literal():
    """."""
    text = "99999999.0"
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 99999999) < 10 ** (-9)


def test_float_bigger_than_int_limit():
    """."""
    text = "100000000.0"
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 100000000) < 10 ** (-9)


def test_to_big_float_literal_more_than_20_chars():
    """."""
    text = "1" + "0"*19 + ".0"
    r = StringReader(text)
    l = Lexer(r)
    with pytest.raises(FloatLiteralTooBig):
        l.get_next_token()

