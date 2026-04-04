"""Tests for shape analysis module."""

import pytest
from digital_geometry.shape import (
    polygon_area,
    polygon_centroid,
    polygon_perimeter,
    point_to_polygon_distance,
    bounding_box,
    shape_circularity,
    shape_solidity,
    shape_aspect_ratio,
    shape_eccentricity,
    shape_extent,
    shape_compactness,
)


def test_polygon_area():
    polygon = [(0, 0), (4, 0), (4, 3), (0, 3)]
    area = polygon_area(polygon)
    assert area == 12.0


def test_polygon_centroid():
    polygon = [(0, 0), (4, 0), (4, 3), (0, 3)]
    cx, cy = polygon_centroid(polygon)
    assert 1.5 < cx < 2.5
    assert 1.0 < cy < 2.0


def test_polygon_perimeter():
    polygon = [(0, 0), (3, 0), (3, 4), (0, 4)]
    perimeter = polygon_perimeter(polygon)
    assert perimeter == 14.0


def test_point_to_polygon_distance():
    polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
    dist = point_to_polygon_distance(5, 2, polygon)
    assert dist == 1.0


def test_bounding_box():
    points = [(0, 0), (3, 0), (3, 4), (0, 4)]
    xmin, ymin, xmax, ymax = bounding_box(points)
    assert xmin == 0
    assert ymin == 0
    assert xmax == 3
    assert ymax == 4


def test_shape_circularity():
    polygon = [(0, 0), (2, 0), (2, 2), (0, 2)]
    circ = shape_circularity(polygon)
    assert circ > 0


def test_shape_solidity():
    polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
    solidity = shape_solidity(polygon)
    assert solidity == 1.0


def test_shape_aspect_ratio():
    points = [(0, 0), (4, 0), (4, 2), (0, 2)]
    aspect = shape_aspect_ratio(points)
    assert aspect == 2.0


def test_shape_eccentricity():
    points = [(0, 0), (2, 0), (2, 1), (0, 1)]
    ecc = shape_eccentricity(points)
    assert ecc > 0


def test_shape_extent():
    points = [(0, 0), (2, 0), (2, 2), (0, 2)]
    extent = shape_extent(points)
    assert extent == 1.0


def test_shape_compactness():
    polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
    compactness = shape_compactness(polygon)
    assert compactness > 0
