"""Tests for voxel module."""

import pytest
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
    volume = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    result = classify_voxel_grid(volume)
    assert len(result) == 2


def test_find_voxel_borders():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    borders = find_voxel_borders(volume)
    assert len(borders) > 0


def test_find_voxel_edges():
    volume = [[[1, 1], [0, 0]], [[0, 0], [0, 0]]]
    edges = find_voxel_edges(volume)
    assert isinstance(edges, list)


def test_find_voxel_vertices():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    vertices = find_voxel_vertices(volume)
    assert isinstance(vertices, list)


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
    volume = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    volume[1][1][1] = 1
    volume[2][2][2] = 1
    vertices, faces = surface_nets(volume)
    assert isinstance(vertices, list)


def test_voxel_carving():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [(0, 1, 2)]
    silhouettes = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    result = voxel_carving(vertices, triangles, [silhouettes], resolution=8)
    assert result is not None


def test_ray_voxel_intersection():
    origin = (0, 0, 0)
    direction = (1, 0, 0)
    bounds = ((0, 0, 0), (1, 1, 1))
    result = ray_voxel_intersection(origin, direction, bounds)
    assert result is not None


def test_ray_cast_volume():
    volume = [[[1] * 4 for _ in range(4)] for _ in range(4)]
    origin = (0, 0, 0)
    direction = (1, 1, 1)
    result = ray_cast_volume(origin, direction, volume)
    assert isinstance(result, list)


def test_minkowski_sum_voxel():
    vol1 = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    vol2 = [[[0, 1], [0, 0]], [[0, 0], [0, 0]]]
    result = minkowski_sum_voxel(vol1, vol2)
    assert len(result) > 0


def test_merge_voxels():
    volume = [[[1] * 4 for _ in range(4)] for _ in range(4)]
    merged = merge_voxels(volume, level=2)
    assert len(merged) == 2


def test_voxel_euler_number():
    volume = [[[1] * 2 for _ in range(2)] for _ in range(2)]
    euler = voxel_euler_number(volume)
    assert isinstance(euler, (int, float))


def test_voxel_connectivity_count():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    count = voxel_connectivity_count(volume)
    assert count == 1


def test_voxel_sdf_3d():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    sdf = voxel_sdf_3d(volume)
    assert len(sdf) == 2


def test_skeleton_3d_medial():
    volume = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    skeleton = skeleton_3d_medial(volume)
    assert len(skeleton) == 2


def test_extract_boundary_faces():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    faces = extract_boundary_faces(volume)
    assert isinstance(faces, list)


def test_voxel_dilate_3d():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    dilated = voxel_dilate_3d(volume, iterations=1)
    assert len(dilated) == 2


def test_voxel_erode_3d():
    volume = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    eroded = voxel_erode_3d(volume, iterations=1)
    assert len(eroded) == 2


def test_fill_voxel_holes():
    volume = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    filled = fill_voxel_holes(volume)
    assert len(filled) == 2


def test_compute_voxel_moments():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    moments = compute_voxel_moments(volume)
    assert "m000" in moments


def test_extract_3d_contours():
    volume = [[[0, 0], [0, 1]], [[0, 1], [1, 1]]]
    contours = extract_3d_contours(volume)
    assert isinstance(contours, list)


def test_voxel_to_octree():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    octree = voxel_to_octree(volume, min_size=1)
    assert octree is not None


def test_octree_to_voxel():
    octree = {"leaf": True, "x": 0, "y": 0, "z": 0, "size": 2}
    volume = octree_to_voxel(octree, resolution=4)
    assert len(volume) == 4


def test_voxel_contour_3d():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    contour = voxel_contour_3d(volume)
    assert len(contour) == 2


def test_sparse_voxel_octree():
    octree = SparseVoxelOctree(max_depth=3)
    octree.insert(1, 1, 1)
    assert octree.contains(1, 1, 1)


def test_build_sparse_voxel_octree():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    octree = build_sparse_voxel_octree(volume)
    assert octree is not None


def test_voxel_neighbor_lookup():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    lookup = VoxelNeighborLookup(volume)
    assert lookup.has_voxel(0, 0, 0)


def test_voxel_coloring():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    colors, count = voxel_coloring(volume)
    assert count >= 1


def test_voxel_separated():
    volume = [[[1, 0], [0, 0]], [[0, 0], [0, 0]]]
    separated = voxel_separated(volume)
    assert isinstance(separated, bool)


def test_cut_voxel_by_plane():
    volume = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    result = cut_voxel_by_plane(volume, (1, 0, 0), 0)
    assert len(result) == 2


def test_volume_raymarch():
    volume = [[[1] * 4 for _ in range(4)] for _ in range(4)]
    origin = (0, 0, 0)
    direction = (1, 1, 1)
    hit, t = volume_raymarch(volume, origin, direction)
    assert hit is not None


def test_volume_raymarch_with_normal():
    volume = [[[1] * 4 for _ in range(4)] for _ in range(4)]
    origin = (0, 0, 0)
    direction = (1, 1, 1)
    hit, normal = volume_raymarch_with_normal(volume, origin, direction)
    assert hit is not None


def test_smooth_isosurface():
    volume = [[[0.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]]]
    smoothed = smooth_isosurface(volume, iterations=1)
    assert len(smoothed) == 2


def test_voxel_gradient_normals():
    volume = [[[0, 1], [1, 0]], [[1, 0], [0, 1]]]
    normals = voxel_gradient_normals(volume)
    assert len(normals) == 2


def test_dual_contouring():
    volume = [[[0, 1, 0], [1, 1, 1], [0, 1, 0]] for _ in range(3)]
    vertices, faces = dual_contouring(volume)
    assert isinstance(vertices, list)


def test_voxel_epitome():
    epit = VoxelEpitome(epitome_size=4)
    volume = [[[1] * 4 for _ in range(4)] for _ in range(4)]
    epit.fill_from_voxel_grid(volume, 0, 0, 0)
    dense = epit.to_dense()
    assert len(dense) == 4


def test_build_voxel_epitomes():
    volume = [[[1] * 4 for _ in range(4)] for _ in range(4)]
    epitomes = build_voxel_epitomes(volume)
    assert len(epitomes) > 0


def test_voxel_pyramid():
    volume = [[[1] * 8 for _ in range(8)] for _ in range(8)]
    pyramid = voxel_pyramid(volume, levels=2)
    assert len(pyramid) == 2


def test_is_voxel_surface_manifold():
    volume = [[[1, 1], [1, 1]] for _ in range(2)]
    is_manifold = is_voxel_surface_manifold(volume)
    assert isinstance(is_manifold, bool)


def test_voxel_junction_count():
    volume = [[[1, 1], [1, 1]] for _ in range(2)]
    count = voxel_junction_count(volume)
    assert count >= 0


def test_voxel_endpoint_count():
    volume = [[[1, 0], [0, 0]] for _ in range(2)]
    count = voxel_endpoint_count(volume)
    assert count >= 0


def test_euler_operators():
    volume = [[[0, 0], [0, 0]] for _ in range(2)]
    result = EulerOperators.make_voxel(volume, 0, 0, 0)
    assert result[0][0][0] == 1


def test_detect_3d_corners():
    volume = [[[1, 0], [0, 0]] for _ in range(2)]
    corners = detect_3d_corners(volume)
    assert isinstance(corners, list)


def test_detect_3d_junctions():
    volume = [[[1, 1], [1, 1]] for _ in range(2)]
    junctions = detect_3d_junctions(volume)
    assert junctions >= 0
