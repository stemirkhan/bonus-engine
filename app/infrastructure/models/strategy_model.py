from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field
from .common import PyObjectId


class StrategyRule(BaseModel):
    rule_id: PyObjectId = Field(..., alias="rule_id")
    order: int
    enabled: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class StrategyModel(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    name: str
    description: str | None = None
    rules: List[StrategyRule]
    enabled: bool = True
    is_default: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
