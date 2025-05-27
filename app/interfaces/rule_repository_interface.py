from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.models import RuleModel
from app.infrastructure.models.common import PyObjectId


class RuleRepositoryI(ABC):
    @abstractmethod
    async def get_by_id(self, rule_id: str) -> RuleModel:
        raise NotImplementedError

    @abstractmethod
    async def get_many_by_ids(self, ids: List[PyObjectId]) -> List[RuleModel]:
        raise NotImplementedError
