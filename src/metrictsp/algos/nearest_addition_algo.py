from ..tsp import *
from .base_algo import TOUR, BaseAlgo


class NearestAdditionAlgo(BaseAlgo):

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
        mask = np.ones_like(dist, dtype = bool)

        if is_asymmetric:
            np.fill_diagonal(mask, False)
        else:
            mask = np.triu(mask, k = 1)

        work = np.where(mask, dist, np.inf)
        start_u, start_v = np.unravel_index(np.argmin(work), work.shape)
        start_u, start_v = int(start_u), int(start_v)

        tour = [start_u, start_v]
        in_tour = np.zeros(num_nodes, dtype = bool)
        in_tour[start_u] = True
        in_tour[start_v] = True

        while len(tour) < num_nodes:

            tour_arr = np.array(tour, dtype = np.int64)

            candidate_dist = dist[tour_arr, :]
            candidate_dist = np.where(in_tour[None, :], np.inf, candidate_dist)

            flat_idx = int(np.argmin(candidate_dist))
            best_position, nearest_node = np.unravel_index(flat_idx, candidate_dist.shape)
            best_position, nearest_node = int(best_position), int(nearest_node)

            tour.insert(best_position + 1, nearest_node)
            in_tour[nearest_node] = True

        tour_arr = np.array(tour, dtype = np.int64)
        total_distance = float(dist[tour_arr, np.roll(tour_arr, -1)].sum())

        return (tour, total_distance)
