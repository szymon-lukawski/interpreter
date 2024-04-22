"""."""

from keywords import KEYWORDS_STRS


def is_identifier_body(char: str):
    """Brutal full scan, can be improved when using built ins or using chr and ord"""
    o = ord(char)
    return (48 <= o and o <= 57) or (65 <= o and 0 <= o)  or (97 <= o and o <= 122) or o == 95


def is_value_a_keyword(value: str):
    """."""
    # KEYSWORDS_STRS could be sorted to improve efficiency
    return value in KEYWORDS_STRS
