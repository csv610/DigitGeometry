"""Voxel utilities - compatibility module.

This module imports from the split voxel submodules for backward compatibility.
"""

from digital_geometry.voxel_core import (
    get_neighbors_6,
    get_neighbors_18,
    get_neighbors_26,
    voxel_euler_number,
    voxel_connectivity_count,
    voxel_coloring,
    voxel_separated,
)

from digital_geometry.voxel_topology import (
    classify_voxel_grid,
    find_voxel_borders,
    find_voxel_edges,
    find_voxel_vertices,
    is_voxel_surface_manifold,
    voxel_junction_count,
    voxel_endpoint_count,
    extract_boundary_faces,
    voxel_contour_3d,
)

from digital_geometry.voxel_transforms import (
    voxelize_triangle_mesh,
    voxelize_surface_mesh,
    merge_voxels,
    minkowski_sum_voxel,
    voxel_dilate_3d,
    voxel_erode_3d,
    fill_voxel_holes,
    voxel_pyramid,
)

from digital_geometry.volume_thinning import morphological_skeleton, skeleton_3d_medial
from digital_geometry.volume_isosurface import surface_nets
from digital_geometry.voxel_render import (
    ray_voxel_intersection,
    ray_cast_volume,
    volume_raymarch,
    volume_raymarch_with_normal,
    dual_contouring,
    voxel_gradient_normals,
    smooth_isosurface,
    voxel_carving,
)


def voxel_sdf_3d(volume):
    """Compute 3D signed distance field."""
    from digital_geometry.distance import euclidean_distance_transform

    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    sdf = [[[0.0] * width for _ in range(height)] for _ in range(depth)]

    for z in range(depth):
        dist_map = euclidean_distance_transform(volume[z])
        for y in range(height):
            for x in range(width):
                sdf[z][y][x] = dist_map[y][x]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1:
                    sdf[z][y][x] = -sdf[z][y][x]

    return sdf


def compute_voxel_moments(volume):
    """Compute 3D moments for voxel shape."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    m000 = m100 = m010 = m001 = m110 = m101 = m011 = m200 = m020 = m002 = 0

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1:
                    m000 += 1
                    m100 += x
                    m010 += y
                    m001 += z
                    m110 += x * y
                    m101 += x * z
                    m011 += y * z
                    m200 += x * x
                    m020 += y * y
                    m002 += z * z

    if m000 == 0:
        return {"m000": 0}

    cx = m100 / m000
    cy = m010 / m000
    cz = m001 / m000

    return {
        "m000": m000,
        "centroid": (cx, cy, cz),
    }


def voxel_to_octree(volume, min_size=1):
    """Convert voxel grid to octree."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    def build_node(x, y, z, size):
        if size < min_size:
            return None
        has_foreground = has_background = False
        for dz in range(size):
            for dy in range(size):
                for dx in range(size):
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        if volume[nz][ny][nx] == 1:
                            has_foreground = True
                        else:
                            has_background = True
        if not has_foreground:
            return None
        if not has_background:
            return {"leaf": True, "x": x, "y": y, "z": z, "size": size}
        half = size // 2
        if half < min_size:
            return {"leaf": True, "x": x, "y": y, "z": z, "size": size}
        children = []
        for dz in [0, half]:
            for dy in [0, half]:
                for dx in [0, half]:
                    child = build_node(x + dx, y + dy, z + dz, half)
                    if child:
                        children.append(child)
        if not children:
            return None
        return {
            "leaf": False,
            "x": x,
            "y": y,
            "z": z,
            "size": size,
            "children": children,
        }

    root = build_node(0, 0, 0, max(depth, max(width, height)))
    return root


def octree_to_voxel(node, resolution=32):
    """Convert octree back to voxel grid."""
    if node is None:
        return [
            [[0] * resolution for _ in range(resolution)] for _ in range(resolution)
        ]
    volume = [[[0] * resolution for _ in range(resolution)] for _ in range(resolution)]

    def fill(node, x, y, z, size):
        if node is None:
            return
        if node.get("leaf", False):
            step = resolution // size if size > 0 else 1
            for dz in range(step):
                for dy in range(step):
                    for dx in range(step):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if (
                            0 <= nx < resolution
                            and 0 <= ny < resolution
                            and 0 <= nz < resolution
                        ):
                            volume[nz][ny][nx] = 1
            return
        if "children" in node:
            half = size // 2
            for child in node["children"]:
                if "x" in child and "y" in child and "z" in child:
                    fill(
                        child,
                        child.get("x", x),
                        child.get("y", y),
                        child.get("z", z),
                        half,
                    )

    fill(node, 0, 0, 0, resolution)
    return volume


