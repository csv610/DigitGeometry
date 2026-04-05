"""Semantic voxel grid for multi-class 3D reconstruction.

Implements semantic voxel representation for scene understanding,
object detection, and multi-class segmentation in 3D space.

Based on:
- SCFusion: Real-time Incremental Scene Reconstruction with Semantic Completion
- Semantic Voxel Networks for 3D scene understanding
"""

from typing import Optional, List, Tuple, Dict, Any, Set
from dataclasses import dataclass
from collections import defaultdict
import math


@dataclass
class SemanticVoxel:
    """Single voxel with semantic class and confidence."""

    position: Tuple[int, int, int]
    class_id: int
    confidence: float = 1.0
    instance_id: Optional[int] = None
    color: Optional[Tuple[int, int, int]] = None


class SemanticVoxelGrid:
    """3D voxel grid with semantic class labels.

    Supports multi-class segmentation, instance segmentation,
    and confidence-weighted updates for 3D scene understanding.

    Based on:
    - SCFusion: Semantic incremental 3D reconstruction
    - 3D semantic segmentation networks
    """

    DEFAULT_CLASSES = {
        0: "void",
        1: "wall",
        2: "floor",
        3: "ceiling",
        4: "table",
        5: "chair",
        6: "window",
        7: "door",
        8: "object",
        9: "person",
    }

    def __init__(
        self,
        resolution: int = 256,
        num_classes: int = 10,
        class_names: Optional[Dict[int, str]] = None,
        bounds: Optional[Tuple[float, float, float, float, float, float]] = None,
    ):
        self.resolution = resolution
        self.num_classes = num_classes
        self.class_names = class_names or self.DEFAULT_CLASSES
        self.bounds = bounds or (-5.0, -5.0, -5.0, 5.0, 5.0, 5.0)

        self.voxels: Dict[Tuple[int, int, int], SemanticVoxel] = {}

        self.class_counts: Dict[int, int] = defaultdict(int)
        self.instance_count = 0

    def world_to_voxel(self, x: float, y: float, z: float) -> Tuple[int, int, int]:
        """Convert world coordinates to voxel indices."""
        min_x, min_y, min_z, max_x, max_y, max_z = self.bounds

        fx = (x - min_x) / (max_x - min_x) * (self.resolution - 1)
        fy = (y - min_y) / (max_y - min_y) * (self.resolution - 1)
        fz = (z - min_z) / (max_z - min_z) * (self.resolution - 1)

        return (
            max(0, min(self.resolution - 1, int(fx))),
            max(0, min(self.resolution - 1, int(fy))),
            max(0, min(self.resolution - 1, int(fz))),
        )

    def voxel_to_world(self, vx: int, vy: int, vz: int) -> Tuple[float, float, float]:
        """Convert voxel indices to world coordinates."""
        min_x, min_y, min_z, max_x, max_y, max_z = self.bounds

        x = min_x + vx / (self.resolution - 1) * (max_x - min_x)
        y = min_y + vy / (self.resolution - 1) * (max_y - min_y)
        z = min_z + vz / (self.resolution - 1) * (max_z - min_z)

        return (x, y, z)

    def set_voxel(
        self,
        x: int,
        y: int,
        z: int,
        class_id: int,
        confidence: float = 1.0,
        instance_id: Optional[int] = None,
        color: Optional[Tuple[int, int, int]] = None,
    ):
        """Set voxel at position with semantic class."""
        if not (0 <= class_id < self.num_classes):
            class_id = 0

        key = (x, y, z)

        existing = self.voxels.get(key)
        if existing and existing.confidence > confidence:
            return

        self.voxels[key] = SemanticVoxel(
            position=(x, y, z),
            class_id=class_id,
            confidence=confidence,
            instance_id=instance_id,
            color=color,
        )

        self.class_counts[class_id] += 1

    def get_voxel(self, x: int, y: int, z: int) -> Optional[SemanticVoxel]:
        """Get voxel at position."""
        return self.voxels.get((x, y, z))

    def get_class_at_world(self, x: float, y: float, z: float) -> int:
        """Get class ID at world coordinates."""
        vx, vy, vz = self.world_to_voxel(x, y, z)
        voxel = self.get_voxel(vx, vy, vz)
        return voxel.class_id if voxel else 0

    def remove_voxel(self, x: int, y: int, z: int) -> bool:
        """Remove voxel at position."""
        key = (x, y, z)
        if key in self.voxels:
            class_id = self.voxels[key].class_id
            del self.voxels[key]
            self.class_counts[class_id] -= 1
            return True
        return False

    def get_voxels_by_class(self, class_id: int) -> List[SemanticVoxel]:
        """Get all voxels of a specific class."""
        return [v for v in self.voxels.values() if v.class_id == class_id]

    def get_instances(
        self, class_id: Optional[int] = None
    ) -> Dict[int, List[SemanticVoxel]]:
        """Get all instance groups."""
        instances = defaultdict(list)

        for voxel in self.voxels.values():
            if voxel.instance_id is not None:
                if class_id is None or voxel.class_id == class_id:
                    instances[voxel.instance_id].append(voxel)

        return dict(instances)

    def merge_instances(self, instance_id1: int, instance_id2: int) -> bool:
        """Merge two instances."""
        for voxel in self.voxels.values():
            if voxel.instance_id == instance_id2:
                voxel.instance_id = instance_id1
        return True

    def get_boundary_voxels(self, class_id: int) -> List[SemanticVoxel]:
        """Get voxels of a class that are adjacent to different classes."""
        boundary = []

        offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

        for voxel in self.get_voxels_by_class(class_id):
            x, y, z = voxel.position
            for dx, dy, dz in offsets:
                neighbor = self.get_voxel(x + dx, y + dy, z + dz)
                if neighbor and neighbor.class_id != class_id:
                    boundary.append(voxel)
                    break

        return boundary

    def compute_iou(self, other: "SemanticVoxelGrid", class_id: int) -> float:
        """Compute IoU with another semantic voxel grid for a class."""
        voxels_a = set(v.position for v in self.get_voxels_by_class(class_id))
        voxels_b = set(v.position for v in other.get_voxels_by_class(class_id))

        intersection = len(voxels_a & voxels_b)
        union = len(voxels_a | voxels_b)

        return intersection / union if union > 0 else 0.0

    def to_dense_grid(self) -> List[List[List[int]]]:
        """Convert to dense 3D grid of class IDs."""
        grid = [
            [[0] * self.resolution for _ in range(self.resolution)]
            for _ in range(self.resolution)
        ]

        for (x, y, z), voxel in self.voxels.items():
            if (
                0 <= x < self.resolution
                and 0 <= y < self.resolution
                and 0 <= z < self.resolution
            ):
                grid[z][y][x] = voxel.class_id

        return grid

    def from_dense_grid(self, grid: List[List[List[int]]]):
        """Load from dense 3D grid of class IDs."""
        depth = len(grid)
        height = len(grid[0]) if depth > 0 else 0
        width = len(grid[0][0]) if height > 0 else 0

        factor = min(
            self.resolution / depth, self.resolution / height, self.resolution / width
        )

        for z in range(min(depth, self.resolution)):
            for y in range(min(height, self.resolution)):
                for x in range(min(width, self.resolution)):
                    class_id = grid[z][y][x]
                    if class_id > 0:
                        self.set_voxel(x, y, z, class_id)

    def get_stats(self) -> Dict[str, Any]:
        """Get semantic voxel grid statistics."""
        return {
            "resolution": self.resolution,
            "num_classes": self.num_classes,
            "total_voxels": len(self.voxels),
            "class_counts": dict(self.class_counts),
            "instance_count": self.instance_count,
            "bounds": self.bounds,
        }


