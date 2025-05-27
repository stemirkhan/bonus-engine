from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.interfaces.rule_repository_interface import RuleRepositoryI
from app.infrastructure.models import RuleModel



class RuleRepository(RuleRepositoryI):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["rules"]

    async def get_by_id(self, rule_id: str) -> RuleModel:
        doc = await self.collection.find_one({"_id": ObjectId(rule_id)})
        return RuleModel(**doc)

    async def get_many_by_ids(self, ids: List[str]) -> List[RuleModel]:
        object_ids = [ObjectId(id_) for id_ in ids]
        cursor = self.collection.find({"_id": {"$in": object_ids}})
        docs = await cursor.to_list(length=None)
        return [RuleModel(**doc) for doc in docs]
