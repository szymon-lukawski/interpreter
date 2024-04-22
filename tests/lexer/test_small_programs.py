"""Testing lexer tokenisation but for some small programs"""

from io import StringIO
from char_reader import StringReader
from lexer import Lexer
from token_type import TokenType
from my_token import Token

from my_token_exceptions import MyTokenException

def test_print():
    """Print built in function call"""
    to_tokenise = """print('Hello');"""
    r = StringReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.PRINT, position=(1,1))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(1,6))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Hello", position=(1,7))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(1,14))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(1,15))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,16))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,16))
    assert l.get_next_token() == Token(TokenType.EOT, position=(1,16))


def test_basic_if_statement():
    """Basic if statement"""
    to_tokenise = """
if 1 
begin
    print('Hello');
end
"""
    r = StringReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IF, position=(2,1))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1, position=(2,4))
    assert l.get_next_token() == Token(TokenType.BEGIN, position=(3,1))
    assert l.get_next_token() == Token(TokenType.PRINT, position=(4,5))
    assert l.get_next_token() == Token(TokenType.LEFT_BRACKET, position=(4,10))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Hello", position=(4,11))
    assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET, position=(4,18))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(4,19))
    assert l.get_next_token() == Token(TokenType.END, position=(5,1))
    assert l.get_next_token() == Token(TokenType.EOT, position=(6,1))


def test_int_var_assignment():
    """."""
    to_tokenise = """
calkowita        : int = 10;
"""
    r = StringReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita", position=(2,1))
    assert l.get_next_token() == Token(TokenType.COLON, position=(2,18))
    assert l.get_next_token() == Token(TokenType.INT, position=(2,20))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(2,24))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 10, position=(2,26))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(2,28))
    assert l.get_next_token() == Token(TokenType.EOT, position=(3,1))


def test_builtin_types_vars_assignment():
    """."""
    to_tokenise = """
calkowita            : int   = 10;
zmiennoprzecinkowa   : float = 3.14;
napis                : str   = 'Ala ma kota.';
"""
    r = StringReader(StringIO(to_tokenise))
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita", position=(2,1))
    assert l.get_next_token() == Token(TokenType.COLON,position=(2,22))
    assert l.get_next_token() == Token(TokenType.INT,position=(2,24))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(2,30))
    assert l.get_next_token() == Token(TokenType.INT_LITERAL, 10,position=(2,32))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(2,34))

    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "zmiennoprzecinkowa",position=(3,1))
    assert l.get_next_token() == Token(TokenType.COLON, position=(3,22))
    assert l.get_next_token() == Token(TokenType.FLOAT,position=(3,24))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT, position=(3,30))
    assert l.get_next_token() == Token(
        TokenType.FLOAT_LITERAL, 3.14,position=(3,32)
    )  # Different comparison?
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(3,36))

    assert l.get_next_token() == Token(TokenType.IDENTIFIER, "napis", position=(4,1))
    assert l.get_next_token() == Token(TokenType.COLON, position=(4,22))
    assert l.get_next_token() == Token(TokenType.STR, position=(4,24))
    assert l.get_next_token() == Token(TokenType.ASSIGNMENT,position=(4,30))
    assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Ala ma kota.", position=(4,32))
    assert l.get_next_token() == Token(TokenType.SEMICOLON, position=(4,46))

    assert l.get_next_token() == Token(TokenType.EOT, position=(5,1))


