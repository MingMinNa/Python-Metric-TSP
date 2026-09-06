# Double Tree Algorithm

The Double Tree Algorithm is a $2$-approximation algorithm for Metric TSP.  

## Procedure
1. Create a minimum spanning tree $T$ of $G$.
2. Double every edge in $T$ to form a connected multigraph $H$ in which each vertex has even degree.
3. Form an Eulerian circuit in $H$.
4. Make the circuit found in the previous step into a Hamiltonian circuit by skipping repeated vertices.