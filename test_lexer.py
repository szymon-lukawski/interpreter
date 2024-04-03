from char_reader import Lexer, StringReader, TokenType, Token



def test_only_spaces():
    text = 10 * ' '
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    for _ in range(10):
        token = l.get_next_token()
        assert token == Token(TokenType.END)


def test_string_literal_Ala():
    text = '\'Ala\''
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    token = l.get_next_token()
    assert token == Token(TokenType.STR_LITERAL, 'Ala')

def test_strin_literal_Ala():
    text = '\'Ala\''
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    token = l.get_next_token()
    assert token == Token(TokenType.STR_LITERAL, 'Ala')




def test_keyword_null():
    text = 'null'
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    assert l.get_next_token() == Token(TokenType.NULL)
