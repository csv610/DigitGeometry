"""Adaptive octree for dynamic voxel operations.

Supports adaptive refinement based on surface proximity, feature detection,
and hierarchical operations. Based on modern voxel octree approaches including:
- HIVE: Hierarchical Volume Encoding (2023)
- HVOFusion: Hybrid Voxel Octree (2024)
- GALA: Geometry-Aware Local Adaptive Grids (2024)
"""

from typing import Optional, List, Tuple, Dict, Any, Callable
from dataclasses import dataclass
import math


@dataclass
class OctreeNode:
    """Single node in the adaptive octree."""

    center: Tuple[float, float, float]
    size: float
    level: int

    is_leaf: bool = True
    has_surface: bool = False
    sdf_value: float = float("inf")

    children: Optional[List["OctreeNode"]] = None
    features: Optional[List[float]] = None

    data: Any = None


class AdaptiveOctree:
    """Adaptive octree with dynamic refinement based on surface detection.

    Features:
    - Adaptive refinement for detailed surface representation
    - Hierarchical feature encoding
    - Dynamic splitting based on surface proximity
    - Support for both voxel and implicit representations

    Based on:
    - HIVE (2023): Hierarchical Volume Encoding
    - HVOFusion (2024): Hybrid Voxel Octree
    - GALA (2024): Geometry-Aware Local Adaptive Grids
    """

    def __init__(
        self,
        min_size: float = 0.125,
        max_depth: int = 10,
        refine_threshold: float = 0.1,
        feature_dim: int = 4,
    ):
        self.min_size = min_size
        self.max_depth = max_depth
        self.refine_threshold = refine_threshold
        self.feature_dim = feature_dim

        self.root: Optional[OctreeNode] = None
        self.node_count = 0
        self.leaf_count = 0

        self.volume_bounds: Optional[
            Tuple[float, float, float, float, float, float]
        ] = None

    def build_from_sdf(
        self,
        sdf_func: Callable[[float, float, float], float],
        bounds: Tuple[float, float, float, float, float, float],
        initial_resolution: int = 32,
    ):
        """Build adaptive octree from SDF function.

        Args:
            sdf_func: Function that takes (x, y, z) and returns signed distance
            bounds: (min_x, min_y, min_z, max_x, max_y, max_z)
            initial_resolution: Initial grid resolution
        """
        self.volume_bounds = bounds
        size = bounds[3] - bounds[0]
        center = (
            (bounds[0] + bounds[3]) / 2,
            (bounds[1] + bounds[4]) / 2,
            (bounds[2] + bounds[5]) / 2,
        )

        self.root = self._build_node(sdf_func, center, size, 0)

    def _build_node(
        self,
        sdf_func: Callable,
        center: Tuple[float, float, float],
        size: float,
        level: int,
    ) -> OctreeNode:
        """Recursively build octree node."""
        node = OctreeNode(
            center=center,
            size=size,
            level=level,
            features=[0.0] * self.feature_dim if self.feature_dim > 0 else None,
        )

        if level >= self.max_depth or size <= self.min_size:
            sdf = sdf_func(*center)
            node.sdf_value = sdf
            node.has_surface = abs(sdf) < size
            self.node_count += 1
            self.leaf_count += 1
            return node

        half = size / 2
        sdf_center = sdf_func(*center)

        if abs(sdf_center) < size:
            children = []
            for dz in [-1, 1]:
                for dy in [-1, 1]:
                    for dx in [-1, 1]:
                        child_center = (
                            center[0] + dx * half,
                            center[1] + dy * half,
                            center[2] + dz * half,
                        )
                        child = self._build_node(
                            sdf_func, child_center, half, level + 1
                        )
                        children.append(child)

            node.children = children
            node.is_leaf = False

            avg_sdf = sum(c.sdf_value for c in children) / 8
            node.sdf_value = avg_sdf
            node.has_surface = any(c.has_surface for c in children)

            self.node_count += 1
        else:
            node.sdf_value = sdf_center
            node.has_surface = False
            self.node_count += 1
            self.leaf_count += 1

        return node

    def refine_near_surface(self, max_iterations: int = 5):
        """Refine nodes near the surface (iso-surface)."""
        if self.root is None:
            return

        for _ in range(max_iterations):
            changed = self._refine_iteration()
            if not changed:
                break

    def _refine_iteration(self) -> bool:
        """Single refinement iteration."""
        changed = False

        def refine(node: OctreeNode) -> bool:
            nonlocal changed

            if node.is_leaf:
                if (
                    node.has_surface
                    and node.size > self.min_size
                    and node.level < self.max_depth
                ):
                    if abs(node.sdf_value) < node.size * self.refine_threshold:
                        children = self._split_node(node)
                        if children:
                            node.children = children
                            node.is_leaf = False
                            self.leaf_count -= 1
                            self.leaf_count += 8
                            changed = True
                            return True
                return False

            if node.children:
                for child in node.children:
                    refine(child)
            return False

        refine(self.root)
        return changed

    def _split_node(self, node: OctreeNode) -> Optional[List[OctreeNode]]:
        """Split leaf node into 8 children."""
        if node.level >= self.max_depth or node.size <= self.min_size:
            return None

        half = node.size / 2
        children = []

        for dz in [-1, 1]:
            for dy in [-1, 1]:
                for dx in [-1, 1]:
                    child_center = (
                        node.center[0] + dx * half,
                        node.center[1] + dy * half,
                        node.center[2] + dz * half,
                    )
                    child = OctreeNode(
                        center=child_center,
                        size=half,
                        level=node.level + 1,
                        sdf_value=node.sdf_value,
                        has_surface=node.has_surface,
                        features=[0.0] * self.feature_dim
                        if self.feature_dim > 0
                        else None,
                    )
                    children.append(child)

        self.node_count += 8
        return children

    def query_point(self, x: float, y: float, z: float) -> Optional[OctreeNode]:
        """Query the octree at a point."""
        if self.root is None:
            return None

        node = self.root
        while node:
            dx = x - node.center[0]
            dy = y - node.center[1]
            dz = z - node.center[2]

            if (
                abs(dx) > node.size / 2
                or abs(dy) > node.size / 2
                or abs(dz) > node.size / 2
            ):
                return None

            if node.is_leaf:
                return node

            half = node.size / 2
            idx = (0 if dx < 0 else 4) | (0 if dy < 0 else 2) | (0 if dz < 0 else 1)
            idx = idx // 2 if dz >= 0 else idx

            octant = (0 if dx < 0 else 1) + (0 if dy < 0 else 2) + (0 if dz < 0 else 4)

            if node.children and octant < len(node.children):
                node = node.children[octant]
            else:
                return node

        return None

    def get_surface_leaves(self) -> List[OctreeNode]:
        """Get all leaf nodes near the surface."""
        leaves = []

        def traverse(node: OctreeNode):
            if node.is_leaf:
                if node.has_surface:
                    leaves.append(node)
            elif node.children:
                for child in node.children:
                    traverse(child)

        if self.root:
            traverse(self.root)
        return leaves

    def get_all_leaves(self) -> List[OctreeNode]:
        """Get all leaf nodes."""
        leaves = []

        def traverse(node: OctreeNode):
            if node.is_leaf:
                leaves.append(node)
            elif node.children:
                for child in node.children:
                    traverse(child)

        if self.root:
            traverse(self.root)
        return leaves

    def get_octree_depth(self) -> int:
        """Get maximum depth of the octree."""
        max_depth = 0

        def traverse(node: OctreeNode, depth: int):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            if node.children:
                for child in node.children:
                    traverse(child, depth + 1)

        if self.root:
            traverse(self.root, 0)
        return max_depth

    def to_voxel_grid(self, resolution: int = 32) -> Tuple[Any, Tuple[int, int, int]]:
        """Convert octree to dense voxel grid."""
        if self.root is None:
            return [], (0, 0, 0)

        if self.volume_bounds is None:
            return [], (0, 0, 0)

        min_x, min_y, min_z, max_x, max_y, max_z = self.volume_bounds

        grid = [
            [[0] * resolution for _ in range(resolution)] for _ in range(resolution)
        ]
        step_x = (max_x - min_x) / resolution
        step_y = (max_y - min_y) / resolution
        step_z = (max_z - min_z) / resolution

        for z in range(resolution):
            for y in range(resolution):
                for x in range(resolution):
                    wx = min_x + (x + 0.5) * step_x
                    wy = min_y + (y + 0.5) * step_y
                    wz = min_z + (z + 0.5) * step_z

                    node = self.query_point(wx, wy, wz)
                    if node and node.has_surface and abs(node.sdf_value) < node.size:
                        grid[z][y][x] = 1

        return grid, (resolution, resolution, resolution)

    def get_stats(self) -> Dict[str, Any]:
        """Get octree statistics."""
        return {
            "total_nodes": self.node_count,
            "leaf_nodes": self.leaf_count,
            "depth": self.get_octree_depth(),
            "min_size": self.min_size,
            "max_depth": self.max_depth,
        }


