"""Tests for edge detection module."""

import pytest
from digital_geometry.edge import (
    sobel,
    prewitt,
    roberts,
    laplacian_4,
    laplacian_8,
    canny,
    gaussian_smooth,
)


def test_sobel():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = sobel(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_prewitt():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = prewitt(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_roberts():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = roberts(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_laplacian_4():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = laplacian_4(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_laplacian_8():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = laplacian_8(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_gaussian_smooth():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = gaussian_smooth(grid, sigma=1.0)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_canny():
    grid = [[0] * 10 for _ in range(10)]
    for i in range(3, 7):
        for j in range(3, 7):
            grid[i][j] = 255
    result = canny(grid)
    assert len(result) == 10
    assert len(result[0]) == 10
