from abc import ABC, abstractmethod
from io import StringIO

class CharReader(ABC):
    """
    Abstract class for reading source char by char
    while tracking position of the current character
    """

    def __init__(self):
        self.char: str
        self._row: int = 1
        self._col: int = 1

    def next_char(self):
        """Advances to next char in source"""
        self._update_position()
        self._next_char()


    def get_position(self):
        """Returns position of current char in source"""
        return self._row, self._col

    @abstractmethod
    def _next_char(self):
        pass
    
    def _update_position(self):
        if self.char == '':
            return
        if self.char == '\n':
            self._col = 1
            self._row += 1
        else:
            self._col += 1

    def get_next_char(self):
        """Advances one char and returns it"""
        self.next_char()
        return self.char


class StringReader(CharReader):
    """CharReader that source is text python's string literal"""

    def __init__(self, string_literal: StringIO):
        super().__init__()
        self.string_io = string_literal
        self.string_io.seek(0)
        self._next_char()

    def _next_char(self):
        self.char = self.string_io.read(1)
