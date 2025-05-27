from app.infrastructure.mongo_unit_of_work import MongoUnitOfWork
from app.services.bonus_strategy_service import BonusStrategyService
from app.db.mongo import mongo_client, mongo_db



async def get_bonus_strategy_service() -> BonusStrategyService:
    uow = MongoUnitOfWork(client=mongo_client, mongo_db=mongo_db)
    return BonusStrategyService(uow=uow)
