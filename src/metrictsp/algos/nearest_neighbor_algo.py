from ..tsp import *
from .base_algo import TOUR, BaseAlgo


class NearestNeighborAlgo(BaseAlgo):

    @staticmethod
    def solve(tsp_instance: ALL_GROUP, seed: int | None = None) -> tuple[TOUR, float]:

        if not isinstance(tsp_instance, ALL_TUPLE):
            raise TypeError(
                f"The data type of instance must be one of "
                f"{tuple(TYPE.__name__ for TYPE in ALL_TUPLE)}."
            )

        num_nodes = tsp_instance.num_nodes
        dist = tsp_instance.distance_matrix

        # Choose an arbitrary vertex as the starting point.
        rng     = np.random.default_rng(seed)
        current = int(rng.integers(0, num_nodes))

        tour = np.empty(num_nodes, dtype = np.int64)
        tour[0] = current

        visited = np.zeros(num_nodes, dtype = bool)
        visited[current] = True

        for step in range(1, num_nodes):

            # Note: 
            # If visited[i] = True, candidate_row[i] = np.inf.
            # Otherwise           , candidate_row[i] = dist[current][i]
            candidate_row = np.where(visited, np.inf, dist[current])
            nearest_node = int(np.argmin(candidate_row))

            tour[step] = nearest_node
            visited[nearest_node] = True
            current = nearest_node

        total_distance = float(dist[tour, np.roll(tour, -1)].sum())

        return (tour.tolist(), total_distance)