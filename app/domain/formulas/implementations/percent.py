from app.interfaces import FormulaI
from app.domain.formulas.register import formula_registry


@formula_registry("percent")
class PercentFormula(FormulaI):
    def __init__(self, percent: float):
        self.percent = percent

    def calculate(self, value: float) -> float:
        return value * (self.percent / 100)
