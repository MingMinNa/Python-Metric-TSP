# Metric TSP Algorithms

![Static Badge](https://img.shields.io/badge/Python-3.13-blue) [![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

## Introduction 

This project focuses on approximation algorithms for the **Metric TSP** and evaluates them on selected TSPLIB test cases.

### Motivation
While reading [*The Design of Approximation Algorithms*](https://www.designofapproxalgs.com/), I found the Traveling Salesman Problem (TSP) particularly interesting and decided to implement the algorithms described in the book. 

## Traveling Salesman Problem (TSP)

The Traveling Salesman Problem (TSP) is a classic combinatorial optimization problem.  

Given a set of vertices and the cost or distance between every pair of vertices, the goal is to find the minimum-cost tour that visits every vertex exactly once and returns to the starting vertex.

The TSP can be classified based on two properties of the edge weights: **symmetry** and the **triangle inequality**.

### Symmetric TSP / Asymmetric TSP
Whether the TSP satisfies the symmetry condition $c(u,v) = c(v,u)$.

### Metric TSP / Non-Metric TSP
Whether the TSP satisfies the triangle inequality $c(u,w) \leq c(u,v) + c(v,w)$.

Combining these two properties gives four common variants: 
- **Symmetric Metric TSP** (Metric TSP)
- **Asymmetric Metric TSP** (Metric ATSP)
- **Symmetric Non-Metric TSP** (TSP)
- **Asymmetric Non-Metric TSP** (ATSP)

The general TSP is NP-hard, making exact solutions impractical for large instances. Approximation algorithms are therefore particularly useful for variants such as the Metric TSP, where the triangle inequality enables algorithms with provable approximation guarantees.

Note: See Unit 2.4 in [*The Design of Approximation Algorithms*](https://www.designofapproxalgs.com/) for detail.


## Implemented Algorithms

The following algorithms are currently implemented:
| Algorithm | Applicable TSP Variants | Approximation Ratio | Notes |
| --------- | ----------------------- |:-------------------:| ----- |
| Christofides      | Metric TSP       | 1.5-approximation | Approximation algorithm             |
| Double Tree       | Metric TSP       | 2-approximation   | Approximation algorithm             |
| Nearest Addition  | All TSP variants | 2-approximation   | Guarantee holds only for Metric TSP |
| Nearest Insertion | All TSP variants | 2-approximation   | Guarantee holds only for Metric TSP |
| Cheapest Insertion| All TSP variants | 2-approximation   | Guarantee holds only for Metric TSP |
| Farthest Insertion| All TSP variants | $O(\log \\, n)$-approximation   | Guarantee holds only for Metric TSP |
| Nearest Neighbor  | All TSP variants | —                 | Heuristic                           |

## Installation

Run the command below to install `metrictsp` in your Python environment.

```bash
$ git clone https://github.com/MingMinNa/Python-Metric-TSP.git
$ cd Python-Metric-TSP
$ pip install .
```

Then, run the following code to verify the installation:

```python
import metrictsp
print(metrictsp.__version__)
```

## Usage

Here are some simple usage examples.

### Create a TSP Instance

```python
from metrictsp.tsp import TSP, TSPClassifier

# Create a symmetric TSP instance with 4 nodes.
tsp = TSP(4)

# Set distances between nodes.
# For symmetric TSP, set_distance(u, v, d) also sets v → u automatically.
tsp.set_distance(0, 1, 10)
tsp.set_distance(0, 2, 15)
tsp.set_distance(0, 3, 20)
tsp.set_distance(1, 2, 35)
tsp.set_distance(1, 3, 25)
tsp.set_distance(2, 3, 30)

# Look up the distance between two nodes.
print(tsp.lookup_distance(0, 1), "\n")

# Make sure every entry in the matrix has been set,
# or IncompleteMatrixError will be raised.
tsp.check_complete()

print(tsp)
```

<details>
<summary>Output</summary>

```text
10.0 

The number of nodes: 4
[[ 0. 10. 15. 20.]
 [10.  0. 35. 25.]
 [15. 35.  0. 30.]
 [20. 25. 30.  0.]]
```
</details>

### Classify a TSP Instance

```python
from metrictsp.tsp import BaseTSP, TSPClassifier

base = BaseTSP(3)

base.set_distance(0, 1, 10); base.set_distance(1, 0, 10)
base.set_distance(0, 2, 15); base.set_distance(2, 0, 15)
base.set_distance(1, 2, 20); base.set_distance(2, 1, 20)

print(base, "\n")

# Automatically determine whether the instance is symmetric / asymmetric
# and metric / non-metric, then convert it to the corresponding subclass.
classified = TSPClassifier.classify(base)
print(type(classified).__name__)
```

<details>
<summary>Output</summary>

```text
The number of nodes: 3
[[ 0. 10. 15.]
 [10.  0. 20.]
 [15. 20.  0.]] 

MetricTSP
```
</details>

### Solve with an Algorithm

```python
from metrictsp.tsp import TSP
from metrictsp.algos.nearest_neighbor_algo import NearestNeighborAlgo
from metrictsp.algos.nearest_insertion_algo import NearestInsertionAlgo

tsp = TSP(4)

# Set distances between nodes.
tsp.set_distance(0, 1, 10)
tsp.set_distance(0, 2, 15)
tsp.set_distance(0, 3, 20)
tsp.set_distance(1, 2, 35)
tsp.set_distance(1, 3, 25)
tsp.set_distance(2, 3, 30)

# Nearest Neighbor: start from a (seeded) random node and always
# move to the closest unvisited node.
tour, distance = NearestNeighborAlgo.solve(tsp, seed=42)
print(f"Nearest Neighbor  -> tour: {tour}, distance: {distance}")

# Nearest Insertion: repeatedly insert the node nearest to the
# current tour at the position with the smallest increase in length.
tour, distance = NearestInsertionAlgo.solve(tsp)
print(f"Nearest Insertion -> tour: {tour}, distance: {distance}")
```

<details>
<summary>Output</summary>

```text
Nearest Neighbor  -> tour: [0, 1, 3, 2], distance: 80.0
Nearest Insertion -> tour: [0, 2, 3, 1], distance: 80.0
```
</details>

### Note
For `MetricTSP`, set distances in triangular order rather than calling `set_distance(u, v, d)` and `set_distance(v, u, d)` separately — each call re-checks the triangle inequality, so redundant calls add unnecessary overhead.