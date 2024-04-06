"""."""

from string import digits, ascii_letters
from keywords import KEYWORDS_STRS


def is_identifier_body(char: str):
    """Brutal full scan, can be improved when using built ins or using chr and ord"""
    return char in digits or char in ascii_letters


def is_value_a_keyword(value: str):
    """."""
    # KEYSWORDS_STRS could be sorted to improve efficiency
    return value in KEYWORDS_STRS
