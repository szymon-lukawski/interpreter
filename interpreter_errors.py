"""Errors raised by interpreter or scopes classes"""



class InterpreterError(Exception):
    """Class for all Interpreter related errors"""

    def __init__(self, position, msg : str):
        self.row, self.col = position
        self.msg = msg
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.msg}"
