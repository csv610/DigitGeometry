"""Voxel rendering and ray tracing - NumPy Centric Version."""

import numpy as np
from scipy.ndimage import convolve, uniform_filter
from digital_geometry.voxel_core import NEIGHBOR_6


def ray_voxel_intersection(ray_origin, ray_direction, voxel_bounds):
    """Ray-voxel intersection using AABB test."""
    ox, oy, oz = np.asanyarray(ray_origin)
    dx, dy, dz = np.asanyarray(ray_direction)

    x0, y0, z0 = voxel_bounds[0]
    x1, y1, z1 = voxel_bounds[1]

    with np.errstate(divide='ignore', invalid='ignore'):
        txmin = (x0 - ox) / dx
        txmax = (x1 - ox) / dx
        tymin = (y0 - oy) / dy
        tymax = (y1 - oy) / dy
        tzmin = (z0 - oz) / dz
        tzmax = (z1 - oz) / dz

    tmin_x, tmax_x = min(txmin, txmax), max(txmin, txmax)
    tmin_y, tmax_y = min(tymin, tymax), max(tymin, tymax)
    tmin_z, tmax_z = min(tzmin, tzmax), max(tzmin, tzmax)

    t_enter = max(tmin_x, tmin_y, tmin_z)
    t_exit = min(tmax_x, tmax_y, tmax_z)

    if t_enter > t_exit or t_exit < 0:
        return None

    t = t_enter if t_enter > 0 else t_exit
    return ox + dx * t, oy + dy * t, oz + dz * t


def ray_cast_volume(ray_origin, ray_direction, volume: np.ndarray, step=1.0):
    """Cast ray through voxel volume."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    depth, height, width = volume.shape

    intersections = []
    ox, oy, oz = ray_origin
    dx, dy, dz = ray_direction

    length = np.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / length, dy / length, dz / length

    max_dist = np.sqrt(width**2 + height**2 + depth**2)
    t = 0.0

    while t < max_dist:
        x, y, z = int(ox + dx * t), int(oy + dy * t), int(oz + dz * t)

        if 0 <= x < width and 0 <= y < height and 0 <= z < depth:
            if volume[z, y, x] == 1:
                intersections.append((x, y, z, t))
        t += step

    return intersections


def volume_raymarch(volume: np.ndarray, ray_origin, ray_direction, threshold=0.5):
    """Raymarch through voxel volume."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    depth, height, width = volume.shape

    ox, oy, oz = ray_origin
    dx, dy, dz = ray_direction

    length = np.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / length, dy / length, dz / length

    t = 0.0
    max_t = np.sqrt(width**2 + height**2 + depth**2)
    step = 0.5

    while t < max_t:
        x, y, z = int(ox + dx * t), int(oy + dy * t), int(oz + dz * t)

        if 0 <= x < width and 0 <= y < height and 0 <= z < depth:
            if volume[z, y, x] >= threshold:
                return (x, y, z), t
        t += step

    return None, -1


def volume_raymarch_with_normal(volume: np.ndarray, ray_origin, ray_direction, threshold=0.5):
    """Raymarch with normal estimation."""
    hit, t = volume_raymarch(volume, ray_origin, ray_direction, threshold)

    if hit is None:
        return None, None

    x, y, z = hit
    depth, height, width = volume.shape
    
    # Boundary-safe normal estimation
    def get_val(vx, vy, vz):
        if 0 <= vx < width and 0 <= vy < height and 0 <= vz < depth:
            return float(volume[vz, vy, vx])
        return 0.0

    # Central difference-like approximation
    nx = get_val(x+1, y, z) - get_val(x-1, y, z)
    ny = get_val(x, y+1, z) - get_val(x, y-1, z)
    nz = get_val(x, y, z+1) - get_val(x, y, z-1)

    length = np.sqrt(nx**2 + ny**2 + nz**2)
    if length > 0:
        normal = np.array([nx, ny, nz]) / length
    else:
        normal = np.array([0.0, 0.0, 0.0])

    return hit, normal


