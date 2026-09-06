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
- **Symmetric Metric TSP** (MetricTSP)
- **Asymmetric Metric TSP** (MetricATSP)
- **Symmetric Non-Metric TSP** (TSP)
- **Asymmetric Non-Metric TSP** (ATSP)

The general TSP is NP-hard, making exact solutions impractical for large instances. Approximation algorithms are therefore particularly useful for variants such as the Metric TSP, where the triangle inequality enables algorithms with provable approximation guarantees.

Note: See Unit 2.4 in [*The Design of Approximation Algorithms*](https://www.designofapproxalgs.com/) for detail.


## Implemented Algorithms

The following algorithms are currently implemented:
| Algorithm | Applicable TSP Variants | Approximation Ratio | Notes |
| -- | --- |:---:| --- |
| Nearest Neighbor | All TSP variants | — | Heuristic |
| Nearest Addition | All TSP variants | 2-approximation | Guarantee holds only for Metric TSP |
| Double Tree | Metric TSP | 2-approximation | Approximation algorithm |
| Christofides | Metric TSP | 1.5-approximation | Approximation algorithm |

## Installation

Use the command below to install `metrictsp` to your Python environment.

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



## Benchmarks

