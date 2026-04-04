"""Tests for contours module."""

import pytest
from digital_geometry import (
    flood_fill,
    moore_neighbor_boundary_trace,
    suzuki_contour_trace,
    run_length_encode,
    run_length_decode,
    freeman_chain_code,
)


def test_flood_fill():
    grid = [[0]]
    flood_fill(grid, 0, 0, 1)
    assert grid == [[1]]


def test_moore_neighbor_boundary_trace():
    grid = [[0, 1, 1], [0, 1, 1], [0, 0, 0]]
    boundary = moore_neighbor_boundary_trace(grid, 1, 1)
    assert len(boundary) >= 4


def test_suzuki_contour_trace():
    grid = [[0, 0, 0], [0, 1, 1], [0, 1, 1]]
    contours = suzuki_contour_trace(grid)
    assert len(contours) >= 1


def test_run_length_encode():
    grid = [[1, 1, 1, 0, 0]]
    rle = run_length_encode(grid)
    assert rle[0] == [(1, 3), (0, 2)]


def test_run_length_decode():
    rle = [[(1, 3), (0, 2)]]
    decoded = run_length_decode(rle, 5)
    assert decoded == [[1, 1, 1, 0, 0]]


def test_freeman_chain_code():
    points = [(0, 0), (1, 0), (1, 1)]
    chain = freeman_chain_code(points)
    assert len(chain) >= 2
