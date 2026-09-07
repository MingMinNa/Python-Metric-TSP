# Cheapest Insertion Algorithm

The Cheapest Insertion Algorithm provides no approximation guarantee for general TSP,  
but it provides a 2-approximation guarantee for Metric TSP.

## Procedure
1. Find the nearest pair of nodes and use them to initialize the tour.
2. For each unvisited node $v$ and each edge $(i,j)$ in the current tour, calculate the increase in tour length when inserting $v$ between $i$ and $j$:

$$
\text{increase} = d(i, v) + d(v, j) - d(i, j)
$$

3. Find the unvisited node $v$ and edge $(i,j)$ that result in the smallest increase in tour length.
4. Insert $v$ between $i$ and $j$.
5. If all nodes have been added to the tour, terminate. Otherwise, go to step 2.
