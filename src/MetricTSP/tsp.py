import numpy as np

from .exceptions import *


# Base class
class BaseTSP: 

    _num_nodes  : int
    _matrix     : np.ndarray
    _is_virtual : bool = True

    def __init__(self, num_nodes: int) -> None:

        if not isinstance(num_nodes, int): 
            raise TypeError(
                f"The data type of num_nodes must be integer, "
                f"got {type(num_nodes).__name__}."
            )

        if num_nodes <= 0: 
            raise ValueError(
                f"num_nodes must be positive integer, "
                f"got {num_nodes}."
            )

        self._num_nodes = num_nodes
        self._matrix = np.full(
            (self._num_nodes, self._num_nodes), 
            np.inf, dtype = float,
        )

        np.fill_diagonal(self._matrix, 0.0)

    def __str__(self) -> str:
        return (
            f"The number of nodes: {self._num_nodes}\n" + 
            f"{self._matrix!s}"
        )

    def __init_subclass__(cls, *, virtual: bool, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._is_virtual = virtual
 
    def __new__(cls, *args, **kwargs):
        if cls._is_virtual:
            raise TypeError(
                f"{cls.__name__} is a virtual class and "
                f"cannot be instantiated directly."
            )
        return super().__new__(cls)

    @property
    def num_nodes(self) -> int:
        return self._num_nodes

    def _set_raw(self, u: int, v: int, distance: float) -> None:
        self._matrix[u, v] = float(distance)

    def set_distance(self, u: int, v: int, distance: float) -> None:
        """ Set the distance from u to v. """

        _check_node(u, self._num_nodes)
        _check_node(v, self._num_nodes)
        _check_distance(distance)

        if u == v:
            raise ValueError(
                f"The two nodes must be different, "
                f"got u={u}, v={v}."
            )

        self._set_raw(u, v, distance)

    def lookup_distance(self, u: int, v: int) -> float:
        """ Lookup the distance from u to v. """

        _check_node(u, self._num_nodes)
        _check_node(v, self._num_nodes)
        
        distance = self._matrix[u, v]

        if u != v and np.isinf(distance):
            raise IncompleteMatrixError(
                f"The distance between node {u} and node {v} "
                f"has not been set yet."
            )

        return distance

    def check_complete(self) -> None:
        """ Check each entry in the matrix for a value, or it will raise IncompleteMatrixError. """
        
        num_nodes = self._num_nodes

        for u in range(num_nodes):
            for v in range(num_nodes):
                if u != v and np.isinf(self._matrix[u, v]):
                    raise IncompleteMatrixError(
                        f"The distance matrix is incomplete: "
                        f"entry ({u}, {v}) has no value."
                    )


# Triangle inequality checker
class _Metric(BaseTSP, virtual = True):

    def check_triangle_inequality(self, tolerance: float = 1e-9) -> None:
        """ Check if triangle inequality holds, or it will raise TriangleInequalityError. """
    
        num_nodes = self.num_nodes

        is_valid = lambda u, v, w, tolerance: (
            self.lookup_distance(u, w) < 
            self.lookup_distance(u, v) +
            self.lookup_distance(v, w) +
            tolerance
        )

        for u in range(num_nodes):
            for v in range(num_nodes):
                for w in range(num_nodes):
                    if not is_valid(u, v, w, tolerance):
                        raise TriangleInequalityError(
                            f"Triangle inequality violated: "
                            f"d({u}, {w}) = {self.lookup_distance(u, w)} > "
                            f"d({u}, {v}) + d({v}, {w}) = {self.lookup_distance(u, v) + self.lookup_distance(v, w)}."
                        )


# Symmetric TSP
class TSP(BaseTSP, virtual = False): 

    def set_distance(self, u: int, v: int, distance: float) -> None:
        """ Set the distance from u to v. """
    
        _check_node(u, self.num_nodes)
        _check_node(v, self.num_nodes)
        _check_distance(distance)

        if u == v:
            raise ValueError(
                f"The two nodes must be different, "
                f"got u={u}, v={v}."
            )

        self._set_raw(u, v, distance)
        self._set_raw(v, u, distance)


# Asymmetric TSP
class ATSP(BaseTSP, virtual = False): 
    pass

# Metric symmetric TSP
class MetricTSP(_Metric, TSP, virtual = False): 
    pass

# Metric asymmetric TSP
class MetricATSP(_Metric, ATSP, virtual = False): 
    pass

# Helper functions

def _check_node(node: int, num_nodes: int) -> None:

    if not isinstance(node, int):
        raise TypeError(
            f"The data type of node must be integer, "
            f"got {type(node).__name__}."
        )

    if node < 0 or node >= num_nodes:
        raise ValueError(
            f"The range of node is within [0, {num_nodes - 1}], "
            f"got {node}."
        )

def _check_distance(distance: float) -> None:

    if not isinstance(distance, (int, float)):
        raise TypeError(
            f"The data type of distance must be int or float, "
            f"got {type(distance).__name__}."
        )

    if distance < 0:
        raise ValueError(
            f"distance must be non-negative, "
            f"got {distance}."
        )

# Class groups

type ALL_GROUP    = TSP | ATSP | MetricTSP | MetricATSP
type TSP_GROUP    = TSP | MetricTSP
type ATSP_GROUP   = ATSP | MetricATSP
type METRIC_GROUP = MetricTSP | MetricATSP
type NON_METRIC_GROUP = TSP | ATSP

ALL_TUPLE    = (TSP, ATSP, MetricTSP, MetricATSP)
TSP_TUPLE    = (TSP, MetricTSP)
ATSP_TUPLE   = (ATSP, MetricATSP)
METRIC_TUPLE = (MetricTSP, MetricATSP)
NON_METRIC_TUPLE = (TSP, ATSP)
