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
    IdentifierTooLong,
    IdentifierCanNotStartWithUnderscore,
    NumberLiteralTooManyChars,
    EscapingEOT
)

from utils import is_identifier_body, is_str_a_keyword


class Lexer:
    """Lexer"""

    STRING_LITERAL_DELIMITER = "'"
    STRING_ESCAPE = "\\"
    INT_LIMIT = 10**8 - 1
    FLOAT_CHAR_LIMIT = 20
    IDENTIFIER_LEN_LIMIT = 100

    def __init__(self, reader: CharReader) -> None:
        self.reader = reader

        self.curr_token = None
        # pylint: disable=C0103:invalid-name
        self._EOT_token_in_place = False

        self.NUMBER_CHAR_LIMIT = 30

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
        char = self.reader.get_curr_char()
        pos = self.reader.get_position()
        match char:
            case Lexer.STRING_LITERAL_DELIMITER:
                self._parse_string_literal(pos)
            case _ if char in string.ascii_letters:
                self._parse_keyword_or_identifier(pos)
            case _ if char in string.digits:
                self._parse_number(pos)
            case "_":
                raise IdentifierCanNotStartWithUnderscore(position=pos)
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
        char = self.reader.get_next_char()
        if char == '' or char == "\n":
            raise StringLiteralNotEnded(self.reader.get_position())


        
        
        string_literal_value = self._parse_str_literal_value()
        if string_literal_value in KEYWORDS_STRS:
            self.curr_token = Token(
                KEYWORDS_TO_TOKEN_TYPE[string_literal_value], position
            )

        self.curr_token = Token(TokenType.STR_LITERAL, string_literal_value, position)

    def _parse_str_literal_value(self):
        string_literal_value: List[str] = []
        char = self.reader.get_curr_char()
        is_escaped = char == Lexer.STRING_ESCAPE
        while char != Lexer.STRING_LITERAL_DELIMITER or is_escaped:
            if is_escaped:
                self._parse_escaped_char(string_literal_value)
            else:
                string_literal_value.append(char)
            char = self.reader.get_next_char()
            if char == '' or char == "\n":
                raise StringLiteralNotEnded(self.reader.get_position())
            is_escaped = char == Lexer.STRING_ESCAPE
        self.reader.next_char()
        return "".join(string_literal_value)
    
    def _parse_escaped_char(self, string_literal_buffer : List[str]):
        match self.reader.get_next_char():
            case "t":
                string_literal_buffer.append("\t")
            case "n":
                string_literal_buffer.append("\n")
            case Lexer.STRING_ESCAPE:
                string_literal_buffer.append(Lexer.STRING_ESCAPE)
            case Lexer.STRING_LITERAL_DELIMITER:
                string_literal_buffer.append(Lexer.STRING_LITERAL_DELIMITER)
            case "":
                raise EscapingEOT(self.reader.get_position())
            case _:
                raise EscapingWrongChar(self.reader.get_position())
        

    def _parse_keyword_or_identifier(self, position: PositionType):
        self._parse_identifier(position)
        token_value = self.curr_token.get_value()
        if is_str_a_keyword(token_value):
            self.curr_token.set_value_and_type(KEYWORDS_TO_TOKEN_TYPE[token_value], None)

    def _parse_identifier(self, position: PositionType):
        buffer: List[str] = []
        buffer.append(self.reader.get_curr_char())
        value = self._parse_identifier_body(buffer, position)
        self.curr_token = Token(TokenType.IDENTIFIER, value, position)


    def _parse_identifier_body(self, buffer : List[str], pos : PositionType):
        char = self.reader.get_next_char()
        while (
            char != ''
            and is_identifier_body(char)
            and len(buffer) <= Lexer.IDENTIFIER_LEN_LIMIT
        ):
            buffer.append(char)
            char = self.reader.get_next_char()
        if len(buffer) > Lexer.IDENTIFIER_LEN_LIMIT:
            raise IdentifierTooLong(position=pos)
        return "".join(buffer)


    def _parse_number(self, position: PositionType):
        first_digit_value = int(self.reader.get_curr_char())
        self._check_for_preciding_zeros(first_digit_value, position)
        char_counter = 1
        value, char_counter = self._try_build_number(first_digit_value, char_counter, position)
        if self.reader.get_curr_char() != ".":
            self.curr_token = Token(TokenType.INT_LITERAL, value, position)
            return
        char = self.reader.get_next_char()
        if char == '' or not char in string.digits:
            raise InvalidCharsInNumberLiteral(position)
        int_part_len = char_counter + 0
        value, char_counter = self._try_build_number(value, char_counter, position)
        self.curr_token = Token(
            TokenType.FLOAT_LITERAL, value / (10**(char_counter - int_part_len)), position
        )

    def _check_for_preciding_zeros(self, first_digit_value, pos):
        char = self.reader.get_next_char()
        if first_digit_value == 0 and char == "0":
            raise PrecidingZerosError(position=pos)

    def _try_build_number(self, value : int, char_counter : int, pos : PositionType):
        char = self.reader.get_curr_char()
        while char != '' and char in string.digits and char_counter <= self.NUMBER_CHAR_LIMIT:
            char_counter += 1
            value = value * 10 + int(char)
            char = self.reader.get_next_char()
        if char_counter > self.NUMBER_CHAR_LIMIT:
            raise NumberLiteralTooManyChars(pos, self.NUMBER_CHAR_LIMIT)
        return value, char_counter

    def _parse_comment(self, position: Tuple[int, int]):
        self.reader.next_char()
        comment_value: List[str] = []

        char = self.reader.get_curr_char()

        while char != "\n":
            comment_value.append(char)
            char = self.reader.get_next_char()

        comment_value = "".join(comment_value)

        self.curr_token = Token(TokenType.COMMENT, comment_value, position)

    def _is_end_of_file(self):
        return self.reader.get_curr_char() == ''

    def _skip_whitespaces(self):
        while not self._is_end_of_file() and self.reader.get_curr_char().isspace():
            self.reader.next_char()
