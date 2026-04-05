import pytest
from digital_geometry.voxel_semantic import (
    SemanticVoxelGrid,
    SemanticVoxel,
    voxelize_point_cloud_semantic,
    grow_region_semantic,
    semantic_connected_components,
    compute_segmentation_metrics,
    raycast_semantic,
    create_example_semantic_scene,
)


def test_semantic_voxel_grid_creation():
    grid = SemanticVoxelGrid(resolution=32, num_classes=10)
    assert grid.resolution == 32
    assert grid.num_classes == 10
    assert len(grid.voxels) == 0


def test_world_to_voxel():
    grid = SemanticVoxelGrid(resolution=10, bounds=(-1, -1, -1, 1, 1, 1))
    vx, vy, vz = grid.world_to_voxel(0, 0, 0)
    assert 0 <= vx < 10
    assert 0 <= vy < 10
    assert 0 <= vz < 10


def test_voxel_to_world():
    grid = SemanticVoxelGrid(resolution=10, bounds=(-1, -1, -1, 1, 1, 1))
    x, y, z = grid.voxel_to_world(5, 5, 5)
    assert abs(x) < 0.2
    assert abs(y) < 0.2
    assert abs(z) < 0.2


def test_set_and_get_voxel():
    grid = SemanticVoxelGrid(resolution=32)
    grid.set_voxel(10, 10, 10, class_id=1, confidence=0.9)
    voxel = grid.get_voxel(10, 10, 10)
    assert voxel is not None
    assert voxel.class_id == 1
    assert voxel.confidence == 0.9


def test_get_voxels_by_class():
    grid = SemanticVoxelGrid(resolution=32)
    grid.set_voxel(5, 5, 5, class_id=2)
    grid.set_voxel(6, 5, 5, class_id=2)
    grid.set_voxel(5, 6, 5, class_id=1)
    voxels = grid.get_voxels_by_class(2)
    assert len(voxels) == 2


def test_semantic_voxel_grid_stats():
    grid = SemanticVoxelGrid(resolution=16)
    grid.set_voxel(5, 5, 5, class_id=1)
    grid.set_voxel(6, 5, 5, class_id=1)
    stats = grid.get_stats()
    assert stats["resolution"] == 16
    assert stats["total_voxels"] == 2
    assert stats["class_counts"][1] == 2


def test_voxelize_point_cloud_semantic():
    points = [(0, 0, 0), (0.5, 0.5, 0), (1, 1, 0)]
    labels = [1, 1, 2]
    grid = voxelize_point_cloud_semantic(points, labels, resolution=16)
    assert grid.resolution == 16
    assert len(grid.voxels) > 0


def test_grow_region_semantic():
    grid = create_example_semantic_scene()
    region = grow_region_semantic(grid, (10, 1, 10), class_id=4)
    assert len(region) > 0


def test_semantic_connected_components():
    grid = create_example_semantic_scene()
    components = semantic_connected_components(grid, class_id=4)
    assert len(components) >= 1


def test_compute_segmentation_metrics():
    grid1 = create_example_semantic_scene()
    grid2 = create_example_semantic_scene()
    metrics = compute_segmentation_metrics(grid1, grid2)
    assert "per_class" in metrics
    assert "overall" in metrics
    assert "mIoU" in metrics["overall"]


def test_raycast_semantic():
    grid = create_example_semantic_scene()
    result = raycast_semantic(grid, origin=(0, 5, 0), direction=(1, 0, 0))
    assert result is None or (isinstance(result, tuple) and len(result) == 3)


def test_create_example_semantic_scene():
    grid = create_example_semantic_scene()
    assert grid.resolution == 32
    stats = grid.get_stats()
    assert stats["total_voxels"] > 0


def test_compute_iou():
    grid1 = create_example_semantic_scene()
    grid2 = create_example_semantic_scene()
    iou = grid1.compute_iou(grid2, class_id=2)
    assert 0.0 <= iou <= 1.0


def test_dense_grid_conversion():
    grid = create_example_semantic_scene()
    dense = grid.to_dense_grid()
    assert len(dense) == grid.resolution
    assert len(dense[0]) == grid.resolution
    assert len(dense[0][0]) == grid.resolution


def test_boundary_voxels():
    grid = create_example_semantic_scene()
    boundary = grid.get_boundary_voxels(class_id=2)
    assert isinstance(boundary, list)
