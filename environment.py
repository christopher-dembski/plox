from typing import Dict

from lox_token import Token
from runtime_exception import RuntimeException


class Environment:

    def __init__(self):
        self.values: Dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme not in self.values:
            raise RuntimeException(name, f'Undefined variable {name.lexeme}.')
        return self.values[name.lexeme]
