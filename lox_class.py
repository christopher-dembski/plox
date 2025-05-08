from typing import Sequence, Dict

from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def call(self, interpreter, arguments: Sequence[object]) -> object:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def find_method(self, name: str):
        return self.methods.get(name, None)

    def __repr__(self):
        return self.name
