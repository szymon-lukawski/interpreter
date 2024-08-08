"""Parser exceptions"""

from my_token import PositionType
from token_type import TokenType

class ParserException(Exception):
    """Base class for all Parser related errors"""

    def __init__(self, position: PositionType = (None, None)):
        self.row, self.col = position
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}"



class ExpectedDifferentToken(ParserException):
    """Got different token than expected"""
    def __init__(self, position: PositionType = (None, None), msg = None):
        self.row, self.col = position
        self.msg = msg

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.msg}"

class PatternNotRecognised(ParserException):
    """While building new statement, starting pattern was not recognised."""