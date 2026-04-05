import time
import random
import statistics
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, Any, Optional

from digital_geometry import (
    bresenham_line,
    manhattan_distance_transform,
    euclidean_distance_transform,
    a_star,
    voronoi_diagram,
    calculate_topology,
    compute_h0_persistence,
    jump_flooding_dt,
    fractal_dimension,
    marching_tetrahedra,
    calculate_zernike_moments,
    hausdorff_distance,
    iterative_closest_point,
    medial_axis_transform,
)


@dataclass
class BenchmarkResult:
    name: str
    mean_ms: float
    std_ms: float
    min_ms: float
    max_ms: float
    runs: int


def generate_grid(size: int) -> list:
    return [[random.choice([0, 0, 0, 1]) for _ in range(size)] for _ in range(size)]


def generate_volume(size: int) -> list:
    return [
        [[random.random() for _ in range(size)] for _ in range(size)]
        for _ in range(size)
    ]


def generate_point_set(count: int, scale: float = 100.0) -> list:
    return [(random.random() * scale, random.random() * scale) for _ in range(count)]


def generate_seeds(count: int, size: int) -> list:
    return [
        (random.randint(0, size - 1), random.randint(0, size - 1)) for _ in range(count)
    ]


def run_benchmark(
    name: str,
    func: Callable,
    args: tuple = (),
    kwargs: dict = None,
    runs: int = 10,
    warmup: int = 2,
) -> BenchmarkResult:
    if kwargs is None:
        kwargs = {}

    for _ in range(warmup):
        func(*args, **kwargs)

    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        times.append((end - start) * 1000)

    return BenchmarkResult(
        name=name,
        mean_ms=statistics.mean(times),
        std_ms=statistics.stdev(times) if len(times) > 1 else 0,
        min_ms=min(times),
        max_ms=max(times),
        runs=runs,
    )


def print_result(res: BenchmarkResult):
    print(
        f"  {res.name:40}: {res.mean_ms:8.2f} ± {res.std_ms:6.2f} ms  (min={res.min_ms:.2f}, max={res.max_ms:.2f})"
    )


def run_iteration_benchmarks():
    results = []

    print("=" * 80)
    print("Iteration-based Benchmarks (10 runs each, 2 warmup)")
    print("=" * 80)

    print("\n[1] Bresenham Line (varying length)")
    for length in [100, 500, 1000, 2000, 5000]:
        res = run_benchmark(
            f"Bresenham {length}px", bresenham_line, (0, 0, length, length), runs=20
        )
        print_result(res)
        results.append(res)

    print("\n[2] Distance Transforms (100x100)")
    grid = generate_grid(100)
    for name, func in [
        ("Manhattan DT", manhattan_distance_transform),
        ("Euclidean DT", euclidean_distance_transform),
        ("JFA DT", jump_flooding_dt),
    ]:
        res = run_benchmark(name, func, (grid,), runs=10)
        print_result(res)
        results.append(res)

    print("\n[3] A* Pathfinding (varying size)")
    for size in [50, 100, 150]:
        grid = generate_grid(size)
        res = run_benchmark(
            f"A* {size}x{size}", a_star, (grid, (0, 0), (size - 1, size - 1)), runs=5
        )
        print_result(res)
        results.append(res)

    print("\n[4] Voronoi Diagram (100x100, varying seeds)")
    grid_size = 100
    for num_seeds in [5, 10, 20, 50]:
        seeds = generate_seeds(num_seeds, grid_size)
        res = run_benchmark(
            f"Voronoi {num_seeds} seeds",
            voronoi_diagram,
            (grid_size, grid_size, seeds),
            runs=5,
        )
        print_result(res)
        results.append(res)

    print("\n[5] Topology (varying size)")
    for size in [50, 100, 150]:
        grid = generate_grid(size)
        res = run_benchmark(
            f"Topology {size}x{size}", calculate_topology, (grid,), runs=5
        )
        print_result(res)
        results.append(res)

    print("\n[6] Persistent Homology H0 (varying size)")
    for size in [25, 50, 75]:
        grid = [[random.randint(0, 255) for _ in range(size)] for _ in range(size)]
        res = run_benchmark(
            f"H0 {size}x{size}", compute_h0_persistence, (grid,), runs=3
        )
        print_result(res)
        results.append(res)

    print("\n[7] Fractal Dimension (varying size)")
    for size in [50, 100, 150]:
        grid = generate_grid(size)
        res = run_benchmark(
            f"Fractal {size}x{size}", fractal_dimension, (grid,), runs=5
        )
        print_result(res)
        results.append(res)

    print("\n[8] Marching Tetrahedra (varying volume size)")
    for size in [10, 15, 20]:
        vol = generate_volume(size)
        res = run_benchmark(f"Marching {size}^3", marching_tetrahedra, (vol,), runs=5)
        print_result(res)
        results.append(res)

    print("\n[9] Zernike Moments (varying size)")
    for size in [50, 100, 150]:
        grid = generate_grid(size)
        res = run_benchmark(
            f"Zernike {size}x{size}",
            calculate_zernike_moments,
            (grid, size / 2),
            runs=5,
        )
        print_result(res)
        results.append(res)

    print("\n[10] Hausdorff Distance (varying point count)")
    for count in [50, 100, 200]:
        set1 = generate_point_set(count)
        set2 = generate_point_set(count)
        res = run_benchmark(
            f"Hausdorff {count}pts", hausdorff_distance, (set1, set2), runs=5
        )
        print_result(res)
        results.append(res)

    print("\n[11] ICP Alignment (varying point count)")
    for count in [50, 100, 200]:
        set1 = generate_point_set(count)
        set2 = generate_point_set(count)
        res = run_benchmark(
            f"ICP {count}pts", iterative_closest_point, (set1, set2), runs=3
        )
        print_result(res)
        results.append(res)

    print("\n[12] Medial Axis Transform (varying size)")
    for size in [50, 100, 150]:
        grid = generate_grid(size)
        res = run_benchmark(
            f"Medial {size}x{size}", medial_axis_transform, (grid,), runs=5
        )
        print_result(res)
        results.append(res)

    return results


def save_results(results: list[BenchmarkResult]):
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "iteration_benchmarks.json", "w") as f:
        import json

        data = [
            {
                "name": r.name,
                "mean_ms": r.mean_ms,
                "std_ms": r.std_ms,
                "min_ms": r.min_ms,
                "max_ms": r.max_ms,
                "runs": r.runs,
            }
            for r in results
        ]
        json.dump(data, f, indent=2)

    print(f"\n[Results saved to {output_dir / 'iteration_benchmarks.json'}]")


if __name__ == "__main__":
    random.seed(123)
    results = run_iteration_benchmarks()
    save_results(results)
