"""Tests for pathfinding module."""

import pytest
from digital_geometry import a_star, fast_marching_method


def test_a_star():
    grid = [[0]]
    assert a_star(grid, (0, 0), (0, 0)) == [(0, 0)]
    grid = [[1, 0], [0, 0]]
    assert a_star(grid, (0, 0), (1, 1)) == []


def test_fast_marching():
    grid = [[1.0 for _ in range(5)] for _ in range(5)]
    seeds = [(2, 2)]
    times = fast_marching_method(grid, seeds)
    assert times[2][2] == 0.0
    assert times[2][3] > 0.0
