"""Tests for transforms module."""

import pytest
import math
from digital_geometry import (
    translate_points,
    rotate_points,
    scale_points,
    translate_grid,
    rotate_grid,
    scale_grid,
    bilinear_resample,
    bicubic_resample,
    upscale_grid,
    downscale_grid,
)


def test_translate_points():
    points = [(1, 1)]
    tp = translate_points(points, 2, 3)
    assert tp[0] == (3, 4)


def test_rotate_points():
    points = [(1, 1)]
    rp = rotate_points(points, 90, center=(0, 0))
    assert abs(rp[0][0] + 1) < 1e-6
    assert abs(rp[0][1] - 1) < 1e-6


def test_scale_points():
    points = [(2, 2)]
    sp = scale_points(points, 2, 2, center=(0, 0))
    assert sp[0] == (4, 4)


def test_translate_grid():
    grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    t_grid = translate_grid(grid, 1, 1)
    assert t_grid[1][1] == 1


def test_rotate_grid():
    grid = [[0, 1], [0, 0]]
    rotated = rotate_grid(grid, 90)
    assert len(rotated) == 2


def test_scale_grid():
    grid = [[1, 0], [0, 0]]
    scaled = scale_grid(grid, 2, 2)
    assert len(scaled) == 4


def test_bilinear_resample():
    grid = [[1.0, 0.0], [0.0, 1.0]]
    result = bilinear_resample(grid, 2.0)
    assert len(result) == 4
    assert len(result[0]) == 4


def test_bicubic_resample():
    grid = [[1.0, 0.0], [0.0, 1.0]]
    result = bicubic_resample(grid, 2.0)
    assert len(result) == 4


def test_upscale_grid():
    grid = [[1, 0], [0, 1]]
    upscaled = upscale_grid(grid, 2)
    assert len(upscaled) == 4
    assert upscaled[0][0] == 1


def test_downscale_grid():
    grid = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
    downscaled = downscale_grid(grid, 2)
    assert len(downscaled) == 2
