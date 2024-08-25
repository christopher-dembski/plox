from token_type import TokenType


class Token:

    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f'Token(type:{self.type}, lexeme:{self.lexeme}, literal:{self.literal}, line:{self.line})'

    def __eq__(self, other):
        return (self.type == other.type and
                self.lexeme == other.lexeme and
                self.literal == other.literal and
                self.line == other.line)
