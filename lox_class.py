from typing import Sequence, Dict

from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def call(self, interpreter, arguments: Sequence[object]) -> object:
        return LoxInstance(self)

    def arity(self) -> int:
        return 0

    def find_method(self, name: str):
        return self.methods.get(name, None)

    def __repr__(self):
        return self.name
