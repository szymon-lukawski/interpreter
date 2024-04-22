"""Lexer class"""

import string
from typing import List, Tuple

from token_type import TokenType
from keywords import KEYWORDS_STRS, KEYWORDS_TO_TOKEN_TYPE
from char_reader import CharReader
from my_token import Token, PositionType
from my_token_exceptions import (
    MyTokenException,
    StringLiteralNotEnded,
    EscapingWrongChar,
    ExclamationMarkError,
    IntLiteralTooBig,
    FloatLiteralTooBig,
    InvalidCharsInNumberLiteral,
    PrecidingZerosError,
    NumberLiteralTooBig,
    IdentifierTooLong,
)

from utils import is_identifier_body, is_value_a_keyword


class Lexer:
    """Lexer"""

    STRING_LITERAL_DELIMITER = "'"
    STRING_ESCAPE = "\\"
    INT_LIMIT = 10**8 - 1
    FLOAT_CHAR_LIMIT = 20
    IDENTIFIER_LEN_LIMIT = 100

    def __init__(self, reader: CharReader, INT_LIMIT=10**8 - 1) -> None:
        Lexer.INT_LIMIT = INT_LIMIT

        self.reader = reader

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
            self.curr_token = Token(
                TokenType.EOT, position=self.reader.get_position()
            )
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
                self.curr_token = Token(TokenType.COMMA, position=pos)
            case "(":
                self.reader.next_char()
                self.curr_token = Token(TokenType.LEFT_BRACKET, position=pos)
            case ")":
                self.reader.next_char()
                self.curr_token = Token(TokenType.RIGHT_BRACKET, position=pos)
            case ";":
                self.reader.next_char()
                self.curr_token = Token(TokenType.SEMICOLON, position=pos)
            case ":":
                self.reader.next_char()
                self.curr_token = Token(TokenType.COLON, position=pos)
            case ".":
                self.reader.next_char()
                self.curr_token = Token(TokenType.DOT, position=pos)
            case "&":
                self.reader.next_char()
                self.curr_token = Token(TokenType.AND, position=pos)
            case "|":
                self.reader.next_char()
                self.curr_token = Token(TokenType.OR, position=pos)
            case "+":
                self.reader.next_char()
                self.curr_token = Token(TokenType.PLUS, position=pos)
            case "-":
                self.reader.next_char()
                self.curr_token = Token(TokenType.MINUS, position=pos)
            case "*":
                self.reader.next_char()
                self.curr_token = Token(TokenType.TIMES, position=pos)
            case "/":
                self.reader.next_char()
                self.curr_token = Token(TokenType.DIVIDE, position=pos)
            case "<":
                self._try_parse_two_char_operator(
                    TokenType.LESS, TokenType.LESS_EQUAL, position=pos
                )
            case ">":
                self._try_parse_two_char_operator(
                    TokenType.GREATER, TokenType.GREATER_EQUAL, position=pos
                )
            case "=":
                self._try_parse_two_char_operator(
                    TokenType.ASSIGNMENT, TokenType.EQUAL, position=pos
                )
            case "!":
                char = self.reader.get_next_char()
                if char != "=":
                    raise ExclamationMarkError(position=pos)
                self.reader.next_char()
                self.curr_token = Token(TokenType.INEQUAL, position=pos)
            case _:
                raise MyTokenException(position=pos)

    def _try_parse_two_char_operator(
        self, if_one_char: TokenType, if_two_chars: TokenType, position: Tuple[int, int]
    ):
        char = self.reader.get_next_char()
        if char == "=":
            self.reader.next_char()
            self.curr_token = Token(if_two_chars, position=position)
            return
        self.curr_token = Token(if_one_char, position=position)

    def _parse_string_literal(self, position: PositionType):
        string_literal_value: List[str] = []

        char = self.reader.get_next_char()
        if char == '' or char == "\n":
            raise StringLiteralNotEnded(self.reader.get_position())
        is_escaped = char == Lexer.STRING_ESCAPE

        # TODO add proper handling of other escaped characters

        while char != Lexer.STRING_LITERAL_DELIMITER or is_escaped:
            if is_escaped:
                char = self.reader.get_next_char()
                if char == "t":
                    string_literal_value.append("\t")
                elif char == "n":
                    string_literal_value.append("\n")
                elif char == Lexer.STRING_ESCAPE:
                    string_literal_value.append(Lexer.STRING_ESCAPE)
                elif char == Lexer.STRING_LITERAL_DELIMITER:
                    string_literal_value.append(Lexer.STRING_LITERAL_DELIMITER)
                else:
                    raise EscapingWrongChar(self.reader.get_position())
                char = self.reader.get_next_char()
            else:
                string_literal_value.append(char)
                char = self.reader.get_next_char()
            if char == '' or char == "\n":
                raise StringLiteralNotEnded(self.reader.get_position())
            is_escaped = char == Lexer.STRING_ESCAPE

        self.reader.next_char()
        string_literal_value = "".join(string_literal_value)

        if string_literal_value in KEYWORDS_STRS:
            self.curr_token = Token(
                KEYWORDS_TO_TOKEN_TYPE[string_literal_value], position
            )

        self.curr_token = Token(TokenType.STR_LITERAL, string_literal_value, position)

    def _parse_keyword_or_identifier(self, position: Tuple[int, int]):
        self._parse_identifier(position)

        if is_value_a_keyword(self.curr_token.value):
            self.curr_token.type = KEYWORDS_TO_TOKEN_TYPE[self.curr_token.value]
            self.curr_token.value = None

    def _parse_identifier(self, position: Tuple[int, int]):
        buffer: List[str] = []
        char = self.reader.char
        buffer.append(char)
        char = self.reader.get_next_char()

        while (
            char != ''
            and is_identifier_body(char)
            and len(buffer) <= Lexer.IDENTIFIER_LEN_LIMIT
        ):
            buffer.append(char)
            char = self.reader.get_next_char()
        if len(buffer) > Lexer.IDENTIFIER_LEN_LIMIT:
            raise IdentifierTooLong(position=position)

        value = "".join(buffer)

        self.curr_token = Token(TokenType.IDENTIFIER, value, position)

    def _parse_number(self, position: PositionType):
        char_counter = 1
        value = int(self.reader.char)
        char = self.reader.get_next_char()
        if value == 0 and char == "0":
            raise PrecidingZerosError(position=position)

        value = self._try_build_number(value, char_counter)
        char = self.reader.char
        if char != ".":
            if value > Lexer.INT_LIMIT:
                raise IntLiteralTooBig(position)
            self.curr_token = Token(TokenType.INT_LITERAL, value, position)
            return

        char = self.reader.get_next_char()
        if char == '' or not char.isdigit():
            raise InvalidCharsInNumberLiteral(position)

        int_part_len = len(str(value))
        value = value * 10 + int(char)
        char = self.reader.get_next_char()
        counter = 1
        char_counter += 1
        value = self._try_build_number(value, char_counter)
        total_len = len(str(value))
        if total_len >= Lexer.FLOAT_CHAR_LIMIT:
            raise FloatLiteralTooBig(position=position)
        counter = total_len - int_part_len
        self.curr_token = Token(
            TokenType.FLOAT_LITERAL, value / (10**counter), position
        )

    def _try_build_number(self, value, char_counter):
        char = self.reader.char
        while char != '' and char.isdigit():
            char_counter += 1
            value = value * 10 + int(char)
            char = self.reader.get_next_char()
        return value

    def _parse_comment(self, position: Tuple[int, int]):
        self.reader.next_char()
        comment_value: List[str] = []

        char = self.reader.char

        while char != "\n":
            comment_value.append(char)
            char = self.reader.get_next_char()

        comment_value = "".join(comment_value)

        self.curr_token = Token(TokenType.COMMENT, comment_value, position)

    def _is_end_of_file(self):
        return self.reader.char == ''

    def _skip_whitespaces(self):
        while not self._is_end_of_file() and self.reader.char.isspace():
            self.reader.next_char()
