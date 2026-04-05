"""Hash-based spatial indexing for large-scale voxel operations.

Based on "Real-time 3D Reconstruction at Scale using Voxel Hashing" (Nießner et al. 2013)
and modern hash-encoded neural implicit representations (Instant NGP, 2022).
"""

import math
import hashlib
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass


@dataclass
class HashEntry:
    """Single entry in the voxel hash table."""

    position: Tuple[int, int, int]
    voxel_data: Optional[Any] = None
    age: int = 0


class VoxelHash:
    """Hash-based spatial indexing for efficient voxel operations.

    Uses spatial hashing to map 3D coordinates to a fixed-size hash table,
    enabling O(1) lookups for large-scale voxel data.

    Based on:
    - Nießner et al., "Real-time 3D Reconstruction at Scale using Voxel Hashing" (2013)
    - Müller et al., "Instant Neural Graphics Primitives" (2022)
    """

    def __init__(
        self, table_size: int = 2**20, voxel_size: float = 1.0, world_size: float = 32.0
    ):
        self.table_size = table_size
        self.voxel_size = voxel_size
        self.world_size = world_size

        self.table: Dict[int, HashEntry] = {}
        self.active_entries: int = 0

    def _hash_position(self, x: int, y: int, z: int) -> int:
        """Compute hash for integer 3D position using spatial hashing."""
        p1 = 73856093
        p2 = 19349663
        p3 = 83492791
        hash_val = (abs(x) * p1 ^ abs(y) * p2 ^ abs(z) * p3) % self.table_size
        return hash_val

    def world_to_voxel(self, wx: float, wy: float, wz: float) -> Tuple[int, int, int]:
        """Convert world coordinates to voxel grid coordinates."""
        return (
            int(math.floor(wx / self.voxel_size)),
            int(math.floor(wy / self.voxel_size)),
            int(math.floor(wz / self.voxel_size)),
        )

    def voxel_to_world(self, vx: int, vy: int, vz: int) -> Tuple[float, float, float]:
        """Convert voxel coordinates to world coordinates."""
        return (vx * self.voxel_size, vy * self.voxel_size, vz * self.voxel_size)

    def insert(
        self, x: int, y: int, z: int, data: Any = None, max_age: int = 100
    ) -> bool:
        """Insert a voxel at the given position.

        Args:
            x, y, z: Integer voxel coordinates
            data: Optional data to store with the voxel
            max_age: Maximum age before eviction (for LRU-style replacement)

        Returns:
            True if inserted successfully, False if hash collision
        """
        hash_val = self._hash_position(x, y, z)

        entry = self.table.get(hash_val)
        if entry is None:
            self.table[hash_val] = HashEntry(position=(x, y, z), voxel_data=data, age=0)
            self.active_entries += 1
            return True
        elif entry.position == (x, y, z):
            entry.voxel_data = data
            entry.age = 0
            return True
        else:
            if entry.age >= max_age:
                self.table[hash_val] = HashEntry(
                    position=(x, y, z), voxel_data=data, age=0
                )
                return True
            return False

    def query(self, x: int, y: int, z: int) -> Optional[Any]:
        """Query voxel data at position.

        Args:
            x, y, z: Integer voxel coordinates

        Returns:
            Voxel data if found, None otherwise
        """
        hash_val = self._hash_position(x, y, z)
        entry = self.table.get(hash_val)

        if entry and entry.position == (x, y, z):
            entry.age = 0
            return entry.voxel_data
        return None

    def contains(self, x: int, y: int, z: int) -> bool:
        """Check if voxel exists at position."""
        return self.query(x, y, z) is not None

    def remove(self, x: int, y: int, z: int) -> bool:
        """Remove voxel at position."""
        hash_val = self._hash_position(x, y, z)
        entry = self.table.get(hash_val)

        if entry and entry.position == (x, y, z):
            del self.table[hash_val]
            self.active_entries -= 1
            return True
        return False

    def update_age(self):
        """Increment age of all entries for LRU-style aging."""
        for entry in self.table.values():
            entry.age += 1

    def get_neighbors(
        self, x: int, y: int, z: int, radius: int = 1
    ) -> List[Tuple[Tuple[int, int, int], Any]]:
        """Get all voxels within radius.

        Args:
            x, y, z: Center position
            radius: Search radius in voxels

        Returns:
            List of (position, data) tuples for nearby voxels
        """
        neighbors = []
        for dz in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    data = self.query(x + dx, y + dy, z + dz)
                    if data is not None:
                        neighbors.append(((x + dx, y + dy, z + dz), data))
        return neighbors

    def get_all_positions(self) -> List[Tuple[int, int, int]]:
        """Get all occupied positions."""
        return [entry.position for entry in self.table.values()]

    def clear(self):
        """Clear all entries."""
        self.table.clear()
        self.active_entries = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get hash table statistics."""
        return {
            "table_size": self.table_size,
            "active_entries": self.active_entries,
            "load_factor": self.active_entries / self.table_size,
            "world_size": self.world_size,
            "voxel_size": self.voxel_size,
        }


class MultiResolutionHash:
    """Multi-resolution hash encoding for neural implicit representations.

    Based on "Instant Neural Graphics Primitives with a Multiresolution Hash Encoding"
    (Müller et al., 2022).

    Uses multiple hash tables at different resolution levels for efficient
    feature storage and interpolation.
    """

    def __init__(
        self,
        num_levels: int = 16,
        min_resolution: int = 16,
        max_resolution: int = 1024,
        feature_dim: int = 2,
    ):
        self.num_levels = num_levels
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.feature_dim = feature_dim

        self.levels = []
        for i in range(num_levels):
            t = i / (num_levels - 1)
            resolution = int(min_resolution * (max_resolution / min_resolution) ** t)
            log2_resolution = int(math.floor(math.log2(resolution)))
            table_size = 2 ** min(log2_resolution + 10, 21)

            self.levels.append(
                {
                    "resolution": 2**log2_resolution,
                    "hash_offset": i * 2**21,
                    "table_size": table_size,
                    "features": [[0.0] * feature_dim for _ in range(table_size)],
                }
            )

    def _hash_position(self, level: int, x: int, y: int, z: int) -> int:
        """Hash 3D position for a given level."""
        level_info = self.levels[level]

        p1, p2, p3 = 1, 2654435769, 2911630577
        hash_val = (
            (x * p1) ^ (y * p2) ^ (z * p3) + level_info["hash_offset"]
        ) % level_info["table_size"]
        return hash_val

    def get_feature(self, x: float, y: float, z: float) -> List[float]:
        """Get interpolated feature vector at world position.

        Args:
            x, y, z: World coordinates

        Returns:
            Feature vector (list of floats)
        """
        feature = [0.0] * self.feature_dim

        for level_info in self.levels:
            res = level_info["resolution"]
            fx = x * res
            fy = y * res
            fz = z * res

            x0, y0, z0 = int(math.floor(fx)), int(math.floor(fy)), int(math.floor(fz))
            x1, y1, z1 = x0 + 1, y0 + 1, z0 + 1

            tx, ty, tz = fx - x0, fy - y0, fz - z0

            for dx in [0, 1]:
                for dy in [0, 1]:
                    for dz in [0, 1]:
                        hash_idx = self._hash_position(
                            self.levels.index(level_info), x0 + dx, y0 + dy, z0 + dz
                        )
                        level_features = level_info["features"][hash_idx]

                        wx = (1 - dx) * (1 - tx) + dx * tx
                        wy = (1 - dy) * (1 - ty) + dy * ty
                        wz = (1 - dz) * (1 - tz) + dz * tz
                        w = wx * wy * wz

                        for i in range(self.feature_dim):
                            feature[i] += w * level_features[i]

        return feature

    def update_feature(self, x: float, y: float, z: float, delta: List[float]):
        """Update features at position with gradient delta."""
        for level_info in self.levels:
            res = level_info["resolution"]
            fx, fy, fz = x * res, y * res, z * res

            x0, y0, z0 = int(math.floor(fx)), int(math.floor(fy)), int(math.floor(fz))

            for dx in [0, 1]:
                for dy in [0, 1]:
                    for dz in [0, 1]:
                        hash_idx = self._hash_position(
                            self.levels.index(level_info), x0 + dx, y0 + dy, z0 + dz
                        )
                        for i in range(min(len(delta), self.feature_dim)):
                            level_info["features"][hash_idx][i] += delta[i]

    def clear_gradients(self):
        """Reset all feature gradients to zero."""
        for level_info in self.levels:
            for feat in level_info["features"]:
                for i in range(len(feat)):
                    feat[i] = 0.0


def voxel_hash_from_volume(volume, voxel_size=1.0):
    """Create a VoxelHash from a 3D volume.

    Args:
        volume: 3D list/array of voxel values
        voxel_size: Size of each voxel in world units

    Returns:
        VoxelHash with all non-zero voxels inserted
    """
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    world_size = max(depth, height, width) * voxel_size
    hash_obj = VoxelHash(voxel_size=voxel_size, world_size=world_size)

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] != 0:
                    hash_obj.insert(x, y, z, volume[z][y][x])

    return hash_obj


def volume_from_voxel_hash(hash_obj: VoxelHash) -> Tuple[List, Tuple[int, int, int]]:
    """Convert VoxelHash back to 3D volume.

    Args:
        hash_obj: VoxelHash to convert

    Returns:
        Tuple of (3D volume, dimensions)
    """
    if hash_obj.active_entries == 0:
        return [], (0, 0, 0)

    positions = hash_obj.get_all_positions()
    max_x = max(p[0] for p in positions) + 1
    max_y = max(p[1] for p in positions) + 1
    max_z = max(p[2] for p in positions) + 1

    volume = [[[0] * max_x for _ in range(max_y)] for _ in range(max_z)]

    for (x, y, z), data in zip(positions, [hash_obj.query(*p) for p in positions]):
        if data is not None:
            volume[z][y][x] = data if data != 0 else 1

    return volume, (max_z, max_y, max_x)


def spatial_hash_nearest_neighbors(
    points: List[Tuple[float, float, float]], k: int = 5, radius: float = 1.0
) -> List[List[Tuple[int, float]]]:
    """Find k-nearest neighbors using spatial hashing.

    Args:
        points: List of (x, y, z) coordinates
        k: Number of nearest neighbors to find
        radius: Search radius for bucketing

    Returns:
        List of lists of (neighbor_index, distance) tuples
    """
    hash_obj = VoxelHash()
    bucket_size = radius

    for i, (x, y, z) in enumerate(points):
        vx, vy, vz = int(x / bucket_size), int(y / bucket_size), int(z / bucket_size)
        bucket = hash_obj.query(vx, vy, vz)
        if bucket is None:
            bucket = []
            hash_obj.insert(vx, vy, vz, bucket)
        bucket.append(i)

    results = []
    for i, (x, y, z) in enumerate(points):
        vx, vy, vz = int(x / bucket_size), int(y / bucket_size), int(z / bucket_size)

        candidates = []
        for dz in range(-2, 3):
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    bucket = hash_obj.query(vx + dx, vy + dy, vz + dz)
                    if bucket:
                        candidates.extend(bucket)

        distances = [
            (
                j,
                math.sqrt(
                    (points[j][0] - x) ** 2
                    + (points[j][1] - y) ** 2
                    + (points[j][2] - z) ** 2
                ),
            )
            for j in candidates
            if j != i
        ]

        distances.sort(key=lambda x: x[1])
        results.append(distances[:k])

    return results


def hash_grid_raycast(
    hash_obj: VoxelHash,
    origin: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    max_steps: int = 1000,
) -> Optional[Tuple[int, int, int]]:
    """Cast a ray through the voxel hash.

    Args:
        hash_obj: VoxelHash to raycast through
        origin: Ray origin (x, y, z)
        direction: Ray direction (dx, dy, dz)
        max_steps: Maximum ray marching steps

    Returns:
        First hit voxel position or None
    """
    px, py, pz = origin
    dx, dy, dz = direction

    dx = dx if dx != 0 else 1e-10
    dy = dy if dy != 0 else 1e-10
    dz = dz if dz != 0 else 1e-10

    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1
    step_z = 1 if dz > 0 else -1

    t_delta_x = 1.0 / abs(dx)
    t_delta_y = 1.0 / abs(dy)
    t_delta_z = 1.0 / abs(dz)

    voxel_x = int(math.floor(px / hash_obj.voxel_size))
    voxel_y = int(math.floor(py / hash_obj.voxel_size))
    voxel_z = int(math.floor(pz / hash_obj.voxel_size))

    if dx > 0:
        t_max_x = ((voxel_x + 1) * hash_obj.voxel_size - px) / dx
    else:
        t_max_x = (voxel_x * hash_obj.voxel_size - px) / dx

    if dy > 0:
        t_max_y = ((voxel_y + 1) * hash_obj.voxel_size - py) / dy
    else:
        t_max_y = (voxel_y * hash_obj.voxel_size - py) / dy

    if dz > 0:
        t_max_z = ((voxel_z + 1) * hash_obj.voxel_size - pz) / dz
    else:
        t_max_z = (voxel_z * hash_obj.voxel_size - pz) / dz

    for _ in range(max_steps):
        if hash_obj.contains(voxel_x, voxel_y, voxel_z):
            return (voxel_x, voxel_y, voxel_z)

        if t_max_x < t_max_y and t_max_x < t_max_z:
            voxel_x += step_x
            t_max_x += t_delta_x
        elif t_max_y < t_max_z:
            voxel_y += step_y
            t_max_y += t_delta_y
        else:
            voxel_z += step_z
            t_max_z += t_delta_z

    return None
