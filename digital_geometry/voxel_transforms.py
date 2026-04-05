"""Voxel transforms and conversions - NumPy Centric Version."""

import numpy as np
from scipy import ndimage
from digital_geometry.voxel_core import NEIGHBOR_6


def voxelize_triangle_mesh(vertices: np.ndarray, triangles: np.ndarray, resolution=32):
    """Voxelize a triangle mesh."""
    if not isinstance(vertices, np.ndarray):
        vertices = np.asanyarray(vertices)
    if not isinstance(triangles, np.ndarray):
        triangles = np.asanyarray(triangles)

    if vertices.size == 0 or triangles.size == 0:
        return np.zeros((resolution, resolution, resolution), dtype=np.uint8)

    xmin, ymin, zmin = vertices.min(axis=0)
    xmax, ymax, zmax = vertices.max(axis=0)

    max_range = max(xmax - xmin, ymax - ymin, zmax - zmin)
    if max_range == 0:
        max_range = 1

    volume = np.zeros((resolution, resolution, resolution), dtype=np.uint8)

    for tri in triangles:
        if len(tri) < 3:
            continue
        v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]

        v_tri = np.stack([v0, v1, v2])
        min_v = (((v_tri.min(axis=0) - [xmin, ymin, zmin]) / max_range) * resolution).astype(int)
        max_v = (((v_tri.max(axis=0) - [xmin, ymin, zmin]) / max_range) * resolution).astype(int)

        min_coords = np.clip(min_v, 0, resolution - 1)
        max_coords = np.clip(max_v, 0, resolution - 1)

        for z in range(min_coords[2], max_coords[2] + 1):
            for y in range(min_coords[1], max_coords[1] + 1):
                for x in range(min_coords[0], max_coords[0] + 1):
                    px = xmin + (x + 0.5) / resolution * max_range
                    py = ymin + (y + 0.5) / resolution * max_range
                    pz = zmin + (z + 0.5) / resolution * max_range
                    if point_in_triangle(px, py, pz, v0, v1, v2):
                        volume[z, y, x] = 1

    return volume


def point_in_triangle(px, py, pz, v0, v1, v2):
    """
    Robust Edge Function predicate for voxel-triangle intersection.
    Determines if point (px, py, pz) is near the triangle surface.
    """
    # 1. Project to the plane of the triangle
    normal = np.cross(v1 - v0, v2 - v0)
    norm_mag = np.linalg.norm(normal)
    if norm_mag < 1e-15:
        return False
    unit_normal = normal / norm_mag
    
    # 2. Check distance from point to plane (must be within half-voxel thickness)
    dist_to_plane = np.dot(np.array([px, py, pz]) - v0, unit_normal)
    if abs(dist_to_plane) > 0.5: # Half-voxel thickness
        return False
        
    # 3. Project 3D point and triangle to 2D (choose best axis)
    abs_n = np.abs(unit_normal)
    if abs_n[2] >= abs_n[0] and abs_n[2] >= abs_n[1]:
        # Project to XY
        p, a, b, c = (px, py), v0[:2], v1[:2], v2[:2]
    elif abs_n[1] >= abs_n[0]:
        # Project to XZ
        p, a, b, c = (px, pz), v0[[0, 2]], v1[[0, 2]], v2[[0, 2]]
    else:
        # Project to YZ
        p, a, b, c = (py, pz), v0[1:], v1[1:], v2[1:]
        
    # 4. Edge functions (2D Cross Product) - Exact sign check
    def edge_func(p1, p2, p3):
        return (p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])
    
    w0 = edge_func(a, b, p)
    w1 = edge_func(b, c, p)
    w2 = edge_func(c, a, p)
    
    # Check if point is on the same side of all edges
    return (w0 >= 0 and w1 >= 0 and w2 >= 0) or (w0 <= 0 and w1 <= 0 and w2 <= 0)


def voxelize_surface_mesh(vertices, triangles, resolution=32):
    """Voxelize only the surface."""
    return voxelize_triangle_mesh(vertices, triangles, resolution)


def merge_voxels(volume: np.ndarray, level=2):
    """Merge voxels at given level using block maximum."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")
        
    d, h, w = volume.shape
    new_d, new_h, new_w = (d + level - 1) // level, (h + level - 1) // level, (w + level - 1) // level
    
    padded = np.zeros((new_d * level, new_h * level, new_w * level), dtype=volume.dtype)
    padded[:d, :h, :w] = volume
    
    reshaped = padded.reshape(new_d, level, new_h, level, new_w, level)
    result = reshaped.max(axis=(1, 3, 5))
    
    return result


def minkowski_sum_voxel(volume1: np.ndarray, volume2: np.ndarray):
    """Compute Minkowski sum using convolution."""
    from scipy.signal import convolve
    if not isinstance(volume1, np.ndarray) or not isinstance(volume2, np.ndarray):
        raise TypeError("Inputs must be numpy.ndarrays")
        
    res = convolve((volume1 > 0).astype(int), (volume2 > 0).astype(int), mode='full') > 0
    return res.astype(np.uint8)


def voxel_dilate_3d(volume: np.ndarray, iterations=1):
    """3D morphological dilation."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")
        
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    
    result = ndimage.binary_dilation(volume > 0, structure=structure, iterations=iterations)
    return result.astype(np.uint8)


def voxel_erode_3d(volume: np.ndarray, iterations=1):
    """3D morphological erosion."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")
        
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    
    result = ndimage.binary_erosion(volume > 0, structure=structure, iterations=iterations, border_value=0)
    return result.astype(np.uint8)


def fill_voxel_holes(volume: np.ndarray):
    """Fill holes in voxel volume."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")
        
    result = ndimage.binary_fill_holes(volume > 0)
    return result.astype(np.uint8)


def voxel_pyramid(volume: np.ndarray, levels=3):
    """Build multi-resolution voxel pyramid."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")
        
    pyramid = [volume]
    curr = volume.astype(float)

    for _ in range(1, levels):
        d, h, w = curr.shape
        if d < 2 or h < 2 or w < 2:
            break
        new_d, new_h, new_w = d // 2, h // 2, w // 2
        
        trimmed = curr[:new_d*2, :new_h*2, :new_w*2]
        reshaped = trimmed.reshape(new_d, 2, new_h, 2, new_w, 2)
        curr = reshaped.mean(axis=(1, 3, 5))
        pyramid.append(curr)
        
    return pyramid