def voxelize_point_cloud_semantic(
    points: List[Tuple[float, float, float]],
    labels: List[int],
    resolution: int = 256,
    bounds: Optional[Tuple[float, float, float, float, float, float]] = None,
) -> SemanticVoxelGrid:
    """Voxelize point cloud with semantic labels.

    Args:
        points: List of (x, y, z) world coordinates
        labels: List of class IDs (same length as points)
        resolution: Voxel grid resolution
        bounds: Optional world bounds

    Returns:
        SemanticVoxelGrid with labeled voxels
    """
    if bounds is None:
        min_x = min(p[0] for p in points)
        min_y = min(p[1] for p in points)
        min_z = min(p[2] for p in points)
        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)
        max_z = max(p[2] for p in points)

        padding = 0.1
        bounds = (
            min_x - padding,
            min_y - padding,
            min_z - padding,
            max_x + padding,
            max_y + padding,
            max_z + padding,
        )

    grid = SemanticVoxelGrid(resolution=resolution, bounds=bounds)

    for point, label in zip(points, labels):
        vx, vy, vz = grid.world_to_voxel(*point)
        grid.set_voxel(vx, vy, vz, label)

    return grid


def grow_region_semantic(
    grid: SemanticVoxelGrid,
    seed: Tuple[int, int, int],
    class_id: int,
    min_confidence: float = 0.5,
) -> List[Tuple[int, int, int]]:
    """Grow semantic region from seed using connectivity.

    Args:
        grid: SemanticVoxelGrid
        seed: Starting voxel position
        class_id: Target class ID
        min_confidence: Minimum confidence threshold

    Returns:
        List of positions in the grown region
    """
    from collections import deque

    visited = set()
    queue = deque([seed])
    region = []

    while queue:
        x, y, z = queue.popleft()

        if (x, y, z) in visited:
            continue
        visited.add((x, y, z))

        voxel = grid.get_voxel(x, y, z)
        if voxel and voxel.class_id == class_id and voxel.confidence >= min_confidence:
            region.append((x, y, z))

            for dx, dy, dz in [
                (-1, 0, 0),
                (1, 0, 0),
                (0, -1, 0),
                (0, 1, 0),
                (0, 0, -1),
                (0, 0, 1),
            ]:
                nx, ny, nz = x + dx, y + dy, z + dz
                if (
                    0 <= nx < grid.resolution
                    and 0 <= ny < grid.resolution
                    and 0 <= nz < grid.resolution
                ):
                    if (nx, ny, nz) not in visited:
                        queue.append((nx, ny, nz))

    return region


