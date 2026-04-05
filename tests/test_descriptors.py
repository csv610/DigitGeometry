"""Tests for descriptors module."""

import pytest
from digital_geometry import (
    compute_hu_moments,
    compute_zernike_moments,
    fourier_descriptors,
    shape_context_descriptor,
    generalized_hough_transform,
    detect_critical_points,
)


def test_compute_hu_moments():
    grid1 = [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    hu1 = compute_hu_moments(grid1)
    assert len(hu1) == 7


def test_compute_zernike_moments():
    grid = [[0 for _ in range(10)] for _ in range(10)]
    for y in range(3, 7):
        for x in range(3, 7):
            grid[y][x] = 1
    moments = compute_zernike_moments(grid, radius=5.0, degree=2)
    assert moments[0] > 0


def test_fourier_descriptors():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    fd = fourier_descriptors(points, n_descriptors=3)
    assert len(fd) == 3


def test_shape_context_descriptor():
    points = [(0, 0), (1, 0), (0, 1)]
    desc = shape_context_descriptor(points, n_bins_r=2, n_bins_theta=4)
    assert len(desc) == 3


def test_generalized_hough_transform():
    grid = [[0 for _ in range(10)] for _ in range(10)]
    for y in range(2, 5):
        for x in range(2, 5):
            grid[y][x] = 1
    template = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    acc = generalized_hough_transform(grid, template)
    assert len(acc) == 10
    assert len(acc[0]) == 10


def test_detect_critical_points():
    grid = [[0, 0, 0], [0, 10, 0], [0, 0, 0]]
    cp = detect_critical_points(grid)
    assert (1, 1) in cp["peaks"]
