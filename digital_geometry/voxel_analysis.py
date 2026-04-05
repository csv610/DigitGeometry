"""Voxel analysis utilities - NumPy Centric Version."""

import numpy as np
from digital_geometry.voxel_core import NEIGHBOR_6
from digital_geometry.voxel_topology import voxel_junction_count


def compute_voxel_moments(volume: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute 3D moments for voxel shape with anisotropic spacing."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    z_idx, y_idx, x_idx = np.where(volume == 1)
    if z_idx.size == 0:
        return {"m000": 0}

    dz, dy, dx = spacing
    xs, ys, zs = x_idx * dx, y_idx * dy, z_idx * dz
    
    m000 = z_idx.size * (dx * dy * dz)
    m100 = np.sum(xs)
    m010 = np.sum(ys)
    m001 = np.sum(zs)
    
    # We could compute higher order moments if needed, but centroid is key
    cx = m100 / (m000 / (dx*dy*dz))
    cy = m010 / (m000 / (dx*dy*dz))
    cz = m001 / (m000 / (dx*dy*dz))

    return {
        "m000": m000,
        "centroid": (cx, cy, cz),
    }


class VoxelNeighborLookup:
    """Fast neighbor lookup using NumPy search."""

    def __init__(self, volume: np.ndarray):
        self.volume = volume
        self.voxel_coords = set(zip(*np.where(volume == 1)))

    def has_voxel(self, x, y, z):
        # Coordinates in where() are (z, y, x)
        return (z, y, x) in self.voxel_coords


def detect_3d_corners(volume: np.ndarray):
    """Detect corners in 3D voxel volume (vectorized approximation)."""
    # A voxel is a corner if it has 3-6 neighbors but those neighbors 
    # are distributed across at least 2 or 3 principal axes.
    # For now, keeping logic similar but using NumPy.
    from scipy.ndimage import convolve
    
    # Structure to count 6-neighbors
    kernel = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=np.uint8)
    
    neighbor_count = convolve(volume.astype(np.uint8), kernel, mode='constant', cval=0)
    
    # Candidate voxels (foreground with some neighbors)
    candidates = (volume == 1) & (neighbor_count >= 3)
    z, y, x = np.where(candidates)
    
    corners = []
    depth, height, width = volume.shape
    for i in range(len(z)):
        cz, cy, cx = z[i], y[i], x[i]
        # Check axis diversity
        axis_hits = [0, 0, 0]
        for dz, dy, dx in NEIGHBOR_6:
            nz, ny, nx = cz+dz, cy+dy, cx+dx
            if 0 <= nz < depth and 0 <= ny < height and 0 <= nx < width:
                if volume[nz, ny, nx] == 1:
                    if dz != 0: axis_hits[0] += 1
                    if dy != 0: axis_hits[1] += 1
                    if dx != 0: axis_hits[2] += 1
        if sum(1 for c in axis_hits if c > 0) >= 2:
            corners.append((cx, cy, cz))
            
    return corners


def detect_3d_junctions(volume: np.ndarray):
    """Detect junction voxels in 3D."""
    return voxel_junction_count(volume)


def extract_3d_contours(volume: np.ndarray):
    """Extract contours from 3D volume."""
    from digital_geometry.volume_isosurface import marching_squares

    depth = volume.shape[0]
    contours = []
    for z in range(depth):
        slice_2d = volume[z]
        lines = marching_squares(slice_2d, threshold=0.5)
        if lines:
            contours.append((z, lines))
    return contours
