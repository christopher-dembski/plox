import time
from typing import Sequence

from lox_callable import LoxCallable


class Clock(LoxCallable):
    def arity(self) -> int:
        pass

    def call(self, interpreter, arguments: Sequence[object]) -> object:
        return time.time()

    def __str__(self):
        return f'<foreign fn: clock>'
