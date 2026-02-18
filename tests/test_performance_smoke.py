import time

from fishertools import explain_error
from fishertools.safe import safe_divide, safe_get, safe_sum
from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer


def _run_timed(fn):
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def test_perf_smoke_explain_error_budget():
    def workload():
        for _ in range(30):
            try:
                1 / 0
            except Exception as e:
                explain_error(e, format_type="plain")

    elapsed = _run_timed(workload)
    assert elapsed < 2.5, f"explain_error perf regression: {elapsed:.3f}s > 2.5s"


def test_perf_smoke_safe_helpers_budget():
    data = {"x": 1, "y": 2}

    def workload():
        for _ in range(50_000):
            safe_get(data, "x", 0)
            safe_divide(10, 2)
            safe_sum([1, 2, 3, 4, 5])

    elapsed = _run_timed(workload)
    assert elapsed < 2.0, f"safe_* perf regression: {elapsed:.3f}s > 2.0s"


def test_perf_smoke_visualization_budget():
    visualizer = AlgorithmVisualizer()
    arr = list(range(200, 0, -1))

    def workload():
        visualizer.visualize_sorting(arr, algorithm="quick_sort")

    elapsed = _run_timed(workload)
    assert elapsed < 3.0, f"visualization perf regression: {elapsed:.3f}s > 3.0s"
