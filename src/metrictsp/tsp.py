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

    @property
    def distance_matrix(self) -> np.ndarray:

        view = self._matrix.view()
        view.setflags(write = False)

        return view

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
        
        incomplete = np.isinf(self._matrix)

        if incomplete.any():
            flat_idx = int(incomplete.reshape(-1).argmax())
            u, v = divmod(flat_idx, self._num_nodes)
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

    d_vw = matrix[v, :]  # d(v, w) for every w
    d_uw = matrix[u, :]  # d(u, w) for every w
    d_wv = matrix[:, v]  # d(w, v) for every w
    d_wu = matrix[:, u]  # d(w, u) for every w

    skip = np.zeros(num_nodes, dtype = bool)
    skip[u] = True
    skip[v] = True

    # d(u, v) > d(u, w) + d(w, v) + tolerance
    cond_1 = (
        ~skip & 
        ~(np.isinf(d_uw) | np.isinf(d_wv)) & 
        (d_uv > d_uw + d_wv + tolerance)
    )

    if cond_1.any():
        w = int(np.flatnonzero(cond_1)[0])
        raise TriangleInequalityError(
            f"Triangle inequality violated: "
            f"d({u}, {v}) = {d_uv} > "
            f"d({u}, {w}) + d({w}, {v}) = {d_uw[w] + d_wv[w]}."
        )

    # d(u, w) > d(u, v) + d(v, w) + tolerance
    cond_2 = (
        ~skip & 
        ~(np.isinf(d_uw) | np.isinf(d_vw)) & 
        (d_uw > d_uv + d_vw + tolerance)
    )

    if cond_2.any():
        w = int(np.flatnonzero(cond_2)[0])
        raise TriangleInequalityError(
            f"Triangle inequality violated: "
            f"d({u}, {w}) = {d_uw[w]} > "
            f"d({u}, {v}) + d({v}, {w}) = {d_uv + d_vw[w]}."
        )

    # d(w, v) > d(w, u) + d(u, v) + tolerance
    cond_3 = (
        ~skip & 
        ~(np.isinf(d_wv) | np.isinf(d_wu)) & 
        (d_wv > d_wu + d_uv + tolerance)
    )

    if cond_3.any():
        w = int(np.flatnonzero(cond_3)[0])
        raise TriangleInequalityError(
            f"Triangle inequality violated: "
            f"d({w}, {v}) = {d_wv[w]} > "
            f"d({w}, {u}) + d({u}, {v}) = {d_wu[w] + d_uv}."
        )

def _is_metric(instance: BaseTSP, tolerance: float) -> bool:

    num_nodes = instance.num_nodes
    matrix = instance._matrix

    for v in range(num_nodes):

        col = matrix[:, v]  # d(u, v) for every u, shape (n,)
        row = matrix[v, :]  # d(v, w) for every w, shape (n,)

        # via_v[u, w] = d(u, v) + d(v, w), shape (n, n)
        via_v = col[:, None] + row[None, :]

        if np.any(matrix > via_v + tolerance):
            return False

    return True

def _is_symmetric(instance: BaseTSP) -> bool:
    matrix = instance._matrix
    return bool(np.allclose(matrix, matrix.T))


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
