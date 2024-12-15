"""Token exceptions"""

from lexer.my_token import PositionType


class MyTokenException(Exception):
    """Base class for all Lexer related errors"""

    def __init__(self, position: PositionType = (None, None)):
        self.row, self.col = position
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}"


class UnrecognisedStartOfToken(MyTokenException):
    """Encountered character that no token starts with!"""


class IdentifierCanNotStartWithUnderscore(MyTokenException):
    """While building new token first char was '_'. Identifiers can not start with '_'!"""


class StringLiteralError(MyTokenException):
    """Error when building string literal token"""


class StringLiteralNotEnded(StringLiteralError):
    """Got newline or end of text while building string literal"""


class UseOfQuotationMarksIsInvalid(StringLiteralError):
    """Use apostrophe (') instead of quotattion mark (") to mark boundaries of string literal."""


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

    def __init__(self, position: PositionType = (None, None), limit: int = 30):
        self.row, self.col = position
        self.limit = limit
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}: row: {self.row}, column: {self.col}, {self.__doc__}: {self.limit}"


class IntLiteralTooBig(NumberLiteralTooManyChars):
    """Int char limit is"""


class FloatLiteralTooBig(NumberLiteralTooManyChars):
    """Float char limit is"""


class DigitRequiredAfterDot(NumberError):
    """When building float literal, there has to be at least one digit after a dot"""


class InvalidCharInIdentifier(MyTokenException):
    """Identifier body can only consist of letterz a-z, A-Z, digits and _."""


class PrecidingZerosError(NumberError):
    """Putting additional zeros to the left of number literal is not allowed. 0 is ok, so is 0.1 so is 0.0001. 01 is  not. 00.1 is not"""


class IdentifierTooLong(MyTokenException):
    """self explanatory"""
