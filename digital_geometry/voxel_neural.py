"""Voxel-based neural implicit representations.

Implements feature volume encoding and neural implicit SDF representations
without requiring external ML frameworks. Based on:
- HIVE: Hierarchical Volume Encoding (2023)
- Instant NGP (2022)
- Neural Radiance Field approaches
"""

import math
from typing import Optional, List, Tuple, Dict, Any, Callable
from dataclasses import dataclass


@dataclass
class FeatureVoxel:
    """Voxel with feature encoding."""

    position: Tuple[int, int, int]
    features: List[float]
    sdf: Optional[float] = None
    density: Optional[float] = None


class FeatureVolume:
    """Feature volume for neural implicit representations.

    Stores per-voxel features that can be queried and interpolated
    for neural implicit surface reconstruction.

    Based on:
    - HIVE: Hierarchical Volume Encoding (Gu et al., 2023)
    - Sparse Feature Volumes for surface reconstruction
    """

    def __init__(
        self,
        resolution: int = 64,
        feature_dim: int = 4,
        bounds: Optional[Tuple[float, float, float, float, float, float]] = None,
    ):
        self.resolution = resolution
        self.feature_dim = feature_dim

        if bounds is None:
            bounds = (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0)
        self.bounds = bounds

        self.voxels: Dict[Tuple[int, int, int], FeatureVoxel] = {}

        self._init_default_features()

    def _init_default_features(self):
        """Initialize default feature values."""
        for x in range(self.resolution):
            for y in range(self.resolution):
                for z in range(self.resolution):
                    self.voxels[(x, y, z)] = FeatureVoxel(
                        position=(x, y, z), features=[0.0] * self.feature_dim
                    )

    def world_to_voxel(self, x: float, y: float, z: float) -> Tuple[int, int, int]:
        """Convert world coordinates to voxel indices."""
        min_x, min_y, min_z, max_x, max_y, max_z = self.bounds

        fx = (x - min_x) / (max_x - min_x) * (self.resolution - 1)
        fy = (y - min_y) / (max_y - min_y) * (self.resolution - 1)
        fz = (z - min_z) / (max_z - min_z) * (self.resolution - 1)

        return (
            int(max(0, min(self.resolution - 1, math.floor(fx)))),
            int(max(0, min(self.resolution - 1, math.floor(fy)))),
            int(max(0, min(self.resolution - 1, math.floor(fz)))),
        )

    def voxel_to_world(self, vx: int, vy: int, vz: int) -> Tuple[float, float, float]:
        """Convert voxel indices to world coordinates."""
        min_x, min_y, min_z, max_x, max_y, max_z = self.bounds

        x = min_x + vx / (self.resolution - 1) * (max_x - min_x)
        y = min_y + vy / (self.resolution - 1) * (max_y - min_y)
        z = min_z + vz / (self.resolution - 1) * (max_z - min_z)

        return (x, y, z)

    def query_features(self, x: float, y: float, z: float) -> List[float]:
        """Query interpolated features at world position.

        Args:
            x, y, z: World coordinates

        Returns:
            Interpolated feature vector
        """
        min_x, min_y, min_z, max_x, max_y, max_z = self.bounds

        fx = (x - min_x) / (max_x - min_x) * (self.resolution - 1)
        fy = (y - min_y) / (max_y - min_y) * (self.resolution - 1)
        fz = (z - min_z) / (max_z - min_z) * (self.resolution - 1)

        x0 = int(math.floor(fx))
        y0 = int(math.floor(fy))
        z0 = int(math.floor(fz))

        x1 = min(x0 + 1, self.resolution - 1)
        y1 = min(y0 + 1, self.resolution - 1)
        z1 = min(z0 + 1, self.resolution - 1)

        tx = fx - x0
        ty = fy - y0
        tz = fz - z0

        features = [0.0] * self.feature_dim

        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    wx = (1 - dx) * (1 - tx) + dx * tx
                    wy = (1 - dy) * (1 - ty) + dy * ty
                    wz = (1 - dz) * (1 - tz) + dz * tz
                    w = wx * wy * wz

                    vx = x0 + dx
                    vy = y0 + dy
                    vz = z0 + dz

                    voxel = self.voxels.get((vx, vy, vz))
                    if voxel:
                        for i in range(self.feature_dim):
                            features[i] += w * voxel.features[i]

        return features

    def set_feature(self, vx: int, vy: int, vz: int, features: List[float]):
        """Set feature vector at voxel position."""
        key = (vx, vy, vz)
        if key in self.voxels:
            self.voxels[key].features = features[: self.feature_dim]

    def set_sdf(self, vx: int, vy: int, vz: int, sdf: float):
        """Set SDF value at voxel position."""
        key = (vx, vy, vz)
        if key in self.voxels:
            self.voxels[key].sdf = sdf

    def query_sdf(self, x: float, y: float, z: float) -> float:
        """Query interpolated SDF at world position."""
        min_x, min_y, min_z, max_x, max_y, max_z = self.bounds

        fx = (x - min_x) / (max_x - min_x) * (self.resolution - 1)
        fy = (y - min_y) / (max_y - min_y) * (self.resolution - 1)
        fz = (z - min_z) / (max_z - min_z) * (self.resolution - 1)

        x0 = int(math.floor(fx))
        y0 = int(math.floor(fy))
        z0 = int(math.floor(fz))

        x1 = min(x0 + 1, self.resolution - 1)
        y1 = min(y0 + 1, self.resolution - 1)
        z1 = min(z0 + 1, self.resolution - 1)

        tx = fx - x0
        ty = fy - y0
        tz = fz - z0

        sdf = 0.0

        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    wx = (1 - dx) * (1 - tx) + dx * tx
                    wy = (1 - dy) * (1 - ty) + dy * ty
                    wz = (1 - dz) * (1 - tz) + dz * tz
                    w = wx * wy * wz

                    vx = x0 + dx
                    vy = y0 + dy
                    vz = z0 + dz

                    voxel = self.voxels.get((vx, vy, vz))
                    if voxel and voxel.sdf is not None:
                        sdf += w * voxel.sdf

        return sdf

    def get_active_voxels(self) -> List[FeatureVoxel]:
        """Get all voxels with non-zero features or SDF."""
        return [
            v
            for v in self.voxels.values()
            if any(abs(f) > 1e-6 for f in v.features) or v.sdf is not None
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get feature volume statistics."""
        active = self.get_active_voxels()
        return {
            "resolution": self.resolution,
            "feature_dim": self.feature_dim,
            "total_voxels": len(self.voxels),
            "active_voxels": len(active),
            "bounds": self.bounds,
        }


class NeuralImplicitSDF:
    """Neural implicit SDF representation using feature volumes.

    Combines feature volumes with a simple MLP-like computation
    for neural implicit surface reconstruction.

    Based on:
    - Neural Radiance Field (NeRF) approaches
    - HIVE: Hierarchical Volume Encoding
    - SDF-based neural networks
    """

    def __init__(
        self,
        resolution: int = 64,
        feature_dim: int = 4,
        hidden_dim: int = 32,
        num_layers: int = 3,
    ):
        self.resolution = resolution
        self.feature_dim = feature_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.biases = []

        self.feature_volume = FeatureVolume(
            resolution=resolution, feature_dim=feature_dim
        )

        self._init_network()

    def _init_network(self):
        """Initialize simple MLP weights (for demonstration)."""
        self.weights = []
        biases = []

        input_dim = self.feature_dim + 3

        for i in range(self.num_layers):
            output_dim = self.hidden_dim if i < self.num_layers - 1 else 1

            w = [[0.0] * input_dim for _ in range(output_dim)]
            b = [0.0] * output_dim

            for j in range(output_dim):
                for k in range(input_dim):
                    w[j][k] = 0.01 * (2 * hash((i, j, k)) % 1000 - 500) / 500

            self.weights.append(w)
            self.biases.append(b)

            input_dim = output_dim

    def query(self, x: float, y: float, z: float) -> float:
        """Query SDF at world position using feature interpolation + MLP.

        Args:
            x, y, z: World coordinates

        Returns:
            Predicted SDF value
        """
        features = self.feature_volume.query_features(x, y, z)

        input_vec = [x, y, z] + features

        hidden = input_vec
        for i in range(self.num_layers):
            new_hidden = []
            for j in range(len(self.weights[i])):
                val = self.biases[i][j] if i < len(self.biases) else 0.0
                for k in range(len(hidden)):
                    val += self.weights[i][j][k] * hidden[k]
                if i < self.num_layers - 1:
                    val = max(0, val)
                new_hidden.append(val)
            hidden = new_hidden

        return hidden[0] if hidden else 0.0

    def set_features_from_volume(self, volume_data: List):
        """Set feature volume from 3D array.

        Args:
            volume_data: 3D array of feature vectors
        """
        depth = len(volume_data)
        height = len(volume_data[0]) if depth > 0 else 0
        width = len(volume_data[0][0]) if height > 0 else 0

        for z in range(min(depth, self.resolution)):
            for y in range(min(height, self.resolution)):
                for x in range(min(width, self.resolution)):
                    if (
                        z < len(volume_data)
                        and y < len(volume_data[z])
                        and x < len(volume_data[z][y])
                    ):
                        features = volume_data[z][y][x]
                        if isinstance(features, (list, tuple)):
                            self.feature_volume.set_feature(x, y, z, list(features))
                        else:
                            self.feature_volume.set_feature(x, y, z, [float(features)])

    def set_sdf_from_grid(self, sdf_grid: List):
        """Set SDF values from 3D array.

        Args:
            sdf_grid: 3D array of SDF values
        """
        depth = len(sdf_grid)
        height = len(sdf_grid[0]) if depth > 0 else 0
        width = len(sdf_grid[0][0]) if height > 0 else 0

        for z in range(min(depth, self.resolution)):
            for y in range(min(height, self.resolution)):
                for x in range(min(width, self.resolution)):
                    if (
                        z < len(sdf_grid)
                        and y < len(sdf_grid[z])
                        and x < len(sdf_grid[z][y])
                    ):
                        self.feature_volume.set_sdf(x, y, z, sdf_grid[z][y][x])

    def get_gradient(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Compute gradient of SDF at position (for normal calculation)."""
        eps = 1e-4

        dx = (self.query(x + eps, y, z) - self.query(x - eps, y, z)) / (2 * eps)
        dy = (self.query(x, y + eps, z) - self.query(x, y - eps, z)) / (2 * eps)
        dz = (self.query(x, y, z + eps) - self.query(x, y, z - eps)) / (2 * eps)

        length = math.sqrt(dx * dx + dy * dy + dz * dz)
        if length > 1e-8:
            dx, dy, dz = dx / length, dy / length, dz / length

        return (dx, dy, dz)


def raymarch_sdf(
    sdf: NeuralImplicitSDF,
    origin: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    max_steps: int = 100,
    max_distance: float = 10.0,
    surface_threshold: float = 1e-4,
) -> Optional[Tuple[float, Tuple[float, float, float]]]:
    """Ray march through neural implicit SDF.

    Args:
        sdf: NeuralImplicitSDF to raymarch
        origin: Ray origin
        direction: Ray direction (will be normalized)
        max_steps: Maximum ray steps
        max_distance: Maximum ray distance
        surface_threshold: Distance threshold for surface hit

    Returns:
        (distance, hit_point) or None if no hit
    """
    ox, oy, oz = origin
    dx, dy, dz = direction

    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-8:
        return None

    dx, dy, dz = dx / length, dy / length, dz / length

    t = 0.0
    prev_sdf = float("inf")

    for _ in range(max_steps):
        if t > max_distance:
            break

        px = ox + dx * t
        py = oy + dy * t
        pz = oz + dz * t

        sdf_val = sdf.query(px, py, pz)

        if abs(sdf_val) < surface_threshold:
            return (t, (px, py, pz))

        if sdf_val > prev_sdf:
            break

        prev_sdf = sdf_val

        step_size = max(abs(sdf_val) * 0.5, 0.01)
        t += step_size

    return None


def extract_surface_mesh(
    sdf: NeuralImplicitSDF,
    resolution: int = 64,
    bounds: Tuple[float, float, float, float, float, float] = (-1, -1, -1, 1, 1, 1),
) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
    """Extract mesh from neural implicit SDF using marching cubes.

    Args:
        sdf: NeuralImplicitSDF to extract mesh from
        resolution: Grid resolution for marching cubes
        bounds: World bounds

    Returns:
        (vertices, faces)
    """
    from digital_geometry.volume_isosurface import marching_cubes

    grid = []
    min_x, min_y, min_z, max_x, max_y, max_z = bounds
    step = (max_x - min_x) / resolution

    for z in range(resolution):
        layer = []
        for y in range(resolution):
            row = []
            for x in range(resolution):
                wx = min_x + (x + 0.5) * step
                wy = min_y + (y + 0.5) * step
                wz = min_z + (z + 0.5) * step
                sdf_val = sdf.query(wx, wy, wz)
                row.append(sdf_val)
            layer.append(row)
        grid.append(layer)

    vertices, faces = marching_cubes(grid, 0.0)

    return vertices, faces


def create_sdf_from_voxel_grid(volume) -> FeatureVolume:
    """Create feature volume with SDF from voxel grid.

    Args:
        volume: 3D binary voxel grid

    Returns:
        FeatureVolume with SDF values computed
    """
    import numpy as np
    from digital_geometry.voxel_sdf import voxel_sdf_3d

    volume = np.asanyarray(volume)
    sdf_grid = voxel_sdf_3d(volume)

    depth = len(sdf_grid)
    height = len(sdf_grid[0]) if depth > 0 else 0
    width = len(sdf_grid[0][0]) if height > 0 else 0

    feature_vol = FeatureVolume(
        resolution=max(depth, height, width),
        feature_dim=4,
        bounds=(-depth / 2, -height / 2, -width / 2, depth / 2, height / 2, width / 2),
    )

    for z in range(min(depth, feature_vol.resolution)):
        for y in range(min(height, feature_vol.resolution)):
            for x in range(min(width, feature_vol.resolution)):
                if (
                    z < len(sdf_grid)
                    and y < len(sdf_grid[z])
                    and x < len(sdf_grid[z][y])
                ):
                    feature_vol.set_sdf(x, y, z, sdf_grid[z][y][x])

    return feature_vol


def feature_volume_from_point_cloud(
    points: List[Tuple[float, float, float]],
    resolution: int = 64,
    bandwidth: float = 0.1,
) -> FeatureVolume:
    """Create feature volume from point cloud with density encoding.

    Args:
        points: List of (x, y, z) points
        resolution: Volume resolution
        bandwidth: Kernel bandwidth for density

    Returns:
        FeatureVolume with density features
    """
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

    feature_vol = FeatureVolume(resolution=resolution, feature_dim=4, bounds=bounds)

    for z in range(resolution):
        for y in range(resolution):
            for x in range(resolution):
                wx, wy, wz = feature_vol.voxel_to_world(x, y, z)

                density = 0.0
                normal = [0.0, 0.0, 0.0]

                for px, py, pz in points:
                    dist = math.sqrt((wx - px) ** 2 + (wy - py) ** 2 + (wz - pz) ** 2)
                    if dist < bandwidth * 3:
                        weight = math.exp(-dist * dist / (2 * bandwidth * bandwidth))
                        density += weight

                feature_vol.voxels[(x, y, z)].features[0] = density
                feature_vol.voxels[(x, y, z)].features[1:4] = normal

    return feature_vol
