from fastapi import APIRouter, Depends

from app.schemas.bonus_input import BonusCalculationRequest
from app.services.bonus_strategy_service import BonusStrategyService
from app.dependencies.get_bonus_strategy_service import get_bonus_strategy_service

router = APIRouter()


@router.post("/calculate-bonus")
async def calculate_bonus(
    data: BonusCalculationRequest,
    service: BonusStrategyService = Depends(get_bonus_strategy_service),
):
    result = await service.calculate_bonus(data)
    return result
