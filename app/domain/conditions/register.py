from typing import Type, Dict
from app.interfaces.condition_interface import ConditionI

class ConditionRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[ConditionI]] = {}

    def __call__(self, name: str):
        def decorator(cls: Type[ConditionI]):
            self._registry[name] = cls
            return cls
        return decorator

    def get(self, name: str) -> Type[ConditionI]:
        try:
            return self._registry[name]
        except KeyError:
            raise ValueError(f"Unsupported condition type: {name}")

    def list(self) -> list[str]:
        return list(self._registry.keys())

condition_registry = ConditionRegistry()
