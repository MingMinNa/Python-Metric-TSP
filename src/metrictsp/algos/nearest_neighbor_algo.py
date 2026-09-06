import random

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

        # Choose an arbitrary vertex as the starting point.
        rng     = random.Random(seed)
        current = rng.randint(0, num_nodes - 1)
        tour    = [current]
        
        visited = [False] * num_nodes
        visited[current] = True
 
        for _ in range(num_nodes - 1):
 
            nearest_node = None
            nearest_distance = float("inf")

            # Select the next node from the remaining nodes.
            for candidate in range(num_nodes):

                if visited[candidate]:
                    continue

                distance = tsp_instance.lookup_distance(current, candidate)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_node = candidate

            assert nearest_node is not None

            tour.append(nearest_node)
            visited[nearest_node] = True
            current = nearest_node
 
        total_distance = sum(
            tsp_instance.lookup_distance(tour[i], tour[i + 1])
            for i in range(num_nodes - 1)
        )

        total_distance += tsp_instance.lookup_distance(tour[-1], tour[0])
 
        return (tour, total_distance)