from typing import Dict
from app.interfaces.unit_of_work_interface import UnitOfWorkI
from app.schemas.bonus_input import BonusCalculationRequest
from app.domain.strategy.strategy import BonusStrategy
from app.domain.conditions.condition_context import ConditionContext
from app.exceptions import (
    BonusCalculationBaseError,
    StrategyNotFoundError,
    RuleNotFoundError,
    BonusCalculationError,
)


class BonusStrategyService:
    def __init__(self, uow: UnitOfWorkI):
        self.uow = uow

    async def calculate_bonus(self, data: BonusCalculationRequest) -> Dict:
        try:
            async with self.uow:
                strategy_data = await self.uow.strategy_repo.get_default()
                if not strategy_data:
                    raise StrategyNotFoundError()

                rule_ids = [r.rule_id for r in strategy_data.rules]
                rules_data = await self.uow.rule_repo.get_many_by_ids(rule_ids)
                if not rules_data:
                    raise RuleNotFoundError()

                holidays = await self.uow.holiday_repo.get_all_dates()

            rule_lookup = {str(rule.id): rule.dict() for rule in rules_data}

            strategy = BonusStrategy(strategy_data.dict(), rule_lookup)

            context = ConditionContext(
                input_data=data.model_dump(),
                holidays=holidays
            )

            return strategy.apply(context)

        except BonusCalculationBaseError:
            raise
        except Exception as e:
            raise BonusCalculationError(f"Unexpected error during bonus calculation: {e}") from e
