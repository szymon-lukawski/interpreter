"""Tests position attribute of each parsed ASTNode"""

import pytest

from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *
from parser_exceptions import ParserException, ExpectedDifferentToken
from token_provider import TokenProvider


def test_sanity():
    assert 1 == True


def test_program_pos():
    """while 1 begin\n    a = 1; end"""
    start_of_program_pos = (45,1023)
    tokens = [
        Token(TokenType.WHILE, position=start_of_program_pos),
        Token(TokenType.INT_LITERAL, 1, position=(1, 7)),
        Token(TokenType.BEGIN, position=(1, 8)),
        Token(TokenType.IDENTIFIER, "a", position=(2, 5)),
        Token(TokenType.ASSIGNMENT, position=(2, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 9)),
        Token(TokenType.SEMICOLON, position=(2, 10)),
        Token(TokenType.END, position=(2, 11)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert start_of_program_pos == result.pos



def test_block_pos():
    """Position of block is the position of the first statement within it"""
    start_of_block_pos = (45,1023)
    tokens = [
        Token(TokenType.BEGIN, position=start_of_block_pos),
        Token(TokenType.IDENTIFIER, "a", position=(2, 5)),
        Token(TokenType.ASSIGNMENT, position=(2, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 9)),
        Token(TokenType.SEMICOLON, position=(2, 10)),
        Token(TokenType.END, position=(2, 11)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._parse_block()
    assert (2,5) == result.pos


def test_return_pos():
    """return a;"""
    start_of_program_pos = (45,1023)
    tokens = [
        Token(TokenType.RETURN, position=(2, 11)),
        Token(TokenType.IDENTIFIER, "a" ,position=(2, 12)),
        Token(TokenType.SEMICOLON, position=(2, 13)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_return()
    assert (2, 11) == result.pos

def test_while_pos():
    """while 1 begin\n    a = 1; end"""
    start_of_while_pos = (45,1023)
    tokens = [
        Token(TokenType.WHILE, position=start_of_while_pos),
        Token(TokenType.INT_LITERAL, 1, position=(1, 7)),
        Token(TokenType.BEGIN, position=(1, 8)),
        Token(TokenType.IDENTIFIER, "a", position=(2, 5)),
        Token(TokenType.ASSIGNMENT, position=(2, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 9)),
        Token(TokenType.SEMICOLON, position=(2, 10)),
        Token(TokenType.END, position=(2, 11)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_while_statement()
    assert start_of_while_pos == result.pos



def test_if_pos():
    """if 1 begin\n    a = 1; end"""
    start_of_if_pos = (45,1023)
    tokens = [
        Token(TokenType.IF, position=start_of_if_pos),
        Token(TokenType.INT_LITERAL, 1, position=(1, 7)),
        Token(TokenType.BEGIN, position=(1, 8)),
        Token(TokenType.IDENTIFIER, "a", position=(2, 5)),
        Token(TokenType.ASSIGNMENT, position=(2, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 9)),
        Token(TokenType.SEMICOLON, position=(2, 10)),
        Token(TokenType.END, position=(2, 11)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_if_statement()
    assert start_of_if_pos == result.pos


def test_visit_pos():
    """visit cos.a.x.d begin case I begin x = 2; end case J begin x = 3; end  end
    """
    tokens = [
        Token(TokenType.VISIT, position=(1, 1)),
        Token(TokenType.IDENTIFIER, 'cos', position=(1, 7)),
        Token(TokenType.DOT, position=(1, 10)),
        Token(TokenType.IDENTIFIER, 'a', position=(1, 11)),
        Token(TokenType.DOT, position=(1, 12)),
        Token(TokenType.IDENTIFIER, 'x', position=(1, 13)),
        Token(TokenType.DOT, position=(1, 14)),
        Token(TokenType.IDENTIFIER, 'd', position=(1, 15)),
        Token(TokenType.BEGIN, position=(1, 17)),
        Token(TokenType.CASE, position=(1, 23)),
        Token(TokenType.IDENTIFIER, 'I', position=(1, 28)),
        Token(TokenType.BEGIN, position=(1, 30)),
        Token(TokenType.IDENTIFIER, 'x', position=(1, 36)),
        Token(TokenType.ASSIGNMENT, position=(1, 38)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 40)),
        Token(TokenType.SEMICOLON, position=(1, 41)),
        Token(TokenType.END, position=(1, 43)),
        Token(TokenType.CASE, position=(1, 47)),
        Token(TokenType.IDENTIFIER, 'J', position=(1, 52)),
        Token(TokenType.BEGIN, position=(1, 54)),
        Token(TokenType.IDENTIFIER, 'x', position=(1, 60)),
        Token(TokenType.ASSIGNMENT, position=(1, 62)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 64)),
        Token(TokenType.SEMICOLON, position=(1, 65)),
        Token(TokenType.END, position=(1, 67)),
        Token(TokenType.END, position=(1, 72)),
        Token(TokenType.EOT, position=(2, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser._try_parse_visit_statement()
    
    assert result.pos == (1,1)


def test_pos_of_diff_starting_with_identifier():
    """x : int = 1; y(x, 12); z(x: int, y: float): int begin end A : struct begin end V : variant begin end
    """
    tokens = [
        Token(TokenType.IDENTIFIER, 'x', position=(1, 1)),
        Token(TokenType.COLON, position=(1, 3)),
        Token(TokenType.INT, position=(1, 5)),
        Token(TokenType.ASSIGNMENT, position=(1, 9)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 11)),
        Token(TokenType.SEMICOLON, position=(1, 12)),
        Token(TokenType.IDENTIFIER, 'y', position=(1, 14)),
        Token(TokenType.LEFT_BRACKET, position=(1, 15)),
        Token(TokenType.IDENTIFIER, 'x', position=(1, 16)),
        Token(TokenType.COMMA, position=(1, 17)),
        Token(TokenType.INT_LITERAL, 12, position=(1, 19)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 21)),
        Token(TokenType.SEMICOLON, position=(1, 22)),
        Token(TokenType.IDENTIFIER, 'z', position=(1, 24)),
        Token(TokenType.LEFT_BRACKET, position=(1, 25)),
        Token(TokenType.IDENTIFIER, 'x', position=(1, 26)),
        Token(TokenType.COLON, position=(1, 27)),
        Token(TokenType.INT, position=(1, 29)),
        Token(TokenType.COMMA, position=(1, 32)),
        Token(TokenType.IDENTIFIER, 'y', position=(1, 34)),
        Token(TokenType.COLON, position=(1, 35)),
        Token(TokenType.FLOAT, position=(1, 37)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 42)),
        Token(TokenType.COLON, position=(1, 43)),
        Token(TokenType.INT, position=(1, 45)),
        Token(TokenType.BEGIN, position=(1, 49)),
        Token(TokenType.END, position=(1, 55)),
        Token(TokenType.IDENTIFIER, 'A', position=(1, 59)),
        Token(TokenType.COLON, position=(1, 61)),
        Token(TokenType.STRUCT, position=(1, 63)),
        Token(TokenType.BEGIN, position=(1, 70)),
        Token(TokenType.END, position=(1, 76)),
        Token(TokenType.IDENTIFIER, 'V', position=(1, 80)),
        Token(TokenType.COLON, position=(1, 82)),
        Token(TokenType.VARIANT, position=(1, 84)),
        Token(TokenType.BEGIN, position=(1, 92)),
        Token(TokenType.END, position=(1, 98)),
        Token(TokenType.EOT, position=(2, 5)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()

    simple_var_decl_pos = result.children[0].pos
    assert simple_var_decl_pos == (1,1)
    func_call_pos = result.children[1].pos
    assert func_call_pos == (1,14)
    func_def_pos = result.children[2].pos
    assert func_def_pos == (1,24)
    struct_def_pos = result.children[3].pos
    assert struct_def_pos == (1,59)
    variant_def_pos = result.children[4].pos
    assert variant_def_pos == (1,80)