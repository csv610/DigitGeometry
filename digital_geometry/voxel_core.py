"""Core voxel utilities - NumPy Centric Version."""

import numpy as np
from scipy.ndimage import label

NEIGHBOR_6 = np.array([[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]])

NEIGHBOR_18 = np.array([
    [-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1],
    [-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0],
    [-1, 0, -1], [-1, 0, 1], [1, 0, -1], [1, 0, 1],
    [0, -1, -1], [0, -1, 1], [0, 1, -1], [0, 1, 1],
])

NEIGHBOR_26 = np.array([
    [-1, -1, -1], [-1, -1, 0], [-1, -1, 1], [-1, 0, -1], [-1, 0, 0], [-1, 0, 1],
    [-1, 1, -1], [-1, 1, 0], [-1, 1, 1], [0, -1, -1], [0, -1, 0], [0, -1, 1],
    [0, 0, -1], [0, 0, 1], [0, 1, -1], [0, 1, 0], [0, 1, 1], [1, -1, -1],
    [1, -1, 0], [1, -1, 1], [1, 0, -1], [1, 0, 0], [1, 0, 1], [1, 1, -1],
    [1, 1, 0], [1, 1, 1],
])


def get_neighbors_6(x, y, z):
    return (np.array([x, y, z]) + NEIGHBOR_6).tolist()


def get_neighbors_18(x, y, z):
    return (np.array([x, y, z]) + NEIGHBOR_18).tolist()


def get_neighbors_26(x, y, z):
    return (np.array([x, y, z]) + NEIGHBOR_26).tolist()


def voxel_euler_number(volume: np.ndarray):
    """Compute Euler number using NumPy slicing (optimized)."""
    # V - E + F - C (Cells/Voxels)
    # For a binary grid, we can approximate it via neighbor counts
    # But for rigor, let's use the property that it's a sum of local contributions
    # This is a Phase 2 Numba candidate for full rigor, but let's provide a vectorized version.
    v = np.sum(volume == 1)
    
    # Edges (connections between adjacent voxels)
    # We count connections in each axis
    e_x = np.sum(volume[:, :, :-1] & volume[:, :, 1:])
    e_y = np.sum(volume[:, :-1, :] & volume[:, 1:, :])
    e_z = np.sum(volume[:-1, :, :] & volume[1:, :, :])
    e = e_x + e_y + e_z
    
    # Faces (2x2 squares of voxels)
    f_xy = np.sum(volume[:, :-1, :-1] & volume[:, 1:, :-1] & volume[:, :-1, 1:] & volume[:, 1:, 1:])
    f_yz = np.sum(volume[:-1, :-1, :] & volume[1:, :-1, :] & volume[:-1, 1:, :] & volume[1:, 1:, :])
    f_xz = np.sum(volume[:-1, :, :-1] & volume[1:, :, :-1] & volume[:-1, :, 1:] & volume[1:, :, 1:])
    f = f_xy + f_yz + f_xz
    
    # Cells (2x2x2 cubes)
    c = np.sum(volume[:-1, :-1, :-1] & volume[1:, :-1, :-1] & volume[:-1, 1:, :-1] & volume[1:, 1:, :-1] &
               volume[:-1, :-1, 1:] & volume[1:, :-1, 1:] & volume[:-1, 1:, 1:] & volume[1:, 1:, 1:])
    
    return int(v - e + f - c)


def voxel_connectivity_count(volume: np.ndarray):
    """Count connected components using scipy.ndimage."""
    _, count = label(volume)
    return count


def voxel_coloring(volume: np.ndarray):
    """Color voxels using scipy.ndimage labeling."""
    colors, count = label(volume)
    return colors, count


def voxel_separated(volume: np.ndarray):
    """Check if voxel volume has separate components."""
    _, count = label(volume)
    return count > 1
