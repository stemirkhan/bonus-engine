from abc import ABC, abstractmethod



class ConditionI(ABC):
    @abstractmethod
    def evaluate(self, context: object) -> bool:
        raise NotImplementedError