class SparseOctree:
    """Sparse octree using hash-based storage for memory efficiency.

    Similar to neural radiance field approaches (PlenOctree, 2021).
    """

    def __init__(self, voxel_size: float = 1.0):
        self.voxel_size = voxel_size
        self.nodes: Dict[Tuple[int, int, int], Dict] = {}

    def insert(self, x: int, y: int, z: int, data: Any = None):
        """Insert a voxel at integer coordinates."""
        key = (x, y, z)
        self.nodes[key] = {"position": (x, y, z), "data": data, "features": [0.0] * 4}

    def query(self, x: int, y: int, z: int) -> Optional[Dict]:
        """Query voxel at integer coordinates."""
        return self.nodes.get((x, y, z))

    def get_neighbors(self, x: int, y: int, z: int, radius: int = 1) -> List[Dict]:
        """Get neighboring voxels."""
        neighbors = []
        for dz in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    node = self.query(x + dx, y + dy, z + dz)
                    if node:
                        neighbors.append(node)
        return neighbors

    def remove(self, x: int, y: int, z: int) -> bool:
        """Remove voxel at position."""
        if (x, y, z) in self.nodes:
            del self.nodes[(x, y, z)]
            return True
        return False

    def clear(self):
        """Clear all nodes."""
        self.nodes.clear()

    def get_all_nodes(self) -> List[Dict]:
        """Get all nodes."""
        return list(self.nodes.values())

    def get_stats(self) -> Dict[str, Any]:
        """Get sparse octree statistics."""
        return {"node_count": len(self.nodes), "voxel_size": self.voxel_size}


