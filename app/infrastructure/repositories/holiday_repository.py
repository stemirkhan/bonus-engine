from datetime import date
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.interfaces.holiday_repository_interface import HolidayRepositoryI


class HolidayRepository(HolidayRepositoryI):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["holidays"]

    async def get_all_dates(self) -> List[date]:
        cursor = self.collection.find({}, {"date": 1, "_id": 0})
        docs = await cursor.to_list(length=None)
        return [doc["date"] for doc in docs if "date" in doc]
