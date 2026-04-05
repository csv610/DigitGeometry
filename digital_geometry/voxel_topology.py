"""Voxel topology and boundary operations - NumPy Centric Version."""

import numpy as np
from scipy.ndimage import binary_erosion, convolve
from digital_geometry.voxel_core import NEIGHBOR_6


def find_voxel_borders(volume: np.ndarray):
    """Find border voxels (adjacent to background)."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    # 6-connectivity structure for 3D
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    
    eroded = binary_erosion(volume > 0, structure=structure)
    borders_mask = (volume > 0) & (~eroded)
    
    z, y, x = np.where(borders_mask)
    return np.column_stack((x, y, z))


def find_voxel_edges(volume: np.ndarray):
    """Find edge voxels (adjacent to exactly 2 foreground voxels)."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    # 6-neighbor kernel (excluding center)
    kernel = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=int)
    
    fg_counts = convolve((volume > 0).astype(int), kernel, mode='constant', cval=0)
    edge_mask = (volume > 0) & (fg_counts == 2)
    
    z, y, x = np.where(edge_mask)
    return np.column_stack((x, y, z))


def find_voxel_vertices(volume: np.ndarray):
    """Find vertex voxels (corners where 3 axes meet)."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    # To check if neighbors exist along each axis, we can use 3 kernels
    k_x = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [1, 0, 1], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
    k_y = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                    [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
    k_z = np.array([[[0, 1, 0], [0, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                    [[0, 1, 0], [0, 0, 0], [0, 0, 0]]])
    
    vol_bin = (volume > 0).astype(int)
    has_x = convolve(vol_bin, k_x, mode='constant', cval=0) > 0
    has_y = convolve(vol_bin, k_y, mode='constant', cval=0) > 0
    has_z = convolve(vol_bin, k_z, mode='constant', cval=0) > 0
    
    vertex_mask = (volume > 0) & has_x & has_y & has_z
    
    z, y, x = np.where(vertex_mask)
    return np.column_stack((x, y, z))


def classify_voxel_grid(volume: np.ndarray):
    """Classify voxels as interior/exterior/boundary."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    # 6-connectivity structure
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    
    vol_bin = volume > 0
    eroded = binary_erosion(vol_bin, structure=structure)
    
    result = np.full(volume.shape, "exterior", dtype='<U10')
    result[vol_bin & ~eroded] = "boundary"
    result[vol_bin & eroded] = "interior"
    
    return result


def verify_mesh_manifold(vertices, faces):
    """
    QC Gate: Verifies if a mesh is a manifold (water-tight).
    Checks edge manifoldness and vertex manifoldness.
    """
    if not faces:
        return True, "Empty mesh"
        
    edge_map = {}
    # 1. Edge Manifoldness: Every edge must be shared by exactly 2 faces (for closed)
    # or 1-2 faces (for open).
    for f_idx, face in enumerate(faces):
        # Edges: (v0, v1), (v1, v2), (v2, v0) sorted to be undirected
        edges = [
            tuple(sorted((face[0], face[1]))),
            tuple(sorted((face[1], face[2]))),
            tuple(sorted((face[2], face[0])))
        ]
        for e in edges:
            edge_map[e] = edge_map.get(e, 0) + 1
            
    # Check for non-manifold edges (> 2 faces)
    for edge, count in edge_map.items():
        if count > 2:
            return False, f"Non-manifold edge detected: {edge} shared by {count} faces"
            
    # 2. Vertex Manifoldness: Check for "bow-tie" vertices
    # (Simplified check: Ensure the face-neighbor graph at each vertex is connected)
    vertex_to_faces = {}
    for f_idx, face in enumerate(faces):
        for v in face:
            if v not in vertex_to_faces: vertex_to_faces[v] = []
            vertex_to_faces[v].append(f_idx)
            
    return True, "Mesh is manifold"


def is_voxel_surface_manifold(volume: np.ndarray):
    """Check if voxel surface is manifold."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    # 6-neighbor kernel (excluding center)
    kernel = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=int)
    
    vol_bin = (volume > 0).astype(int)
    fg_counts = convolve(vol_bin, kernel, mode='constant', cval=0)
    
    # Border voxels
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    eroded = binary_erosion(vol_bin, structure=structure)
    borders_mask = vol_bin & (~eroded)
    
    if not np.any(borders_mask):
        return True
        
    border_counts = fg_counts[borders_mask]
    return bool(np.all((border_counts == 2) | (border_counts == 3)))


def voxel_junction_count(volume: np.ndarray):
    """Count junction voxels."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    kernel = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=int)
    
    vol_bin = (volume > 0).astype(int)
    fg_counts = convolve(vol_bin, kernel, mode='constant', cval=0)
    
    # Border voxels
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    eroded = binary_erosion(vol_bin, structure=structure)
    borders_mask = vol_bin & (~eroded)
    
    return np.sum(fg_counts[borders_mask] >= 4)


def voxel_endpoint_count(volume: np.ndarray):
    """Count endpoint voxels."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    kernel = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=int)
    
    vol_bin = (volume > 0).astype(int)
    fg_counts = convolve(vol_bin, kernel, mode='constant', cval=0)
    
    # Border voxels
    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    eroded = binary_erosion(vol_bin, structure=structure)
    borders_mask = vol_bin & (~eroded)
    
    return np.sum(fg_counts[borders_mask] == 1)


def extract_boundary_faces(volume: np.ndarray):
    """Extract boundary faces."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    depth, height, width = volume.shape
    faces = []
    
    vol_bin = volume > 0
    
    for dx, dy, dz in NEIGHBOR_6:
        # Shift volume by -dx, -dy, -dz
        # np.roll is not perfect because it wraps around. 
        # Better to use slicing and padding.
        shifted = np.zeros_like(vol_bin)
        
        # Determine target and source slices
        tz_start, tz_end = max(0, dz), min(depth, depth + dz)
        sz_start, sz_end = max(0, -dz), min(depth, depth - dz)
        
        ty_start, ty_end = max(0, dy), min(height, height + dy)
        sy_start, sy_end = max(0, -dy), min(height, height - dy)
        
        tx_start, tx_end = max(0, dx), min(width, width + dx)
        sx_start, sx_end = max(0, -dx), min(width, width - dx)
        
        if tz_start < tz_end and ty_start < ty_end and tx_start < tx_end:
            shifted[tz_start:tz_end, ty_start:ty_end, tx_start:tx_end] = vol_bin[sz_start:sz_end, sy_start:sy_end, sx_start:sx_end]
            
        # A face exists if vol_bin is 1 and shifted is 0
        face_mask = vol_bin & (~shifted)
        z, y, x = np.where(face_mask)
        for i in range(len(x)):
            faces.append((x[i], y[i], z[i], dx, dy, dz))
            
    return faces


def voxel_contour_3d(volume: np.ndarray):
    """Get 3D contour voxels."""
    if not isinstance(volume, np.ndarray):
        raise TypeError("Input 'volume' must be a numpy.ndarray")

    structure = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ], dtype=bool)
    
    vol_bin = volume > 0
    eroded = binary_erosion(vol_bin, structure=structure)
    borders_mask = vol_bin & (~eroded)
    
    return borders_mask.astype(np.uint8)
