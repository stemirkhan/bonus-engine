from abc import ABC, abstractmethod


class RuleI(ABC):
    @abstractmethod
    async def is_applicable(self, context: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def apply(self, value: float) -> float:
        raise NotImplementedError
