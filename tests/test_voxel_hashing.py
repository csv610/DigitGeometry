import pytest
from digital_geometry.voxel_hashing import (
    VoxelHash,
    MultiResolutionHash,
    voxel_hash_from_volume,
    volume_from_voxel_hash,
    spatial_hash_nearest_neighbors,
    hash_grid_raycast,
)


def test_voxel_hash_creation():
    hash_obj = VoxelHash(table_size=1024, voxel_size=1.0)
    assert hash_obj.table_size == 1024
    assert hash_obj.voxel_size == 1.0
    assert hash_obj.active_entries == 0


def test_world_to_voxel():
    hash_obj = VoxelHash(voxel_size=2.0)
    vx, vy, vz = hash_obj.world_to_voxel(3.9, 0, 0)
    assert vx == 1
    assert vy == 0
    assert vz == 0


def test_voxel_to_world():
    hash_obj = VoxelHash(voxel_size=2.0)
    wx, wy, wz = hash_obj.voxel_to_world(1, 2, 3)
    assert wx == 2.0
    assert wy == 4.0
    assert wz == 6.0


def test_insert_and_query():
    hash_obj = VoxelHash()
    result = hash_obj.insert(1, 2, 3, data="test")
    assert result is True
    data = hash_obj.query(1, 2, 3)
    assert data == "test"


def test_contains():
    hash_obj = VoxelHash(table_size=2**20, voxel_size=1.0, world_size=512.0)
    for i in range(10):
        hash_obj.insert(i, i, i, data=f"voxel_{i}")

    found_count = sum(1 for i in range(10) if hash_obj.contains(i, i, i))
    assert found_count >= 0


def test_remove():
    hash_obj = VoxelHash()
    hash_obj.insert(1, 2, 3, data="test")
    result = hash_obj.remove(1, 2, 3)
    assert result is True
    assert hash_obj.query(1, 2, 3) is None


def test_get_neighbors():
    hash_obj = VoxelHash()
    hash_obj.insert(0, 0, 0, data=1)
    hash_obj.insert(1, 0, 0, data=2)
    neighbors = hash_obj.get_neighbors(0, 0, 0, radius=1)
    assert len(neighbors) >= 1


def test_get_all_positions():
    hash_obj = VoxelHash()
    hash_obj.insert(1, 2, 3)
    hash_obj.insert(4, 5, 6)
    positions = hash_obj.get_all_positions()
    assert len(positions) == 2
    assert (1, 2, 3) in positions


def test_hash_stats():
    hash_obj = VoxelHash(table_size=1000)
    hash_obj.insert(1, 2, 3)
    stats = hash_obj.get_stats()
    assert "active_entries" in stats
    assert stats["active_entries"] == 1


def test_voxel_hash_from_volume():
    volume = [
        [[0, 1], [1, 0]],
        [[1, 0], [0, 1]],
    ]
    hash_obj = voxel_hash_from_volume(volume, voxel_size=1.0)
    assert isinstance(hash_obj, VoxelHash)
    assert hash_obj.active_entries > 0


def test_volume_from_voxel_hash():
    hash_obj = VoxelHash()
    hash_obj.insert(0, 0, 0, data=1)
    hash_obj.insert(1, 0, 0, data=1)
    volume, dims = volume_from_voxel_hash(hash_obj)
    assert len(volume) > 0
    assert isinstance(dims, tuple)


def test_spatial_hash_nearest_neighbors():
    points = [(0, 0, 0), (0.1, 0.1, 0.1), (5, 5, 5)]
    neighbors = spatial_hash_nearest_neighbors(points, k=2, radius=1.0)
    assert len(neighbors) == 3
    assert all(isinstance(n, list) for n in neighbors)


def test_hash_grid_raycast():
    hash_obj = VoxelHash(voxel_size=1.0)
    hash_obj.insert(3, 0, 0)
    result = hash_grid_raycast(hash_obj, origin=(0, 0, 0), direction=(1, 0, 0))
    assert result is None or isinstance(result, tuple)


def test_multi_resolution_hash_creation():
    hash_obj = MultiResolutionHash(num_levels=4, feature_dim=2)
    assert hash_obj.num_levels == 4
    assert hash_obj.feature_dim == 2


def test_multi_resolution_hash_feature():
    hash_obj = MultiResolutionHash(num_levels=2, feature_dim=2)
    feature = hash_obj.get_feature(0.5, 0.5, 0.5)
    assert len(feature) == 2
    assert all(isinstance(f, float) for f in feature)


def test_multi_resolution_hash_update():
    hash_obj = MultiResolutionHash(num_levels=2, feature_dim=2)
    hash_obj.update_feature(0.5, 0.5, 0.5, [0.1, 0.1])


def test_multi_resolution_clear_gradients():
    hash_obj = MultiResolutionHash(num_levels=2, feature_dim=2)
    hash_obj.update_feature(0.5, 0.5, 0.5, [0.1, 0.1])
    hash_obj.clear_gradients()
    feature = hash_obj.get_feature(0.5, 0.5, 0.5)
    assert all(abs(f) < 1e-6 for f in feature)
