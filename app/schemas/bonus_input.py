from pydantic import BaseModel, Field
from datetime import datetime


class BonusCalculationRequest(BaseModel):
    transaction_amount: float = Field(..., gt=0)
    timestamp: datetime
    customer_status: str