class SparseVoxelOctree:
    """Sparse Voxel Octree for efficient voxel storage."""

    def __init__(self, max_depth=8):
        self.max_depth = max_depth
        self.root = None

    def insert(self, x, y, z):
        if self.root is None:
            self.root = {"children": {}, "leaf": True}
        self._insert_recursive(self.root, x, y, z, 0, 2**self.max_depth, 0)

    def _insert_recursive(self, node, x, y, z, depth, size, offset):
        if depth >= self.max_depth:
            return
        size //= 2
        idx = 0
        if x >= offset + size:
            idx += 1
        if y >= offset + size:
            idx += 2
        if z >= offset + size:
            idx += 4
        if node.get("leaf", False):
            node["leaf"] = False
            node["children"] = {}
        if idx not in node["children"]:
            node["children"][idx] = {"leaf": True}
        child = node["children"][idx]
        if depth == self.max_depth - 1:
            child["leaf"] = True
        else:
            self._insert_recursive(child, x, y, z, depth + 1, size, offset)

    def contains(self, x, y, z):
        return self._contains_recursive(self.root, x, y, z, 0, 2**self.max_depth, 0)

    def _contains_recursive(self, node, x, y, z, depth, size, offset):
        if node is None:
            return False
        if node.get("leaf", False):
            return True
        size //= 2
        idx = 0
        if x >= offset + size:
            idx += 1
        if y >= offset + size:
            idx += 2
        if z >= offset + size:
            idx += 4
        return self._contains_recursive(
            node.get("children", {}).get(idx), x, y, z, depth + 1, size, offset
        )


def build_sparse_voxel_octree(volume, max_depth=5):
    """Build sparse voxel octree from dense volume."""
    octree = SparseVoxelOctree(max_depth)
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1:
                    octree.insert(x, y, z)
    return octree


class VoxelNeighborLookup:
    """Fast neighbor lookup using hash table."""

    def __init__(self, volume):
        self.volume = volume
        self.depth = len(volume)
        self.height = len(volume[0])
        self.width = len(volume[0][0])
        self.voxel_set = set()
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if volume[z][y][x] == 1:
                        self.voxel_set.add((x, y, z))

    def has_voxel(self, x, y, z):
        return (x, y, z) in self.voxel_set


def cut_mesh_by_plane(vertices, triangles, plane_normal, plane_d):
    """Cut mesh by plane."""
    from digital_geometry.voxel_transforms import point_in_triangle

    intersection_points = []
    intersection_lines = []
    for tri in triangles:
        if len(tri) < 3:
            continue
        v0 = vertices[tri[0]]
        v1 = vertices[tri[1]]
        v2 = vertices[tri[2]]
        d0 = (
            plane_normal[0] * v0[0]
            + plane_normal[1] * v0[1]
            + plane_normal[2] * v0[2]
            - plane_d
        )
        d1 = (
            plane_normal[0] * v1[0]
            + plane_normal[1] * v1[1]
            + plane_normal[2] * v1[2]
            - plane_d
        )
        d2 = (
            plane_normal[0] * v2[0]
            + plane_normal[1] * v2[1]
            + plane_normal[2] * v2[2]
            - plane_d
        )
        if d0 == 0:
            intersection_points.append(v0)
        if d1 == 0:
            intersection_points.append(v1)
        if d2 == 0:
            intersection_points.append(v2)
    return intersection_points, intersection_lines


