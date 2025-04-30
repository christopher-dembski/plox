from typing import Sequence

from environment import Environment
from lox_callable import LoxCallable
from stmt import FunctionStmt


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt):
        self.declaration = declaration

    def call(self, interpreter, arguments: Sequence[object]) -> object:
        environment = Environment(interpreter.globals)
        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)
        interpreter.execute_block(self.declaration.body, environment)
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
