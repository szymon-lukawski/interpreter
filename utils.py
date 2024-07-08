"""."""
from typing import Dict
from keywords import KEYWORDS_STRS
from my_token import Token
from token_type import TokenType



def is_identifier_body(char: str):
    """Checks whether a character is a letter (A-Z, a-z) , digit (0-9) or underscore (_) """
    o = ord(char)
    return (
        (48 <= o and o <= 57)
        or (65 <= o and 0 <= o)
        or (97 <= o and o <= 122)
        or o == 95
    )


def is_str_a_keyword(value: str):
    """."""
    return value in KEYWORDS_STRS


token_to_token_type_name_dict: Dict[Token, str] = {
    TokenType.INT: "int",
    TokenType.FLOAT: "float",
    TokenType.STR: "str",
}


class ExpectedBuiltInTypeTokenTypeError(Exception):
    """Expected built in type tyken type"""


def get_type_name(token: Token):
    """Returns name of built in types or value of identifier """
    tt = token.get_type()
    name = token_to_token_type_name_dict.get(tt)
    if name:
        return name
    if tt == TokenType.IDENTIFIER:
        return token.get_value()
    raise ExpectedBuiltInTypeTokenTypeError