def cut_voxel_by_plane(volume, plane_normal, plane_d):
    """Cut voxel volume by plane."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])
    result = [[[0] * width for _ in range(height)] for _ in range(depth)]
    nx, ny, nz = plane_normal
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1:
                    dist = nx * x + ny * y + nz * z - plane_d
                    if dist <= 0:
                        result[z][y][x] = 1
    return result


class VoxelEpitome:
    """Voxel epitome for compressed representation."""

    def __init__(self, epitome_size=4, color_channels=3):
        self.epitome_size = epitome_size
        self.channels = color_channels
        self.data = []
        self.mask = []
        for z in range(epitome_size):
            layer = []
            mask_layer = []
            for y in range(epitome_size):
                row = [0.0 for _ in range(epitome_size)]
                mask_row = [0 for _ in range(epitome_size)]
                layer.append(row)
                mask_layer.append(mask_row)
            self.data.append(layer)
            self.mask.append(mask_layer)

    def fill_from_voxel_grid(self, volume, start_x, start_y, start_z):
        depth = len(volume)
        height = len(volume[0])
        width = len(volume[0][0])
        sz = self.epitome_size
        for z in range(sz):
            for y in range(sz):
                for x in range(sz):
                    vx = start_x + x
                    vy = start_y + y
                    vz = start_z + z
                    if 0 <= vx < width and 0 <= vy < height and 0 <= vz < depth:
                        self.mask[z][y][x] = 1
                        self.data[z][y][x] = float(volume[vz][vy][vx])

    def to_dense(self, resolution=None):
        if resolution is None:
            resolution = self.epitome_size
        scale = max(1, resolution // self.epitome_size)
        result = [
            [[0.0 for _ in range(resolution)] for _ in range(resolution)]
            for _ in range(resolution)
        ]
        for z in range(resolution):
            for y in range(resolution):
                for x in range(resolution):
                    ez = min(z // scale, self.epitome_size - 1)
                    ey = min(y // scale, self.epitome_size - 1)
                    ex = min(x // scale, self.epitome_size - 1)
                    if self.mask[ez][ey][ex]:
                        result[z][y][x] = self.data[ez][ey][ex]
        return result


def build_voxel_epitomes(volume, epitome_size=4):
    """Build epitomes from voxel volume."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])
    epitomes = []
    step = epitome_size
    for z in range(0, depth, step):
        for y in range(0, height, step):
            for x in range(0, width, step):
                epit = VoxelEpitome(epitome_size)
                epit.fill_from_voxel_grid(volume, x, y, z)
                epitomes.append((x, y, z, epit))
    return epitomes


class EulerOperators:
    """Euler operators for topological voxel editing."""

    @staticmethod
    def make_voxel(volume, x, y, z):
        result = [[[v for v in row] for row in layer] for layer in volume]
        result[z][y][x] = 1
        return result

    @staticmethod
    def remove_voxel(volume, x, y, z):
        result = [[[v for v in row] for row in layer] for layer in volume]
        result[z][y][x] = 0
        return result

    @staticmethod
    def toggle_voxel(volume, x, y, z):
        result = [[[v for v in row] for row in layer] for layer in volume]
        result[z][y][x] = 1 - result[z][y][x]
        return result


def detect_3d_corners(volume):
    """Detect corners in 3D voxel volume."""
    from digital_geometry.voxel_core import NEIGHBOR_6

    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])
    corners = []
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue
                neighbors = []
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        if volume[nz][ny][nx] == 1:
                            neighbors.append((dx, dy, dz))
                if len(neighbors) >= 3:
                    axis_counts = [0, 0, 0]
                    for dx, dy, dz in neighbors:
                        if dx != 0:
                            axis_counts[0] += 1
                        if dy != 0:
                            axis_counts[1] += 1
                        if dz != 0:
                            axis_counts[2] += 1
                    if sum(1 for c in axis_counts if c > 0) >= 2:
                        corners.append((x, y, z))
    return corners


def detect_3d_junctions(volume):
    """Detect junction voxels in 3D."""
    from digital_geometry.voxel_topology import voxel_junction_count

    return voxel_junction_count(volume)


def extract_3d_contours(volume):
    """Extract contours from 3D volume."""
    from digital_geometry.volume_isosurface import marching_squares

    depth = len(volume)
    contours = []
    for z in range(depth):
        slice_2d = volume[z]
        lines = marching_squares(slice_2d, threshold=0.5)
        if lines:
            contours.append((z, lines))
    return contours