def octree_raymarch(
    octree: AdaptiveOctree,
    origin: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    max_steps: int = 500,
) -> Optional[Tuple[float, Tuple[float, float, float]]]:
    """Ray march through the adaptive octree to find surface intersection.

    Args:
        octree: AdaptiveOctree to raymarch
        origin: Ray origin
        direction: Ray direction (normalized)
        max_steps: Maximum ray steps

    Returns:
        (distance, hit_point) or None if no hit
    """
    if octree.root is None:
        return None

    ox, oy, oz = origin
    dx, dy, dz = direction

    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / length, dy / length, dz / length

    t = 0.0
    for _ in range(max_steps):
        px = ox + dx * t
        py = oy + dy * t
        pz = oz + dz * t

        node = octree.query_point(px, py, pz)
        if node and node.has_surface and abs(node.sdf_value) < node.size:
            return (t, (px, py, pz))

        if node:
            t += node.size * 0.5
        else:
            t += 1.0

        if t > 1000:
            break

    return None


def octree_meshing(octree: AdaptiveOctree) -> Tuple[List, List]:
    """Generate mesh from octree using marching cubes on leaf nodes.

    Args:
        octree: AdaptiveOctree to mesh

    Returns:
        (vertices, faces) - vertex positions and face indices
    """
    vertices = []
    faces = []

    surface_nodes = octree.get_surface_leaves()

    vertex_map = {}
    vertex_idx = 0

    for node in surface_nodes:
        cx, cy, cz = node.center
        s = node.size / 2

        cube_verts = [
            (cx - s, cy - s, cz - s),
            (cx + s, cy - s, cz - s),
            (cx + s, cy + s, cz - s),
            (cx - s, cy + s, cz - s),
            (cx - s, cy - s, cz + s),
            (cx + s, cy - s, cz + s),
            (cx + s, cy + s, cz + s),
            (cx - s, cy + s, cz + s),
        ]

        sdf_values = [sdf_func(v[0], v[1], v[2]) for v in cube_verts]

        if all(s < 0 for s in sdf_values) or all(s > 0 for s in sdf_values):
            continue

        for v in cube_verts:
            if v not in vertex_map:
                vertex_map[v] = vertex_idx
                vertices.append(v)
                vertex_idx += 1

        face_verts = [
            (0, 1, 2, 3),
            (4, 7, 6, 5),
            (0, 4, 5, 1),
            (2, 6, 7, 3),
            (0, 3, 7, 4),
            (1, 5, 6, 2),
        ]

        for f in face_verts:
            v0 = cube_verts[f[0]]
            v1 = cube_verts[f[1]]
            v2 = cube_verts[f[2]]

            faces.append([vertex_map[v0], vertex_map[v1], vertex_map[v2]])

    return vertices, faces


def sdf_func(x: float, y: float, z: float) -> float:
    """Example SDF function (sphere at origin)."""
    return math.sqrt(x * x + y * y + z * z) - 1.0


def build_example_octree() -> AdaptiveOctree:
    """Build example adaptive octree from a sphere SDF."""
    octree = AdaptiveOctree(min_size=0.05, max_depth=8, refine_threshold=0.2)

    octree.build_from_sdf(
        sdf_func, bounds=(-2.0, -2.0, -2.0, 2.0, 2.0, 2.0), initial_resolution=16
    )

    octree.refine_near_surface(max_iterations=3)

    return octree
