"""."""

import pytest
from io import StringIO
from lexer.char_reader import TextIOReader
from lexer.lexer import Lexer
from lexer.token_type import TokenType
from lexer.my_token import Token

from lexer.my_token_exceptions import (
    FloatLiteralTooBig,
    IntLiteralTooBig,
    DigitRequiredAfterDot,
    PrecidingZerosError,
)


def test_int_literal_0():
    """0"""
    text = "0"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0, position=(1, 1))


def test_int_literal_0_plus():
    """0+"""
    text = "0+"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0, position=(1, 1))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 2))

def test_int_literal_00():
    """00"""
    text = "00"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    with pytest.raises(PrecidingZerosError):
        l.get_next_token()

def test_starting_with_dot_normal():
    """.11"""
    text = ".11"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.DOT, position=(1,1))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 11, position=(1,2))

def test_starting_with_dot():
    """.01"""
    text = ".01"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.DOT, position=(1,1))
    with pytest.raises(PrecidingZerosError) as e_info:
        l.get_next_token()
    assert str(e_info.value) == "PrecidingZerosError: row: 1, column: 2, Putting additional zeros to the left of number literal is not allowed. 0 is ok, so is 0.1 so is 0.0001. 01 is  not. 00.1 is not"


def test_int_literal_1():
    """1"""
    text = "1"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 1))


def test_int_literal_2():
    """2"""
    text = "2"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2, position=(1, 1))

def test_01_raises_preceiding_zeros():
    """01"""
    text = "01"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(PrecidingZerosError):
        l.get_next_token()



def test_int_literal_12():
    """12"""
    text = "12"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 12, position=(1, 1))


def test_int_literal_123():
    """123"""
    text = "123"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 123, position=(1, 1))


def test_float_literal_123_dot():
    """123."""
    text = "123."
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    with pytest.raises(DigitRequiredAfterDot):
        l.get_next_token()


def test_float_literal_123_dot_some_letters():
    """123.abc"""
    text = "123.abc"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    with pytest.raises(DigitRequiredAfterDot):
        l.get_next_token()


def test_float_literal_123_dot_0_some_letters():
    """123.0abc"""
    text = "123.0abc"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(
        TokenType.FLOAT_LITERAL, 123.0, position=(1, 1)
    )
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "abc", position=(1, 6))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 9))


def test_float_literal():
    """123.123"""
    text = "123.123"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    t = l.get_next_token()
    assert t.get_type() == TokenType.FLOAT_LITERAL
    assert abs(t.get_value() - 123.123) < 10 ** (-9)


def test_big_int_literal():
    """99999999"""
    text = "99999999"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(
        TokenType.INT_LITERAL, 99999999, position=(1, 1)
    )


def test_too_big_int_literal():
    """100000000"""
    text = "100000000"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    with pytest.raises(IntLiteralTooBig):
        l.get_next_token()


def test_big_float_literal():
    """99999999.0"""
    text = "99999999.0"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    t = l.get_next_token()
    assert t.get_type() == TokenType.FLOAT_LITERAL
    assert abs(t.get_value() - 99999999) < 10 ** (-9)


def test_float_bigger_than_int_limit():
    """100000000.0"""
    text = "100000000.0"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    t = l.get_next_token()
    assert t.get_type() == TokenType.FLOAT_LITERAL
    assert abs(t.get_value() - 100000000) < 10 ** (-9)


def test_too_big_float_literal_more_than_20_chars():
    """10000000000000000000.0"""
    text = "1" + "0"*19 + ".0"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    with pytest.raises(FloatLiteralTooBig):
        l.get_next_token()

