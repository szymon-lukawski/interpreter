"""Token exceptions"""

from my_token import PositionType


class MyTokenException(Exception):
    """Base class for all Lexer related errors"""

    def __init__(self, position: PositionType = (None, None)):
        self.row, self.col = position
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}"


class IdentifierCanNotStartWithUnderscore(MyTokenException):
    """While building new token first char was '_'. Identifiers can not start with '_'!"""

class StringLiteralError(MyTokenException):
    """Error when building string literal token"""


class StringLiteralNotEnded(StringLiteralError):
    """Got newline or end of text while building string literal"""


class EscapingWrongChar(StringLiteralError):
    """Valid escaping chars are \\, t, n, '"""

class EscapingEOT(StringLiteralError):
    """Received end of text instead of \\, t, n, '"""



class ExclamationMarkError(MyTokenException):
    """Exclamation mark is used only with equal sign. There can not be whitespace"""


class NumberError(MyTokenException):
    """Error when building number token"""

class NumberLiteralTooBig(NumberError):
    """Number literal has a limit"""

class NumberLiteralTooManyChars(NumberError):
    """Number literals have a limit. Sum of digits of integer part and fractional part can not exceed"""
    def __init__(self, position: PositionType = (None, None), limit : int = 30):
        self.row, self.col = position
        self.limit = limit
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}: {self.limit}"
class IntLiteralTooBig(NumberError):
    """Int limit is set to {Lexer.INT_LIMIT}"""

class FloatLiteralTooBig(NumberError):
    """Float char limit is set to {Lexer.FLOAT_LIMIT}"""

class InvalidCharsInNumberLiteral(NumberError):
    """When building number literal there can only be digits 0-9"""

# TODO add int and float limits to doc strings...

class PrecidingZerosError(NumberError):
    """There can only be one preciding zero in number literal"""

class IdentifierTooLong(MyTokenException):
    """self explanatory"""