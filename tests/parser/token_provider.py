from lexer.lexer import Lexer
from lexer.my_token import Token
from lexer.token_type import TokenType

class TokenProvider(Lexer):
    """Mocks lexer."""

    def __init__(self, _, list_of_tokens) -> None:
        self.tokens = list_of_tokens
        self.idx = -1
        self._EOT_token_in_place = False
        super().__init__(_)

    def _next_token(self):
        if self._EOT_token_in_place:
            return
        if self._is_end_of_file():
            self.curr_token = Token(TokenType.EOT)
            self._EOT_token_in_place = True
            return
        self.idx += 1
        self.curr_token = self.tokens[self.idx]

    def _is_end_of_file(self):
        return self.idx + 2 > len(self.tokens)