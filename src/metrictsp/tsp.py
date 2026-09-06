from __future__ import annotations

from typing import override

import numpy as np

from .exceptions import *


# Base class
class BaseTSP: 

    _num_nodes  : int
    _matrix     : np.ndarray

    def __init__(self, num_nodes: int | None = None) -> None:

        # Empty instance
        if num_nodes is None:
            return 

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
        """ 
        Check each entry in the matrix for a value,
        or it will raise IncompleteMatrixError. 
        """
        
        num_nodes = self._num_nodes

        for u in range(num_nodes):
            for v in range(num_nodes):
                if u != v and np.isinf(self._matrix[u, v]):
                    raise IncompleteMatrixError(
                        f"The distance matrix is incomplete: "
                        f"entry ({u}, {v}) has no value."
                    )


# Symmetric TSP
class TSP(BaseTSP): 

    @override
    def set_distance(self, u: int, v: int, distance: float) -> None:
        """ Set the distance from u to v. """
    
        super().set_distance(u, v, distance)
        self._set_raw(v, u, distance)


# Asymmetric TSP
class ATSP(BaseTSP): 
    pass


# Metric symmetric TSP
class MetricTSP(TSP): 

    @override
    def set_distance(self, u: int, v: int, distance: float, tolerance: float = 1e-9) -> None:

        super().set_distance(u, v, distance)
        _check_triangle_inequality_for_edge(self, u, v, tolerance)


# Metric asymmetric TSP
class MetricATSP(ATSP): 

    @override
    def set_distance(self, u: int, v: int, distance: float, tolerance: float = 1e-9) -> None:

        super().set_distance(u, v, distance) 
        _check_triangle_inequality_for_edge(self, u, v, tolerance)


# Classifier
class TSPClassifier:

    @staticmethod
    def classify(base_instance: BaseTSP, tolerance: float = 1e-9) -> ALL_GROUP:

        if not isinstance(base_instance, BaseTSP):
            raise TypeError(
                "The data type of base_instance must inherit from BaseTSP."
            )

        base_instance.check_complete()
        is_metric = _is_metric(base_instance, tolerance)
        is_symmetric = _is_symmetric(base_instance)

        TSP_Types = [
            #     False,      True
            [      ATSP,       TSP],  # is_metric == False
            [MetricATSP, MetricTSP]   # is_metric == True
        ]

        instance: ALL_GROUP = TSP_Types[is_metric][is_symmetric]()
        instance._num_nodes = base_instance._num_nodes
        instance._matrix    = base_instance._matrix

        return instance


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

def _check_triangle_inequality_for_edge(
    instance: BaseTSP, u: int, v: int, tolerance: float,
) -> None:

    num_nodes = instance.num_nodes
    matrix = instance._matrix

    d_uv = matrix[u, v]

    for w in range(num_nodes):

        if w == u or w == v:
            continue

        d_uw = matrix[u, w]
        d_wv = matrix[w, v]
        d_wu = matrix[w, u]
        d_vw = matrix[v, w]

        if (
            not (np.isinf(d_uw) or np.isinf(d_wv)) and
            d_uv > d_uw + d_wv + tolerance
        ):
            raise TriangleInequalityError(
                f"Triangle inequality violated: "
                f"d({u}, {v}) = {d_uv} > "
                f"d({u}, {w}) + d({w}, {v}) = {d_uw + d_wv}."
            )

        if (
            not (np.isinf(d_uw) or np.isinf(d_vw)) and 
            d_uw > d_uv + d_vw + tolerance
        ):
            raise TriangleInequalityError(
                f"Triangle inequality violated: "
                f"d({u}, {w}) = {d_uw} > "
                f"d({u}, {v}) + d({v}, {w}) = {d_uv + d_vw}."
            )

        if (
            not (np.isinf(d_wv) or np.isinf(d_wu))
            and d_wv > d_wu + d_uv + tolerance
        ):
            raise TriangleInequalityError(
                f"Triangle inequality violated: "
                f"d({w}, {v}) = {d_wv} > "
                f"d({w}, {u}) + d({u}, {v}) = {d_wu + d_uv}."
            )

def _is_metric(instance: BaseTSP, tolerance: float) -> bool:

    num_nodes = instance.num_nodes
    matrix = instance._matrix

    for u in range(num_nodes):
        for v in range(num_nodes):
            for w in range(num_nodes):
                if matrix[u, w] > matrix[u, v] + matrix[v, w] + tolerance:
                    return False
    return True

def _is_symmetric(instance: BaseTSP) -> bool:

    num_nodes = instance.num_nodes
    matrix = instance._matrix

    for u in range(num_nodes):
        for v in range(u + 1, num_nodes):
            if not np.isclose(matrix[u, v], matrix[v, u]):
                return False
    return True


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
