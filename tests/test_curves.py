"""Tests for curves module."""

import pytest
from digital_geometry import (
    point_in_polygon,
    convex_hull,
    douglas_peucker,
    is_digitally_straight,
    estimate_tangents,
    compute_curvature,
    certify_dsls,
    dsls_Arithmetical_Distance,
    naive_dsls_recognition,
)


def test_point_in_polygon():
    polygon = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
    assert point_in_polygon((0.5, 0.5), polygon) == True
    assert point_in_polygon((1.5, 1.5), polygon) == False


def test_convex_hull():
    points = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 5)]
    hull = convex_hull(points)
    assert (5, 5) not in hull


def test_douglas_peucker():
    points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    assert douglas_peucker(points, 0.1) == [(0, 0), (4, 0)]


def test_is_digitally_straight():
    line = [(0, 0), (1, 0), (2, 0), (3, 0)]
    assert is_digitally_straight(line)


def test_estimate_tangents():
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    tangents = estimate_tangents(points, k=1)
    assert len(tangents) == 4


def test_compute_curvature():
    points = [(0, 0), (1, 1), (2, 0)]
    curvatures = compute_curvature(points, is_closed=False)
    assert len(curvatures) == 3


def test_certify_dsls():
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    is_straight, a, b, mu = certify_dsls(points)
    assert is_straight == True


def test_dsls_arithmetical_distance():
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    dist = dsls_Arithmetical_Distance(points)
    assert dist == 0


def test_naive_dsls_recognition():
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    result = naive_dsls_recognition(points)
    assert result is not None
