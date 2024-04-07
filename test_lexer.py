"""."""
from char_reader import StringReader
from lexer import Lexer
from token_type import TokenType
from my_token import MyToken

from my_token_exceptions import MyTokenException


def test_only_spaces():
    """."""
    text = 10 * ' '
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    for _ in range(10):
        my_token = l.get_next_token()
        assert my_token == MyToken(TokenType.END)


def test_string_literal_ala():
    """."""
    text = '\'ala\''
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == MyToken(TokenType.STR_LITERAL, 'ala')

def test_strin_literal_ala():
    """."""
    text = '\'ala\''
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == MyToken(TokenType.STR_LITERAL, 'ala')

def test_strin_literal_not_properly_ended():
    """."""
    text = '\'ala'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    try:
        l.get_next_token()
    except MyTokenException:
        pass


def test_keyword_null():
    """."""
    text = 'null'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    assert l.get_next_token() == MyToken(TokenType.NULL)


def test_int_literal_1():
    """."""
    text = '1'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)

def test_int_literal_2():
    """."""
    text = '2'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 2)


def test_int_literal_12():
    """."""
    text = '12'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 12)

def test_int_literal_123():
    """."""
    text = '123'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 123)

def test_float_literal_123_dot():
    """."""
    text = '123.'
    r = StringReader(text)
    l = Lexer(r)
    try:
        l.get_next_token()
    except MyTokenException:
        pass

def test_float_literal_123_dot_some_letters():
    """."""
    text = '123.abc'
    r = StringReader(text)
    l = Lexer(r)
    try:
        l.get_next_token()
    except MyTokenException:
        pass

def test_float_literal():
    """."""
    text = '123.123'
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 123.123) < 10**(-9)


def test_big_int_literal():
    """."""
    text = '99999999'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 99999999)

def test_to_big_int_literal():
    """."""
    text = '100000000'
    r = StringReader(text)
    l = Lexer(r)
    try:
        l.get_next_token()
    except MyTokenException:
        pass


def test_big_float_literal():
    """."""
    text = '99999999.0'
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 99999999) < 10**(-9)

def test_float_bigger_than_int_limit():
    """."""
    text = '100000000.0'
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 100000000) < 10**(-9)

def test_to_big_float_literal():
    """TODO"""



def test_basic_if_statement():
    """."""
    to_tokenise = """
    if 1 
    begin
        print('Hello');
    end
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IF)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)
    assert l.get_next_token() == MyToken(TokenType.BEGIN)
    assert l.get_next_token() == MyToken(TokenType.PRINT)
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, 'Hello')
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.END)
    assert l.get_next_token() == MyToken(TokenType.EOT)
