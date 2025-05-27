from app.exceptions.base import BonusCalculationBaseError


class StrategyNotFoundError(BonusCalculationBaseError):
    def __init__(self, message: str = "Strategy not found."):
        super().__init__(message)


class RuleNotFoundError(BonusCalculationBaseError):
    def __init__(self, message: str = "One or more rules referenced by the strategy are missing."):
        super().__init__(message)


class BonusCalculationError(BonusCalculationBaseError):
    def __init__(self, message: str = "An error occurred during bonus calculation."):
        super().__init__(message)


class MissingRuleDefinitionError(BonusCalculationBaseError):
    def __init__(self, rule_id: str):
        super().__init__(f"Rule definition for rule_id '{rule_id}' is missing.")


class InvalidContextDataError(BonusCalculationBaseError):
    def __init__(self, key: str):
        super().__init__(f"Missing or invalid context data for key: '{key}'.")


class RuleApplicationError(BonusCalculationBaseError):
    def __init__(self, rule_code: str, message: str = "Error applying rule."):
        super().__init__(f"Rule '{rule_code}': {message}")


class BaseRuleTypeRequiredError(BonusCalculationBaseError):
    def __init__(self):
        super().__init__("The first rule in the strategy must be of type 'base'.")


class ModifierRuleTypeRequiredError(BonusCalculationBaseError):
    def __init__(self, rule_code: str):
        super().__init__(f"Rule '{rule_code}' must have type 'modifier'.")
