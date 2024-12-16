"""Testing lexer behaviour when code is mistaken."""

from io import StringIO
import pytest
from lexer.char_reader import TextIOReader
from lexer.lexer import Lexer
from lexer.token_type import TokenType
from lexer.my_token import Token

from lexer.my_token_exceptions import UnrecognisedStartOfToken


def test_prind():
    """Mistake in built in function print name: prind"""
    to_tokenise = """prind('Hello');"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "prind", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Hello", position=(1, 7))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 14))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 15))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 16))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 16))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1, 16))


def test_use_of_curly_brackets_instead_of_begin_and_end():
    """{a = 1;}"""
    to_tokenise = """{a = 1;}"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    with pytest.raises(UnrecognisedStartOfToken):
        l.get_next_token()


def test_python_like_while():
    """while 1:
    a = 1;"""
    to_tokenise = """while 1:\n    a = 1;"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.WHILE, position=(1, 1))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 8))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(2, 5))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(2, 7))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(2, 9))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(2, 10))


def test_cpp_like_incrementation():
    """i++"""
    to_tokenise = """i++"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "i", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 2))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 3))


def test_expr_missing_left_bracket():
    """a + 2+b)*3"""
    to_tokenise = """a + 2+b)*3"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 3))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 7))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 8))
    assert l.get_next_token() == Token(TokenType.TIMES, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3, position=(1, 10))


def test_expr_missing_right_bracket():
    """a + (2+b*3"""
    to_tokenise = """a + (2+b*3"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 3))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 8))
    assert l.get_next_token() == Token(TokenType.TIMES, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3, position=(1, 10))


def test_expr_empty_brackets():
    """a + ()2+b*3"""
    to_tokenise = """a + ()2+b*3"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 3))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 8))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 9))
    assert l.get_next_token() == Token(TokenType.TIMES, position=(1, 10))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3, position=(1, 11))


def test_forgot_to_remove_one_of_the_operators():
    """a -+ 1"""
    to_tokenise = """a -+ 1"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.MINUS, position=(1, 3))
    assert l.get_next_token() == Token(TokenType.PLUS, position=(1, 4))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 6))


def test_semicolons_instead_of_commas_as_separators_of_arguments():
    """sum(1;2;3);"""
    to_tokenise = """sum(1;2;3);"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "sum", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 4))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 8))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 10))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 11))


def test_semicolons_instead_of_commas_as_separators_of_parameters():
    """sum(arg1: mut int = 0; arg2: int = 0) : int begin end"""
    to_tokenise = """sum(arg1: mut int = 0; arg2: int = 0) : int begin end"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "sum", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 4))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1", position=(1, 5))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.MUT, position=(1, 11))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 15))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(1, 19))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0, position=(1, 21))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 22))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2", position=(1, 24))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 28))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 30))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(1, 34))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0, position=(1, 36))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 37))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 39))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 41))
    assert l.get_next_token() == Token(TokenType.BEGIN, position=(1, 45))
    assert l.get_next_token() == Token(TokenType.END, position=(1, 51))


def test_no_semicolon_at_the_end_of_an_assignment():
    """sum(1,2);a=1sum(3,4);"""
    to_tokenise = """sum(1,2);a=1sum(3,4);"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "sum", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 4))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.COMMA, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 8))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 10))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(1, 11))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 12))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "sum", position=(1, 13))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 16))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3, position=(1, 17))
    assert l.get_next_token() == Token(TokenType.COMMA, position=(1, 18))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 4, position=(1, 19))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 20))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 21))


def test_missing_left_bracket_in_function_call():
    """print'Ala');"""
    to_tokenise = """print'Ala');"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'print', position=(1, 1))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Ala", position=(1, 6))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 11))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 12))


def test_missing_right_bracket_in_function_call():
    """print('Ala';"""
    to_tokenise = """print('Ala';"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'print', position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Ala", position=(1, 7))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 12))


def test_argument_not_inside_brackets():
    """print()'Ala';"""
    to_tokenise = """print()'Ala';"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'print', position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Ala", position=(1, 8))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 13))


def test_params_outside_brackets():
    """add()a: int, b:int : int begin end"""
    to_tokenise = """add()a: int, b:int : int begin end"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 4))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 6))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.COMMA, position=(1, 12))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 14))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 15))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 16))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 20))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 22))
    assert l.get_next_token() == Token(TokenType.BEGIN, position=(1, 26))
    assert l.get_next_token() == Token(TokenType.END, position=(1, 32))


def test_func_def_missing_left_bracket():
    """adda: int, b:int) : int begin end"""
    to_tokenise = """adda: int, b:int) : int begin end"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "adda", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 5))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.COMMA, position=(1, 10))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 12))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 13))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 14))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1, 17))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 19))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 21))
    assert l.get_next_token() == Token(TokenType.BEGIN, position=(1, 25))
    assert l.get_next_token() == Token(TokenType.END, position=(1, 31))


def test_func_def_missing_right_bracket():
    """add(a: int, b:int : int begin end"""
    to_tokenise = """add(a: int, b:int : int begin end"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1, 4))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 5))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 8))
    assert l.get_next_token() == Token(TokenType.COMMA, position=(1, 11))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 13))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 14))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 15))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 19))
    assert l.get_next_token() == Token(TokenType.INT, position=(1, 21))
    assert l.get_next_token() == Token(TokenType.BEGIN, position=(1, 25))
    assert l.get_next_token() == Token(TokenType.END, position=(1, 31))


def test_negating_in_name_chain():
    """a.-b != -a.b"""
    to_tokenise = """a.-b != -a.b"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.DOT, position=(1, 2))
    assert l.get_next_token() == Token(TokenType.MINUS, position=(1, 3))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 4))
    assert l.get_next_token() == Token(TokenType.INEQUAL, position=(1, 6))
    assert l.get_next_token() == Token(TokenType.MINUS, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "a", position=(1, 10))
    assert l.get_next_token() == Token(TokenType.DOT, position=(1, 11))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "b", position=(1, 12))


def test_variable_def_in_variant_def():
    """Fruit : variant begin apple : Apple = 1; pear : Pear;"""
    to_tokenise = """Fruit : variant begin apple : Apple = 1; pear : Pear;"""
    r = TextIOReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Fruit", position=(1, 1))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 7))
    assert l.get_next_token() == Token(TokenType.VARIANT, position=(1, 9))
    assert l.get_next_token() == Token(TokenType.BEGIN, position=(1, 17))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "apple", position=(1, 23))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 29))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Apple", position=(1, 31))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(1, 37))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(1, 39))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 40))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "pear", position=(1, 42))
    assert l.get_next_token() == Token(TokenType.COLON, position=(1, 47))
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Pear", position=(1, 49))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1, 53))
