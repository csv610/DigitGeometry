"""Tests for raster module."""

import pytest
from digital_geometry import (
    bresenham_line,
    midpoint_circle,
    wu_line,
    supercover_line_2d,
    supercover_line_3d,
    scanline_polygon_fill,
)


def test_bresenham_line():
    assert bresenham_line(5, 5, 5, 5) == [(5, 5)]
    assert bresenham_line(0, 0, 1, 0) == [(0, 0), (1, 0)]
    assert len(bresenham_line(0, 0, 100, 100)) == 101


def test_midpoint_circle():
    assert midpoint_circle(5, 5, 0) == [(5, 5)]
    circle = midpoint_circle(0, 0, 1)
    assert len(circle) == 4


def test_wu_line():
    points = wu_line(0, 0, 5, 5)
    assert len(points) > 0
    assert points[0] == (0, 0, 1.0)


def test_supercover_line():
    points_2d = supercover_line_2d(0, 0, 3, 3)
    assert len(points_2d) >= 4
    assert (0, 0) in points_2d

    points_3d = supercover_line_3d(0, 0, 0, 2, 2, 2)
    assert len(points_3d) >= 3
    assert (0, 0, 0) in points_3d
    assert (2, 2, 2) in points_3d


def test_scanline_polygon_fill():
    polygon = [(1, 1), (5, 1), (5, 5), (1, 5)]
    grid = scanline_polygon_fill(polygon, 10, 10, 1)
    assert grid[3][3] == 1
    assert grid[0][0] == 0
