
from app.domain.conditions.condition_context import ConditionContext
from app.domain.conditions.register import condition_registry
from app.interfaces.condition_interface import ConditionI

@condition_registry("customer_status")
class CustomerStatusCondition(ConditionI):
    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context: ConditionContext) -> bool:
        return context.input_data.get("customer_status") == self.value
