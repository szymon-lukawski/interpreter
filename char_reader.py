"""."""

class CharReader:
    """
    Abstract class for reading source char by char
    while tracking position of the current character
    """

    def __init__(self):
        self.char: str
        self._row : int = 1
        self._col : int = 0

    def next_char(self):
        """Advances to next char in source"""
        self._next_char()
        if self.char is None:
            return
        if self.char == '\n':
            self._col = 0
            self._row +=1
        else:
            self._col += 1

    def get_position(self):
        """Returns position of current char in source"""
        return self._row, self._col

    def _next_char(self):
        return ""

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
