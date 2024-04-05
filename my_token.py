"""."""

from token_type import TokenType

class MyToken:
    """."""

    def __init__(self, token_type: TokenType, token_value=None) -> None:
        self.type = token_type
        self.value = token_value

    def __eq__(self, __value: object) -> bool:
        # __value should be of type MyToken
        return self.type.value == __value.type.value and self.value == __value.value
