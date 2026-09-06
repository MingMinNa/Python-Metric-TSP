import time
from pathlib import Path

import tsplib95

from metrictsp import *
from metrictsp.algos import TOUR
from metrictsp.tsp import *

BENCH_FOLDER = Path(__file__).resolve().parents[0]

# testcase
TESTCASE_FOLDER = BENCH_FOLDER / "testcase"
PROBLEMS_FOLDER = TESTCASE_FOLDER / "problems"
OPTIMAL_FOLDER  = TESTCASE_FOLDER / "optimal"

# results
RESULTS_FOLDER = BENCH_FOLDER / "results"

problem_files = PROBLEMS_FOLDER.glob("*.tsp")
optimal_files = OPTIMAL_FOLDER.glob("*.opt")

PROBLEM_NAMES = [path.stem for path in problem_files]


def load_problem(name: str, tsp_class: type[BaseTSP] = BaseTSP) -> ALL_GROUP:

    path = PROBLEMS_FOLDER / f"{name}.tsp"
        
    if not path.exists():
        raise FileNotFoundError(
            f"No such problem file: {path}."
        )

    if (
        tsp_class is not BaseTSP and 
        tsp_class not in ALL_TUPLE
    ):
        raise TypeError(
            "The class of tsp_class must inherit from BaseTSP."
        )

    problem = tsplib95.load(path)
    num_nodes = problem.dimension
    
    assert isinstance(num_nodes, int)

    instance = tsp_class(num_nodes)
    offset = 0 if _is_zero_indexed(problem) else 1

    for u in range(num_nodes):
        for v in range(num_nodes):

            if u == v: continue

            if tsp_class in METRIC_TUPLE:

                # assert type(instance) in METRIC_TUPLE

                assert (
                    type(instance) is MetricATSP or
                    type(instance) is MetricTSP
                )

                # EUC_2D and EUC_3D may have slight rounding errors.
                instance.set_distance(u, v, problem.get_weight(u + offset, v + offset), 2.0)
            else:
                instance.set_distance(u, v, problem.get_weight(u + offset, v + offset))

    if type(instance) is BaseTSP:
        return TSPClassifier.classify(instance, 2.0)

    # assert type(instance) in ALL_TUPLE

    assert (
        type(instance) is TSP        or
        type(instance) is ATSP       or
        type(instance) is MetricTSP  or
        type(instance) is MetricATSP 
    )

    return instance

def load_optimal(name: str) -> float | None:

    path = OPTIMAL_FOLDER / f"{name}.opt"
    
    if not path.exists():
        return None

    return float(path.read_text().strip())

def save_result(
    instance: ALL_GROUP,
    name: str, 
    algo: str, 
    tour: TOUR, 
    distance: float, 
    optimal: float | None,
    elapsed: float
):
    ratio = distance / optimal if optimal else float("nan")

    header_section = [
        f"{'Problem'  :10s}: {name}",
        f"{'TSP_Type' :10s}: {type(instance).__name__}",
        f"{'Algorithm':10s}: {algo}",
        f"{'Distance' :10s}: {distance:.4f}",
        f"{'Optimal'  :10s}: {optimal:.4f}",
        f"{'Ratio'    :10s}: {ratio:.4f}",
        f"{'Time'     :10s}: {elapsed:.4f}s",
    ]

    tour_section = ["Tour:"] + _format_tour_lines(tour)
    report = _render_box([header_section, tour_section])

    output_folder = RESULTS_FOLDER / name
    RESULTS_FOLDER.mkdir(parents = True, exist_ok = True)
    output_folder.mkdir(parents = True, exist_ok = True)
    
    result_path = output_folder / f"{name}-{algo}.txt"
    result_path.write_text(report + "\n", encoding = "utf-8")

def run_benchmark(
    algo: type,
    problem_names: list[str] | None = None,
    required_type: type[BaseTSP] = BaseTSP,
) -> None:

    names = PROBLEM_NAMES if problem_names is None else problem_names

    print(f"\nRunning {algo.__name__} on {len(names)} problem(s)...")

    for name in names:

        instance = load_problem(name)

        # # check_complete() will be called in TSPClassifier.classify. 
        # instance.check_complete()

        if (
            required_type is not None and 
            not isinstance(instance, required_type)
        ):
            print(
                f"[{name:^10s}] SKIPPED "
                f"(classified as {type(instance).__name__}, "
                f"not {required_type.__name__})"
            )
            continue
        
        start = time.perf_counter()

        tour, distance = algo.solve(instance)

        elapsed = time.perf_counter() - start

        optimal = load_optimal(name)
        ratio = distance / optimal if optimal else float("nan")
        optimal_display = f"{optimal:.2f}" if optimal is not None else "N/A"

        print(
            f"[{name:^10s}] distance = {distance:12.2f}, "
            f"optimal = {optimal_display:>10s}, "
            f"ratio = {ratio:6.4f}, "
            f"time = {elapsed:7.4f}s"
        )

        save_result(instance, name, algo.__name__, tour, distance, optimal, elapsed)

    print("\nDone. Reports saved under:", RESULTS_FOLDER)


def _render_box(sections: list[list[str]]) -> str:

    all_lines = [line for section in sections for line in section]
    inner_width = max((len(line) for line in all_lines), default = 0) + 2

    top     = "┌" + "─" * inner_width + "┐"
    bottom  = "└" + "─" * inner_width + "┘"
    divider = "├" + "─" * inner_width + "┤"

    rendered = [top]
    for i, section in enumerate(sections):
        for line in section:
            rendered.append("│ " + line.ljust(inner_width - 1) + "│")
        if i != len(sections) - 1:
            rendered.append(divider)
    rendered.append(bottom)

    return "\n".join(rendered)

def _format_tour_lines(
    tour: TOUR, 
    nodes_per_line: int = 10,
) -> list[str]:

    n = len(tour)
    width = len(str(max(tour) + 1))

    segments = [f"{tour[i] + 1:>{width}} —→" for i in range(n)]

    lines = []
    for start in range(0, n, nodes_per_line):
        lines.append(" ".join(segments[start : start + nodes_per_line]))

    # close the loop
    lines[-1] += f" {tour[0] + 1}" 

    return lines

def _is_zero_indexed(problem: tsplib95.models.StandardProblem) -> bool:
    return 0 in problem.get_nodes()