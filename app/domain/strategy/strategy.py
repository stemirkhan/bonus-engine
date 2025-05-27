from app.domain.conditions.condition_context import ConditionContext
from app.exceptions import BaseRuleTypeRequiredError, ModifierRuleTypeRequiredError
from app.interfaces.strategy_interface import StrategyI
from app.domain.rule.rule import Rule


class BonusStrategy(StrategyI):
    def __init__(self, data: dict, rule_lookup: dict[str, dict]):
        sorted_rules_info = sorted(data.get("rules", []), key=lambda ri: ri.get("order", 0))

        self.rules = [
            Rule(rule_lookup[str(rule_info["rule_id"])])
            for rule_info in sorted_rules_info
            if str(rule_info["rule_id"]) in rule_lookup
        ]

    def apply(self, context: ConditionContext) -> dict:
        applied_rules = []


        if not self.rules:
            return {
                "total_bonus": 0.0,
                "applied_rules": applied_rules
            }

        if self.rules[0].type != "base":
            raise BaseRuleTypeRequiredError()

        base_rule = self.rules[0]
        bonus = base_rule.apply(context.input_data['transaction_amount'])
        applied_rules.append({
            "rule": base_rule.code,
            "bonus": bonus
        })

        sum_bonus = bonus

        for rule in self.rules[1:]:
            if rule.type == "base":
                raise BaseRuleTypeRequiredError()

            if rule.is_applicable(context):
                bonus = rule.apply(sum_bonus)
                applied_rules.append({
                    "rule": rule.code,
                    "bonus": bonus
                })
                sum_bonus += bonus

        return {
            "total_bonus":  sum_bonus,
            "applied_rules": applied_rules
        }