def voxel_carving(mesh_vertices, mesh_triangles, silhouettes, resolution=32):
    """Carve voxels using silhouette images."""
    if not silhouettes or len(mesh_vertices) == 0:
        return None

    volume = np.ones((resolution, resolution, resolution), dtype=np.uint8)

    vertices = np.asanyarray(mesh_vertices)
    xmin, ymin, zmin = vertices.min(axis=0)
    xmax, ymax, zmax = vertices.max(axis=0)

    max_range = max(xmax - xmin, ymax - ymin, zmax - zmin)
    if max_range == 0: max_range = 1

    # This is still a slow triple loop, but at least using NumPy
    for silhouette in silhouettes:
        # Silhouette is expected to be a 2D NumPy array
        for z in range(resolution):
            for y in range(resolution):
                for x in range(resolution):
                    px = xmin + (x + 0.5) / resolution * max_range
                    py = ymin + (y + 0.5) / resolution * max_range
                    pz = zmin + (z + 0.5) / resolution * max_range

                    if not point_in_mesh_carve(px, py, pz, vertices, mesh_triangles):
                        volume[z, y, x] = 0

    return volume


def point_in_mesh_carve(px, py, pz, vertices, triangles):
    """Check if point is inside mesh using ray casting (approximate)."""
    intersections = 0
    p = np.array([px, py, pz])
    for tri in triangles:
        if len(tri) < 3: continue
        v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]

        if min(v0[2], v1[2], v2[2]) <= pz <= max(v0[2], v1[2], v2[2]):
            if point_in_triangle_carve(p, v0, v1, v2):
                intersections += 1
    return intersections % 2 == 1


def point_in_triangle_carve(p, v0, v1, v2):
    """Check if point is inside triangle."""
    e0, e1 = v1 - v0, v2 - v0
    rel_p = p - v0

    d00 = np.dot(e0, e0)
    d01 = np.dot(e0, e1)
    d11 = np.dot(e1, e1)
    d20 = np.dot(rel_p, e0)
    d21 = np.dot(rel_p, e1)

    denom = d00 * d11 - d01 * d01
    if abs(denom) < 1e-10: return False

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return u >= 0 and v >= 0 and w >= 0


def surface_nets(volume: np.ndarray, threshold=0.5, spacing=(1.0, 1.0, 1.0)):
    """Extract mesh using Surface Nets with anisotropic spacing."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    depth, height, width = volume.shape
    dz, dy, dx = spacing

    vertices = []
    faces = []
    vertex_indices = {}

    # Faster iteration over potential dual cells
    for z in range(depth - 1):
        for y in range(height - 1):
            for x in range(width - 1):
                sub = volume[z:z+2, y:y+2, x:x+2]
                inside = np.any(sub >= threshold)
                outside = np.any(sub < threshold)
                if inside and outside:
                    # Physical center of the cell
                    vertices.append(((x + 0.5) * dx, (y + 0.5) * dy, (z + 0.5) * dz))
                    vertex_indices[(x, y, z)] = len(vertices) - 1

    # Extract faces (simplification of original logic)
    for z in range(1, depth - 1):
        for y in range(1, height - 1):
            for x in range(width - 1):
                v1 = volume[z, y, x] >= threshold
                v2 = volume[z, y, x + 1] >= threshold
                if v1 != v2:
                    cells = [(x, y-1, z-1), (x, y, z-1), (x, y, z), (x, y-1, z)]
                    if all(c in vertex_indices for c in cells):
                        idx = [vertex_indices[c] for c in cells]
                        if v1:
                            faces.extend([(idx[0], idx[1], idx[2]), (idx[0], idx[2], idx[3])])
                        else:
                            faces.extend([(idx[0], idx[3], idx[2]), (idx[0], idx[2], idx[1])])

    # Similar blocks for Y and Z axes would follow here (omitted for brevity, keeping original logic structure)
    # The original code had them, so I should keep them for correctness.
    for z in range(1, depth - 1):
        for y in range(height - 1):
            for x in range(1, width - 1):
                v1 = volume[z, y, x] >= threshold
                v2 = volume[z, y + 1, x] >= threshold
                if v1 != v2:
                    cells = [(x-1, y, z-1), (x, y, z-1), (x, y, z), (x-1, y, z)]
                    if all(c in vertex_indices for c in cells):
                        idx = [vertex_indices[c] for c in cells]
                        if not v1:
                            faces.extend([(idx[0], idx[1], idx[2]), (idx[0], idx[2], idx[3])])
                        else:
                            faces.extend([(idx[0], idx[3], idx[2]), (idx[0], idx[2], idx[1])])

    for z in range(depth - 1):
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                v1 = volume[z, y, x] >= threshold
                v2 = volume[z + 1, y, x] >= threshold
                if v1 != v2:
                    cells = [(x-1, y-1, z), (x, y-1, z), (x, y, z), (x-1, y, z)]
                    if all(c in vertex_indices for c in cells):
                        idx = [vertex_indices[c] for c in cells]
                        if v1:
                            faces.extend([(idx[0], idx[1], idx[2]), (idx[0], idx[2], idx[3])])
                        else:
                            faces.extend([(idx[0], idx[3], idx[2]), (idx[0], idx[2], idx[1])])

    return vertices, faces


def dual_contouring(volume: np.ndarray, threshold=0.5):
    """Dual contouring for quality isosurface."""
    return surface_nets(volume, threshold)


def voxel_gradient_normals(volume: np.ndarray):
    """Compute gradient-based normals using NumPy gradient."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    dz, dy, dx = np.gradient(volume.astype(float))
    
    # dz, dy, dx are the same shape as volume
    normals = np.stack([-dx, -dy, -dz], axis=-1)
    
    length = np.linalg.norm(normals, axis=-1, keepdims=True)
    length[length == 0] = 1.0
    normals /= length
    
    return normals


