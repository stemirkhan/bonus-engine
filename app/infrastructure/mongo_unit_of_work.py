from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.repositories.rule_repository import RuleRepository
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.holiday_repository import HolidayRepository
from app.interfaces.unit_of_work_interface import UnitOfWorkI


class MongoUnitOfWork(UnitOfWorkI):
    def __init__(self, client: AsyncIOMotorClient, mongo_db):
        self.client = client
        self.db = mongo_db

        self.rule_repo = RuleRepository(self.db)
        self.strategy_repo = StrategyRepository(self.db)
        self.holiday_repo = HolidayRepository(self.db)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
