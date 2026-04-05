import pytest
import math
from digital_geometry.voxel_octree import (
    OctreeNode,
    AdaptiveOctree,
    SparseOctree,
    octree_raymarch,
    octree_meshing,
    build_example_octree,
)


def test_octree_node_creation():
    node = OctreeNode(center=(0, 0, 0), size=1.0, level=0)
    assert node.center == (0, 0, 0)
    assert node.size == 1.0
    assert node.level == 0
    assert node.is_leaf is True


def test_adaptive_octree_creation():
    octree = AdaptiveOctree(min_size=0.1, max_depth=5)
    assert octree.min_size == 0.1
    assert octree.max_depth == 5
    assert octree.root is None


def test_adaptive_octree_build_from_sdf():
    def sphere_sdf(x, y, z):
        return math.sqrt(x * x + y * y + z * z) - 1.0

    octree = AdaptiveOctree(min_size=0.25, max_depth=4)
    octree.build_from_sdf(
        sphere_sdf, bounds=(-2, -2, -2, 2, 2, 2), initial_resolution=8
    )
    assert octree.root is not None


def test_adaptive_octree_refine():
    octree = build_example_octree()
    octree.refine_near_surface(max_iterations=2)
    stats = octree.get_stats()
    assert stats["total_nodes"] > 0


def test_octree_query_point():
    octree = build_example_octree()
    node = octree.query_point(0.5, 0.5, 0.5)
    assert node is None or isinstance(node, OctreeNode)


def test_octree_surface_leaves():
    octree = build_example_octree()
    leaves = octree.get_surface_leaves()
    assert isinstance(leaves, list)


def test_octree_all_leaves():
    octree = build_example_octree()
    leaves = octree.get_all_leaves()
    assert len(leaves) > 0


def test_octree_depth():
    octree = build_example_octree()
    depth = octree.get_octree_depth()
    assert depth >= 0


def test_octree_to_voxel_grid():
    octree = build_example_octree()
    grid, dims = octree.to_voxel_grid(resolution=16)
    assert len(grid) > 0
    assert len(dims) == 3


def test_octree_stats():
    octree = build_example_octree()
    stats = octree.get_stats()
    assert "total_nodes" in stats
    assert "leaf_nodes" in stats
    assert "depth" in stats


def test_sparse_octree_creation():
    octree = SparseOctree(voxel_size=1.0)
    assert octree.voxel_size == 1.0
    assert len(octree.nodes) == 0


def test_sparse_octree_insert():
    octree = SparseOctree()
    octree.insert(1, 2, 3, data="test")
    assert len(octree.nodes) == 1


def test_sparse_octree_query():
    octree = SparseOctree()
    octree.insert(1, 2, 3, data="test")
    result = octree.query(1, 2, 3)
    assert result is not None
    assert result["data"] == "test"


def test_sparse_octree_neighbors():
    octree = SparseOctree()
    octree.insert(0, 0, 0)
    octree.insert(1, 0, 0)
    neighbors = octree.get_neighbors(0, 0, 0, radius=1)
    assert len(neighbors) >= 2


def test_sparse_octree_remove():
    octree = SparseOctree()
    octree.insert(1, 2, 3)
    result = octree.remove(1, 2, 3)
    assert result is True
    assert len(octree.nodes) == 0


def test_sparse_octree_get_all_nodes():
    octree = SparseOctree()
    octree.insert(1, 2, 3)
    octree.insert(4, 5, 6)
    nodes = octree.get_all_nodes()
    assert len(nodes) == 2


def test_sparse_octree_stats():
    octree = SparseOctree()
    octree.insert(1, 2, 3)
    stats = octree.get_stats()
    assert "node_count" in stats
    assert stats["node_count"] == 1


def test_octree_raymarch():
    octree = build_example_octree()
    result = octree_raymarch(
        octree, origin=(3, 0, 0), direction=(-1, 0, 0), max_steps=100
    )
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


def test_octree_meshing():
    octree = build_example_octree()
    vertices, faces = octree_meshing(octree)
    assert isinstance(vertices, list)
    assert isinstance(faces, list)


def test_build_example_octree():
    octree = build_example_octree()
    assert isinstance(octree, AdaptiveOctree)
    assert octree.root is not None
