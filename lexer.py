"""Lexer class"""

import string
from typing import List, Tuple

from token_type import TokenType
from keywords import KEYWORDS_STRS, KEYWORDS_TO_TOKEN_TYPE
from char_reader import CharReader
from my_token import MyToken
from my_token_exceptions import MyTokenException

from utils import is_identifier_body, is_value_a_keyword


class Lexer:
    """Lexer"""

    STRING_LITERAL_DELIMITER = "'"
    STRING_ESCAPE = "\\"
    INT_LIMIT = 10**8 - 1

    def __init__(self, reader: CharReader, INT_LIMIT=10**8 - 1) -> None:
        Lexer.INT_LIMIT = INT_LIMIT

        self.reader = reader
        self.reader.next_char()

        self.curr_token = None
        self._EOT_token_in_place = False

    def get_next_token(self):
        """Returns next my_token from reader"""
        self._next_token()
        return self.curr_token

    def _next_token(self):
        if self._EOT_token_in_place:
            return

        self._skip_whitespaces()

        if self._is_end_of_file():
            self.curr_token = MyToken(TokenType.EOT)
            return

        self._parse_token()

    def _parse_token(self):
        #
        char = self.reader.char
        pos = self.reader.get_position()
        match char:
            case Lexer.STRING_LITERAL_DELIMITER:
                self._parse_string_literal(pos)
            case _ if char in string.ascii_letters:
                self._parse_keyword_or_identifier(pos)
            case _ if char in string.digits:
                self._parse_number(pos)
            case "@":
                self._parse_comment(pos)
            case ",":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.COMMA, position=pos)
            case "(":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.LEFT_BRACKET, position=pos)
            case ")":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.RIGHT_BRACKET, position=pos)
            case ";":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.SEMICOLON, position=pos)
            case ":":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.COLON, position=pos)
            case ".":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.DOT, position=pos)
            case "&":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.AND, position=pos)
            case "|":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.OR, position=pos)
            case "+":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.PLUS, position=pos)
            case "-":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.MINUS, position=pos)
            case "*":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.TIMES, position=pos)
            case "/":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.DIVIDE, position=pos)
            case "<":
                self._try_parse_two_char_operator(TokenType.LESS, TokenType.LESS_EQUAL, position=pos)
            case ">":
                self._try_parse_two_char_operator(TokenType.GREATER, TokenType.GREATER_EQUAL, position=pos)
            case "=":
                self._try_parse_two_char_operator(TokenType.ASSIGNMENT, TokenType.EQUAL, position=pos)
            case "!":
                char = self.reader.get_next_char()
                if char != "=":
                    raise MyTokenException(f"Expected `=` but got `{char}`", position=pos)
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.INEQUAL, position=pos)
            case _:
                raise MyTokenException(None, position=pos)


    def _try_parse_two_char_operator(
        self, if_one_char: TokenType, if_two_chars: TokenType, position : Tuple[int,int]
    ):
        char = self.reader.get_next_char()
        if char == "=":
            self.reader.next_char()
            self.curr_token = MyToken(if_two_chars, position=position)
            return
        self.curr_token = MyToken(if_one_char, position=position)

    def _parse_string_literal(self, position : Tuple[int,int]):
        string_literal_value: List[str] = []

        char = self.reader.get_next_char()
        if char is None or char == '\n':
            raise MyTokenException("String literal not properly ended!", position=position)
        is_escaped = char == Lexer.STRING_ESCAPE

        # TODO add proper handling of other escaped characters

        while char != Lexer.STRING_LITERAL_DELIMITER or is_escaped:
            if is_escaped:
                char = self.reader.get_next_char()
                if char == 't':
                    string_literal_value.append('\t')
                elif char == 'n':
                    string_literal_value.append('\n')
                elif char == Lexer.STRING_ESCAPE:
                    string_literal_value.append(Lexer.STRING_ESCAPE)
                elif char == Lexer.STRING_LITERAL_DELIMITER:
                    string_literal_value.append(Lexer.STRING_LITERAL_DELIMITER)
                else:
                    raise MyTokenException("Escaping wrong character in string literal", position)
                char = self.reader.get_next_char()
            else:
                string_literal_value.append(char)
                char = self.reader.get_next_char()
            if char is None or char == '\n':
                raise MyTokenException("String literal not properly ended!", position)
            is_escaped = char == Lexer.STRING_ESCAPE

        self.reader.next_char()
        string_literal_value = "".join(string_literal_value)

        if string_literal_value in KEYWORDS_STRS:
            self.curr_token = MyToken(KEYWORDS_TO_TOKEN_TYPE[string_literal_value],position)

        self.curr_token = MyToken(TokenType.STR_LITERAL, string_literal_value,position)

    def _parse_keyword_or_identifier(self, position: Tuple[int,int]):
        self._parse_identifier(position)

        if is_value_a_keyword(self.curr_token.value):
            self.curr_token.type = KEYWORDS_TO_TOKEN_TYPE[self.curr_token.value]
            self.curr_token.value = None

    def _parse_identifier(self, position: Tuple[int,int]):
        # TODO Add limit to identifier length
        buffer: List[str] = []
        char = self.reader.char
        if char in string.ascii_letters:
            buffer.append(char)
            char = self.reader.get_next_char()
        else:
            raise MyTokenException("Identifier can not start with non ascii letter", position)
        while char is not None and is_identifier_body(char):
            buffer.append(char)
            char = self.reader.get_next_char()

        value = "".join(buffer)

        self.curr_token = MyToken(TokenType.IDENTIFIER, value, position)

    def _parse_number(self, position: Tuple[int,int]):
        # TODO add limit to float
        value = int(self.reader.char)
        char = self.reader.get_next_char()

        while char is not None and char.isdigit():
            if value > Lexer.INT_LIMIT:
                raise MyTokenException("INT LITERAL value to big", position)
            value = value * 10 + int(char)
            char = self.reader.get_next_char()

        if char == ".":
            char = self.reader.get_next_char()
            if char is not None and char.isdigit():
                value = value * 10 + int(char)
                char = self.reader.get_next_char()
                counter = 1
                while char is not None and char.isdigit():
                    value = value * 10 + int(char)
                    char = self.reader.get_next_char()
                    counter += 1
                self.curr_token = MyToken(
                    TokenType.FLOAT_LITERAL, value / (10**counter), position
                )
            else:
                raise MyTokenException("Float literal has to have a digit after dot", position)
        else:
            self.curr_token = MyToken(TokenType.INT_LITERAL, value,  position)

    def _parse_comment(self, position: Tuple[int, int ]):
        self.reader.next_char()
        comment_value: List[str] = []

        char = self.reader.char

        while char != "\n":
            comment_value.append(char)
            char = self.reader.get_next_char()

        comment_value = "".join(comment_value)

        self.curr_token = MyToken(TokenType.COMMENT, comment_value,position)

    def _is_end_of_file(self):
        return self.reader.char is None

    def _skip_whitespaces(self):
        while not self._is_end_of_file() and self.reader.char.isspace():
            self.reader.next_char()
