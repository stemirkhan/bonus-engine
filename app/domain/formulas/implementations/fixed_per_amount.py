from app.interfaces import FormulaI
from app.domain.formulas.register import formula_registry


@formula_registry("fixed_per_amount")
class FixedPerAmountFormula(FormulaI):
    def __init__(self, per_amount: float, bonus: float):
        self.per_amount = per_amount
        self.bonus = bonus

    def calculate(self, value: float) -> float:
        if self.per_amount <= 0:
            return 0
        return (value // self.per_amount) * self.bonus
