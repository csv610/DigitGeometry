"""Tests for voxel module."""

import pytest
import numpy as np
from digital_geometry.voxel import (
    get_neighbors_6,
    get_neighbors_18,
    get_neighbors_26,
    classify_voxel_grid,
    find_voxel_borders,
    find_voxel_edges,
    find_voxel_vertices,
    voxelize_triangle_mesh,
    voxelize_surface_mesh,
    surface_nets,
    ray_voxel_intersection,
    ray_cast_volume,
    minkowski_sum_voxel,
    merge_voxels,
    voxel_euler_number,
    voxel_connectivity_count,
    voxel_sdf_3d,
    skeleton_3d_medial,
    extract_boundary_faces,
    voxel_dilate_3d,
    voxel_erode_3d,
    fill_voxel_holes,
    compute_voxel_moments,
    extract_3d_contours,
    voxel_to_octree,
    octree_to_voxel,
    voxel_contour_3d,
    SparseVoxelOctree,
    build_sparse_voxel_octree,
    VoxelNeighborLookup,
    voxel_coloring,
    voxel_separated,
    cut_voxel_by_plane,
    volume_raymarch,
    volume_raymarch_with_normal,
    smooth_isosurface,
    voxel_gradient_normals,
    dual_contouring,
    VoxelEpitome,
    build_voxel_epitomes,
    voxel_pyramid,
    is_voxel_surface_manifold,
    voxel_junction_count,
    voxel_endpoint_count,
    EulerOperators,
    detect_3d_corners,
    detect_3d_junctions,
    morphological_skeleton,
    voxel_carving,
)


def test_get_neighbors_6():
    n = get_neighbors_6(0, 0, 0)
    assert len(n) == 6


def test_get_neighbors_18():
    n = get_neighbors_18(0, 0, 0)
    assert len(n) == 18


def test_get_neighbors_26():
    n = get_neighbors_26(0, 0, 0)
    assert len(n) == 26


def test_classify_voxel_grid():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    result = classify_voxel_grid(volume)
    assert result.shape == (2, 2, 2)
    assert result[0, 0, 0] == "boundary"


def test_find_voxel_borders():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    borders = find_voxel_borders(volume)
    assert len(borders) > 0
    assert isinstance(borders, np.ndarray)


def test_find_voxel_edges():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    volume[0, 0, 1] = 1
    volume[0, 1, 0] = 1
    edges = find_voxel_edges(volume)
    assert isinstance(edges, np.ndarray)


def test_find_voxel_vertices():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    volume[0, 0, 1] = 1
    volume[0, 1, 0] = 1
    volume[1, 0, 0] = 1
    vertices = find_voxel_vertices(volume)
    assert isinstance(vertices, np.ndarray)


def test_voxelize_triangle_mesh():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [(0, 1, 2)]
    volume = voxelize_triangle_mesh(vertices, triangles, resolution=8)
    assert len(volume) == 8
    assert len(volume[0]) == 8
    assert len(volume[0][0]) == 8


def test_voxelize_surface_mesh():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [(0, 1, 2)]
    volume = voxelize_surface_mesh(vertices, triangles, resolution=8)
    assert len(volume) == 8


def test_surface_nets():
    volume = np.zeros((4, 4, 4), dtype=np.uint8)
    volume[1, 1, 1] = 1
    volume[2, 2, 2] = 1
    vertices, faces = surface_nets(volume)
    assert isinstance(vertices, list)


def test_voxel_carving():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [(0, 1, 2)]
    silhouettes = [np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]], dtype=np.uint8)]
    result = voxel_carving(vertices, triangles, silhouettes, resolution=8)
    assert result is not None


def test_ray_voxel_intersection():
    origin = (0, 0, 0)
    direction = (1, 0, 0)
    bounds = ((0, 0, 0), (1, 1, 1))
    result = ray_voxel_intersection(origin, direction, bounds)
    assert result is not None


def test_ray_cast_volume():
    volume = np.ones((4, 4, 4), dtype=np.uint8)
    origin = (0, 0, 0)
    direction = (1, 1, 1)
    result = ray_cast_volume(origin, direction, volume)
    assert isinstance(result, list)


def test_minkowski_sum_voxel():
    vol1 = np.zeros((2, 2, 2), dtype=np.uint8)
    vol1[0, 0, 0] = 1
    vol2 = np.zeros((2, 2, 2), dtype=np.uint8)
    vol2[0, 0, 1] = 1
    result = minkowski_sum_voxel(vol1, vol2)
    assert result.shape == (3, 3, 3)


def test_merge_voxels():
    volume = np.ones((4, 4, 4), dtype=np.uint8)
    merged = merge_voxels(volume, level=2)
    assert merged.shape == (2, 2, 2)


def test_voxel_euler_number():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    euler = voxel_euler_number(volume)
    assert isinstance(euler, (int, np.integer))


def test_voxel_connectivity_count():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    count = voxel_connectivity_count(volume)
    assert count == 1


def test_voxel_sdf_3d():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    sdf = voxel_sdf_3d(volume)
    assert sdf.shape == (2, 2, 2)


