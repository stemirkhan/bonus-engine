from datetime import datetime

from app.interfaces.condition_interface import ConditionI
from app.domain.conditions.condition_context import ConditionContext
from app.domain.conditions.register import condition_registry


@condition_registry("is_holiday")
class IsHolidayCondition(ConditionI):
    def evaluate(self, context: ConditionContext) -> bool:
        timestamp = context.input_data.get("timestamp")

        if not timestamp:
            return False

        return timestamp.date() in context.holidays
