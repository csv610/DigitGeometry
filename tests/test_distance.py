"""Tests for distance module."""

import pytest
from digital_geometry import (
    manhattan_distance,
    euclidean_distance,
    manhattan_distance_transform,
    euclidean_distance_transform,
    chamfer_distance_transform,
    geodesic_distance_transform,
    voronoi_diagram,
    hausdorff_distance,
    earth_movers_distance,
)


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7


def test_euclidean_distance():
    assert abs(euclidean_distance((0, 0), (3, 4)) - 5.0) < 1e-6


def test_manhattan_distance_transform():
    grid = [[0, 0], [0, 0]]
    assert manhattan_distance_transform(grid)[0][0] == float("inf")


def test_euclidean_distance_transform():
    grid = [[0, 0], [0, 0]]
    dist = euclidean_distance_transform(grid)
    assert dist[0][0] == 0


def test_chamfer_distance_transform():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    dist = chamfer_distance_transform(grid)
    assert dist[1][1] == 0.0


def test_geodesic_distance_transform():
    grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    mask = [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
    dist = geodesic_distance_transform(grid, mask)
    assert dist[0][0] == 0


def test_voronoi_diagram():
    assert voronoi_diagram(3, 3, []).tolist() == [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]


def test_hausdorff_distance():
    set1 = [(0, 0), (1, 0), (0, 1)]
    set2 = [(0, 0), (1, 0), (0, 1.1)]
    assert 0.09 < hausdorff_distance(set1, set2) < 0.11


def test_earth_movers_distance():
    h1 = [1, 0, 0]
    h2 = [0, 0, 1]
    assert earth_movers_distance(h1, h2) == 2.0
