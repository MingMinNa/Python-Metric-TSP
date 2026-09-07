from ..tsp import *
from .base_algo import TOUR, BaseAlgo


class FarthestInsertionAlgo(BaseAlgo):

    @staticmethod
    def solve(tsp_instance: ALL_GROUP) -> tuple[TOUR, float]:

        if not isinstance(tsp_instance, ALL_TUPLE):
            raise TypeError(
                f"The data type of instance must be one of "
                f"{tuple(TYPE.__name__ for TYPE in ALL_TUPLE)}."
            )

        num_nodes = tsp_instance.num_nodes

        if num_nodes == 1:
            return ([0], 0.0)

        is_asymmetric = isinstance(tsp_instance, ATSP_TUPLE)
        dist = tsp_instance.distance_matrix

        # Start from the nearest pair of nodes.
        sym_dist = dist + (dist.T if is_asymmetric else dist)
        mask = np.ones_like(dist, dtype = bool)

        if is_asymmetric:
            np.fill_diagonal(mask, False)
        else:
            mask = np.triu(mask, k = 1)

        work = np.where(mask, dist, -np.inf)
        start_u, start_v = np.unravel_index(np.argmax(work), work.shape)
        start_u, start_v = int(start_u), int(start_v)

        tour = [start_u, start_v]
        in_tour = np.zeros(num_nodes, dtype = bool)
        in_tour[start_u] = True
        in_tour[start_v] = True

        while len(tour) < num_nodes:

            tour_arr = np.array(tour, dtype = np.int64)

            # Computed for all candidates at once.
            candidate_min = sym_dist[:, tour_arr].min(axis = 1)
            candidate_min = np.where(in_tour, -np.inf, candidate_min)
            farthest_node = int(np.argmax(candidate_min))

            # Find the best position to insert farthest_node.
            tour_next = np.roll(tour_arr, -1)
            increase = (
                dist[tour_arr, farthest_node] +
                dist[farthest_node, tour_next] -
                dist[tour_arr, tour_next]
            )

            best_position = int(np.argmin(increase)) + 1
            tour.insert(best_position, farthest_node)
            in_tour[farthest_node] = True

        tour_arr = np.array(tour, dtype = np.int64)
        total_distance = float(dist[tour_arr, np.roll(tour_arr, -1)].sum())

        return (tour, total_distance)