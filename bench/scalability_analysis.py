import time
import random
import json
import os
from pathlib import Path

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


def benchmark(name, func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    return (end - start) * 1000


def generate_grid(size):
    return [[random.choice([0, 0, 0, 1]) for _ in range(size)] for _ in range(size)]


def generate_volume(size):
    return [
        [[random.random() for _ in range(size)] for _ in range(size)]
        for _ in range(size)
    ]


def generate_point_set(count, scale=100):
    return [(random.random() * scale, random.random() * scale) for _ in range(count)]


def generate_seeds(count, size):
    return [
        (random.randint(0, size - 1), random.randint(0, size - 1)) for _ in range(count)
    ]


def run_scalability_analysis():
    results = {}

    print("=" * 70)
    print("Scalability Analysis: Performance vs Input Size")
    print("=" * 70)

    sizes = [50, 100, 200, 400]

    print("\n[1] Distance Transforms (grid size NxN)")
    print("-" * 50)
    for size in sizes:
        grid = generate_grid(size)
        t_manhattan = benchmark(
            f"Manhattan DT {size}x{size}", manhattan_distance_transform, grid
        )
        t_euclidean = benchmark(
            f"Euclidean DT {size}x{size}", euclidean_distance_transform, grid
        )
        t_jfa = benchmark(f"JFA DT {size}x{size}", jump_flooding_dt, grid)
        print(
            f"  {size}x{size}: Manhattan={t_manhattan:7.2f}ms, Euclidean={t_euclidean:7.2f}ms, JFA={t_jfa:7.2f}ms"
        )
        results[f"dt_{size}"] = {
            "manhattan": t_manhattan,
            "euclidean": t_euclidean,
            "jfa": t_jfa,
        }

    print("\n[2] A* Pathfinding (grid size NxN)")
    print("-" * 50)
    for size in sizes:
        grid = generate_grid(size)
        t = benchmark(f"A* {size}x{size}", a_star, grid, (0, 0), (size - 1, size - 1))
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"astar_{size}"] = t

    print("\n[3] Voronoi Diagram (grid size NxN, 10 seeds)")
    print("-" * 50)
    for size in sizes:
        seeds = generate_seeds(10, size)
        t = benchmark(f"Voronoi {size}x{size}", voronoi_diagram, size, size, seeds)
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"voronoi_{size}"] = t

    print("\n[4] Topology (grid size NxN)")
    print("-" * 50)
    for size in sizes:
        grid = generate_grid(size)
        t = benchmark(f"Topology {size}x{size}", calculate_topology, grid)
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"topology_{size}"] = t

    print("\n[5] Persistent Homology H0 (grid size NxN)")
    print("-" * 50)
    small_sizes = [25, 50, 75, 100]
    for size in small_sizes:
        grid = [[random.randint(0, 255) for _ in range(size)] for _ in range(size)]
        t = benchmark(f"H0 Persistence {size}x{size}", compute_h0_persistence, grid)
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"h0_{size}"] = t

    print("\n[6] Fractal Dimension (grid size NxN)")
    print("-" * 50)
    for size in sizes:
        grid = generate_grid(size)
        t = benchmark(f"Fractal {size}x{size}", fractal_dimension, grid)
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"fractal_{size}"] = t

    print("\n[7] Marching Tetrahedra (volume size NxNxN)")
    print("-" * 50)
    vol_sizes = [10, 15, 20, 25]
    for size in vol_sizes:
        vol = generate_volume(size)
        t = benchmark(f"Marching {size}^3", marching_tetrahedra, vol)
        print(f"  {size}^3: {t:7.2f}ms")
        results[f"marching_{size}"] = t

    print("\n[8] Zernike Moments (grid size NxN)")
    print("-" * 50)
    for size in sizes:
        grid = generate_grid(size)
        t = benchmark(
            f"Zernike {size}x{size}", calculate_zernike_moments, grid, size / 2
        )
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"zernike_{size}"] = t

    print("\n[9] Hausdorff Distance (N points)")
    print("-" * 50)
    point_counts = [50, 100, 200, 400]
    for count in point_counts:
        set1 = generate_point_set(count)
        set2 = generate_point_set(count)
        t = benchmark(f"Hausdorff {count}pts", hausdorff_distance, set1, set2)
        print(f"  {count} points: {t:7.2f}ms")
        results[f"hausdorff_{count}"] = t

    print("\n[10] ICP Alignment (N points)")
    print("-" * 50)
    for count in point_counts:
        set1 = generate_point_set(count)
        set2 = generate_point_set(count)
        t = benchmark(f"ICP {count}pts", iterative_closest_point, set1, set2)
        print(f"  {count} points: {t:7.2f}ms")
        results[f"icp_{count}"] = t

    print("\n[11] Medial Axis Transform (grid size NxN)")
    print("-" * 50)
    for size in sizes:
        grid = generate_grid(size)
        t = benchmark(f"Medial Axis {size}x{size}", medial_axis_transform, grid)
        print(f"  {size}x{size}: {t:7.2f}ms")
        results[f"medial_{size}"] = t

    return results


def compute_complexity(results):
    print("\n" + "=" * 70)
    print("Complexity Analysis")
    print("=" * 70)

    def estimate_complexity(results_dict, key_prefix, subkey=None):
        values = []
        for k, v in results_dict.items():
            if k.startswith(key_prefix):
                if isinstance(v, dict) and subkey:
                    values.append((int(k.split("_")[-1]), v[subkey]))
                elif not isinstance(v, dict):
                    n = int(k.split("_")[-1])
                    values.append((n, v))
        values.sort(key=lambda x: x[0])
        if len(values) < 2:
            return "N/A"
        n1, t1 = values[0]
        n2, t2 = values[-1]
        if t1 <= 0:
            return "N/A"
        ratio = (t2 / t1) / ((n2 / n1) ** 2)
        if ratio < 0.5:
            return "O(n)"
        elif ratio < 2:
            return "O(n log n)"
        elif ratio < 10:
            return "O(n^2)"
        else:
            return "O(n^2+) or worse"

    complexity_estimates = {
        "Manhattan DT": estimate_complexity(results, "dt_", "manhattan") + " (approx)",
        "Euclidean DT": estimate_complexity(results, "dt_", "euclidean") + " (approx)",
        "JFA DT": estimate_complexity(results, "dt_", "jfa") + " (approx)",
        "A* Search": estimate_complexity(results, "astar_"),
        "Voronoi": estimate_complexity(results, "voronoi_"),
        "Topology": estimate_complexity(results, "topology_"),
        "H0 Persistence": estimate_complexity(results, "h0_"),
        "Fractal Dimension": estimate_complexity(results, "fractal_"),
        "Marching Tetrahedra": estimate_complexity(results, "marching_"),
        "Zernike Moments": estimate_complexity(results, "zernike_"),
        "Hausdorff": estimate_complexity(results, "hausdorff_"),
        "ICP": estimate_complexity(results, "icp_"),
        "Medial Axis": estimate_complexity(results, "medial_"),
    }

    for op, comp in complexity_estimates.items():
        print(f"  {op:20}: {comp}")

    return complexity_estimates


def save_results(results, complexity):
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    data = {"scalability": results, "complexity": complexity}

    with open(output_dir / "scalability_results.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n[Results saved to {output_dir / 'scalability_results.json'}]")


if __name__ == "__main__":
    random.seed(42)
    results = run_scalability_analysis()
    complexity = compute_complexity(results)
    save_results(results, complexity)
