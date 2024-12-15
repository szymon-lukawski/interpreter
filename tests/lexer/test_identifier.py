"""Module for testing Lexer's identifier"""

import pytest

from lexer.char_reader import TextIOReader
from lexer.lexer import Lexer
from lexer.token_type import TokenType
from lexer.my_token import Token
from io import StringIO, TextIOBase

from lexer.my_token_exceptions import *


def test_valid_one_letter_identifier():
    """Basic identifier"""
    text = "a"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", (1, 1))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 2))

def test_identifier_can_not_start_with_underscore_char():
    """ _ala is not a valid identifier"""
    text = "_ala"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(IdentifierCanNotStartWithUnderscore) as e_info:
        l.get_next_token()
    assert str(e_info.value) == """IdentifierCanNotStartWithUnderscore: row: 1, column: 1, While building new token first char was '_'. Identifiers can not start with '_'!"""

def test_identifiers_can_have_underscores_if_it_is_not_first():
    """a_____"""
    text = "a_____"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a_____", (1, 1))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 7))

def test_int_just_before_identifier_returns_both_tokens():
    """1a"""
    # TODO is this the intended behaviour?
    text = "1a"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, (1, 1))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'a', position=(1, 2))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 3))

def test_float_just_before_identifier_returns_both_tokens():
    """3.14a"""
    # TODO is this the intended behaviour?
    text = "3.14a"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.FLOAT_LITERAL, 3.14, (1, 1))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'a', position=(1, 5))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 6))

def test_null_just_before_identifier_returns_identifier_with_null_in_its_name():
    """nulla"""
    text = "nulla"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'nulla', position=(1, 1))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 6))

def test_null_space_identifier_returns_identifier_both_null_and_identifier():
    """null a"""
    text = "null a"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.NULL, position=(1, 1))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'a', position=(1, 6))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 7))

def test_valid_separators_of_identifiers():
    """a b\nc@\nd''e;f:g=h,i.j(k)l*m/n+o-p<q<=r==s!=t>=u>v&w|x"""
    text = "a b\nc@\nd''e;f:g=h,i.j(k)l*m/n+o-p<q<=r==s!=t>=u>v&w|x"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'a', position=(1, 1))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'b', position=(1, 3))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'c', position=(2, 1))
    assert l.get_next_token() == Token(TokenType.COMMENT, '', position=(2, 2))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'd', position=(3, 1))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, '', position=(3, 2))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'e', position=(3, 4))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(3, 5))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'f', position=(3, 6))
    assert l.get_next_token() == Token(TokenType.COLON, position=(3, 7))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'g', position=(3, 8))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(3, 9))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'h', position=(3, 10))
    assert l.get_next_token() == Token(TokenType.COMMA, position=(3, 11))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'i', position=(3, 12))
    assert l.get_next_token() == Token(TokenType.DOT, position=(3, 13))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'j', position=(3, 14))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(3, 15))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'k', position=(3, 16))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(3, 17))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'l', position=(3, 18))
    assert l.get_next_token() == Token(TokenType.TIMES, position=(3, 19))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'm', position=(3, 20))
    assert l.get_next_token() == Token(TokenType.DIVIDE, position=(3, 21))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'n', position=(3, 22))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(3, 23))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'o', position=(3, 24))
    assert l.get_next_token() == Token(TokenType.MINUS, position=(3, 25))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'p', position=(3, 26))
    assert l.get_next_token() == Token(TokenType.LESS, position=(3, 27))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'q', position=(3, 28))
    assert l.get_next_token() == Token(TokenType.LESS_EQUAL, position=(3, 29))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'r', position=(3, 31))
    assert l.get_next_token() == Token(TokenType.EQUAL, position=(3, 32))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 's', position=(3, 34))
    assert l.get_next_token() == Token(TokenType.INEQUAL, position=(3, 35))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 't', position=(3, 37))
    assert l.get_next_token() == Token(TokenType.GREATER_EQUAL, position=(3, 38))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'u', position=(3, 40))
    assert l.get_next_token() == Token(TokenType.GREATER, position=(3, 41))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'v', position=(3, 42))
    assert l.get_next_token() == Token(TokenType.AND, position=(3, 43))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'w', position=(3, 44))
    assert l.get_next_token() == Token(TokenType.OR, position=(3, 45))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'x', position=(3, 46))
    assert l.get_next_token() == Token(TokenType.EOT, position=(3, 47))

def test_escape_char_can_not_be_in_body_of_identifier():
    """a\\n"""
    text = "a\\n"
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(InvalidCharInIdentifier):
        l.get_next_token()

def test_max_long_identifiers():
    """100 char long identifier is max allowed by default"""
    text = "a" * 100
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a" * 100, (1, 1))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 101))


def test_too_long_identifiers():
    """101 char long identifier is not allowed by default"""
    text = "a" * 101
    text_io = StringIO(text)
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(IdentifierTooLong):
        l.get_next_token()


def test_infinite_identifier_raises_an_error():
    """aaaa...a...aaaa..."""
    class InfiniteFile(TextIOBase):
        """Mocks an inifite file with repeating pattern"""
        def __init__(self, rep_string : str) -> None:
            self._rep_str = rep_string

        def read(self, size=-1):
            if size == -1:
                return self._rep_str * 5000
            return self._rep_str * size

        def readline(self):
            return '1\n'

        def readlines(self):
            while True:
                yield '1\n'

        def __iter__(self):
            return self

        def __next__(self):
            return self._rep_str
        
    text_io = InfiniteFile('a')
    r = TextIOReader(text_io)
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(IdentifierTooLong):
        l.get_next_token()