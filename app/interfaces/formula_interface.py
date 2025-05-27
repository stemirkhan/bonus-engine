from abc import ABC, abstractmethod


class FormulaI(ABC):
    @abstractmethod
    def calculate(self, value: float) -> float:
        raise NotImplementedError
