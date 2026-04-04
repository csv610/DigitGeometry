"""Tests for volume3d module."""

import pytest
import math
from digital_geometry import (
    zhang_suen_thinning,
    thinning_3d,
    marching_squares,
    marching_tetrahedra,
    marching_cubes,
    medial_axis_transform,
    medial_axis_transform_3d,
    fractal_dimension,
    is_simple_point_2d,
    is_simple_point_3d,
    dominant_laplacian_eigenvalues,
    laplacian_mesh_smoothing,
    mesh_simplification_edge_collapse,
    active_contour_snake,
    iterative_closest_point,
    mean_curvature_flow_grid,
    prune_skeleton,
    skeleton_to_graph,
)


def test_zhang_suen_thinning():
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    thinned = zhang_suen_thinning(grid)
    assert sum(thinned[2]) >= 1


def test_thinning_3d():
    vol = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for z in range(5):
        for y in range(5):
            for x in range(5):
                if (x - 2) ** 2 + (y - 2) ** 2 + (z - 2) ** 2 <= 4:
                    vol[z][y][x] = 1
    thinned = thinning_3d(vol)
    assert isinstance(thinned, list)


def test_marching_squares():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    lines = marching_squares(grid, threshold=0.5)
    assert isinstance(lines, list)


def test_marching_tetrahedra():
    vol = [[[0.0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for z in range(4):
        for y in range(4):
            for x in range(4):
                if (x - 1.5) ** 2 + (y - 1.5) ** 2 + (z - 1.5) ** 2 <= 1:
                    vol[z][y][x] = 1.0
    v, f = marching_tetrahedra(vol, threshold=0.5)
    assert len(v) >= 0


def test_marching_cubes():
    vol = [[[0.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]]]
    vertices, triangles = marching_cubes(vol, threshold=0.5)
    assert isinstance(vertices, list)


def test_medial_axis_transform():
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    mat = medial_axis_transform(grid)
    assert len(mat) == 5
    assert len(mat[0]) == 5


def test_medial_axis_transform_3d():
    vol = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for z in range(1, 4):
        for y in range(1, 4):
            for x in range(1, 4):
                vol[z][y][x] = 1
    mat = medial_axis_transform_3d(vol)
    assert mat[2][2][2] == 1


def test_fractal_dimension():
    grid = [[0 for _ in range(32)] for _ in range(32)]
    for i in range(32):
        grid[16][i] = 1
    dim = fractal_dimension(grid)
    assert 0.8 < dim < 1.2


def test_is_simple_point_2d():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert not is_simple_point_2d(grid, 1, 1)

    grid = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
    assert is_simple_point_2d(grid, 1, 1)


def test_is_simple_point_3d():
    vol = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for z in range(3):
        for y in range(3):
            for x in range(3):
                vol[z][y][x] = 1
    assert is_simple_point_3d(vol, 1, 1, 1)


def test_dominant_laplacian_eigenvalues():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    eigs = dominant_laplacian_eigenvalues(grid, k=1)
    assert len(eigs) == 1


def test_laplacian_mesh_smoothing():
    vertices = [(0, 0, 0), (1, 0, 0), (0.5, 1, 0), (0.5, 0.5, 1)]
    faces = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
    v_out, f_out = laplacian_mesh_smoothing(vertices, faces, iterations=1)
    assert v_out[3][2] < 1.0


def test_mesh_simplification():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    faces = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
    v_out, f_out = mesh_simplification_edge_collapse(vertices, faces, target_count=2)
    assert len(f_out) <= 4


def test_active_contour_snake():
    grid = [[0.0 for _ in range(20)] for _ in range(20)]
    for y in range(5, 15):
        for x in range(5, 15):
            grid[y][x] = 1.0
    initial = [
        (
            10 + 8 * math.cos(i * math.pi / 4),
            10 + 8 * math.sin(i * math.pi / 4),        )
        for i in range(8)
    ]
    final = active_contour_snake(grid, initial, max_iterations=5)
    assert len(final) == 8


def test_iterative_closest_point():
    source = [(0, 0), (1, 0), (0, 1)]
    target = [(1, 1), (2, 1), (1, 2)]
    aligned = iterative_closest_point(source, target)
    c_s = [sum(p[0] for p in aligned) / 3, sum(p[1] for p in aligned) / 3]
    assert abs(c_s[0] - 4.0 / 3.0) < 0.1


def test_mean_curvature_flow_grid():
    grid = [[0.0 for _ in range(5)] for _ in range(5)]
    grid[2][2] = 10.0
    flowed = mean_curvature_flow_grid(grid, iterations=5, step_size=0.05)
    assert flowed[2][2] < 10.0


def test_prune_skeleton():
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    pruned = prune_skeleton(grid, min_branch_length=3)
    assert pruned[3][2] == 0


def test_skeleton_to_graph():
    graph_grid = [[0, 0, 0], [1, 1, 1], [0, 1, 0]]
    graph = skeleton_to_graph(graph_grid)
    assert (1, 1) in graph
