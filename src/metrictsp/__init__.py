from importlib.metadata import PackageNotFoundError, version

from .algos import *
from .exceptions import *
from .tsp import ATSP, TSP, BaseTSP, MetricATSP, MetricTSP

__all__ = [
    "ATSP",
    "TSP",
    "BaseTSP",
    "ChristofidesAlgo",
    "DoubleTreeAlgo",
    "IncompleteMatrixError",
    "MetricATSP",
    "MetricTSP",
    "NearestAdditionAlgo",
    "NearestNeighborAlgo",
    "TriangleInequalityError"
]

try:
    __version__ = version("python-metric-tsp")
except PackageNotFoundError:
    __version__ = "0.0.0"