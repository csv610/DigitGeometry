import pytest
import numpy as np
from digital_geometry.registration import iterative_closest_point


def test_icp_basic():
    source = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    target = [(1, 1, 0), (2, 1, 0), (1, 2, 0)]
    result = iterative_closest_point(source, target, max_iterations=5)
    assert len(result) == 3
    assert all(len(p) == 3 for p in result)


def test_icp_single_point():
    source = [(0, 0, 0)]
    target = [(1, 1, 1)]
    result = iterative_closest_point(source, target)
    assert len(result) == 1


def test_icp_empty():
    result = iterative_closest_point([], [])
    assert result == []


def test_icp_2d():
    source = [(0, 0), (1, 0), (0, 1)]
    target = [(1, 1), (2, 1), (1, 2)]
    result = iterative_closest_point(source, target)
    assert len(result) == 3
    assert all(len(p) == 2 for p in result)


def test_icp_convergence():
    source = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (2, 2, 0)]
    target = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (2, 2, 0)]
    result = iterative_closest_point(source, target, max_iterations=10)
    assert len(result) == 4
