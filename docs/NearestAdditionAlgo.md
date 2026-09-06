# Nearest Addition Algorithm

The Nearest Addition Algorithm provides no approximation guarantee for general TSP,  
but it provides a 2-approximation guarantee for Metric TSP.

## Procedure
1. Find the nearest pair of nodes and use them to initialize the tour.
2. Find the unvisited node $v$ that is nearest to any node $u$ in the current tour.
3. Let $w$ be the node that follows $u$ in the current tour. Insert $v$ into the current tour between $u$ and $w$.
4. If all nodes have been added to the tour, terminate. Otherwise, go to step 2.
