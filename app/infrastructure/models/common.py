from bson import ObjectId
from pydantic import GetJsonSchemaHandler, ValidationInfo, BeforeValidator
from pydantic import BaseModel, Field
from typing import Any

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, info: ValidationInfo) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: dict, handler: GetJsonSchemaHandler) -> dict:
        # Отмечаем, что в JSON-схеме это будет string
        return {'type': 'string', 'format': 'objectid'}
