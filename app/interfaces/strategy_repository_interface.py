from abc import ABC, abstractmethod

from app.infrastructure.models import StrategyModel


class StrategyRepositoryI(ABC):
    @abstractmethod
    async def get_default(self) -> StrategyModel:
        raise NotImplementedError
