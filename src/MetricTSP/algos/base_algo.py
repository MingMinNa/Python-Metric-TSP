from abc import ABC, abstractmethod
from typing import Any

from ..tsp import *


class BaseAlgo(ABC):

    @staticmethod
    @abstractmethod
    def solve(*args: Any, **kwargs: Any) -> tuple[list[int], float]:
        pass

