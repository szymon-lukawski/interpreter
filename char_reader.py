"""."""

from typing import List, Dict
from enum import Enum
import string


class TokenType(Enum):
    """-"""

    IDENTIFIER = 1
    STR_LITERAL = 2
    FLOAT_LITERAL = 3
    INT_LITERAL = 4
    NULL = 5
    COMMENT = 6
    MUT = 7
    INT = 8
    FLOAT = 9
    STR = 10
    NULL_TYPE = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    RETURN = 15
    PRINT = 16
    READ = 17
    LEFT_BRACKET = 18
    RIGHT_BRACKET = 19
    SEMICOLON = 20
    COLON = 21
    PLUS = 22
    MINUS = 23
    TIMES = 24
    DIVIDE = 25
    DOT = 26
    ASSIGNMENT = 27
    LESS = 28
    GREATER = 29
    OR = 30
    AND = 31
    LESS_EQUAL = 32
    EQUAL = 33
    INEQUAL = 34
    GREATER_EQUAL = 35
    BEGIN = 36
    END = 37
    STRUCT = 38
    VARIANT = 39
    VISIT = 40
    CASE = 41


KEYWORDS_TO_TOKEN_TYPE: Dict[str, TokenType] = {
    "null": TokenType.NULL,
    "mut": TokenType.MUT,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "str": TokenType.STR,
    "null_type": TokenType.NULL_TYPE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "print": TokenType.PRINT,
    "read": TokenType.READ,
    "end": TokenType.END,
    "begin": TokenType.BEGIN,
    "struct": TokenType.STRUCT,
    "variant": TokenType.VARIANT,
    "visit": TokenType.VISIT,
    "case": TokenType.CASE,
}

KEYWORDS_STRS = list(KEYWORDS_TO_TOKEN_TYPE.keys())


class Token:
    """."""

    def __init__(self, token_type: TokenType, token_value=None) -> None:
        self.type = token_type
        self.value = token_value

    def __eq__(self, __value: object) -> bool:
        # __value should be of type Token
        return self.type.value == __value.type.value and self.value == __value.value


class CharReader:
    """
    Abstract class for reading source char by char
    while tracking position of the current character
    """

    def __init__(self):
        self.char: str

    def next_char(self):
        """Advances to next char in source"""
        self._next_char()

    def get_position(self):
        """Returns position of current char in source"""

    def _next_char(self):
        return ''

    def get_next_char(self):
        """Advances one char and returns it"""
        self._next_char()
        return self.char


class StringReader(CharReader):
    """CharReader that source is text python's string literal"""

    def __init__(self, string_literal: str):
        super().__init__()
        self.string_literal = string_literal
        self.idx = 0

    def _next_char(self):
        if self.idx < len(self.string_literal):
            self.char = self.string_literal[self.idx]
            self.idx += 1
            return
        self.char = None


class Lexer:
    """Lexer"""

    STRING_LITERAL_DELIMITER = "'"
    STRING_ESCAPE = "\\"

    def __init__(self, reader: CharReader) -> None:
        self.reader = reader
        self.reader.next_char()

        self.curr_token = None
        self._end_token_in_place = False

    def get_next_token(self):
        """Returns next token from reader"""
        self._next_token()
        return self.curr_token

    def _next_token(self):
        if self._end_token_in_place:
            return

        self._skip_whitespaces()

        if self._is_end_of_file():
            self.curr_token = Token(TokenType.END)
            return
        
        self._parse_token()

    def _parse_token(self):

        char = self.reader.char
        if char == Lexer.STRING_LITERAL_DELIMITER:
            self._parse_string_literal()
        elif char in string.ascii_letters:
            self._parse_keyword_or_identifier()
        elif char in string.digits:
            self._parse_number()
        else:
            self._parse_other()

    def _parse_string_literal(self):
        string_literal_value: List[str] = []

        char = self.reader.get_next_char()
        is_escaped = char == Lexer.STRING_ESCAPE

        while char != Lexer.STRING_LITERAL_DELIMITER or is_escaped:
            string_literal_value.append(char)
            char = self.reader.get_next_char()
            is_escaped = char == Lexer.STRING_ESCAPE

        string_literal_value = "".join(string_literal_value)

        if string_literal_value in KEYWORDS_STRS:
            return Token(KEYWORDS_TO_TOKEN_TYPE[string_literal_value])
        
        self.curr_token = Token(TokenType.STR_LITERAL, string_literal_value)

    def _parse_keyword_or_identifier(self):
        pass

    def _parse_number(self):
        pass

    def _parse_other(self):
        pass

    def _is_end_of_file(self):
        return self.reader.char is None

    def _skip_whitespaces(self):
        while not self._is_end_of_file() and self.reader.char.isspace():
            self.reader.next_char()
