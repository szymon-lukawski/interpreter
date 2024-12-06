from token_type import TokenType
from my_token import Token
from my_parser import Parser
from lexer import Lexer
from AST import *
from token_provider import TokenProvider


def test_func_one_arg():
    """add_one(a : int) : int begin return a + 1; end"""
    tokens = [
        Token(TokenType.IDENTIFIER, "add_one", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 8)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 9)),
        Token(TokenType.COLON, position=(1, 11)),
        Token(TokenType.INT, position=(1, 13)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 16)),
        Token(TokenType.COLON, position=(1, 18)),
        Token(TokenType.INT, position=(1, 20)),
        Token(TokenType.BEGIN, position=(1, 24)),
        Token(TokenType.RETURN, position=(1, 30)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 37)),
        Token(TokenType.PLUS, position=(1, 39)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 41)),
        Token(TokenType.SEMICOLON, position=(1, 42)),
        Token(TokenType.END, position=(1, 44)),
    ]

    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert result == Program(
        [
            FuncDef(
                "add_one",
                [Param("a", "int", False)],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"])
                        )
                    ]
                ),
            )
        ]
    )


def test_rec_fib():
    """fib(n) : int begin if n < 2 begin return 1; end return fib(n-1) + fib(n-2); end a : int = fib(8);"""
    tokens = [
        Token(TokenType.IDENTIFIER, "fib", position=(1, 1)),
        Token(TokenType.LEFT_BRACKET, position=(1, 4)),
        Token(TokenType.IDENTIFIER, "n", position=(1, 5)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 6)),
        Token(TokenType.COLON, position=(1, 8)),
        Token(TokenType.INT, position=(1, 10)),
        Token(TokenType.BEGIN, position=(1, 14)),
        Token(TokenType.IF, position=(1, 20)),
        Token(TokenType.IDENTIFIER, "n", position=(1, 23)),
        Token(TokenType.LESS, position=(1, 25)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 27)),
        Token(TokenType.BEGIN, position=(1, 29)),
        Token(TokenType.RETURN, position=(1, 35)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 42)),
        Token(TokenType.SEMICOLON, position=(1, 43)),
        Token(TokenType.END, position=(1, 45)),
        Token(TokenType.RETURN, position=(1, 49)),
        Token(TokenType.IDENTIFIER, "fib", position=(1, 56)),
        Token(TokenType.LEFT_BRACKET, position=(1, 59)),
        Token(TokenType.IDENTIFIER, "n", position=(1, 60)),
        Token(TokenType.MINUS, position=(1, 61)),
        Token(TokenType.INT_LITERAL, 1, position=(1, 62)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 63)),
        Token(TokenType.PLUS, position=(1, 65)),
        Token(TokenType.IDENTIFIER, "fib", position=(1, 67)),
        Token(TokenType.LEFT_BRACKET, position=(1, 70)),
        Token(TokenType.IDENTIFIER, "n", position=(1, 71)),
        Token(TokenType.MINUS, position=(1, 72)),
        Token(TokenType.INT_LITERAL, 2, position=(1, 73)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 74)),
        Token(TokenType.SEMICOLON, position=(1, 75)),
        Token(TokenType.END, position=(1, 77)),
        Token(TokenType.IDENTIFIER, "a", position=(1, 81)),
        Token(TokenType.COLON, position=(1, 83)),
        Token(TokenType.INT, position=(1, 85)),
        Token(TokenType.ASSIGNMENT, position=(1, 89)),
        Token(TokenType.IDENTIFIER, "fib", position=(1, 91)),
        Token(TokenType.LEFT_BRACKET, position=(1, 94)),
        Token(TokenType.INT_LITERAL, 8, position=(1, 95)),
        Token(TokenType.RIGHT_BRACKET, position=(1, 96)),
        Token(TokenType.SEMICOLON, position=(1, 97)),
    ]
    lexer = TokenProvider(None, tokens)
    parser = Parser(lexer)
    result = parser.parse_program()
    assert 1
