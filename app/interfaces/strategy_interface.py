from abc import ABC, abstractmethod
from typing import Dict


class StrategyI(ABC):
    @abstractmethod
    def apply(self, context: dict) -> Dict:
        raise NotImplementedError
