import pytest
import math
from digital_geometry.voxel_neural import (
    FeatureVolume,
    FeatureVoxel,
    NeuralImplicitSDF,
    raymarch_sdf,
    extract_surface_mesh,
    create_sdf_from_voxel_grid,
    feature_volume_from_point_cloud,
)


def test_feature_volume_creation():
    vol = FeatureVolume(resolution=8, feature_dim=4)
    assert vol.resolution == 8
    assert vol.feature_dim == 4
    assert len(vol.voxels) == 8**3


def test_world_to_voxel():
    vol = FeatureVolume(resolution=10, bounds=(-1, -1, -1, 1, 1, 1))
    vx, vy, vz = vol.world_to_voxel(0, 0, 0)
    assert 0 <= vx < 10
    assert 0 <= vy < 10
    assert 0 <= vz < 10


def test_voxel_to_world():
    vol = FeatureVolume(resolution=10, bounds=(-1, -1, -1, 1, 1, 1))
    x, y, z = vol.voxel_to_world(5, 5, 5)
    assert abs(x) < 0.2
    assert abs(y) < 0.2
    assert abs(z) < 0.2


def test_query_features():
    vol = FeatureVolume(resolution=8, feature_dim=4)
    vol.set_feature(3, 3, 3, [1.0, 2.0, 3.0, 4.0])
    features = vol.query_features(0.3, 0.3, 0.3)
    assert len(features) == 4
    assert all(isinstance(f, float) for f in features)


def test_set_and_query_sdf():
    vol = FeatureVolume(resolution=8)
    vol.set_sdf(3, 3, 3, 0.5)
    sdf = vol.query_sdf(0.3, 0.3, 0.3)
    assert isinstance(sdf, float)


def test_get_active_voxels():
    vol = FeatureVolume(resolution=4, feature_dim=2)
    vol.set_feature(1, 1, 1, [1.0, 1.0])
    vol.set_sdf(1, 1, 1, 0.5)
    active = vol.get_active_voxels()
    assert len(active) > 0


def test_feature_volume_stats():
    vol = FeatureVolume(resolution=8, feature_dim=4)
    stats = vol.get_stats()
    assert stats["resolution"] == 8
    assert stats["feature_dim"] == 4
    assert stats["total_voxels"] == 8**3


def test_neural_implicit_sdf_creation():
    sdf = NeuralImplicitSDF(resolution=8, feature_dim=4, num_layers=2)
    assert sdf.resolution == 8
    assert sdf.feature_dim == 4
    assert sdf.num_layers == 2


def test_neural_sdf_query():
    sdf = NeuralImplicitSDF(resolution=8)
    val = sdf.query(0, 0, 0)
    assert isinstance(val, float)


def test_neural_sdf_gradient():
    sdf = NeuralImplicitSDF(resolution=8)
    grad = sdf.get_gradient(0, 0, 0)
    assert len(grad) == 3
    assert all(isinstance(g, float) for g in grad)


def test_set_sdf_from_grid():
    sdf = NeuralImplicitSDF(resolution=4)
    grid = [[[0.1] * 4 for _ in range(4)] for _ in range(4)]
    sdf.set_sdf_from_grid(grid)
    assert sdf.query(0, 0, 0) is not None


def test_raymarch_sdf():
    sdf = NeuralImplicitSDF(resolution=16)
    vol = sdf.feature_volume
    for x in range(4):
        for y in range(4):
            for z in range(4):
                dist = math.sqrt((x - 2) ** 2 + (y - 2) ** 2 + (z - 2) ** 2) - 2
                vol.set_sdf(x, y, z, dist)

    result = raymarch_sdf(sdf, origin=(0, 0, 0), direction=(1, 0, 0), max_steps=50)
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


def test_extract_surface_mesh():
    sdf = NeuralImplicitSDF(resolution=8)
    vol = sdf.feature_volume
    for x in range(4):
        for y in range(4):
            for z in range(4):
                dist = math.sqrt(x * x + y * y + z * z) - 2
                vol.set_sdf(x, y, z, dist)

    vertices, faces = extract_surface_mesh(sdf, resolution=8)
    assert isinstance(vertices, list)
    assert isinstance(faces, list)


def test_create_sdf_from_voxel_grid():
    volume = [[[0, 1, 0], [1, 1, 1], [0, 1, 0]]] * 3
    vol = create_sdf_from_voxel_grid(volume)
    assert isinstance(vol, FeatureVolume)


def test_feature_volume_from_point_cloud():
    points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    vol = feature_volume_from_point_cloud(points, resolution=8)
    assert isinstance(vol, FeatureVolume)
    assert vol.resolution == 8