# def test_non_mutable_var_without_init():
#     """."""
#     to_tokenise = """
#     calkowita   : int;
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_mutable_var_without_init():
#     """."""
#     to_tokenise = """
#     calkowita   : mut int;
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_mutable_var_with_init():
#     """."""
#     to_tokenise = """
#     calkowita   : mut int = 2;
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_init_non_mutable_var_in_sep_statement():
#     """
#     Tokenisation of code that declares non mutable int variable and
#     initialises its value in separete statement
#     """
#     to_tokenise = """
#     calkowita   : int; 
#     calkowita = 3;
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "calkowita")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_empty_string_literal():
#     """."""
#     to_tokenise = """''"""
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "")
#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_str_var_empty_literal_no_whitespaces():
#     """."""
#     to_tokenise = """x:str='';"""
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STR)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_negative_int_var():
#     """."""
#     to_tokenise = """x:int=-1;"""
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.MINUS)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_struct_def():
#     """."""
#     to_tokenise = """
#     Point1D : struct
#     begin
#         x : mut int = 0;
#     end
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Point1D")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STRUCT)
#     assert l.get_next_token() == Token(TokenType.BEGIN)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_empty_comment():
#     """."""
#     to_tokenise = "@\n"
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.COMMENT, "")

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_space_comment():
#     """."""
#     to_tokenise = "@ \n"
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.COMMENT, " ")

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_cos_comment_immidiete_after_at():
#     """."""
#     to_tokenise = "@cos\n"
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.COMMENT, "cos")

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_czlowiek_struct_example():
#     """."""
#     to_tokenise = """
# Czlowiek : struct
# begin
#     imie : str;
#     wiek  : mut int;
# end
# janek : Czlowiek;
# janek.imie = 'Janek';
# janek.wiek = 20;
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Czlowiek")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STRUCT)
#     assert l.get_next_token() == Token(TokenType.BEGIN)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "imie")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STR)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiek")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "janek")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Czlowiek")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "janek")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "imie")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Janek")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "janek")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiek")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 20)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_smallest_valid_struct():
#     """."""
#     to_tokenise = """x:struct begin end"""
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STRUCT)
#     assert l.get_next_token() == Token(TokenType.BEGIN)
#     assert l.get_next_token() == Token(TokenType.END)
#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_begin_end_merged():
#     """."""
#     to_tokenise = """beginend"""
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "beginend")
#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_begin_end_separated_by_tab():
#     """."""
#     to_tokenise = """begin\tend"""
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.BEGIN)
#     assert l.get_next_token() == Token(TokenType.END)
#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_variant():
#     """."""
#     to_tokenise = """
# Punkt : variant
# begin
#     p2d : Punkt2D;
#     p3d : Punkt3D;
# end
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Punkt")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.VARIANT)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p2d")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Punkt2D")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p3d")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Punkt3D")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_visit():
#     """."""
#     to_tokenise = """
# visit punkt
# begin
#     case Punkt2D
#     begin
#         wiadomosc = '[' + p2d.x + '; ' + p2d.y + ']';
#     end
#     case Punkt3D
#     begin
#         wiadomosc = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';
#     end
# end
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.VISIT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "punkt")

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.CASE)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Punkt2D")
#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiadomosc")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "[")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p2d")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "; ")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p2d")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "y")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "]")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.CASE)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "Punkt3D")
#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiadomosc")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "[")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p3d")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "; ")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p3d")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "y")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "; ")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "p3d")
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "z")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "]")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_if():
#     """."""
#     to_tokenise = """
# ilosc_psow: mut int = 1;
# msg: mut str = 'Ala ma ' + ilosc_psow + ' ps';
# if ilosc_psow == 1
# begin 
#     msg = msg + 'a';
# end 
# else 
# begin
#     if 1 < ilosc_psow & ilosc_psow < 5
#     begin
#         msg = msg + 'y';
#     end
# end
# else
# begin
#     msg = msg + 'ów';
# end
# msg = msg + '.';
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ilosc_psow")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.STR)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Ala ma ")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ilosc_psow")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, " ps")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.IF)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ilosc_psow")
#     assert l.get_next_token() == Token(TokenType.EQUAL)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "a")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.ELSE)
#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IF)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1)
#     assert l.get_next_token() == Token(TokenType.LESS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ilosc_psow")
#     assert l.get_next_token() == Token(TokenType.AND)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "ilosc_psow")
#     assert l.get_next_token() == Token(TokenType.LESS)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 5)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "y")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.ELSE)
#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "ów")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "msg")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, ".")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_function_with_subfunctions():
#     """."""
#     to_tokenise = """
# add(arg1: int, arg2: int) : int
# begin
#   add_sub_function(arg1: int, arg2: int) : int
#   begin
#     return arg1 + arg2;
#   end
  
#   add(arg1: int, arg2: int) : int
#   begin
#     return add_sub_function(arg1, arg2);
#   end

