from typing import Type, Dict
from app.interfaces import FormulaI

class FormulaRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[FormulaI]] = {}

    def __call__(self, name: str):
        def decorator(cls: Type[FormulaI]):
            self._registry[name] = cls
            return cls
        return decorator

    def get(self, name: str) -> Type[FormulaI]:
        try:
            return self._registry[name]
        except KeyError:
            raise ValueError(f"Unsupported formula type: {name}")

    def list(self) -> list[str]:
        return list(self._registry.keys())

formula_registry = FormulaRegistry()
