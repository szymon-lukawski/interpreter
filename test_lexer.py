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
