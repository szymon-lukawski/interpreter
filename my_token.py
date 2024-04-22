"""."""

from token_type import TokenType
from typing import Tuple

RowType = int
ColumnType = int
PositionType = Tuple[RowType, ColumnType]


class Token:
    """Token has type, optional value and position in source"""

    def __init__(
        self, token_type: TokenType, token_value=None, position: PositionType = None
    ) -> None:
        self.type = token_type
        self.value = token_value
        self.pos = position

    def __eq__(self, __value: object) -> bool:
        # __value should be of type Token
        return (
            self.type.value == __value.type.value
            and self.value == __value.value
            and self.pos == __value.pos
        )
