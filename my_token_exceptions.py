"""Token exceptions"""
from typing import Tuple
from my_token import PositionType

class MyTokenException(Exception):
    """Base class for all Lexer related errors"""
    def __init__(self, msg, position : PositionType):
        self.message = msg if msg else "Can not tokenise this input"
        self.row, self.col = position
        super().__init__()

    def __str__(self):
        return f"MyTokenException: row: {self.row}, column: {self.col}, {self.message}"
    
