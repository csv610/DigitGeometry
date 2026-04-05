"""Tests for 3D geometry module."""

import pytest
from digital_geometry.geometry3d import (
    compute_surface_normals,
    compute_normals_cross_product,
    fit_plane_least_squares,
    compute_curvature_2d,
)


def test_compute_surface_normals():
    grid = [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
    normals = compute_surface_normals(grid)
    assert len(normals) == 3
    assert len(normals[0]) == 3


def test_compute_normals_cross_product():
    grid = [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
    normals = compute_normals_cross_product(grid)
    assert len(normals) == 3
    assert len(normals[0]) == 3


def test_fit_plane_least_squares():
    points = [(0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 2)]
    a, b, c, d = fit_plane_least_squares(points)
    assert isinstance(a, float)


def test_compute_curvature_2d():
    grid = [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
    curvature = compute_curvature_2d(grid)
    assert len(curvature) == 3
    assert len(curvature[0]) == 3
