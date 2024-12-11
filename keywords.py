"""."""

from typing import Dict
from token_type import TokenType

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
    # "print": TokenType.PRINT,
    # "read": TokenType.READ,
    "end": TokenType.END,
    "begin": TokenType.BEGIN,
    "struct": TokenType.STRUCT,
    "variant": TokenType.VARIANT,
    "visit": TokenType.VISIT,
    "case": TokenType.CASE,
}

KEYWORDS_STRS = KEYWORDS_TO_TOKEN_TYPE.keys()
