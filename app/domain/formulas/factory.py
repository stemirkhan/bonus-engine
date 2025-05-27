from typing import Dict
from app.interfaces import FormulaI
from .register import formula_registry


class FormulaFactory:
    @staticmethod
    def create(formula_data: Dict) -> FormulaI:
        formula_type = formula_data["type"]
        config = formula_data.get("config", {})

        formula_cls = formula_registry.get(formula_type)
        return formula_cls(**config)
