from typing import Dict

from lox_token import Token
from runtime_exception import RuntimeException


class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields: Dict[str, object] = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method
        raise RuntimeException(name, f"Undefined property '{name.lexeme}'.")

    def __repr__(self):
        return f'{self.klass.name} instance'
