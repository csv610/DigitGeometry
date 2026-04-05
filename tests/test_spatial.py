"""Tests for spatial module."""

import pytest
from digital_geometry import (
    Quadtree,
    Octree,
    compute_reeb_graph,
    jump_flooding_dt,
    compute_sdf,
)


def test_quadtree():
    qt = Quadtree((0, 0, 100, 100), capacity=1)
    qt.insert((10, 10))
    qt.insert((20, 20))
    assert qt.divided


def test_octree():
    ot = Octree((0, 0, 0, 100, 100, 100), capacity=1)
    ot.insert((10, 10, 10))
    ot.insert((20, 20, 20))
    assert ot.divided


def test_jump_flooding_dt():
    import numpy as np
    grid = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8)
    dist = jump_flooding_dt(grid)
    assert dist[1, 1] == 0.0


def test_compute_sdf():
    import numpy as np
    grid = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8)
    sdf = compute_sdf(grid)
    assert sdf[1, 1] <= 0


def test_compute_reeb_graph():
    import numpy as np
    grid = np.array([[0, 0, 0], [0, 10, 0], [0, 0, 0]], dtype=np.float32)
    graph = compute_reeb_graph(grid)
    assert "nodes" in graph
