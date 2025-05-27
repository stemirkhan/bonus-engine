from motor.motor_asyncio import AsyncIOMotorDatabase

from app.interfaces.strategy_repository_interface import StrategyRepositoryI
from app.infrastructure.models.strategy_model import StrategyModel



class StrategyRepository(StrategyRepositoryI):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["strategies"]

    async def get_default(self) -> StrategyModel:
        doc = await self.collection.find_one({"is_default": True, "enabled": True})
        if not doc:
            raise ValueError("Default strategy not found.")
        return StrategyModel(**doc)
