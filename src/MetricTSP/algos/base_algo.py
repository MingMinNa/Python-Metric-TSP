from abc    import ABC, abstractmethod
from typing import TypeVar

from ..tsp  import *

T = TypeVar("T", bound = BaseTSP)

class BaseAlgo[T: BaseTSP](ABC):

    @staticmethod
    @abstractmethod
    def solve(tsp_instance: T) -> tuple[list[int], float]: 
        pass

