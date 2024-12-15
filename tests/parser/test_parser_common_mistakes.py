"""Token streams that are mistaken."""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck


import pytest

from lexer.token_type import TokenType
from lexer.my_token import Token
from parser.my_parser import Parser
from lexer.lexer import Lexer
from parser.AST import *
from parser.parser_exceptions import ParserException, ExpectedDifferentToken
from token_provider import TokenProvider


def test_sanity():
    assert 1 == True


def test_python_like_while():
    """while 1:\n    a = 1;"""
    tokens = [
        Token(TokenType.WHILE, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 7)),
        Token(TokenType.COLON, position=(1, 8)),
        Token(TokenType.IDENTIFIER, "a", position=(2, 5)),
        Token(TokenType.ASSIGNMENT, position=(2, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(2, 9)),
        Token(TokenType.SEMICOLON, position=(2, 10)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser._try_parse_while_statement()

    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 8, Expected block"
    )


def test_cpp_like_incrementation():
    """i++;"""
    tokens = [
        Token(TokenType.IDENTIFIER, "i", position=(1, 1)),
        Token(TokenType.PLUS, position=(1, 2)),
        Token(TokenType.PLUS, position=(1, 3)),
        Token(TokenType.SEMICOLON, position=(1, 4)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 2, Expected: . = : ("
    )


def test_missing_left_bracket():
    """if a + 2+b)*3 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 4)),
        Token(TokenType.PLUS, position=(1, 6)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 8)),
        Token(TokenType.PLUS, position=(1, 9)),
        Token(TokenType.IDENTIFIER, "b", position=(1, 10)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 11)),
        Token(TokenType.TIMES, position=(1, 12)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 13)),
        Token(TokenType.BEGIN, position=(1, 15)),
        Token(TokenType.END, position=(1, 21)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 11, Expected block"
    )


def test_expr_missing_right_bracket():
    """if a + (2+b*3 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 4)),
        Token(TokenType.PLUS, position=(1, 6)),
        Token(TokenType.LEFT_BRACKET, position=(1, 8)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 9)),
        Token(TokenType.PLUS, position=(1, 10)),
        Token(TokenType.IDENTIFIER, "b", position=(1, 11)),
        Token(TokenType.TIMES, position=(1, 12)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 13)),
        Token(TokenType.BEGIN, position=(1, 15)),
        Token(TokenType.END, position=(1, 21)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 15, Expected token type: TokenType.RIGHT_BRACKET"
    )


def test_expr_empty_brackets():
    """if a + ()2+b*3 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 4)),
        Token(TokenType.PLUS, position=(1, 6)),
        Token(TokenType.LEFT_BRACKET, position=(1, 8)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 9)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 10)),
        Token(TokenType.PLUS, position=(1, 11)),
        Token(TokenType.IDENTIFIER, "b", position=(1, 12)),
        Token(TokenType.TIMES, position=(1, 13)),
        Token(TokenType.INT_LITERAL, 3, position=(1, 14)),
        Token(TokenType.BEGIN, position=(1, 16)),
        Token(TokenType.END, position=(1, 22)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 9, Expected literal, object access or nested expression"
    )


def test_no_multi_expr_after_minus_operator():
    """if a -+ 1 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 4)),
        Token(TokenType.MINUS, position=(1, 6)),
        Token(TokenType.PLUS, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 9)),
        Token(TokenType.BEGIN, position=(1, 11)),
        Token(TokenType.END, position=(1, 17)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 7, Expected literal, object access or nested expression"
    )


def test_no_unary_expr_after_multi_operator():
    """if a */ 1 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 4)),
        Token(TokenType.TIMES, position=(1, 6)),
        Token(TokenType.DIVIDE, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 9)),
        Token(TokenType.BEGIN, position=(1, 11)),
        Token(TokenType.END, position=(1, 17)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 7, Expected literal, object access or nested expression"
    )


def test_plus_one():
    """+1"""
    tokens = [
        Token(TokenType.PLUS, position=(1, 1)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 2)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser._parse_add_expr()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 1, Expected literal, object access or nested expression"
    )


def test_right_part_of_relation_expression():
    """if a <+ 1 begin end"""
    tokens = [
        Token(TokenType.IF, position=(1, 1)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 4)),
        Token(TokenType.LESS, position=(1, 6)),
        Token(TokenType.PLUS, position=(1, 7)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 9)),
        Token(TokenType.BEGIN, position=(1, 11)),
        Token(TokenType.END, position=(1, 17)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    with pytest.raises(ExpectedDifferentToken) as e_info:
        parser.parse_program()
    assert (
        str(e_info.value)
        == "ExpectedDifferentToken: row: 1, column: 7, Expected literal, object access or nested expression"
    )
