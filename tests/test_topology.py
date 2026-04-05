"""Tests for topology module."""

import pytest
from digital_geometry import (
    count_connected_components,
    compute_topology,
    compute_h0_persistence,
    compute_h1_persistence,
    compute_surface_curvatures,
    connected_components_3d,
)


def test_count_connected_components():
    grid = [[0, 0], [0, 0]]
    assert count_connected_components(grid) == 0


def test_compute_topology():
    grid = [[0, 0], [0, 0]]
    topo = compute_topology(grid)
    assert topo["b0"] == 0
    assert topo["b1"] == 0


def test_connected_components_3d():
    vol = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    vol[1][1][1] = 1
    vol[1][1][2] = 1
    labels, count = connected_components_3d(vol, target_value=1, connectivity=6)
    assert count == 1


def test_compute_surface_curvatures():
    grid = [[0.0 for _ in range(5)] for _ in range(5)]
    grid[2][2] = 1.0
    curvatures = compute_surface_curvatures(grid)
    assert curvatures[2][2] != 0
