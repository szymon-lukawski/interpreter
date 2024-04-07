"""Lexer class"""

import string
from typing import List

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
        char = self.reader.char
        match char:
            case Lexer.STRING_LITERAL_DELIMITER:
                self._parse_string_literal()
            case _ if char in string.ascii_letters:
                self._parse_keyword_or_identifier()
            case _ if char in string.digits:
                self._parse_number()
            case "@":
                self._parse_comment()
            case ",":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.COMMA)
            case "(":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.LEFT_BRACKET)
            case ")":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.RIGHT_BRACKET)
            case ";":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.SEMICOLON)
            case ":":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.COLON)
            case ".":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.DOT)
            case "&":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.AND)
            case "|":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.OR)
            case "+":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.PLUS)
            case "-":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.MINUS)
            case "*":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.TIMES)
            case "/":
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.DIVIDE)
            case "<":
                self._try_parse_two_char_operator(TokenType.LESS, TokenType.LESS_EQUAL)
            case ">":
                self._try_parse_two_char_operator(TokenType.GREATER, TokenType.GREATER_EQUAL)
            case "=":
                self._try_parse_two_char_operator(TokenType.ASSIGNMENT, TokenType.EQUAL)
            case "!":
                char = self.reader.get_next_char()
                if char != "=":
                    raise MyTokenException(f"Expected `=` but got `{char}`")
                self.reader.next_char()
                self.curr_token = MyToken(TokenType.INEQUAL)
            case _:
                raise MyTokenException("Can not tokenize this!")


    def _try_parse_two_char_operator(
        self, if_one_char: TokenType, if_two_chars: TokenType
    ):
        char = self.reader.get_next_char()
        if char == "=":
            self.reader.next_char()
            self.curr_token = MyToken(if_two_chars)
            return
        self.curr_token = MyToken(if_one_char)

    def _parse_string_literal(self):
        string_literal_value: List[str] = []

        char = self.reader.get_next_char()
        if char is None:
            raise MyTokenException("String literal not properly ended!")
        is_escaped = char == Lexer.STRING_ESCAPE

        # TODO add proper handling of other escaped characters

        while char != Lexer.STRING_LITERAL_DELIMITER or is_escaped:
            string_literal_value.append(char)
            char = self.reader.get_next_char()
            if char is None:
                raise MyTokenException("String literal not properly ended!")
            is_escaped = char == Lexer.STRING_ESCAPE

        self.reader.next_char()
        string_literal_value = "".join(string_literal_value)

        if string_literal_value in KEYWORDS_STRS:
            self.curr_token = MyToken(KEYWORDS_TO_TOKEN_TYPE[string_literal_value])

        self.curr_token = MyToken(TokenType.STR_LITERAL, string_literal_value)

    def _parse_keyword_or_identifier(self):
        self._parse_identifier()

        if is_value_a_keyword(self.curr_token.value):
            self.curr_token.type = KEYWORDS_TO_TOKEN_TYPE[self.curr_token.value]
            self.curr_token.value = None

    def _parse_identifier(self):
        # TODO Add limit to identifier length
        buffer: List[str] = []
        char = self.reader.char
        if char in string.ascii_letters:
            buffer.append(char)
            char = self.reader.get_next_char()
        else:
            raise MyTokenException("Identifier can not start with non ascii letter")
        while char is not None and is_identifier_body(char):
            buffer.append(char)
            char = self.reader.get_next_char()

        value = "".join(buffer)

        self.curr_token = MyToken(TokenType.IDENTIFIER, value)

    def _parse_number(self):
        # TODO add limit to float
        value = int(self.reader.char)
        char = self.reader.get_next_char()

        while char is not None and char.isdigit():
            if value > Lexer.INT_LIMIT:
                raise MyTokenException("INT LITERAL value to big")
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
                    TokenType.FLOAT_LITERAL, value / (10**counter)
                )
            else:
                raise MyTokenException("Float literal has to have a digit after dot")
        else:
            self.curr_token = MyToken(TokenType.INT_LITERAL, value)

    def _parse_comment(self):
        self.reader.next_char()
        comment_value: List[str] = []

        char = self.reader.char

        while char != "\n":
            comment_value.append(char)
            char = self.reader.get_next_char()

        comment_value = "".join(comment_value)

        self.curr_token = MyToken(TokenType.COMMENT, comment_value)

    def _is_end_of_file(self):
        return self.reader.char is None

    def _skip_whitespaces(self):
        while not self._is_end_of_file() and self.reader.char.isspace():
            self.reader.next_char()
