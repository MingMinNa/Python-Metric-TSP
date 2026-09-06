# Nearest Neighbor Algorithm

The Nearest Neighbor Algorithm is a heuristic algorithm that provides no approximation guarantees.

## Procedure
1. Initialize all vertices as unvisited.
2. Select an arbitrary vertex, set it as the current vertex $u$. Mark $u$ as visited.
3. Find the shortest edge connecting the current vertex $u$ and an unvisited vertex $v$.
4. Set $v$ as the current vertex. Mark $v$ as visited.
5. If all the vertices have been visited, then terminate. Otherwise, go to step 3.

Source: [Wikipedia – Nearest neighbour algorithm](https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm)
