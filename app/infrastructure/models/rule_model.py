from typing import List, Literal

from bson import ObjectId
from pydantic import BaseModel, Field

from .common import PyObjectId


class RuleModel(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    code: str
    name: str
    description: str | None = None
    type: Literal["base", "modifier"]
    conditions: List[dict] = Field(default_factory=list)
    formula: dict

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
