
"""Unit tests for tokenization of keywords and operators"""


from typing import Dict
from io import StringIO
import pytest

from char_reader import TextIOReader
from lexer import Lexer
from token_type import TokenType
from my_token import Token
from keywords import KEYWORDS_TO_TOKEN_TYPE

from my_token_exceptions import *

special_chars_to_token_type : Dict[str, TokenType] = {
    '(' : TokenType.LEFT_BRACKET,
    ')' : TokenType.RIGHT_BRACKET,
    ';' : TokenType.SEMICOLON,
    ':'  :TokenType.COLON,
    '=' : TokenType.ASSIGNMENT,
    '==' : TokenType.EQUAL,
    '!=' : TokenType.INEQUAL,
    '<=' : TokenType.LESS_EQUAL,
    '>=' : TokenType.GREATER_EQUAL,
    '<' : TokenType.LESS,
    '>' : TokenType.GREATER,
    '.' : TokenType.DOT,
    '+' : TokenType.PLUS,
    "-" : TokenType.MINUS,
    "*" : TokenType.TIMES,
    "/" : TokenType.DIVIDE,
    "|" : TokenType.OR,
    "&" : TokenType.AND
}

test_examples = []
for kk, tt in KEYWORDS_TO_TOKEN_TYPE.items():
    test_examples.append((kk, Token(tt, None, (1, 1))))

for kk, tt in special_chars_to_token_type.items():
    test_examples.append((kk, Token(tt, None, (1, 1))))


@pytest.mark.parametrize("text,expected_token", test_examples)
def test_just_single_token(text, expected_token):
    """Parametrised test for each keyword, operator or special character"""
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == expected_token
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,len(text)+1))


@pytest.mark.parametrize("text,expected_token", test_examples)
def test_sht_r_position(text, expected_token : Token):
    """keyword, operator or special character but shifted right"""
    r = TextIOReader(StringIO(' ' + text))
    l = Lexer(r)
    expected_token1 = expected_token.copy()
    expected_token1.set_pos((1, 2))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token1
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,len(text)+2))

@pytest.mark.parametrize("text,expected_token", test_examples)
def test_sht_l_position(text, expected_token : Token):
    """keyword, operator or special character but shifted left"""
    r = TextIOReader(StringIO(text + ' '))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == expected_token
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,len(text)+2))

@pytest.mark.parametrize("text,expected_token", test_examples)
def test_after_newline_position(text, expected_token : Token):
    """keyword, operator or special character but after newline"""
    r = TextIOReader(StringIO('\n' + text))
    l = Lexer(r)
    expected_token.set_pos((2, 1))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token
    assert l.get_next_token() == Token(TokenType.EOT, position=(2,len(text)+1))

@pytest.mark.parametrize("text,expected_token", test_examples.copy())
def test_after_newline_sht_r_position(text, expected_token : Token):
    """keyword, operator or special character but after newline and shifted right"""
    r = TextIOReader(StringIO('\n ' + text))
    l = Lexer(r)
    expected_token.set_pos((2, 2))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token
    assert l.get_next_token() == Token(TokenType.EOT, position=(2,len(text)+2))

@pytest.mark.parametrize("text,expected_token", test_examples)
def test_after_newline_sht_r_double_position(text, expected_token : Token):
    """keyword, operator or special character but after newline and shifted right but doubled"""
    r = TextIOReader(StringIO('\n \n ' + text))
    l = Lexer(r)
    expected_token.set_pos((3, 2))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token
    assert l.get_next_token() == Token(TokenType.EOT, position=(3,len(text)+2))


def test_assign_with_eqaul():
    """Have to separated by some whitespace"""
    text = "= =="
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    expected_token_1 = Token(TokenType.ASSIGNMENT, position=(1,1))
    expected_token_2 = Token(TokenType.EQUAL, position=(1,3))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token_1
    assert l.get_next_token() == expected_token_2
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,5))

def test_equal_with_assign():
    """Dont have to be separated with whitespace"""
    text = "==="
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    expected_token_1 = Token(TokenType.EQUAL, position=(1,1))
    expected_token_2 = Token(TokenType.ASSIGNMENT, position=(1,3))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token_1
    assert l.get_next_token() == expected_token_2
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,4))

def test_plus_with_eqaul():
    """Dont have to be separated with whitespace"""
    text = "+="
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    expected_token_1 = Token(TokenType.PLUS, position=(1,1))
    expected_token_2 = Token(TokenType.ASSIGNMENT, position=(1,2))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token_1
    assert l.get_next_token() == expected_token_2
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,3))


def test_minus_with_eqaul():
    """Dont have to be separated with whitespace"""
    text = "-="
    r = TextIOReader(StringIO(text))
    l = Lexer(r)
    expected_token_1 = Token(TokenType.MINUS, position=(1,1))
    expected_token_2 = Token(TokenType.ASSIGNMENT, position=(1,2))
    assert l.curr_token is None
    assert l.get_next_token() == expected_token_1
    assert l.get_next_token() == expected_token_2
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,3))