def test_skeleton_3d_medial():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    skeleton = skeleton_3d_medial(volume)
    assert skeleton.shape == (2, 2, 2)


def test_extract_boundary_faces():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    faces = extract_boundary_faces(volume)
    assert isinstance(faces, list)


def test_voxel_dilate_3d():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    dilated = voxel_dilate_3d(volume, iterations=1)
    assert dilated.shape == (2, 2, 2)


def test_voxel_erode_3d():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    eroded = voxel_erode_3d(volume, iterations=1)
    assert eroded.shape == (2, 2, 2)


def test_fill_voxel_holes():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    filled = fill_voxel_holes(volume)
    assert filled.shape == (2, 2, 2)


def test_compute_voxel_moments():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    moments = compute_voxel_moments(volume)
    assert "m000" in moments


def test_extract_3d_contours():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 1, 1] = 1
    volume[1, 0, 1] = 1
    volume[1, 1, 1] = 1
    contours = extract_3d_contours(volume)
    assert isinstance(contours, list)


def test_voxel_to_octree():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    octree = voxel_to_octree(volume, min_size=1)
    assert octree is not None


def test_octree_to_voxel():
    octree = {"leaf": True, "x": 0, "y": 0, "z": 0, "size": 2}
    volume = octree_to_voxel(octree, resolution=4)
    assert volume.shape == (4, 4, 4)


def test_voxel_contour_3d():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    contour = voxel_contour_3d(volume)
    assert contour.shape == (2, 2, 2)


def test_sparse_voxel_octree():
    octree = SparseVoxelOctree(max_depth=3)
    octree.insert(1, 1, 1)
    assert octree.contains(1, 1, 1)


def test_build_sparse_voxel_octree():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    octree = build_sparse_voxel_octree(volume)
    assert octree is not None


def test_voxel_neighbor_lookup():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    lookup = VoxelNeighborLookup(volume)
    assert lookup.has_voxel(0, 0, 0)


def test_voxel_coloring():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    colors, count = voxel_coloring(volume)
    assert count >= 1


def test_voxel_separated():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    separated = voxel_separated(volume)
    assert isinstance(separated, bool)


def test_cut_voxel_by_plane():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    result = cut_voxel_by_plane(volume, (1, 0, 0), 0)
    assert result.shape == (2, 2, 2)


def test_volume_raymarch():
    volume = np.ones((4, 4, 4), dtype=np.uint8)
    origin = (0, 0, 0)
    direction = (1, 1, 1)
    hit, t = volume_raymarch(volume, origin, direction)
    assert hit is not None


def test_volume_raymarch_with_normal():
    volume = np.ones((4, 4, 4), dtype=np.uint8)
    origin = (0, 0, 0)
    direction = (1, 1, 1)
    hit, normal = volume_raymarch_with_normal(volume, origin, direction)
    assert hit is not None


def test_smooth_isosurface():
    volume = np.array([[[0.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]]], dtype=np.float32)
    smoothed = smooth_isosurface(volume, iterations=1)
    assert smoothed.shape == (2, 2, 2)


def test_voxel_gradient_normals():
    volume = np.array([[[0, 1], [1, 0]], [[1, 0], [0, 1]]], dtype=np.float32)
    normals = voxel_gradient_normals(volume)
    assert normals.shape == (2, 2, 2, 3)


def test_dual_contouring():
    volume = np.zeros((3, 3, 3), dtype=np.uint8)
    volume[1, 1, 1] = 1
    vertices, faces = dual_contouring(volume)
    assert isinstance(vertices, list)


def test_voxel_epitome():
    epit = VoxelEpitome(epitome_size=4)
    volume = np.ones((4, 4, 4), dtype=np.uint8)
    epit.fill_from_voxel_grid(volume, 0, 0, 0)
    dense = epit.to_dense()
    assert dense.shape == (4, 4, 4)


def test_build_voxel_epitomes():
    volume = np.ones((4, 4, 4), dtype=np.uint8)
    epitomes = build_voxel_epitomes(volume)
    assert len(epitomes) > 0


def test_voxel_pyramid():
    volume = np.ones((8, 8, 8), dtype=np.uint8)
    pyramid = voxel_pyramid(volume, levels=2)
    assert len(pyramid) == 2


def test_is_voxel_surface_manifold():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    is_manifold = is_voxel_surface_manifold(volume)
    assert isinstance(is_manifold, bool)


def test_voxel_junction_count():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    count = voxel_junction_count(volume)
    assert count >= 0


def test_voxel_endpoint_count():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    count = voxel_endpoint_count(volume)
    assert count >= 0


def test_euler_operators():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    result = EulerOperators.make_voxel(volume, 0, 0, 0)
    assert result[0, 0, 0] == 1


def test_detect_3d_corners():
    volume = np.zeros((2, 2, 2), dtype=np.uint8)
    volume[0, 0, 0] = 1
    corners = detect_3d_corners(volume)
    assert isinstance(corners, list)


def test_detect_3d_junctions():
    volume = np.ones((2, 2, 2), dtype=np.uint8)
    junctions = detect_3d_junctions(volume)
    assert junctions >= 0
