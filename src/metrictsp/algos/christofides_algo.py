import networkx as nx
from networkx.algorithms import matching

from ..tsp import *
from .base_algo import TOUR
from .double_tree_algo import DoubleTreeAlgo


class ChristofidesAlgo(DoubleTreeAlgo):

    @staticmethod
    def solve(tsp_instance: MetricTSP) -> tuple[TOUR, float]: 

        if not isinstance(tsp_instance, MetricTSP):
            raise TypeError(
                "The data type of instance must be MetricTSP."
            )

        num_nodes = tsp_instance.num_nodes
        
        if num_nodes == 1:
            return ([0], 0.0)

        mst_edges = ChristofidesAlgo.\
            _build_mst(tsp_instance)

        #### Difference between ChristofidesAlgo and DoubleTreeAlgo #####
        
        odd_nodes = ChristofidesAlgo.\
            _find_odd_degree_nodes(mst_edges, num_nodes)
        
        matching_edges = ChristofidesAlgo.\
            _minimum_weight_perfect_matching(tsp_instance, odd_nodes)

        doubled_edges = mst_edges + matching_edges

        #################################################################

        euler_path = ChristofidesAlgo.\
            _eulerian_circuit(doubled_edges, num_nodes)
        
        tour = ChristofidesAlgo.\
            _shortcut(euler_path, num_nodes)

        total_distance = sum(
            tsp_instance.lookup_distance(tour[i], tour[(i + 1) % num_nodes])
            for i in range(num_nodes)
        )

        return (tour, total_distance)

    @staticmethod
    def _find_odd_degree_nodes(
        edges: list[tuple[int, int]], 
        num_nodes: int,
    ) -> list[int]:
        """ Find nodes with odd degree in a graph. """

        degree = [0] * num_nodes

        for u, v in edges:
            degree[u] += 1
            degree[v] += 1

        return [node for node in range(num_nodes) if degree[node] % 2 == 1]

    @staticmethod
    def _minimum_weight_perfect_matching(
        tsp_instance: MetricTSP, 
        odd_nodes: list[int],
    ) -> list[tuple[int, int]]:
        """ Find a minimum weight perfect matching among `odd_nodes`. """

        graph = nx.Graph()
        graph.add_nodes_from(odd_nodes)

        for i in range(len(odd_nodes)):
            for j in range(i + 1, len(odd_nodes)):
                u, v = odd_nodes[i], odd_nodes[j]
                distance = tsp_instance.lookup_distance(u, v)
                graph.add_edge(u, v, weight = (-1) * distance)

        # Note: since `weight = (-1) * distance`, it is actually min weight matching.
        matching_ = matching.max_weight_matching(
            graph, maxcardinality = True
        )

        return [(int(u), int(v)) for u, v in matching_]