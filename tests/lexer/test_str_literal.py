"""Module for testing Lexer's string literal"""

from io import StringIO
import pytest
from char_reader import StringReader
from lexer import Lexer
from token_type import TokenType
from my_token import Token

from my_token_exceptions import StringLiteralNotEnded, EscapingWrongChar


def test_string_literal_ala():
    """Basic string literal"""
    text = "'ala'"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == Token(TokenType.STR_LITERAL, "ala", (1, 1))


def test_string_literal_ala_in_newline():
    """Basic string literal"""
    text = "\n'ala'"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == Token(TokenType.STR_LITERAL, "ala", (2, 1))


def test_string_literal_not_properly_ended():
    """String literal should be ended with apostrophe"""
    text = "'ala"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(StringLiteralNotEnded):
        l.get_next_token()


def test_as_if_string_literal_not_properly_started():
    """."""
    text = "ala'"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ala", position=(1, 1))
    with pytest.raises(StringLiteralNotEnded) as exinfo:
        l.get_next_token()
    assert "row: 1, column: 5" in str(exinfo.value)


def test_newline_in_str_literal():
    """Newline is two chars: `\\` and `n` but not \n"""
    text = "'\n'"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(StringLiteralNotEnded) as exinfo:
        l.get_next_token()
    assert "row: 1, column: 2" in str(exinfo.value)


def test_escaped_newline_in_str_literal():
    """Escaping newline is not allowed"""
    text = "'\\\n'"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(EscapingWrongChar) as exinfo:
        l.get_next_token()
    assert "row: 1, column: 3" in str(exinfo.value)


def test_valid_newline_in_str_literal():
    """This is valid newline in string literal"""
    text = "'\\n'"
    r = StringReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "\n", (1, 1))
