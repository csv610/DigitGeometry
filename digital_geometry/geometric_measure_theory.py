"""Geometric Measure Theory algorithms for voxel geometry - Optimized with Anisotropic Support."""

import numpy as np
import math
from digital_geometry.voxel_core import NEIGHBOR_6


def compute_voxel_perimeter(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute discrete surface area of voxel set with anisotropic support."""
    if not isinstance(voxels, np.ndarray):
        voxels = np.asanyarray(voxels)
    
    dz, dy, dx = spacing
    area = 0.0
    
    # Check X-direction faces (area = dy * dz)
    area += np.sum(voxels[:, :, :-1] != voxels[:, :, 1:]) * (dy * dz)
    area += (np.sum(voxels[:, :, 0] == 1) + np.sum(voxels[:, :, -1] == 1)) * (dy * dz)
    
    # Check Y-direction faces (area = dx * dz)
    area += np.sum(voxels[:, :-1, :] != voxels[:, 1:, :]) * (dx * dz)
    area += (np.sum(voxels[:, 0, :] == 1) + np.sum(voxels[:, -1, :] == 1)) * (dx * dz)
    
    # Check Z-direction faces (area = dx * dy)
    area += np.sum(voxels[:-1, :, :] != voxels[1:, :, :]) * (dx * dy)
    area += (np.sum(voxels[0, :, :] == 1) + np.sum(voxels[-1, :, :] == 1)) * (dx * dy)
    
    return area


def compute_voxel_surface_area(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute surface area of voxel set."""
    return compute_voxel_perimeter(voxels, spacing)


def compute_isoperimetric_quotient(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute isoperimetric quotient of voxel shape."""
    dx, dy, dz = spacing
    voxel_vol = dx * dy * dz
    total_volume = np.sum(voxels == 1) * voxel_vol
    area = compute_voxel_surface_area(voxels, spacing)

    if total_volume == 0 or area == 0:
        return 0.0

    # IQ = 36 * pi * V^2 / A^3 (for a sphere IQ=1)
    iq = 36.0 * np.pi * (total_volume**2) / (area**3)
    return min(1.0, iq)


def compute_minkowski_content(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute Minkowski functionals of voxel set with anisotropic support."""
    dx, dy, dz = spacing
    v0_volume = np.sum(voxels == 1) * (dx * dy * dz)
    v1_surface = compute_voxel_surface_area(voxels, spacing)
    
    # V2 and V3 are more complex for anisotropic grids, 
    # but Euler characteristic (V3) is topological and invariant to spacing.
    from digital_geometry.voxel_core import voxel_euler_number
    v3_euler = voxel_euler_number(voxels)

    return {
        "V0_volume": v0_volume,
        "V1_surface": v1_surface,
        "V2_mean_breadth": v1_surface / (4.0 * np.pi)**0.5, # Approximation
        "V3_euler": v3_euler,
    }


def compute_mean_curvature_voxel(voxels: np.ndarray, point, spacing=(1.0, 1.0, 1.0)):
    """Compute discrete mean curvature at a voxel (vectorized placeholder)."""
    # Full anisotropic curvature requires Hessian or structure tensor.
    # For now, we use the neighbor count approximation weighted by spacing.
    x, y, z = point
    if not (0 <= z < voxels.shape[0] and 0 <= y < voxels.shape[1] and 0 <= x < voxels.shape[2]):
        return 0.0
    
    # Simple approximation: deviation from flat 6-neighbor connectivity
    # Weighted by average spacing
    avg_s = sum(spacing) / 3.0
    neighbors = 0
    offsets = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]
    for dz, dy, dx in offsets:
        nz, ny, nx = z+dz, y+dy, x+dx
        if 0 <= nz < voxels.shape[0] and 0 <= ny < voxels.shape[1] and 0 <= nx < voxels.shape[2]:
            if voxels[nz, ny, nx] == 1:
                neighbors += 1
                
    return (2.0 * np.pi * (1.0 - neighbors / 6.0)) / avg_s


def compute_gaussian_curvature_voxel(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute total Gaussian curvature via Gauss-Bonnet (Topological)."""
    from digital_geometry.voxel_core import voxel_euler_number
    euler = voxel_euler_number(voxels)
    return 2.0 * np.pi * euler


def compute_principal_curvatures(voxels: np.ndarray, point, spacing=(1.0, 1.0, 1.0)):
    """Compute principal curvatures at a surface point (approximation)."""
    mean_k = compute_mean_curvature_voxel(voxels, point, spacing)
    # total Gaussian curvature is global, we return approximation
    return (mean_k, mean_k)


def compute_crofton_integral(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute Crofton integral for surface area estimation."""
    area = compute_voxel_surface_area(voxels, spacing)
    return np.pi * area


def compute_support_function(voxels: np.ndarray, direction, spacing=(1.0, 1.0, 1.0)):
    """Compute support function in given direction considering spacing."""
    idx = np.where(voxels == 1)
    if len(idx[0]) == 0:
        return 0.0
    
    dz, dy, dx = spacing
    coords = np.vstack([idx[2]*dx, idx[1]*dy, idx[0]*dz]).T
    u = np.array(direction) / np.linalg.norm(direction)
    
    return np.max(np.dot(coords, u))


def compute_mean_width(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute mean width of voxel shape."""
    directions = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (-1, 1, 0), (1, -1, 1),
    ]
    total = sum(compute_support_function(voxels, d, spacing) for d in directions)
    return total / len(directions)


def compute_mean_curvature_flow_voxel(voxels: np.ndarray, iterations=10, dt=0.1, spacing=(1.0, 1.0, 1.0)):
    """Apply mean curvature flow to voxel shape."""
    current = voxels.copy()
    for _ in range(iterations):
        # Optimized placeholder for flow
        current = compute_inverse_mean_curvature_flow(current, iterations=1)
    return current


def compute_inverse_mean_curvature_flow(voxels: np.ndarray, iterations=10):
    """Apply inverse mean curvature flow (expanding flow) - Vectorized."""
    from scipy.ndimage import binary_dilation
    return binary_dilation(voxels > 0, iterations=iterations).astype(np.uint8)


def compute_geodesic_on_voxel_surface(voxels: np.ndarray, start, end):
    """Find geodesic path on voxel surface."""
    # Placeholder for graph search
    return [start, end]


def compute_minimal_surface_voxel(voxels: np.ndarray):
    """Find minimal surface through voxel boundary."""
    from scipy.ndimage import binary_erosion
    boundary = voxels.astype(np.uint8) - binary_erosion(voxels > 0).astype(np.uint8)
    return boundary


def compute_normal_current(voxels: np.ndarray):
    """Compute normal vector field on voxel surface."""
    from scipy.ndimage import sobel
    # Using Sobel as normal estimator
    grad_z = sobel(voxels.astype(float), axis=0)
    grad_y = sobel(voxels.astype(float), axis=1)
    grad_x = sobel(voxels.astype(float), axis=2)
    return {"grad_x": grad_x, "grad_y": grad_y, "grad_z": grad_z}


def compute_euler_characteristic(voxels: np.ndarray):
    """Compute Euler characteristic of voxel shape."""
    from digital_geometry.voxel_core import voxel_euler_number
    return voxel_euler_number(voxels)


def compute_filling_volume(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute volume needed to fill enclosed cavities with anisotropic support."""
    from scipy.ndimage import binary_fill_holes
    filled = binary_fill_holes(voxels > 0)
    cavity_voxels = np.sum((filled.astype(int) - (voxels > 0).astype(int)) == 1)
    dx, dy, dz = spacing
    return cavity_voxels * (dx * dy * dz)


def compute_distance_to_measure(voxels1: np.ndarray, voxels2: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute average distance between two voxel sets."""
    from scipy.ndimage import distance_transform_edt
    if not np.any(voxels1) or not np.any(voxels2):
        return float('inf')
    
    # Distance from every point in voxels1 to nearest point in voxels2
    dist_map = distance_transform_edt(voxels2 == 0, sampling=spacing)
    return np.mean(dist_map[voxels1 == 1])


def compute_medial_axis_voxel(voxels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
    """Compute medial axis of voxel shape - Optimized with Distance Transform."""
    from scipy.ndimage import distance_transform_edt
    if not np.any(voxels):
        return np.zeros_like(voxels)
    
    # The medial axis can be approximated by the local maxima of the distance transform
    dist = distance_transform_edt(voxels > 0, sampling=spacing)
    
    # Simple laplacian-based local maxima detection
    from scipy.ndimage import laplace
    is_max = laplace(dist) < -0.5
    return (voxels > 0) & is_max


def compute_imt_2d(points, rank=2, is_closed=True):
    """Calculates the 2D Irreducible Minkowski Tensor (IMT)."""
    import cmath
    pts = np.array(points)
    if is_closed and not np.allclose(pts[0], pts[-1]):
        pts = np.vstack([pts, pts[0]])
    edges = np.diff(pts, axis=0)
    lengths = np.linalg.norm(edges, axis=1)
    perimeter = np.sum(lengths)
    normals = np.zeros_like(edges)
    normals[:, 0] = -edges[:, 1]
    normals[:, 1] = edges[:, 0]
    psi = 0j
    for i in range(len(edges)):
        if lengths[i] > 1e-9:
            theta = np.arctan2(normals[i, 1], normals[i, 0])
            psi += lengths[i] * cmath.exp(1j * rank * theta)
    beta = abs(psi) / perimeter if perimeter > 0 else 0
    return {"psi": psi, "perimeter": perimeter, "beta": beta}


def compute_imt_3d(volume: np.ndarray, l=2, threshold=0.5):
    """Calculates the 3D Irreducible Minkowski Tensors (IMTs) of rank l."""
    from scipy.special import sph_harm_y
    from digital_geometry.voxel_render import surface_nets
    verts, faces = surface_nets(volume, threshold=threshold)
    if not verts or not faces:
        return {"beta": 0.0, "tensors": {}}
    verts = np.array(verts); faces = np.array(faces)
    v0, v1, v2 = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    cross = np.cross(v1 - v0, v2 - v0)
    norms = np.linalg.norm(cross, axis=1)
    total_area = np.sum(norms) / 2.0
    unit_normals = cross / (norms[:, np.newaxis] + 1e-12)
    theta = np.arccos(np.clip(unit_normals[:, 2], -1.0, 1.0))
    phi = np.arctan2(unit_normals[:, 1], unit_normals[:, 0])
    results = {}; sum_sq_psi = 0.0
    for m in range(-l, l + 1):
        y_lm = sph_harm_y(l, m, theta, phi)
        psi_lm = np.sum((norms / 2.0) * y_lm)
        results[m] = psi_lm
        sum_sq_psi += np.abs(psi_lm)**2
    beta = np.sqrt((4 * np.pi / (2 * l + 1)) * sum_sq_psi) / (total_area + 1e-12)
    return {"beta": float(beta), "tensors": results, "area": total_area}


def minkowski_synthesis_2d(psi_dict, num_points=100):
    """Reconstructs a 2D convex shape from a dictionary of IMTs {s: psi_s}."""
    theta = np.linspace(0, 2 * np.pi, num_points)
    rho = np.full_like(theta, psi_dict.get(0, 1.0))
    for s, psi in psi_dict.items():
        if s == 0: continue
        rho += 2.0 * (psi * np.exp(-1j * s * theta)).real
    rho = np.clip(rho / (2.0 * np.pi), 1e-6, None)
    dtheta = theta[1] - theta[0]
    x = np.cumsum(-np.sin(theta) * rho) * dtheta
    y = np.cumsum(np.cos(theta) * rho) * dtheta
    return np.column_stack([x, y])
