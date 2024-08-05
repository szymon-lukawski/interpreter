"""Module for CharReader with filter"""
from char_reader import CharReader

class CharNotValidError(Exception):
    """Error when FilterReader current char is not in valid chars"""

class FilterReader(CharReader):
    """Lets through only  abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+/?,.<>|'\"\\ newline and tab chars"""
    valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+/?,.<>|'\"\\\n\t")

    def __init__(self, char_reader : CharReader) -> None:
        self._char_reader = char_reader
        self._validate_curr_char()

    def next_char(self):
        self._char_reader.next_char()
        self._validate_curr_char()

    def get_next_char(self):
        char = self._char_reader.get_next_char()
        self._validate_curr_char()
        return char
    
    def get_curr_char(self):
        return self._char_reader.get_curr_char()
    
    def get_position(self):
        return self._char_reader.get_position()

    def _validate_curr_char(self):
        if self._char not in FilterReader.valid_chars and self._char != '':
            raise CharNotValidError(f"Char: {self._char} is not valid!")