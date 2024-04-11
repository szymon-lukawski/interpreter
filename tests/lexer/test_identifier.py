"""Module for testing Lexer's identifier"""

import pytest

from char_reader import StringReader
from lexer import Lexer
from token_type import TokenType
from my_token import MyToken

from my_token_exceptions import *


def test_a_identifier():
    """Basic identifier"""
    text = "a"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "a", (1, 1))
    assert l.get_next_token() == MyToken(TokenType.EOT, position=(1, 2))


def test_a_a_identifiers():
    """Separated by space"""
    text = "a a"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "a", (1, 1))
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "a", (1, 3))
    assert l.get_next_token() == MyToken(TokenType.EOT, position=(1, 4))


def test_max_long_identifiers():
    """100 char long identifier is max allowed by default"""
    text = "a" * 100
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "a" * 100, (1, 1))
    assert l.get_next_token() == MyToken(TokenType.EOT, position=(1, 101))


def test_too_long_identifiers():
    """101 char long identifier is not allowed by default"""
    text = "a" * 101
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    with pytest.raises(IdentifierTooLong):
        l.get_next_token()
