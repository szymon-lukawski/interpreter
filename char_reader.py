from abc import ABC, abstractmethod
from io import TextIOBase

class CharReader(ABC):
    """
    Abstract class for reading source char by char
    while tracking position of the current character
    """

    def __init__(self):
        self._char: str
        self._row: int = 1
        self._col: int = 1

    def next_char(self):
        """Advances to next char in source"""
        self._update_position()
        self._next_char()


    def get_position(self):
        """Returns position of current char in source"""
        return self._row+0, self._col+0
    
    def get_curr_char(self):
        """Returns current char"""
        return self._char

    @abstractmethod
    def _next_char(self):
        pass
    
    def _update_position(self):
        if self._char == '':
            return
        if self._char == '\n':
            self._col = 1
            self._row += 1
        else:
            self._col += 1

    def get_next_char(self):
        """Advances one char and returns it"""
        self.next_char()
        return self._char


class TextIOReader(CharReader):
    """CharReader that works with any TextIOBase"""

    def __init__(self, text_io: TextIOBase):
        super().__init__()
        self.text_io = text_io
        self._next_char()

    def _next_char(self):
        self._char = self.text_io.read(1)
