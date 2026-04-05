import time
import random
from digital_geometry import (
    bresenham_line,
    manhattan_distance_transform,
    euclidean_distance_transform,
    a_star,
    voronoi_diagram,
    compute_topology,
    compute_h0_persistence,
    jump_flooding_dt,
    fractal_dimension,
    marching_tetrahedra,
    compute_zernike_moments,
    hausdorff_distance,
    iterative_closest_point,
    medial_axis_transform
)

def benchmark(name, func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    print(f"{name:30}: {(end - start) * 1000:8.2f} ms")

def run_benchmarks():
    print("Digital Geometry Benchmarks")
    print("-" * 50)
    
    # 1. Bresenham Line (Long line)
    benchmark("Bresenham (1000px)", bresenham_line, 0, 0, 1000, 1000)
    
    # 2. Distance Transforms (100x100 grid)
    size = 100
    grid = [[random.choice([0, 0, 0, 1]) for _ in range(size)] for _ in range(size)]
    benchmark("Manhattan DT (100x100)", manhattan_distance_transform, grid)
    benchmark("Euclidean DT (100x100)", euclidean_distance_transform, grid)
    benchmark("JFA DT (100x100)", jump_flooding_dt, grid)
    
    # 3. A* Search (100x100 grid with obstacles)
    benchmark("A* Search (100x100)", a_star, grid, (0, 0), (99, 99))
    
    # 4. Voronoi Diagram (100x100, 10 seeds)
    seeds = [(random.randint(0, 99), random.randint(0, 99)) for _ in range(10)]
    benchmark("Voronoi (100x100, 10 seeds)", voronoi_diagram, 100, 100, seeds)
    
    # 5. Topology (100x100)
    benchmark("Topology (100x100)", compute_topology, grid)
    
    # 6. Persistent Homology (50x50)
    size_ph = 50
    grid_ph = [[random.randint(0, 255) for _ in range(size_ph)] for _ in range(size_ph)]
    benchmark("H0 Persistence (50x50)", compute_h0_persistence, grid_ph)

    # 7. Complexity & 3D
    benchmark("Fractal Dimension (100x100)", fractal_dimension, grid)
    vol = [[[random.random() for _ in range(20)] for _ in range(20)] for _ in range(20)]
    benchmark("Marching Tetrahedra (20^3)", marching_tetrahedra, vol)

    # 8. Research Grade Tools
    benchmark("Zernike Moments (degree 4)", compute_zernike_moments, grid, 50.0)
    
    set1 = [(random.random()*100, random.random()*100) for _ in range(100)]
    set2 = [(random.random()*100, random.random()*100) for _ in range(100)]
    benchmark("Hausdorff Distance (100 pts)", hausdorff_distance, set1, set2)
    benchmark("ICP Alignment (100 pts)", iterative_closest_point, set1, set2)
    
    benchmark("Medial Axis (100x100)", medial_axis_transform, grid)

if __name__ == "__main__":
    run_benchmarks()