def smooth_isosurface(volume: np.ndarray, iterations=3):
    """Smooth isosurface using uniform filter."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    result = volume.astype(float)
    for _ in range(iterations):
        avg = uniform_filter(result, size=3)
        result = result * 0.5 + avg * 0.5
        
    return result


def fast_winding_number(volume: np.ndarray, query_points, theta=0.5):
    """Approximates the winding number using NumPy vectorization."""
    if not isinstance(volume, np.ndarray):
        volume = np.asanyarray(volume)
        
    depth, height, width = volume.shape
    
    # Use shift to find boundary facets
    facets = []
    directions = [
        (0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)
    ]
    
    vol_bin = (volume > 0)
    for dz, dy, dx in directions:
        # shifted = volume shifted by -dz, -dy, -dx
        shifted = np.zeros_like(vol_bin)
        tz_s, tz_e = max(0, dz), min(depth, depth + dz)
        sz_s, sz_e = max(0, -dz), min(depth, depth - dz)
        ty_s, ty_e = max(0, dy), min(height, height + dy)
        sy_s, sy_e = max(0, -dy), min(height, height - dy)
        tx_s, tx_e = max(0, dx), min(width, width + dx)
        sx_s, sx_e = max(0, -dx), min(width, width - dx)
        
        if tz_s < tz_e and ty_s < ty_e and tx_s < tx_e:
            shifted[tz_s:tz_e, ty_s:ty_e, tx_s:tx_e] = vol_bin[sz_s:sz_e, sy_s:sy_e, sx_s:sx_e]
            
        boundary = vol_bin & (~shifted)
        bz, by, bx = np.where(boundary)
        for i in range(len(bx)):
            center = (bx[i] + dx*0.5, by[i] + dy*0.5, bz[i] + dz*0.5)
            # Normal should point from foreground to background
            # If shifted[z,y,x] = vol[z-dz, y-dy, x-dx], 
            # then vol[z,y,x]=1 and shifted[z,y,x]=0 means vol[z-dz,...]=0
            # So the normal is (-dx, -dy, -dz)
            facets.append((np.array(center), np.array([-dx, -dy, -dz])))
            
    query_points = np.asanyarray(query_points)
    if not facets:
        return np.zeros(len(query_points))
        
    facet_centers = np.array([f[0] for f in facets])
    facet_normals = np.array([f[1] for f in facets])
    
    results = []
    for qp in query_points:
        r_vec = facet_centers - qp
        dist_sq = np.sum(r_vec**2, axis=1)
        dist = np.sqrt(dist_sq)
        dot = np.sum(r_vec * facet_normals, axis=1)
        w = np.sum(dot / (4.0 * np.pi * dist**3 + 1e-18))
        results.append(float(w))
        
    return np.array(results)
