# Nearest Insertion Algorithm

The Nearest Insertion Algorithm provides no approximation guarantee for general TSP,  
but it provides a 2-approximation guarantee for Metric TSP.

## Procedure
1. Find the nearest pair of nodes and use them to initialize the tour.
2. Find the unvisited node $v$ that is nearest to any node in the current tour.
3. For each edge $(i, j)$ in the current tour, calculate the increase in tour length when inserting $v$ between $i$ and $j$:  

$$
\text{increase} = d(i, v) + d(v, j) - d(i, j)
$$

4. Insert $v$ at the position that results in the smallest increase in tour length.
5. If all nodes have been added to the tour, terminate. Otherwise, go to step 2.
