from abc import ABC, abstractmethod
from typing import Any

from ..tsp import *

type TOUR = list[int]


class BaseAlgo(ABC):

    @staticmethod
    @abstractmethod
    def solve(*args: Any, **kwargs: Any) -> tuple[TOUR, float]:
        pass

