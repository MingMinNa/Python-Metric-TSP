# Christofides Algorithm

The Christofides Algorithm is a $1.5$-approximation algorithm for Metric TSP.  

## Procedure
1. Create a minimum spanning tree $T$ of $G$.
2. Let $O$ be the set of vertices with odd degree in $T$. Find a minimum-weight perfect matching $M$ in the subgraph induced in $G$ by $O$.
3. Combine the edges of $M$ and $T$ to form a connected multigraph $H$ in which each vertex has even degree.
4. Form an Eulerian circuit in $H$.
5. Make the circuit found in the previous step into a Hamiltonian circuit by skipping repeated vertices.

Source: [Wikipedia – Christofides algorithm](https://en.wikipedia.org/wiki/Christofides_algorithm)