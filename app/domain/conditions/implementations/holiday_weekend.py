from datetime import datetime


from app.domain.conditions.condition_context import ConditionContext
from app.domain.conditions.register import condition_registry
from app.interfaces.condition_interface import ConditionI

@condition_registry("holiday_weekend")
class IsHolidayWeekendCondition(ConditionI):
    def evaluate(self, context: ConditionContext) -> bool:
        timestamp = context.input_data.get("timestamp")

        if not timestamp:

            return False

        return timestamp.weekday() >= 5 or timestamp.date() in context.holidays
