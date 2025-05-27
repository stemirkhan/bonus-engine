from app.domain.conditions.condition_context import ConditionContext
from app.interfaces.rule_interface import RuleI
from app.domain.conditions.factory import ConditionFactory
from app.domain.formulas import FormulaFactory


class Rule(RuleI):
    def __init__(self, data: dict):
        self._id = data.get("_id")
        self.code = data["code"]
        self.name = data["name"]
        self.description = data.get("description", "")
        self.type = data.get("type", "base")
        self.enabled = data.get("enabled", True)

        self.formula = FormulaFactory.create(data["formula"])

        self.conditions = [
            ConditionFactory.create(condition)
            for condition in data.get("conditions", [])
        ]

    def is_applicable(self, context: ConditionContext) -> bool:
        return all(condition.evaluate(context) for condition in self.conditions)

    def apply(self, value: float) -> float:
        return self.formula.calculate(value)
