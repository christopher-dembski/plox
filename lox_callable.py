from abc import ABC, abstractmethod
from typing import Sequence


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: Sequence[object]) -> object:
        pass
