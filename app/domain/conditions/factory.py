from typing import Dict

from .register import condition_registry
from app.interfaces.condition_interface import ConditionI

class ConditionFactory:
    @staticmethod
    def create(condition_data: Dict) -> ConditionI:
        condition_type = condition_data["type"]
        config = condition_data.get("config", {})

        condition_cls = condition_registry.get(condition_type)

        return condition_cls(**config)
