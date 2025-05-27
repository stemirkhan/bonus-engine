from abc import ABC, abstractmethod

from app.interfaces.holiday_repository_interface import HolidayRepositoryI
from app.interfaces.rule_repository_interface import RuleRepositoryI
from app.interfaces.strategy_repository_interface import StrategyRepositoryI


class UnitOfWorkI(ABC):
    strategy_repo: StrategyRepositoryI
    rule_repo: RuleRepositoryI
    holiday_repo: HolidayRepositoryI

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError("UnitOfWorkI must implement __aenter__ method")

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplemented("UnitOfWorkI must implement __aexit__ method")
