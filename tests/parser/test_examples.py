"""Small programms"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck


import pytest

from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *
from token_provider import TokenProvider




def test_sanity():
    """Test for making sure test infrastructure works"""
    # pylint: disable=C0121:singleton-comparison
    assert True == 1


def test_print():
    """print('Hello');"""

    tokens = [
        Token(TokenType.IDENTIFIER, "print", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 6)),
        Token(TokenType.STR_LITERAL, "Hello", position=(1, 7)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 14)),
        Token(TokenType.SEMICOLON, position=(1, 15)),
        Token(TokenType.EOT, position=(1, 16)),
        Token(TokenType.EOT, position=(1, 16)),
        Token(TokenType.EOT, position=(1, 16)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 1
    assert type(result.children[0]) == FunctionCall
    assert result.children[0].name == "print"
    assert len(result.children[0].args) == 1
    assert type(result.children[0].args[0]) == StrLiteral
    assert result.children[0].args[0].value == "Hello"


def test_basic_if():
    """
    if 1
    begin
        print('Hello');
    end
    """

    tokens = [
        Token(TokenType.IF, position=(2, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 4)),
        Token(TokenType.BEGIN, position=(3, 1)),
        Token(TokenType.IDENTIFIER, "print", position=(4, 5)),
        Token(TokenType.LEFT_BRACKET, position=(4, 10)),
        Token(TokenType.STR_LITERAL, "Hello", position=(4, 11)),
        Token(TokenType.RIGHT_BRACKET, position=(4, 18)),
        Token(TokenType.SEMICOLON, position=(4, 19)),
        Token(TokenType.END, position=(5, 1)),
        Token(TokenType.EOT, position=(6, 1)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 1
    assert type(result.children[0]) == IfStatement
    assert type(result.children[0].cond) == IntLiteral
    assert type(result.children[0].prog) == Program
    assert type(result.children[0].prog.children[0]) == FunctionCall

    assert result.children[0].prog.children[0].name == "print"
    assert len(result.children[0].prog.children[0].args) == 1
    assert type(result.children[0].prog.children[0].args[0]) == StrLiteral
    assert result.children[0].prog.children[0].args[0].value == "Hello"

    assert result.children[0].else_prog is None


def test_int_var_assignment():
    """calkowita : int = 10;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "calkowita", position=(2, 1)),
        Token(TokenType.COLON, position=(2, 18)),
        Token(TokenType.INT, position=(2, 20)),
        Token(TokenType.ASSIGNMENT, position=(2, 24)),
        Token(TokenType.INT_LITERAL, 10, position=(2, 26)),
        Token(TokenType.SEMICOLON, position=(2, 28)),
        Token(TokenType.EOT, position=(3, 1)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 1
    assert type(result.children[0]) == VariableDeclaration
    assert result.children[0].name == "calkowita"
    assert type(result.children[0].type) == str
    assert result.children[0].type == "int"
    assert type(result.children[0].default_value) == IntLiteral
    assert result.children[0].default_value.value == 10


def test_builtin_types_vars_assignment():
    """
    calkowita            : int   = 10;
    zmiennoprzecinkowa   : float = 3.14;
    napis                : str   = 'Ala ma kota.';
    """
    tokens = [
        Token(TokenType.IDENTIFIER, "calkowita", position=(2, 1)),
        Token(TokenType.COLON, position=(2, 22)),
        Token(TokenType.INT, position=(2, 24)),
        Token(TokenType.ASSIGNMENT, position=(2, 30)),
        Token(TokenType.INT_LITERAL, 10, position=(2, 32)),
        Token(TokenType.SEMICOLON, position=(2, 34)),
        Token(TokenType.IDENTIFIER, "zmiennoprzecinkowa", position=(3, 1)),
        Token(TokenType.COLON, position=(3, 22)),
        Token(TokenType.FLOAT, position=(3, 24)),
        Token(TokenType.ASSIGNMENT, position=(3, 30)),
        Token(TokenType.FLOAT_LITERAL, 3.14, position=(3, 32)),
        Token(TokenType.SEMICOLON, position=(3, 36)),
        Token(TokenType.IDENTIFIER, "napis", position=(4, 1)),
        Token(TokenType.COLON, position=(4, 22)),
        Token(TokenType.STR, position=(4, 24)),
        Token(TokenType.ASSIGNMENT, position=(4, 30)),
        Token(TokenType.STR_LITERAL, "Ala ma kota.", position=(4, 32)),
        Token(TokenType.SEMICOLON, position=(4, 46)),
    ]
    #     Token(TokenType.EOT, position=(5,1)),
    # ]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 3
    assert type(result.children[0]) == VariableDeclaration
    assert result.children[0].name == "calkowita"
    assert type(result.children[0].type) == str
    assert result.children[0].type == "int"
    assert type(result.children[0].default_value) == IntLiteral
    assert result.children[0].default_value.value == 10

    assert type(result.children[1]) == VariableDeclaration
    assert result.children[1].name == "zmiennoprzecinkowa"
    assert type(result.children[1].type) == str
    assert result.children[1].type == "float"
    assert type(result.children[1].default_value) == FloatLiteral
    assert result.children[1].default_value.value == 3.14

    assert type(result.children[2]) == VariableDeclaration
    assert result.children[2].name == "napis"
    assert type(result.children[2].type) == str
    assert result.children[2].type == "str"
    assert type(result.children[2].default_value) == StrLiteral
    assert result.children[2].default_value.value == "Ala ma kota."


def test_non_mutable_var_without_init():
    """
    calkowita   : int;
    """
    tokens = [
        Token(TokenType.IDENTIFIER, "calkowita", position=(2, 1)),
        Token(TokenType.COLON, position=(2, 22)),
        Token(TokenType.INT, position=(2, 24)),
        Token(TokenType.SEMICOLON, position=(2, 34)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 1
    assert type(result.children[0]) == VariableDeclaration
    assert result.children[0].name == "calkowita"
    assert type(result.children[0].type) == str
    assert result.children[0].type == "int"
    assert not result.children[0].is_mutable


def test_czlowiek_struct_example():
    """
    Czlowiek : struct
    begin
       imie : str;
       wiek  : mut int;
    end
    janek : Czlowiek;
    janek.imie = 'Janek';
    janek.wiek = 20;
    """
    tokens = [
        Token(TokenType.IDENTIFIER, "Czlowiek"),
        Token(TokenType.COLON),
        Token(TokenType.STRUCT),
        Token(TokenType.BEGIN),
        Token(TokenType.IDENTIFIER, "imie"),
        Token(TokenType.COLON),
        Token(TokenType.STR),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "wiek"),
        Token(TokenType.COLON),
        Token(TokenType.MUT),
        Token(TokenType.INT),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.IDENTIFIER, "janek"),
        Token(TokenType.COLON),
        Token(TokenType.IDENTIFIER, "Czlowiek"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "janek"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "imie"),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.STR_LITERAL, "Janek"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "janek"),
        Token(TokenType.DOT),
        Token(TokenType.IDENTIFIER, "wiek"),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.INT_LITERAL, 20),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 4
    assert type(result.children[0]) == StructDef
    assert type(result.children[1]) == VariableDeclaration
    assert type(result.children[2]) == AssignmentStatement
    assert type(result.children[3]) == AssignmentStatement

    assert result.children[0].name == "Czlowiek"
    assert len(result.children[0].attributes) == 2
    assert type(result.children[0].attributes[0]) == VariableDeclaration
    assert result.children[0].attributes[0].name == "imie"
    assert type(result.children[0].attributes[0].type) == str
    assert result.children[0].attributes[0].type == "str"
    assert not result.children[0].attributes[0].is_mutable

    assert type(result.children[0].attributes[1]) == VariableDeclaration
    assert result.children[0].attributes[1].name == "wiek"
    assert type(result.children[0].attributes[1].type) == str
    assert result.children[0].attributes[1].type == "int"
    assert result.children[0].attributes[1].is_mutable

    assert result.children[1].name == "janek"
    assert result.children[1].type == "Czlowiek"
    assert not result.children[1].is_mutable

    assert result.children[2].obj_access == ["janek", "imie"]
    assert type(result.children[2].expr) == StrLiteral
    assert result.children[2].expr.value == "Janek"

    assert result.children[3].obj_access == ["janek", "wiek"]
    assert type(result.children[3].expr) == IntLiteral
    assert result.children[3].expr.value == 20


