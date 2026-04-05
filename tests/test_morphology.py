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
    tophat,
    bothat,
    Morphology,
    apply_morphology,
    morphological_filter,
    remove_small_holes,
    remove_small_regions,
    extract_peaks,
    extract_valleys,
    remove_white_dots,
    remove_black_dots,
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


def test_tophat():
    grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    result = tophat(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_bothat():
    grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    result = bothat(grid)
    assert len(result) == 3
    assert len(result[0]) == 3


def test_morphology_class():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    m = Morphology(grid)
    result = m.dilate().get()
    assert result[1][1] == 1


def test_morphology_chaining():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    m = Morphology(grid)
    result = m.dilate().erode().get()
    assert result[1][1] == 1


def test_apply_morphology():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = apply_morphology(grid, "dilate")
    assert result[1][1] == 1


def test_morphological_filter():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = morphological_filter(grid, ["dilate", "erode"])
    assert result[1][1] == 1


def test_remove_small_holes():
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    result = remove_small_holes(grid, 2)
    assert result[1][1] == 1


def test_remove_small_regions():
    grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    result = remove_small_regions(grid, 5)
    assert result[1][1] == 1


def test_extract_peaks():
    grid = [[0, 1, 0], [1, 2, 1], [0, 1, 0]]
    result = extract_peaks(grid)
    assert len(result) == 3


def test_extract_valleys():
    grid = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
    result = extract_valleys(grid)
    assert len(result) == 3


def test_remove_white_dots():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result = remove_white_dots(grid)
    assert result[1][1] == 0


def test_remove_black_dots():
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    result = remove_black_dots(grid)
    assert result[1][1] == 1
