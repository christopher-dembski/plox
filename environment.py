from typing import Dict

from lox_token import Token
from runtime_exception import RuntimeException


class Environment:

    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values: Dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def ancestor(self, distance: int):
        environment = self
        for i in range(0, distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance: int, name: str) -> object:
        return self.ancestor(distance).values.get(name, None)

    def assign_at(self, distance: int, name: Token, value: object):
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeException(name, f'Undefined variable {name.lexeme}.')

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise RuntimeException(name, f'Undefined variable {name.lexeme}.')
