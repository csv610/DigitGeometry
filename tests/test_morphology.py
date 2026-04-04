"""Tests for morphology module."""

import pytest
from digital_geometry import (
    dilate,
    erode,
    morph_opening,
    morph_closing,
    morph_boundary,
    morphological_skeleton,
    geodesic_dilation,
    geodesic_erosion,
    create_square_se,
    morph_erode,
    white_tophat,
    black_tophat,
)


def test_dilate():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = dilate(grid)
    assert result[1][1] == 1


def test_erode():
    grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    result = erode(grid)
    assert result[1][1] == 1


def test_morph_opening():
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    result = morph_opening(grid)
    assert result[2][2] == 1


def test_morph_closing():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = morph_closing(grid)
    assert result[1][1] == 1


def test_morph_boundary():
    grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    boundary = morph_boundary(grid)
    assert boundary[0][1] == 1


def test_morphological_skeleton():
    grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    skeleton = morphological_skeleton(grid)
    assert len(skeleton) == 3


def test_geodesic_dilation():
    grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    mask = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    dilated = geodesic_dilation(grid, mask, iterations=1)
    assert dilated[0][2] == 1


def test_geodesic_erosion():
    grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    mask = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    eroded = geodesic_erosion(grid, mask, iterations=1)
    assert eroded[1][1] == 1


def test_create_square_se():
    se = create_square_se(3)
    assert len(se) == 3
    assert len(se[0]) == 3


def test_white_tophat():
    grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    result = white_tophat(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_black_tophat():
    grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    result = black_tophat(grid)
    assert len(result) == 3
    assert len(result[0]) == 3
