"""Tests for pyramids module."""

import pytest
from digital_geometry import build_gaussian_pyramid, build_laplacian_pyramid


def test_gaussian_pyramid():
    grid = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
    gauss_pyr = build_gaussian_pyramid(grid, levels=2)
    assert len(gauss_pyr) == 2


def test_laplacian_pyramid():
    grid = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
    gauss_pyr = build_gaussian_pyramid(grid, levels=2)
    lapl_pyr = build_laplacian_pyramid(gauss_pyr)
    assert len(lapl_pyr) == 2
