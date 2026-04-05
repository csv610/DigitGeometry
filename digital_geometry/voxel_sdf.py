"""Signed Distance Fields and octree structures for voxels - NumPy Centric Version."""

import numpy as np
from scipy import ndimage
from digital_geometry.voxel_core import NEIGHBOR_6


def voxel_sdf_3d(volume: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute 3D signed distance field with anisotropic spacing."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    # sampling handles anisotropic spacing in ndimage.distance_transform_edt
    dist_to_fg = ndimage.distance_transform_edt(volume == 0, sampling=spacing)
    dist_to_bg = ndimage.distance_transform_edt(volume > 0, sampling=spacing)
    
    sdf = dist_to_fg - dist_to_bg
    return sdf


def voxel_to_octree(volume: np.ndarray, min_size=1):
    """Convert voxel grid to octree."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    depth, height, width = volume.shape

    def build_node(x, y, z, size):
        if size < min_size:
            return None
            
        # Extract subvolume
        x_end, y_end, z_end = min(x + size, width), min(y + size, height), min(z + size, depth)
        subvol = volume[z:z_end, y:y_end, x:x_end]
        
        if subvol.size == 0:
            return None
            
        has_foreground = np.any(subvol == 1)
        has_background = np.any(subvol == 0)
        
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

    root = build_node(0, 0, 0, 2**int(np.ceil(np.log2(max(depth, width, height)))))
    return root


def octree_to_voxel(node, resolution=32):
    """Convert octree back to voxel grid."""
    volume = np.zeros((resolution, resolution, resolution), dtype=np.uint8)
    if node is None:
        return volume

    def fill(node, x, y, z, size):
        if node is None:
            return
        if node.get("leaf", False):
            # In octree, 'size' is the size of the node in voxel units of the ORIGINAL volume.
            # But the 'fill' logic here is a bit simplified.
            sz = node.get("size", size)
            nx_end, ny_end, nz_end = min(x + sz, resolution), min(y + sz, resolution), min(z + sz, resolution)
            volume[z:nz_end, y:ny_end, x:nx_end] = 1
            return
        if "children" in node:
            half = size // 2
            for child in node["children"]:
                fill(child, child.get("x", x), child.get("y", y), child.get("z", z), half)

    fill(node, node.get("x", 0), node.get("y", 0), node.get("z", 0), node.get("size", resolution))
    return volume


class SparseVoxelOctree:
    """Sparse Voxel Octree for efficient voxel storage."""

    def __init__(self, max_depth=8):
        self.max_depth = max_depth
        self.root = None

    def insert(self, x, y, z):
        if self.root is None:
            self.root = {"children": {}, "leaf": False}
        self._insert_recursive(self.root, x, y, z, 0, 2**self.max_depth, 0, 0, 0)

    def _insert_recursive(self, node, x, y, z, depth, size, ox, oy, oz):
        if depth >= self.max_depth:
            node["leaf"] = True
            return
        size //= 2
        idx = 0
        if x >= ox + size: idx += 1; ox += size
        if y >= oy + size: idx += 2; oy += size
        if z >= oz + size: idx += 4; oz += size
        
        if "children" not in node:
            node["children"] = {}
            node["leaf"] = False
            
        if idx not in node["children"]:
            node["children"][idx] = {"leaf": False}
            
        self._insert_recursive(node["children"][idx], x, y, z, depth + 1, size, ox, oy, oz)

    def contains(self, x, y, z):
        if self.root is None: return False
        return self._contains_recursive(self.root, x, y, z, 0, 2**self.max_depth, 0, 0, 0)

    def _contains_recursive(self, node, x, y, z, depth, size, ox, oy, oz):
        if node is None: return False
        if node.get("leaf", False): return True
        if "children" not in node: return False
        
        size //= 2
        idx = 0
        if x >= ox + size: idx += 1; ox += size
        if y >= oy + size: idx += 2; oy += size
        if z >= oz + size: idx += 4; oz += size
        
        return self._contains_recursive(node["children"].get(idx), x, y, z, depth + 1, size, ox, oy, oz)


def build_sparse_voxel_octree(volume: np.ndarray, max_depth=5):
    """Build sparse voxel octree from dense volume."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
    octree = SparseVoxelOctree(max_depth)
    z_coords, y_coords, x_coords = np.where(volume == 1)
    for i in range(len(x_coords)):
        octree.insert(x_coords[i], y_coords[i], z_coords[i])
    return octree


class VoxelEpitome:
    """Voxel epitome for compressed representation."""

    def __init__(self, epitome_size=4, color_channels=3):
        self.epitome_size = epitome_size
        self.channels = color_channels
        self.data = np.zeros((epitome_size, epitome_size, epitome_size), dtype=np.float32)
        self.mask = np.zeros((epitome_size, epitome_size, epitome_size), dtype=np.uint8)

    def fill_from_voxel_grid(self, volume: np.ndarray, start_x, start_y, start_z):
        depth, height, width = volume.shape
        sz = self.epitome_size
        
        vz_end = min(start_z + sz, depth)
        vy_end = min(start_y + sz, height)
        vx_end = min(start_x + sz, width)
        
        subvol = volume[start_z:vz_end, start_y:vy_end, start_x:vx_end]
        
        ez_end = vz_end - start_z
        ey_end = vy_end - start_y
        ex_end = vx_end - start_x
        
        self.data[:ez_end, :ey_end, :ex_end] = subvol.astype(np.float32)
        self.mask[:ez_end, :ey_end, :ex_end] = 1

    def to_dense(self, resolution=None):
        if resolution is None:
            resolution = self.epitome_size
        scale = max(1, resolution // self.epitome_size)
        
        # Using np.repeat to scale up
        res = np.repeat(np.repeat(np.repeat(self.data, scale, axis=0), scale, axis=1), scale, axis=2)
        mask_res = np.repeat(np.repeat(np.repeat(self.mask, scale, axis=0), scale, axis=1), scale, axis=2)
        
        final = np.zeros((resolution, resolution, resolution), dtype=np.float32)
        min_res = min(resolution, res.shape[0])
        final[:min_res, :min_res, :min_res] = res[:min_res, :min_res, :min_res] * mask_res[:min_res, :min_res, :min_res]
        
        return final


def build_voxel_epitomes(volume: np.ndarray, epitome_size=4):
    """Build epitomes from voxel volume."""
    depth, height, width = volume.shape
    epitomes = []
    step = epitome_size
    for z in range(0, depth, step):
        for y in range(0, height, step):
            for x in range(0, width, step):
                epit = VoxelEpitome(epitome_size)
                epit.fill_from_voxel_grid(volume, x, y, z)
                epitomes.append((x, y, z, epit))
    return epitomes
