"""."""

from typing import Tuple
from copy import copy
from token_type import TokenType


RowType = int
ColumnType = int
PositionType = Tuple[RowType, ColumnType]

tokentypes_should_none_value = set(TokenType.__members__.values())

tokentypes_should_none_value.remove(TokenType.IDENTIFIER)
tokentypes_should_none_value.remove(TokenType.STR_LITERAL)
tokentypes_should_none_value.remove(TokenType.FLOAT_LITERAL)
tokentypes_should_none_value.remove(TokenType.INT_LITERAL)
tokentypes_should_none_value.remove(TokenType.COMMENT)


class ValueShouldBeNoneError(Exception):
    '''.'''


class Token:
    """Token has type, optional value and position in source"""

    def __init__(
        self, token_type: TokenType, token_value=None, position: PositionType = None
    ) -> None:
        self.__type = None
        self.__value = None
        self.__pos = None
        self.set_token_attrs(token_type, token_value, position)

    def _check_definite_none_value(self):
        if self.__type in tokentypes_should_none_value and not self.__value is None:
            raise ValueShouldBeNoneError

    def set_token_attrs(
        self, token_type: TokenType, token_value=None, position: PositionType = None
    ):
        '''Allows to change atrributes of token instance'''
        self.__type = token_type
        self.__value = token_value
        self.__pos = position
        self._check_definite_none_value()

    def get_value(self):
        """Returns copy of the value of the token. Encapsulation preserved"""
        return copy(self.__value)
    
    def set_value_and_type(self, token_type: TokenType, token_value=None):
        '''Allows to change just value and type of token instance'''
        self.__type = token_type
        self.__value = token_value
        self._check_definite_none_value()

    def get_type(self):
        """Returns copy of token type"""
        return copy(self.__type)
    
    def get_pos(self):
        """Returns copy of position"""
        return copy(self.__pos)
    
    def set_pos(self, new_pos: PositionType):
        """Allows to set postion attribute. Used mainly in testing"""
        self.__pos = new_pos

    def __eq__(self, __value: object) -> bool:
        # __value should be of type Token
        return (
            self.__type.value == __value.get_type().value
            and self.__value == __value.get_value()
            and self.__pos == __value.get_pos()
        )


if __name__ == '__main__':
    print(tokentypes_should_none_value)