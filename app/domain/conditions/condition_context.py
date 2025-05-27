from pydantic import BaseModel
from typing import Any, Dict, List
from datetime import date


class ConditionContext(BaseModel):
    input_data: Dict[str, Any]
    holidays: List[date] = []
