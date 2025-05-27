from app.interfaces import FormulaI
from app.domain.formulas.register import formula_registry


@formula_registry("multiplier")
class MultiplierFormula(FormulaI):
    def __init__(self, multiplier: float):
        self.multiplier = multiplier

    def calculate(self, value: float) -> float:
        print(value * self.multiplier - value)
        return  value * self.multiplier - value