def test_if_if_else():
    """
    ilosc_psow: mut int = 1;
    msg: mut str = 'Ala ma ' + ilosc_psow + ' ps';
    if ilosc_psow == 1
    begin
        msg = msg + 'a';
    end
    if 1 < ilosc_psow & ilosc_psow < 5
    begin
        msg = msg + 'y';
    end
    else
    begin
        msg = msg + 'ów';
    end
    msg = msg + '.';
    """
    tokens = [
        Token(TokenType.IDENTIFIER, "ilosc_psow"),
        Token(TokenType.COLON),
        Token(TokenType.MUT),
        Token(TokenType.INT),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.COLON),
        Token(TokenType.MUT),
        Token(TokenType.STR),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.STR_LITERAL, "Ala ma "),
        Token(TokenType.PLUS),
        Token(TokenType.IDENTIFIER, "ilosc_psow"),
        Token(TokenType.PLUS),
        Token(TokenType.STR_LITERAL, " ps"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.IF),
        Token(TokenType.IDENTIFIER, "ilosc_psow"),
        Token(TokenType.EQUAL),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.BEGIN),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.PLUS),
        Token(TokenType.STR_LITERAL, "a"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.IF),
        Token(TokenType.INT_LITERAL, 1),
        Token(TokenType.LESS),
        Token(TokenType.IDENTIFIER, "ilosc_psow"),
        Token(TokenType.AND),
        Token(TokenType.IDENTIFIER, "ilosc_psow"),
        Token(TokenType.LESS),
        Token(TokenType.INT_LITERAL, 5),
        Token(TokenType.BEGIN),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.PLUS),
        Token(TokenType.STR_LITERAL, "y"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.ELSE),
        Token(TokenType.BEGIN),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.PLUS),
        Token(TokenType.STR_LITERAL, "ów"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.END),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.ASSIGNMENT),
        Token(TokenType.IDENTIFIER, "msg"),
        Token(TokenType.PLUS),
        Token(TokenType.STR_LITERAL, "."),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOT),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert type(result) == Program
    assert len(result.children) == 5

    # Check the first statement: ilosc_psow: mut int = 1;
    assert type(result.children[0]) == VariableDeclaration
    assert result.children[0].name == "ilosc_psow"
    assert result.children[0].is_mutable
    assert result.children[0].type == "int"
    assert type(result.children[0].default_value) == IntLiteral
    assert result.children[0].default_value.value == 1

    # Check the second statement: msg: mut str = 'Ala ma ' + ilosc_psow + ' ps';
    assert type(result.children[1]) == VariableDeclaration
    assert result.children[1].name == "msg"
    assert result.children[1].is_mutable
    assert result.children[1].type == "str"
    assert type(result.children[1].default_value) == AddExpr
    assert type(result.children[1].default_value.children[0]) == StrLiteral
    assert result.children[1].default_value.children[0].value == "Ala ma "
    assert type(result.children[1].default_value.children[1]) == ObjectAccess
    assert result.children[1].default_value.children[1].name_chain == ["ilosc_psow"]
    assert type(result.children[1].default_value.children[2]) == StrLiteral
    assert result.children[1].default_value.children[2].value == " ps"

    # Check the if statement
        # Check if condition
    assert type(result.children[2]) == IfStatement
    assert type(result.children[2].cond) == RelationExpr
    assert result.children[2].cond.operator == '=='
    assert type(result.children[2].cond.left) == ObjectAccess
    assert result.children[2].cond.left.name_chain == ["ilosc_psow"]
    assert type(result.children[2].cond.right) == IntLiteral
    assert result.children[2].cond.right.value == 1
        # Check the if-body
    assert type(result.children[2].prog) == Program
    assert len(result.children[2].prog.children) == 1
    assert type(result.children[2].prog.children[0]) == AssignmentStatement
    assert result.children[2].prog.children[0].obj_access == ["msg"]
    assert type(result.children[2].prog.children[0].expr) == AddExpr
    assert type(result.children[2].prog.children[0].expr.children[0]) == ObjectAccess
    assert result.children[2].prog.children[0].expr.children[0].name_chain == ["msg"]
    assert type(result.children[2].prog.children[0].expr.children[1]) == StrLiteral
    assert result.children[2].prog.children[0].expr.children[1].value == "a"


    # Check the second if statement
        # Check if condition
    assert type(result.children[3]) == IfStatement
    assert type(result.children[3].cond) == AndExpr
    assert len(result.children[3].cond.children) == 2
    assert type(result.children[3].cond.children[0]) == RelationExpr
    


    assert result.children[3].cond.children[0].operator == '<'
    


    assert type(result.children[3].cond.children[0].left) == IntLiteral
    assert result.children[3].cond.children[0].left.value == 1
    assert type(result.children[3].cond.children[0].right) == ObjectAccess
    assert result.children[3].cond.children[0].right.name_chain == ['ilosc_psow']
        # & 
    assert type(result.children[3].cond.children[1]) == RelationExpr
    assert result.children[3].cond.children[1].operator == '<'
    assert type(result.children[3].cond.children[1].left) == ObjectAccess
    assert result.children[3].cond.children[1].left.name_chain == ['ilosc_psow']
    assert type(result.children[3].cond.children[1].right) == IntLiteral
    assert result.children[3].cond.children[1].right.value == 5
        # Check the if-body
    assert type(result.children[3].prog) == Program
    assert len(result.children[3].prog.children) == 1
    assert type(result.children[3].prog.children[0]) == AssignmentStatement
    assert result.children[3].prog.children[0].obj_access == ["msg"]
    assert type(result.children[3].prog.children[0].expr) == AddExpr
    assert type(result.children[3].prog.children[0].expr.children[0]) == ObjectAccess
    assert result.children[3].prog.children[0].expr.children[0].name_chain == ["msg"]
    assert type(result.children[3].prog.children[0].expr.children[1]) == StrLiteral
    assert result.children[3].prog.children[0].expr.children[1].value == "y"

    assert type(result.children[3].else_prog) == Program
    assert len(result.children[3].else_prog.children) == 1
    assert type(result.children[3].else_prog.children[0]) == AssignmentStatement
    assert result.children[3].else_prog.children[0].obj_access == ["msg"]
    assert type(result.children[3].else_prog.children[0].expr) == AddExpr
    assert type(result.children[3].else_prog.children[0].expr.children[0]) == ObjectAccess
    assert result.children[3].else_prog.children[0].expr.children[0].name_chain == ["msg"]
    assert type(result.children[3].else_prog.children[0].expr.children[1]) == StrLiteral
    assert result.children[3].else_prog.children[0].expr.children[1].value == "ów"

    assert type(result.children[4]) == AssignmentStatement
    assert result.children[4].obj_access == ["msg"]
    assert type(result.children[4].expr) == AddExpr
    assert type(result.children[4].expr.children[0]) == ObjectAccess
    assert result.children[4].expr.children[0].name_chain == ["msg"]
    assert type(result.children[4].expr.children[1]) == StrLiteral
    assert result.children[4].expr.children[1].value == "."