#   return add(arg1, arg2);
# end
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.COMMA)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add_sub_function")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.COMMA)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.RETURN)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1")
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.COMMA)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.RETURN)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add_sub_function")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1")
#     assert l.get_next_token() == Token(TokenType.COMMA)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.RETURN)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "add")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg1")
#     assert l.get_next_token() == Token(TokenType.COMMA)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "arg2")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_wypisz_na_ekran():
#     """."""
#     to_tokenise = """
# wypisz_na_ekran(wiadomosc: str) : null_type 
# begin
#   print(wiadomosc);
#   return null;
# end
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wypisz_na_ekran")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiadomosc")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STR)
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.NULL_TYPE)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiadomosc")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.RETURN)
#     assert l.get_next_token() == Token(TokenType.NULL)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)
#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_wypisz_na_ekran_without_return():
#     """."""
#     to_tokenise = """
# wypisz_na_ekran(wiadomosc: str) : null_type 
# begin
#   print(wiadomosc);
# end
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wypisz_na_ekran")
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiadomosc")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STR)
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.NULL_TYPE)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "wiadomosc")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.END)
#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_block():
#     """."""
#     to_tokenise = """
# x : int = 1;
# print(x); @ 1
# begin
#   x : str = 'Ala ma kota';
#   begin
#     x : float = 2.0;
#     print(x); @ 2.0000000
#   end
#   begin
#     x : float = 3.0;
#     print(x); @ 3.0000000
#   end
#   print(x); @ Ala ma kota
# end
# print(x); @ 1
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.COMMENT, " 1")

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STR)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.STR_LITERAL, "Ala ma kota")
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.FLOAT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.FLOAT_LITERAL, 2.0)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.COMMENT, " 2.0000000")

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.BEGIN)

#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.FLOAT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.FLOAT_LITERAL, 3.0)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.COMMENT, " 3.0000000")

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.COMMENT, " Ala ma kota")

#     assert l.get_next_token() == Token(TokenType.END)

#     assert l.get_next_token() == Token(TokenType.PRINT)
#     assert l.get_next_token() == Token(TokenType.LEFT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "x")
#     assert l.get_next_token() == Token(TokenType.RIGHT_BRACKET)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.COMMENT, " 1")

#     assert l.get_next_token() == Token(TokenType.EOT)


# def test_operator_priority():
#     """."""
#     to_tokenise = """
# P : struct
# begin
#     x : mut int = 0;
# end
# p : P;
# p.x = 0 | 1 & 2 < 2 + 3 - 4 * - 5 / - p.x;
# """
#     r = StringReader(StringIO(to_tokenise))
#     l = Lexer(r)
#     assert l.curr_token is None
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, "P", (2,1))
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.STRUCT)
#     assert l.get_next_token() == Token(TokenType.BEGIN)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'x')
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.MUT)
#     assert l.get_next_token() == Token(TokenType.INT)
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0)
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.END)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'p')
#     assert l.get_next_token() == Token(TokenType.COLON)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'P')
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'p')
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'x')
#     assert l.get_next_token() == Token(TokenType.ASSIGNMENT)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 0)
#     assert l.get_next_token() == Token(TokenType.OR)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 1)
#     assert l.get_next_token() == Token(TokenType.AND)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2)
#     assert l.get_next_token() == Token(TokenType.LESS)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 2)
#     assert l.get_next_token() == Token(TokenType.PLUS)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 3)
#     assert l.get_next_token() == Token(TokenType.MINUS)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 4)
#     assert l.get_next_token() == Token(TokenType.TIMES)
#     assert l.get_next_token() == Token(TokenType.MINUS)
#     assert l.get_next_token() == Token(TokenType.INT_LITERAL, 5)
#     assert l.get_next_token() == Token(TokenType.DIVIDE)
#     assert l.get_next_token() == Token(TokenType.MINUS)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'p')
#     assert l.get_next_token() == Token(TokenType.DOT)
#     assert l.get_next_token() == Token(TokenType.IDENTIFIER, 'x')
#     assert l.get_next_token() == Token(TokenType.SEMICOLON)
#     assert l.get_next_token() == Token(TokenType.EOT)