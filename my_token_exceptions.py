"""Token exceptions"""
from typing import Tuple
from my_token import PositionType

class MyTokenException(Exception):
    """Base class for all Lexer related errors"""
    def __init__(self, position : PositionType = (None, None
                                                  ), msg: str = "Can not tokenise this input"):
        self.message = msg
        self.row, self.col = position
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}"
    


class StringLiteralError(MyTokenException):
    """Error when building string literal token"""

class StringLiteralNotEnded(StringLiteralError):
    """Got newline or end of text while building string literal"""

class EscapingWrongChar(StringLiteralError):
    """."""