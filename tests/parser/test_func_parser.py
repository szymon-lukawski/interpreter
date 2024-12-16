from lexer.token_type import TokenType
from lexer.my_token import Token
from parser.my_parser import Parser
from lexer.lexer import Lexer
from parser.AST import *
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


