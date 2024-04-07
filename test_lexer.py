"""."""

from char_reader import StringReader
from lexer import Lexer
from token_type import TokenType
from my_token import MyToken

from my_token_exceptions import MyTokenException


def test_only_spaces():
    """."""
    text = 10 * " "
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    for _ in range(10):
        my_token = l.get_next_token()
        assert my_token == MyToken(TokenType.EOT)


def test_string_literal_ala():
    """."""
    text = "'ala'"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == MyToken(TokenType.STR_LITERAL, "ala")


def test_strin_literal_ala():
    """."""
    text = "'ala'"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    my_token = l.get_next_token()
    assert my_token == MyToken(TokenType.STR_LITERAL, "ala")


def test_strin_literal_not_properly_ended():
    """."""
    text = "'ala"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    try:
        l.get_next_token()
    except MyTokenException:
        pass


def test_keyword_null():
    """."""
    text = "null"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None

    assert l.get_next_token() == MyToken(TokenType.NULL)


def test_int_literal_1():
    """."""
    text = "1"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)


def test_int_literal_2():
    """."""
    text = "2"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 2)


def test_int_literal_12():
    """."""
    text = "12"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 12)


def test_int_literal_123():
    """."""
    text = "123"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 123)


def test_float_literal_123_dot():
    """."""
    text = "123."
    r = StringReader(text)
    l = Lexer(r)
    try:
        l.get_next_token()
    except MyTokenException:
        pass


def test_float_literal_123_dot_some_letters():
    """."""
    text = "123.abc"
    r = StringReader(text)
    l = Lexer(r)
    try:
        l.get_next_token()
    except MyTokenException:
        pass


def test_float_literal():
    """."""
    text = "123.123"
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 123.123) < 10 ** (-9)


def test_big_int_literal():
    """."""
    text = "99999999"
    r = StringReader(text)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 99999999)


def test_to_big_int_literal():
    """."""
    text = "100000000"
    r = StringReader(text)
    l = Lexer(r)
    try:
        l.get_next_token()
    except MyTokenException:
        pass


def test_big_float_literal():
    """."""
    text = "99999999.0"
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 99999999) < 10 ** (-9)


def test_float_bigger_than_int_limit():
    """."""
    text = "100000000.0"
    r = StringReader(text)
    l = Lexer(r)
    t = l.get_next_token()
    assert t.type == TokenType.FLOAT_LITERAL
    assert abs(t.value - 100000000) < 10 ** (-9)


def test_to_big_float_literal():
    """TODO"""


def test_print():
    """."""
    to_tokenise = """
        print('Hello');
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.PRINT)
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "Hello")
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.EOT)
    assert l.get_next_token() == MyToken(TokenType.EOT)
    assert l.get_next_token() == MyToken(TokenType.EOT)


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
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "Hello")
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.END)
    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_int_var_assignment():
    """."""
    to_tokenise = """
    calkowita          : int = 10;
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 10)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_builtin_types_vars_assignment():
    """."""
    to_tokenise = """
    calkowita          : int = 10;
    zmiennoprzecinkowa : float = 3.14;
    napis              : str = 'Ala ma kota.';
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 10)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "zmiennoprzecinkowa")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.FLOAT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(
        TokenType.FLOAT_LITERAL, 3.14
    )  # Different comparison?
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "napis")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STR)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "Ala ma kota.")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_non_mutable_var_without_init():
    """."""
    to_tokenise = """
    calkowita   : int;
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_mutable_var_without_init():
    """."""
    to_tokenise = """
    calkowita   : mut int;
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.MUT)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_mutable_var_with_init():
    """."""
    to_tokenise = """
    calkowita   : mut int = 2;
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.MUT)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 2)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_init_non_mutable_var_in_sep_statement():
    """
    Tokenisation of code that declares non mutable int variable and
    initialises its value in separete statement
    """
    to_tokenise = """
    calkowita   : int; 
    calkowita = 3;
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "calkowita")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 3)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_empty_string_literal():
    """."""
    to_tokenise = """''"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "")
    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_str_var_empty_literal_no_whitespaces():
    """."""
    to_tokenise = """x:str='';"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "x")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STR)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_negative_int_var():
    """."""
    to_tokenise = """x:int=-1;"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "x")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.MINUS)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_struct_def():
    """."""
    to_tokenise = """
    Point1D : struct
    begin
        x : mut int = 0;
    end
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Point1D")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STRUCT)
    assert l.get_next_token() == MyToken(TokenType.BEGIN)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "x")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.MUT)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 0)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_empty_comment():
    """."""
    to_tokenise = "@\n"
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.COMMENT, "")

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_space_comment():
    """."""
    to_tokenise = "@ \n"
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.COMMENT, " ")

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_cos_comment_immidiete_after_at():
    """."""
    to_tokenise = "@cos\n"
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.COMMENT, "cos")

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_czlowiek_struct_example():
    """."""
    to_tokenise = """
Czlowiek : struct
begin
    imie : str;
    wiek  : mut int;
