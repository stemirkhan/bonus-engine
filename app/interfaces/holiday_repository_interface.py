from datetime import date
from typing import List
from abc import ABC, abstractmethod


class HolidayRepositoryI(ABC):
    @abstractmethod
    async def get_all_dates(self) -> List[date]:
        raise NotImplementedError
