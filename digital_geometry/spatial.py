"""Spatial data structures."""

import numpy as np
from digital_geometry.distance import euclidean_distance
from digital_geometry.descriptors import detect_critical_points


class Quadtree:
    """Quadtree for 2D spatial indexing."""

    def __init__(self, bounds, capacity=4):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        x, y = point
        bx, by, bw, bh = self.bounds

        if not (bx <= x < bx + bw and by <= y < by + bh):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        return (
            self.northeast.insert(point)
            or self.northwest.insert(point)
            or self.southeast.insert(point)
            or self.southwest.insert(point)
        )

    def subdivide(self):
        x, y, w, h = self.bounds
        half_w = w // 2
        half_h = h // 2

        self.northeast = Quadtree((x + half_w, y, half_w, half_h), self.capacity)
        self.northwest = Quadtree((x, y, half_w, half_h), self.capacity)
        self.southeast = Quadtree(
            (x + half_w, y + half_h, half_w, half_h), self.capacity
        )
        self.southwest = Quadtree((x, y + half_h, half_w, half_h), self.capacity)
        self.divided = True


class Octree:
    """Octree for 3D spatial indexing."""

    def __init__(self, bounds, capacity=4):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        x, y, z = point
        bx, by, bz, bw, bh, bd = self.bounds

        if not (bx <= x < bx + bw and by <= y < by + bh and bz <= z < bz + bd):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(point):
                return True
        return False

    def subdivide(self):
        x, y, z, w, h, d = self.bounds
        hw, hh, hd = w // 2, h // 2, d // 2

        self.children = []
        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    child_bounds = (x + dx * hw, y + dy * hh, z + dz * hd, hw, hh, hd)
                    self.children.append(Octree(child_bounds, self.capacity))
        self.divided = True


def compute_reeb_graph(grid):
    """Compute Reeb graph from height function."""
    nodes = []
    edges = []

    critical = detect_critical_points(grid)

    for x, y in critical["peaks"]:
        nodes.append({"type": "peak", "x": x, "y": y, "value": grid[y][x]})
    for x, y in critical["pits"]:
        nodes.append({"type": "pit", "x": x, "y": y, "value": grid[y][x]})
    for x, y in critical.get("saddles", []):
        nodes.append({"type": "saddle", "x": x, "y": y, "value": grid[y][x]})

    return {"nodes": nodes, "edges": edges}


def jump_flooding_dt(grid: np.ndarray, spacing=(1.0, 1.0)):
    """Jump Flooding Algorithm for distance transform (vectorized/optimized with spacing)."""
    import numpy as np
    from scipy.ndimage import distance_transform_edt
    arr = np.asarray(grid)
    if not np.any(arr == 1):
        return np.full(arr.shape, float('inf'))
    
    # sampling handles anisotropic spacing
    dist = distance_transform_edt(arr == 0, sampling=spacing)
    return dist


def compute_sdf(grid: np.ndarray, spacing=(1.0, 1.0)):
    """Signed Distance Field (vectorized/optimized with spacing)."""
    import numpy as np
    from scipy.ndimage import distance_transform_edt
    arr = np.asarray(grid)
    if not np.any(arr == 1):
        return np.full(arr.shape, -float('inf'))
    if np.all(arr == 1):
        return np.zeros(arr.shape)
    
    # sampling handles anisotropic spacing
    dist_out = distance_transform_edt(arr == 0, sampling=spacing)
    
    dist = np.zeros_like(arr, dtype=float)
    dist[arr == 0] = -dist_out[arr == 0]
    return dist