def semantic_connected_components(
    grid: SemanticVoxelGrid, class_id: int
) -> List[List[Tuple[int, int, int]]]:
    """Find connected components for a semantic class.

    Args:
        grid: SemanticVoxelGrid
        class_id: Class to find components for

    Returns:
        List of connected component voxel position lists
    """
    from collections import deque

    voxels = grid.get_voxels_by_class(class_id)
    positions = {v.position for v in voxels}

    visited = set()
    components = []

    for seed in positions:
        if seed in visited:
            continue

        component = []
        queue = deque([seed])

        while queue:
            pos = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            component.append(pos)

            x, y, z = pos
            for dx, dy, dz in [
                (-1, 0, 0),
                (1, 0, 0),
                (0, -1, 0),
                (0, 1, 0),
                (0, 0, -1),
                (0, 0, 1),
            ]:
                neighbor = (x + dx, y + dy, z + dz)
                if neighbor in positions and neighbor not in visited:
                    queue.append(neighbor)

        components.append(component)

    return components


def compute_segmentation_metrics(
    pred_grid: SemanticVoxelGrid, gt_grid: SemanticVoxelGrid
) -> Dict[str, float]:
    """Compute semantic segmentation metrics.

    Args:
        pred_grid: Predicted semantic voxel grid
        gt_grid: Ground truth semantic voxel grid

    Returns:
        Dictionary with IoU, precision, recall per class and mIoU
    """
    metrics = {"per_class": {}, "overall": {}}

    all_classes = set(pred_grid.class_counts.keys()) | set(gt_grid.class_counts.keys())

    ious = []
    for class_id in all_classes:
        pred_positions = set(
            v.position for v in pred_grid.get_voxels_by_class(class_id)
        )
        gt_positions = set(v.position for v in gt_grid.get_voxels_by_class(class_id))

        tp = len(pred_positions & gt_positions)
        fp = len(pred_positions - gt_positions)
        fn = len(gt_positions - pred_positions)

        iou = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        class_name = pred_grid.class_names.get(class_id, f"class_{class_id}")
        metrics["per_class"][class_name] = {
            "iou": iou,
            "precision": precision,
            "recall": recall,
        }

        if class_id != 0:
            ious.append(iou)

    metrics["overall"]["mIoU"] = sum(ious) / len(ious) if ious else 0.0

    return metrics


