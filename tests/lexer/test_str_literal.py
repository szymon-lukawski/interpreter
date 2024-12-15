"""Module for testing Lexer's string literal"""

from io import StringIO
from typing import List, Tuple
import pytest
from lexer.char_reader import TextIOReader
from lexer.lexer import Lexer
from lexer.token_type import TokenType
from lexer.my_token import Token

from lexer.my_token_exceptions import (
    StringLiteralNotEnded,
    EscapingWrongChar,
    EscapingEOT,
    UseOfQuotationMarksIsInvalid,
)


def test_string_literal_ala():
    """Basic string literal"""
    text = "'ala'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == Token(TokenType.STR_LITERAL, "ala", (1, 1))


def test_quotation_marks_do_not_mark_limits_of_a_str_literal():
    """Use of quotation marks instead of apostrophe in str literal"""
    text = '"ala"'
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(UseOfQuotationMarksIsInvalid):
        l.get_next_token()


def test_quotation_marks_inside_str_literal():
    """'She said "I like cats.".'"""
    text = "'She said \"I like cats.\".'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, 'She said "I like cats.".', (1, 1))

def test_pos_of_str_literal_is_of_its_initial_apostrophe():
    """\n'ala'"""
    text = "\n'ala'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == Token(TokenType.STR_LITERAL, "ala", (2, 1))


def test_string_literal_not_properly_ended():
    """String literal should be ended with apostrophe"""
    text = "'ala"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(StringLiteralNotEnded):
        l.get_next_token()


def test_string_literal_not_properly_ended_end_backslash():
    """String literal should be ended with apostrophe"""
    text = "'ala\\"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(EscapingEOT):
        l.get_next_token()


def test_missing_innitial_apostrophe():
    """ala'"""
    text = "ala'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ala", position=(1, 1))
    with pytest.raises(StringLiteralNotEnded) as exinfo:
        l.get_next_token()
    assert "row: 1, column: 5" in str(exinfo.value)


def test_str_literal_has_to_be_in_one_line():
    """Newline is two chars: `\\` and `n` but not \n"""
    text = "'\n'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(StringLiteralNotEnded) as exinfo:
        l.get_next_token()
    assert "row: 1, column: 2" in str(exinfo.value)


def test_escaping_newline_is_not_allowed():
    """Escaping newline is not allowed"""
    text = "'\\\n'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(EscapingWrongChar) as exinfo:
        l.get_next_token()
    assert "row: 1, column: 3" in str(exinfo.value)


escape_chars_chars_pair: List[Tuple[str, str]] = [
    ("\\n", "\n"),
    ("\\\\", "\\"),
    ("\\t", "\t"),
    ("\\'", "'"),
]


@pytest.mark.parametrize("text,literal_value", escape_chars_chars_pair)
def test_valid_escape_chars(text, literal_value):
    """This is valid newline in string literal"""
    text = f"'{text}'"
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, literal_value, (1, 1))
