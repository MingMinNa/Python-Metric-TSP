import argparse
import re

from benchmark_utils import *

from metrictsp import *
from metrictsp.algos import *


def _to_cli_name(cls: type) -> str:
    """
    Derive a CLI-friendly name from an algorithm class, e.g. \n
    (1) ChristofidesAlgo -> "christofides", \n
    (2) NearestAdditionAlgo -> "nearest_addition".
    """
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
    name = name.removesuffix("_algo")
    return name

# Each entry pairs an algorithm class with the TSP type it requires.
ALGORITHMS: list[tuple[type, type[BaseTSP]]] = [
    (ChristofidesAlgo,    MetricTSP),
    (DoubleTreeAlgo,      MetricTSP),
    (NearestAdditionAlgo, BaseTSP),
    (NearestNeighborAlgo, BaseTSP),
]


ALGORITHM_BY_NAME: dict[str, tuple[type, type[BaseTSP]]] = {
    _to_cli_name(algo): (algo, required_type)
    for algo, required_type in ALGORITHMS
}


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description = "Run one or all TSP benchmark algorithms."
    )

    parser.add_argument(
        "algorithm",
        choices = [*ALGORITHM_BY_NAME, "all"],
        help = "Which algorithm to run, or 'all' to run all algorithms.",
    )

    return parser.parse_args()

def main() -> None:

    args = parse_args()

    selected = (
        ALGORITHMS if args.algorithm == "all"
        else [ALGORITHM_BY_NAME[args.algorithm]]
    )

    for algo, required_type in selected:
        run_benchmark(algo, required_type = required_type)
        print()


if __name__ == "__main__":
    main()