def test_variant_example():
    """
    jakis_warunek : int = 1;
    Liczba : variant
    begin
        calkowita : int;
        zmiennoprzecinkowa : float;
    end
    moja_liczba : Liczba;
    if jakis_warunek
    begin
        moja_liczba = 30;
    end
    else begin
        moja_liczba = 3.14;
    end
    wynik : str;
    visit moja_liczba
    begin
        case int begin
            wynik = moja_liczba.calkowita;
        end
        case float begin
            wynik = moja_liczba.zmiennoprzecinkowa;
        end
    end
    
    """
    tokens = [
        Token(TokenType.IDENTIFIER, 'jakis_warunek', position=(2, 5)),
        Token(TokenType.COLON, position=(2, 19)),
        Token(TokenType.INT, position=(2, 21)),
        Token(TokenType.ASSIGNMENT, position=(2, 25)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 27)),
        Token(TokenType.SEMICOLON, position=(2, 28)),
        Token(TokenType.IDENTIFIER, 'Liczba', position=(3, 5)),
        Token(TokenType.COLON, position=(3, 12)),
        Token(TokenType.VARIANT, position=(3, 14)),
        Token(TokenType.BEGIN, position=(4, 5)),
        Token(TokenType.IDENTIFIER, 'calkowita', position=(5, 9)),
        Token(TokenType.COLON, position=(5, 19)),
        Token(TokenType.INT, position=(5, 21)),
        Token(TokenType.SEMICOLON, position=(5, 24)),
        Token(TokenType.IDENTIFIER, 'zmiennoprzecinkowa', position=(6, 9)),
        Token(TokenType.COLON, position=(6, 28)),
        Token(TokenType.FLOAT, position=(6, 30)),
        Token(TokenType.SEMICOLON, position=(6, 35)),
        Token(TokenType.END, position=(7, 5)),
        Token(TokenType.IDENTIFIER, 'moja_liczba', position=(8, 5)),
        Token(TokenType.COLON, position=(8, 17)),
        Token(TokenType.IDENTIFIER, 'Liczba', position=(8, 19)),
        Token(TokenType.SEMICOLON, position=(8, 25)),
        Token(TokenType.IF, position=(9, 5)),
        Token(TokenType.IDENTIFIER, 'jakis_warunek', position=(9, 8)),
        Token(TokenType.BEGIN, position=(10, 5)),
        Token(TokenType.IDENTIFIER, 'moja_liczba', position=(11, 9)),
        Token(TokenType.ASSIGNMENT, position=(11, 21)),
        Token(TokenType.INT_LITERAL, 30, position=(11, 23)),
        Token(TokenType.SEMICOLON, position=(11, 25)),
        Token(TokenType.END, position=(12, 5)),
        Token(TokenType.ELSE, position=(13, 5)),
        Token(TokenType.BEGIN, position=(13, 10)),
        Token(TokenType.IDENTIFIER, 'moja_liczba', position=(14, 9)),
        Token(TokenType.ASSIGNMENT, position=(14, 21)),
        Token(TokenType.FLOAT_LITERAL, 3.14, position=(14, 23)),
        Token(TokenType.SEMICOLON, position=(14, 27)),
        Token(TokenType.END, position=(15, 5)),
        Token(TokenType.IDENTIFIER, 'wynik', position=(16, 5)),
        Token(TokenType.COLON, position=(16, 11)),
        Token(TokenType.STR, position=(16, 13)),
        Token(TokenType.SEMICOLON, position=(16, 16)),
        Token(TokenType.VISIT, position=(17, 5)),
        Token(TokenType.IDENTIFIER, 'moja_liczba', position=(17, 11)),
        Token(TokenType.BEGIN, position=(18, 5)),
        Token(TokenType.CASE, position=(19, 9)),
        Token(TokenType.INT, position=(19, 14)),
        Token(TokenType.BEGIN, position=(19, 18)),
        Token(TokenType.IDENTIFIER, 'wynik', position=(20, 13)),
        Token(TokenType.ASSIGNMENT, position=(20, 19)),
        Token(TokenType.IDENTIFIER, 'moja_liczba', position=(20, 21)),
        Token(TokenType.DOT, position=(20, 32)),
        Token(TokenType.IDENTIFIER, 'calkowita', position=(20, 33)),
        Token(TokenType.SEMICOLON, position=(20, 42)),
        Token(TokenType.END, position=(21, 9)),
        Token(TokenType.CASE, position=(22, 9)),
        Token(TokenType.FLOAT, position=(22, 14)),
        Token(TokenType.BEGIN, position=(22, 20)),
        Token(TokenType.IDENTIFIER, 'wynik', position=(23, 13)),
        Token(TokenType.ASSIGNMENT, position=(23, 19)),
        Token(TokenType.IDENTIFIER, 'moja_liczba', position=(23, 21)),
        Token(TokenType.DOT, position=(23, 32)),
        Token(TokenType.IDENTIFIER, 'zmiennoprzecinkowa', position=(23, 33)),
        Token(TokenType.SEMICOLON, position=(23, 51)),
        Token(TokenType.END, position=(24, 9)),
        Token(TokenType.END, position=(25, 5)),
        Token(TokenType.EOT, position=(27, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([VariableDeclaration('jakis_warunek', 'int', False, IntLiteral(1, None), pos=(2, 5)), VariantDef('Liczba', [NamedType('calkowita', 'int', pos=(5, 9)), NamedType('zmiennoprzecinkowa', 'float', pos=(6, 9))], (3, 5)), VariableDeclaration('moja_liczba', 'Liczba', False, pos=(8, 5)), IfStatement(ObjectAccess(['jakis_warunek'], pos=(9, 8)), Program([AssignmentStatement(['moja_liczba'], IntLiteral(30, None), (11, 9))], (11, 9)), Program([AssignmentStatement(['moja_liczba'], FloatLiteral(3.14, None), (14, 9))], (14, 9)), (9, 5)), VariableDeclaration('wynik', 'str', False, pos=(16, 5)), VisitStatement(ObjectAccess(['moja_liczba'], pos=(17, 11)), [CaseSection('int', Program([AssignmentStatement(['wynik'], ObjectAccess(['moja_liczba', 'calkowita'], pos=(20, 21)), (20, 13))], (20, 13)), pos=(19, 9)), CaseSection('float', Program([AssignmentStatement(['wynik'], ObjectAccess(['moja_liczba', 'zmiennoprzecinkowa'], pos=(23, 21)), (23, 13))], (23, 13)), pos=(22, 9))], pos=(17, 5))], (2, 5))
    assert result == expected



def test_func_def():
    """add(arg1: int, arg2: int) : int
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
    tokens = [
        Token(TokenType.IDENTIFIER, 'add', position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.IDENTIFIER, 'arg1', position=(1, 5)),
        Token(TokenType.COLON, position=(1, 9)),
        Token(TokenType.INT, position=(1, 11)),
        Token(TokenType.COMMA, position=(1, 14)),
        Token(TokenType.IDENTIFIER, 'arg2', position=(1, 16)),
        Token(TokenType.COLON, position=(1, 20)),
        Token(TokenType.INT, position=(1, 22)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 25)),
        Token(TokenType.COLON, position=(1, 27)),
        Token(TokenType.INT, position=(1, 29)),
        Token(TokenType.BEGIN, position=(2, 1)),
        Token(TokenType.IDENTIFIER, 'add_sub_function', position=(3, 3)),
        Token(TokenType.LEFT_BRACKET, position=(3, 19)),
        Token(TokenType.IDENTIFIER, 'arg1', position=(3, 20)),
        Token(TokenType.COLON, position=(3, 24)),
        Token(TokenType.INT, position=(3, 26)),
        Token(TokenType.COMMA, position=(3, 29)),
        Token(TokenType.IDENTIFIER, 'arg2', position=(3, 31)),
        Token(TokenType.COLON, position=(3, 35)),
        Token(TokenType.INT, position=(3, 37)),
        Token(TokenType.RIGHT_BRACKET, position=(3, 40)),
        Token(TokenType.COLON, position=(3, 42)),
        Token(TokenType.INT, position=(3, 44)),
        Token(TokenType.BEGIN, position=(4, 3)),
        Token(TokenType.RETURN, position=(5, 5)),
        Token(TokenType.IDENTIFIER, 'arg1', position=(5, 12)),
        Token(TokenType.PLUS, position=(5, 17)),
        Token(TokenType.IDENTIFIER, 'arg2', position=(5, 19)),
        Token(TokenType.SEMICOLON, position=(5, 23)),
        Token(TokenType.END, position=(6, 3)),
        Token(TokenType.IDENTIFIER, 'add', position=(8, 3)),
        Token(TokenType.LEFT_BRACKET, position=(8, 6)),
        Token(TokenType.IDENTIFIER, 'arg1', position=(8, 7)),
        Token(TokenType.COLON, position=(8, 11)),
        Token(TokenType.INT, position=(8, 13)),
        Token(TokenType.COMMA, position=(8, 16)),
        Token(TokenType.IDENTIFIER, 'arg2', position=(8, 18)),
        Token(TokenType.COLON, position=(8, 22)),
        Token(TokenType.INT, position=(8, 24)),
        Token(TokenType.RIGHT_BRACKET, position=(8, 27)),
        Token(TokenType.COLON, position=(8, 29)),
        Token(TokenType.INT, position=(8, 31)),
        Token(TokenType.BEGIN, position=(9, 3)),
        Token(TokenType.RETURN, position=(10, 5)),
        Token(TokenType.IDENTIFIER, 'add_sub_function', position=(10, 12)),
        Token(TokenType.LEFT_BRACKET, position=(10, 28)),
        Token(TokenType.IDENTIFIER, 'arg1', position=(10, 29)),
        Token(TokenType.COMMA, position=(10, 33)),
        Token(TokenType.IDENTIFIER, 'arg2', position=(10, 35)),
        Token(TokenType.RIGHT_BRACKET, position=(10, 39)),
        Token(TokenType.SEMICOLON, position=(10, 40)),
        Token(TokenType.END, position=(11, 3)),
        Token(TokenType.RETURN, position=(13, 3)),
        Token(TokenType.IDENTIFIER, 'add', position=(13, 10)),
        Token(TokenType.LEFT_BRACKET, position=(13, 13)),
        Token(TokenType.IDENTIFIER, 'arg1', position=(13, 14)),
        Token(TokenType.COMMA, position=(13, 18)),
        Token(TokenType.IDENTIFIER, 'arg2', position=(13, 20)),
        Token(TokenType.RIGHT_BRACKET, position=(13, 24)),
        Token(TokenType.SEMICOLON, position=(13, 25)),
        Token(TokenType.END, position=(14, 1)),
        Token(TokenType.EOT, position=(15, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    expected = Program([FuncDef('add', [Param('arg1', 'int', False, pos=(1, 5)), Param('arg2', 'int', False, pos=(1, 16))], 'int', Program([FuncDef('add_sub_function', [Param('arg1', 'int', False, pos=(3, 20)), Param('arg2', 'int', False, pos=(3, 31))], 'int', Program([ReturnStatement(AddExpr([ObjectAccess(['arg1'], pos=(5, 12)), ObjectAccess(['arg2'], pos=(5, 19))], ['+'], pos=(5, 12)), (5, 5))], (5, 5)), pos=(3, 3)), FuncDef('add', [Param('arg1', 'int', False, pos=(8, 7)), Param('arg2', 'int', False, pos=(8, 18))], 'int', Program([ReturnStatement(ObjectAccess([FunctionCall('add_sub_function', [ObjectAccess(['arg1'], pos=(10, 29)), ObjectAccess(['arg2'], pos=(10, 35))], pos=(10, 12))], pos=(10, 12)), (10, 5))], (10, 5)), pos=(8, 3)), ReturnStatement(ObjectAccess([FunctionCall('add', [ObjectAccess(['arg1'], pos=(13, 14)), ObjectAccess(['arg2'], pos=(13, 20))], pos=(13, 10))], pos=(13, 10)), (13, 3))], (3, 3)), pos=(1, 1))], (1, 1))