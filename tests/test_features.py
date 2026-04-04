"""Tests for feature detection module."""

import pytest
from digital_geometry.features import (
    harris_corner,
    shi_tomasi_corner,
    susan_corner,
    fast_corner,
    structure_tensor,
    compute_corner_response,
)


def test_harris_corner():
    grid = [[0] * 10 for _ in range(10)]
    grid[3][3] = 255
    grid[3][6] = 255
    grid[6][3] = 255
    grid[6][6] = 255
    corners = harris_corner(grid)
    assert isinstance(corners, list)


def test_shi_tomasi_corner():
    grid = [[0] * 10 for _ in range(10)]
    grid[4][4] = 255
    grid[4][6] = 255
    corners = shi_tomasi_corner(grid)
    assert isinstance(corners, list)


def test_susan_corner():
    grid = [[100] * 10 for _ in range(10)]
    grid[5][5] = 200
    corners = susan_corner(grid)
    assert isinstance(corners, list)


def test_fast_corner():
    grid = [[0] * 10 for _ in range(10)]
    grid[5][5] = 255
    corners = fast_corner(grid)
    assert isinstance(corners, list)


def test_structure_tensor():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = structure_tensor(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_compute_corner_response():
    grid = [[0] * 10 for _ in range(10)]
    grid[5][5] = 255
    response = compute_corner_response(grid)
    assert len(response) == 10
    assert len(response[0]) == 10
