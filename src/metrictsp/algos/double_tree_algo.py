from ..tsp import *
from .base_algo import TOUR, BaseAlgo


class DoubleTreeAlgo(BaseAlgo):

    @staticmethod
    def solve(tsp_instance: MetricTSP) -> tuple[TOUR, float]: 

        if not isinstance(tsp_instance, MetricTSP):
            raise TypeError(
                "The data type of instance must be MetricTSP."
            )

        num_nodes = tsp_instance.num_nodes
        
        if num_nodes == 1:
            return ([0], 0.0)

        mst_edges = DoubleTreeAlgo.\
            _build_mst(tsp_instance)

        #### Difference between ChristofidesAlgo and DoubleTreeAlgo #####

        doubled_edges = mst_edges + mst_edges
        
        #################################################################

        euler_path = DoubleTreeAlgo.\
            _eulerian_circuit(doubled_edges, num_nodes)
        
        tour = DoubleTreeAlgo.\
            _shortcut(euler_path, num_nodes)

        total_distance = sum(
            tsp_instance.lookup_distance(tour[i], tour[(i + 1) % num_nodes])
            for i in range(num_nodes)
        )

        return (tour, total_distance)

    # Prim's algorithm
    @staticmethod
    def _build_mst(tsp_instance: MetricTSP) -> list[tuple[int, int]]:
        """ Build a minimum spanning tree using Prim's algorithm. """

        num_nodes = tsp_instance.num_nodes

        in_mst        : list[bool]  = [False] * num_nodes
        parent        : list[int]   = [-1] * num_nodes
        min_edge_cost : list[float] = [float("inf")] * num_nodes

        min_edge_cost[0] = 0.0
        mst_edges: list[tuple[int, int]] = []

        for _ in range(num_nodes):

            u = min(
                (node for node in range(num_nodes) if not in_mst[node]),
                key = lambda node: min_edge_cost[node],
            )

            in_mst[u] = True

            if parent[u] != -1:
                mst_edges.append((parent[u], u))

            for v in range(num_nodes):

                if in_mst[v]:
                    continue

                distance = tsp_instance.\
                    lookup_distance(u, v)

                if distance < min_edge_cost[v]:
                    min_edge_cost[v] = distance
                    parent[v] = u

        return mst_edges

    # Hierholzer's algorithm
    @staticmethod
    def _eulerian_circuit(
        edges: list[tuple[int, int]], 
        num_nodes: int,
    ) -> list[int]:
        """
        Find an Eulerian circuit over a multigraph using Hierholzer's algorithm. 
        `edges` must form a connected multigraph in which every node has even degree.
        """

        adjacency: list[list[tuple[int, int]]] \
            = [[] for _ in range(num_nodes)]
        
        for edge_id, (u, v) in enumerate(edges):
            adjacency[u].append((v, edge_id))
            adjacency[v].append((u, edge_id))

        edge_used = [False] * len(edges)
        next_unused = [0] * num_nodes  # pointer into adjacency[node]

        stack = [0]
        circuit: list[int] = []

        while stack:

            u = stack[-1]

            while (
                next_unused[u] < len(adjacency[u]) and 
                edge_used[adjacency[u][next_unused[u]][1]]
            ):
                next_unused[u] += 1

            if next_unused[u] == len(adjacency[u]):
                circuit.append(stack.pop())
            else:
                v, edge_id = adjacency[u][next_unused[u]]
                edge_used[edge_id] = True
                stack.append(v)

        return circuit[::-1]

    @staticmethod
    def _shortcut(euler_path: list[int], num_nodes: int) -> list[int]:
        """
        Convert an Eulerian circuit into a Hamiltonian cycle 
        by skipping nodes that have been visited.
        """

        visited = [False] * num_nodes
        tour: list[int] = []

        for node in euler_path:
            if not visited[node]:
                visited[node] = True
                tour.append(node)

        return tour