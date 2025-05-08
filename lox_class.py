from typing import Sequence

from lox_callable import LoxCallable
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str):
        self.name = name

    def call(self, interpreter, arguments: Sequence[object]) -> object:
        return LoxInstance(self)

    def arity(self) -> int:
        return 0

    def __repr__(self):
        return self.name
