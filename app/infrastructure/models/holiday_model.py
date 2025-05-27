from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from bson import ObjectId
from .common import PyObjectId

class HolidayModel(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    date: date
    name: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
