"""Parser exceptions"""

from my_token import PositionType

class ParserException(Exception):
    """Base class for all Lexer related errors"""

    def __init__(self, position: PositionType = (None, None)):
        self.row, self.col = position
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}"

