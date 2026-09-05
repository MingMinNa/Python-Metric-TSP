from ..tsp import *
from .base_algo import BaseAlgo


class NearestAdditionAlgo(BaseAlgo):

    @staticmethod
    def solve(tsp_instance: ALL_GROUP, seed: int | None = None) -> tuple[list[int], float]: 

        if not isinstance(tsp_instance, ALL_TUPLE):
            raise TypeError(
                f"The data type of instance must be one of "
                f"{tuple(TYPE.__name__ for TYPE in ALL_TUPLE)}."
            )

        num_nodes = tsp_instance.num_nodes
         
        if num_nodes == 1:
            return ([0], 0.0)
    
        # Start from the nearest pair of nodes.
        start_u, start_v = 0, 1
        shortest_edge = tsp_instance. \
            lookup_distance(start_u, start_v)

        is_asymmetric = isinstance(tsp_instance, ATSP_TUPLE)

        if not is_asymmetric:
            for u in range(num_nodes):
                for v in range(u + 1, num_nodes):
                    distance = tsp_instance.lookup_distance(u, v)
                    if distance < shortest_edge:
                        shortest_edge = distance
                        start_u, start_v = u, v
        else:
            for u in range(num_nodes):
                for v in range(num_nodes):
                    distance = tsp_instance.lookup_distance(u, v)
                    if u != v and distance < shortest_edge:
                        shortest_edge = distance
                        start_u, start_v = u, v
    
        tour = [start_u, start_v]
        in_tour = {start_u, start_v}
    
        while len(tour) < num_nodes:
    
            # Find the node that is nearest to any node already in the tour.
            nearest_node = None
            nearest_distance = float("inf")
    
            for candidate in range(num_nodes):

                if candidate in in_tour:
                    continue

                if not is_asymmetric:
                    distance_to_tour = min(
                        tsp_instance.lookup_distance(candidate, node)
                        for node in tour
                    )
                else:
                    distance_to_tour = min(
                        tsp_instance.lookup_distance(candidate, node) +
                        tsp_instance.lookup_distance(node, candidate)
                        for node in tour
                    )

                if distance_to_tour < nearest_distance:
                    nearest_distance = distance_to_tour
                    nearest_node = candidate
    
            # Find the best position to insert nearest_node.
            best_position = None
            smallest_increase = float("inf")
            tour_length = len(tour)
    
            for idx in range(tour_length):
                i = tour[idx]
                j = tour[(idx + 1) % tour_length]

                # Check (i) → (nearest_node) → (j)
                assert type(nearest_node) is int

                increase = (
                    tsp_instance.lookup_distance(i, nearest_node) + 
                    tsp_instance.lookup_distance(nearest_node, j) - 
                    tsp_instance.lookup_distance(i, j)
                )

                if increase < smallest_increase:
                    smallest_increase = increase
                    best_position = idx + 1

            assert (
                type(best_position) is int and 
                type(nearest_node ) is int
            )

            tour.insert(best_position, nearest_node)
            in_tour.add(nearest_node)
    
        total_distance = sum(
            tsp_instance.lookup_distance(
                tour[i], tour[(i + 1) % num_nodes]
            )
            for i in range(num_nodes)
        )
    
        return (tour, total_distance)
