"""Small programms"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck


import pytest

from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *


class TokenProvider(Lexer):
    """Mocks lexer."""

    def __init__(self, _, list_of_tokens) -> None:
        self.tokens = list_of_tokens
        self.idx = -1
        self._EOT_token_in_place = False
        super().__init__(_)

    def _next_token(self):
        if self._EOT_token_in_place:
            return
        if self._is_end_of_file():
            self.curr_token = Token(TokenType.EOT)
            self._EOT_token_in_place = True
            return
        self.idx += 1
        self.curr_token = self.tokens[self.idx]

    def _is_end_of_file(self):
        return self.idx + 2 > len(self.tokens)


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
    assert type(result.children[0]) == Fork
    assert len(result.children[0].statements) == 2
    assert type(result.children[0].statements[0]) == VariableDeclaration
    assert result.children[0].statements[0].name == "calkowita"
    assert type(result.children[0].statements[0].type) == Type
    assert result.children[0].statements[0].type.name == "int"
    assert type(result.children[0].statements[1]) == AssignmentStatement
    assert type(result.children[0].statements[1].expr) == IntLiteral
    assert result.children[0].statements[1].expr.value == 10


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
    assert type(result.children[0]) == Fork
    assert len(result.children[0].statements) == 2
    assert type(result.children[0].statements[0]) == VariableDeclaration
    assert result.children[0].statements[0].name == "calkowita"
    assert type(result.children[0].statements[0].type) == Type
    assert result.children[0].statements[0].type.name == "int"
    assert type(result.children[0].statements[1]) == AssignmentStatement
    assert type(result.children[0].statements[1].expr) == IntLiteral
    assert result.children[0].statements[1].expr.value == 10

    assert len(result.children[1].statements) == 2
    assert type(result.children[1].statements[0]) == VariableDeclaration
    assert result.children[1].statements[0].name == "zmiennoprzecinkowa"
    assert type(result.children[1].statements[0].type) == Type
    assert result.children[1].statements[0].type.name == "float"
    assert type(result.children[1].statements[1]) == AssignmentStatement
    assert type(result.children[1].statements[1].expr) == FloatLiteral
    assert result.children[1].statements[1].expr.value == 3.14

    assert len(result.children[2].statements) == 2
    assert type(result.children[2].statements[0]) == VariableDeclaration
    assert result.children[2].statements[0].name == "napis"
    assert type(result.children[2].statements[0].type) == Type
    assert result.children[2].statements[0].type.name == "str"
    assert type(result.children[2].statements[1]) == AssignmentStatement
    assert type(result.children[2].statements[1].expr) == StrLiteral
    assert result.children[2].statements[1].expr.value == "Ala ma kota."


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
    assert type(result.children[0].type) == Type
    assert result.children[0].type.name == "int"
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
    assert type(result.children[0].attributes[0].type) == Type
    assert result.children[0].attributes[0].type.name == "str"
    assert not result.children[0].attributes[0].is_mutable

    assert type(result.children[0].attributes[1]) == VariableDeclaration
    assert result.children[0].attributes[1].name == "wiek"
    assert type(result.children[0].attributes[1].type) == Type
    assert result.children[0].attributes[1].type.name == "int"
    assert result.children[0].attributes[1].is_mutable

    assert result.children[1].name == "janek"
    assert result.children[1].type.name == "Czlowiek"
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
    assert type(result.children[0]) == Fork
    assert len(result.children[0].statements) == 2
    assert type(result.children[0].statements[0]) == VariableDeclaration
    assert result.children[0].statements[0].name == "ilosc_psow"
    assert result.children[0].statements[0].is_mutable
    assert result.children[0].statements[0].type.name == "int"

    assert type(result.children[0].statements[1]) == AssignmentStatement
    assert result.children[0].statements[1].obj_access == "ilosc_psow"
    assert type(result.children[0].statements[1].expr) == IntLiteral
    assert result.children[0].statements[1].expr.value == 1

    assert type(result.children[1]) == Fork
    assert len(result.children[1].statements) == 2

    # Check the second statement: msg: mut str = 'Ala ma ' + ilosc_psow + ' ps';
    assert type(result.children[1].statements[0]) == VariableDeclaration
    assert result.children[1].statements[0].name == "msg"
    assert result.children[1].statements[0].is_mutable
    assert result.children[1].statements[0].type.name == "str"
    assert type(result.children[1].statements[1]) == AssignmentStatement
    assert result.children[1].statements[1].obj_access == "msg"
    assert type(result.children[1].statements[1].expr) == AddExpr
    assert type(result.children[1].statements[1].expr.children[0]) == StrLiteral
    assert result.children[1].statements[1].expr.children[0].value == "Ala ma "
    assert type(result.children[1].statements[1].expr.children[1]) == ObjectAccess
    assert result.children[1].statements[1].expr.children[1].name_chain == ["ilosc_psow"]
    assert type(result.children[1].statements[1].expr.children[2]) == StrLiteral
    assert result.children[1].statements[1].expr.children[2].value == " ps"

    # Check the if statement
        # Check if condition
    assert type(result.children[2]) == IfStatement
    assert type(result.children[2].cond) == RelationExpr
    assert result.children[2].cond.operator == TokenType.EQUAL
    assert type(result.children[2].cond.left) == ObjectAccess
    assert result.children[2].cond.left.name_chain == ["ilosc_psow"]
    assert type(result.children[2].cond.right) == IntLiteral
    assert result.children[2].cond.right.value == 1
        # Check the if-body
    assert type(result.children[2].prog) == Program
    assert len(result.children[2].prog.children) == 1
    assert type(result.children[2].prog.children[0]) == AssignmentStatement
    assert result.children[2].prog.children[0].obj_access == "msg"
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
    


    assert result.children[3].cond.children[0].operator == TokenType.LESS
    


    assert type(result.children[3].cond.children[0].left) == IntLiteral
    assert result.children[3].cond.children[0].left.value == 1
    assert type(result.children[3].cond.children[0].right) == ObjectAccess
    assert result.children[3].cond.children[0].right.name_chain == ['ilosc_psow']
        # & 
    assert type(result.children[3].cond.children[1]) == RelationExpr
    assert result.children[3].cond.children[1].operator == TokenType.LESS
    assert type(result.children[3].cond.children[1].left) == ObjectAccess
    assert result.children[3].cond.children[1].left.name_chain == ['ilosc_psow']
    assert type(result.children[3].cond.children[1].right) == IntLiteral
    assert result.children[3].cond.children[1].right.value == 5
        # Check the if-body
    assert type(result.children[3].prog) == Program
    assert len(result.children[3].prog.children) == 1
    assert type(result.children[3].prog.children[0]) == AssignmentStatement
    assert result.children[3].prog.children[0].obj_access == "msg"
    assert type(result.children[3].prog.children[0].expr) == AddExpr
    assert type(result.children[3].prog.children[0].expr.children[0]) == ObjectAccess
    assert result.children[3].prog.children[0].expr.children[0].name_chain == ["msg"]
    assert type(result.children[3].prog.children[0].expr.children[1]) == StrLiteral
    assert result.children[3].prog.children[0].expr.children[1].value == "y"

    assert type(result.children[3].else_prog) == Program
    assert len(result.children[3].else_prog.children) == 1
    assert type(result.children[3].else_prog.children[0]) == AssignmentStatement
    assert result.children[3].else_prog.children[0].obj_access == "msg"
    assert type(result.children[3].else_prog.children[0].expr) == AddExpr
    assert type(result.children[3].else_prog.children[0].expr.children[0]) == ObjectAccess
    assert result.children[3].else_prog.children[0].expr.children[0].name_chain == ["msg"]
    assert type(result.children[3].else_prog.children[0].expr.children[1]) == StrLiteral
    assert result.children[3].else_prog.children[0].expr.children[1].value == "ów"

    assert type(result.children[4]) == AssignmentStatement
    assert result.children[4].obj_access == "msg"
    assert type(result.children[4].expr) == AddExpr
    assert type(result.children[4].expr.children[0]) == ObjectAccess
    assert result.children[4].expr.children[0].name_chain == ["msg"]
    assert type(result.children[4].expr.children[1]) == StrLiteral
    assert result.children[4].expr.children[1].value == "."