def raycast_semantic(
    grid: SemanticVoxelGrid,
    origin: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    max_distance: float = 100.0,
) -> Optional[Tuple[float, Tuple[int, int, int], int]]:
    """Ray cast through semantic voxel grid.

    Args:
        grid: SemanticVoxelGrid
        origin: Ray origin (world coords)
        direction: Ray direction (normalized)
        max_distance: Maximum ray distance

    Returns:
        (distance, hit_position, class_id) or None
    """
    ox, oy, oz = origin
    dx, dy, dz = direction

    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-8:
        return None

    dx, dy, dz = dx / length, dy / length, dz / length

    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1
    step_z = 1 if dz > 0 else -1

    t_delta_x = abs(1.0 / dx) if dx != 0 else float("inf")
    t_delta_y = abs(1.0 / dy) if dy != 0 else float("inf")
    t_delta_z = abs(1.0 / dz) if dz != 0 else float("inf")

    vx, vy, vz = grid.world_to_voxel(ox, oy, oz)

    if dx > 0:
        t_max_x = (
            (
                (vx + 1)
                - (ox - grid.bounds[0])
                / (grid.bounds[3] - grid.bounds[0])
                * (grid.resolution - 1)
            )
            / (grid.resolution - 1)
            * (grid.bounds[3] - grid.bounds[0])
        )
    else:
        t_max_x = (
            (
                (vx)
                - (ox - grid.bounds[0])
                / (grid.bounds[3] - grid.bounds[0])
                * (grid.resolution - 1)
            )
            / (grid.resolution - 1)
            * (grid.bounds[3] - grid.bounds[0])
        )

    min_x, min_y, min_z, max_x, max_y, max_z = grid.bounds

    t = 0.0
    prev_voxel = None

    while t < max_distance:
        px = ox + dx * t
        py = oy + dy * t
        pz = oz + dz * t

        if not (min_x <= px <= max_x and min_y <= py <= max_y and min_z <= pz <= max_z):
            break

        vx, vy, vz = grid.world_to_voxel(px, py, pz)

        if (vx, vy, vz) != prev_voxel:
            voxel = grid.get_voxel(vx, vy, vz)
            if voxel:
                return (t, (vx, vy, vz), voxel.class_id)
            prev_voxel = (vx, vy, vz)

        t += 0.1

    return None


def extract_semantic_mesh(
    grid: SemanticVoxelGrid, class_id: Optional[int] = None
) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
    """Extract mesh from semantic voxel grid.

    Args:
        grid: SemanticVoxelGrid
        class_id: Optional filter to specific class

    Returns:
        (vertices, faces)
    """
    from digital_geometry.voxel_render import surface_nets

    dense = grid.to_dense_grid()

    if class_id is not None:
        for z in range(len(dense)):
            for y in range(len(dense[z])):
                for x in range(len(dense[z][y])):
                    if dense[z][y][x] != class_id:
                        dense[z][y][x] = 0

    vertices, faces = surface_nets(dense)

    return vertices, faces


def create_example_semantic_scene() -> SemanticVoxelGrid:
    """Create example semantic scene with multiple objects."""
    grid = SemanticVoxelGrid(resolution=32)

    for x in range(8, 24):
        for z in range(8, 24):
            grid.set_voxel(x, 0, z, 2)

    for x in range(10, 22):
        for z in range(10, 22):
            for y in range(1, 10):
                grid.set_voxel(x, y, z, 4)

    for x in range(22, 26):
        for z in range(12, 18):
            for y in range(1, 8):
                grid.set_voxel(x, y, z, 5)

    for x in range(6, 10):
        for z in range(14, 18):
            for y in range(1, 12):
                grid.set_voxel(x, y, z, 6)

    grid.instance_count = 3

    for x in range(10, 22):
        for z in range(10, 22):
            for y in range(1, 10):
                voxel = grid.get_voxel(x, y, z)
                if voxel:
                    voxel.instance_id = 0

    for x in range(22, 26):
        for z in range(12, 18):
            for y in range(1, 8):
                voxel = grid.get_voxel(x, y, z)
                if voxel:
                    voxel.instance_id = 1

    return grid