end
janek : Czlowiek;
janek.imie = 'Janek';
janek.wiek = 20;
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Czlowiek")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STRUCT)
    assert l.get_next_token() == MyToken(TokenType.BEGIN)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "imie")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STR)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "wiek")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.MUT)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)
    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "janek")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Czlowiek")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "janek")
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "imie")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "Janek")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "janek")
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "wiek")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 20)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_smallest_valid_struct():
    """."""
    to_tokenise = """x:struct begin end"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "x")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STRUCT)
    assert l.get_next_token() == MyToken(TokenType.BEGIN)
    assert l.get_next_token() == MyToken(TokenType.END)
    assert l.get_next_token() == MyToken(TokenType.EOT)

def test_begin_end_merged():
    """."""
    to_tokenise = """beginend"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "beginend")
    assert l.get_next_token() == MyToken(TokenType.EOT)

def test_begin_end_separated_by_tab():
    """."""
    to_tokenise = """begin\tend"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.BEGIN)
    assert l.get_next_token() == MyToken(TokenType.END)
    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_variant():
    """."""
    to_tokenise = """
Punkt : variant
begin
    p2d : Punkt2D;
    p3d : Punkt3D;
end
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Punkt")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.VARIANT)

    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "p2d")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Punkt2D")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)


    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "p3d")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Punkt3D")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)


    assert l.get_next_token() == MyToken(TokenType.EOT)

def test_visit():
    """."""
    to_tokenise = """
visit punkt
begin
    case Punkt2D
    begin
        wiadomosc = '[' + p2d.x + '; ' + p2d.y + ']';
    end
    case Punkt3D
    begin
        wiadomosc = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';
    end
end
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.VISIT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "punkt")

    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.CASE)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Punkt2D")
    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'wiadomosc')
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, '[')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'p2d')
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'x')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, '; ')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'p2d')
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'y')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, ']')
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.CASE)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "Punkt3D")
    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'wiadomosc')
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, '[')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'p3d')
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'x')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, '; ')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'p3d')
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'y')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, '; ')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'p3d')
    assert l.get_next_token() == MyToken(TokenType.DOT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'z')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, ']')
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.EOT)



def test_if():
    """."""
    to_tokenise = """
ilosc_psow: mut int = 1;
msg: mut str = 'Ala ma ' + ilosc_psow + ' ps';
if ilosc_psow == 1
begin 
    msg = msg + 'a';
end 
else 
begin
    if 1 < ilosc_psow & ilosc_psow < 5
    begin
        msg = msg + 'y';
    end
end
else
begin
    msg = msg + 'ów';
end
msg = msg + '.';
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "ilosc_psow")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.MUT)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.MUT)
    assert l.get_next_token() == MyToken(TokenType.STR)
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, 'Ala ma ')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'ilosc_psow')
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, ' ps')
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.IF)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'ilosc_psow')
    assert l.get_next_token() == MyToken(TokenType.EQUAL)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)

    assert l.get_next_token() == MyToken(TokenType.BEGIN)
    
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "a")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.ELSE)
    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IF)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 1)
    assert l.get_next_token() == MyToken(TokenType.LESS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'ilosc_psow')
    assert l.get_next_token() == MyToken(TokenType.AND)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, 'ilosc_psow')
    assert l.get_next_token() == MyToken(TokenType.LESS)
    assert l.get_next_token() == MyToken(TokenType.INT_LITERAL, 5)

    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "y")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.ELSE)
    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, "ów")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.ASSIGNMENT)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "msg")
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.STR_LITERAL, ".")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.EOT)



def test_function_with_subfunctions():
    """."""
    to_tokenise = """
add(arg1: int, arg2: int) : int
begin
  add_sub_function(arg1: int, arg2: int) : int
  begin
    return arg1 + arg2;
  end
  
  add(arg1: int, arg2: int) : int
  begin
    return add_sub_function(arg1, arg2);
  end

  return add(arg1, arg2);
end
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "add")
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg1")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.COMMA)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg2")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)

    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "add_sub_function")
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg1")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.COMMA)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg2")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    
    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.RETURN)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg1")
    assert l.get_next_token() == MyToken(TokenType.PLUS)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg2")
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "add")
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg1")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.COMMA)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg2")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.INT)
    
    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.RETURN)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "add_sub_function")
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg1")
    assert l.get_next_token() == MyToken(TokenType.COMMA)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg2")
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.RETURN)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "add")
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg1")
    assert l.get_next_token() == MyToken(TokenType.COMMA)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "arg2")
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)

    assert l.get_next_token() == MyToken(TokenType.EOT)


def test_wypisz_na_ekran():
    """."""
    to_tokenise = """
wypisz_na_ekran(wiadomosc: str) : null_type 
begin
  print(wiadomosc);
  return null;
end
"""
    r = StringReader(to_tokenise)
    l = Lexer(r)
    assert l.curr_token is None
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "wypisz_na_ekran")
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "wiadomosc")
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.STR)
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.COLON)
    assert l.get_next_token() == MyToken(TokenType.NULL_TYPE)

    assert l.get_next_token() == MyToken(TokenType.BEGIN)

    assert l.get_next_token() == MyToken(TokenType.PRINT)
    assert l.get_next_token() == MyToken(TokenType.LEFT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.IDENTIFIER, "wiadomosc")
    assert l.get_next_token() == MyToken(TokenType.RIGHT_BRACKET)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.RETURN)
    assert l.get_next_token() == MyToken(TokenType.NULL)
    assert l.get_next_token() == MyToken(TokenType.SEMICOLON)

    assert l.get_next_token() == MyToken(TokenType.END)
    assert l.get_next_token() == MyToken(TokenType.EOT)