"""Tests for segmentation module."""

import pytest
from digital_geometry import (
    min_cut_max_flow,
    graph_cut_segmentation,
    watershed_transform,
)


def test_min_cut_max_flow():
    capacity = [[0, 1, 1], [0, 0, 1], [0, 0, 0]]
    flow = min_cut_max_flow(capacity, 0, 2)
    assert flow >= 0


def test_graph_cut_segmentation():
    grid = [[10 for _ in range(10)] for _ in range(10)]
    for y in range(5, 10):
        for x in range(10):
            grid[y][x] = 200
    fg = [(0, 7)]
    bg = [(0, 2)]
    seg = graph_cut_segmentation(grid, fg, bg)
    assert len(seg) == 10
    assert len(seg[0]) == 10


def test_watershed_transform():
    grid = [[0, 0, 0, 0, 0], [0, 10, 0, 8, 0], [0, 0, 0, 0, 0]]
    labeled = watershed_transform(grid)
    assert len(labeled) == 3
    assert len(labeled[0]) == 5
