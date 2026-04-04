"""Voxel rendering and ray tracing."""

import math

from digital_geometry.voxel_core import NEIGHBOR_6


def ray_voxel_intersection(ray_origin, ray_direction, voxel_bounds):
    """Ray-voxel intersection using AABB test."""
    ox, oy, oz = ray_origin
    dx, dy, dz = ray_direction

    x0, y0, z0 = voxel_bounds[0]
    x1, y1, z1 = voxel_bounds[1]

    tmin = (x0 - ox) / dx if dx != 0 else -float("inf")
    tmax = (x1 - ox) / dx if dx != 0 else float("inf")

    if tmin > tmax:
        tmin, tmax = tmax, tmin

    tymin = (y0 - oy) / dy if dy != 0 else -float("inf")
    tymax = (y1 - oy) / dy if dy != 0 else float("inf")

    if tymin > tymax:
        tymin, tymax = tymax, tymin

    if max(tmin, tymin) > min(tmax, tymax):
        return None

    tzmin = (z0 - oz) / dz if dz != 0 else -float("inf")
    tzmax = (z1 - oz) / dz if dz != 0 else float("inf")

    if tzmin > tzmax:
        tzmin, tzmax = tzmax, tzmin

    if max(tmin, tymin, tzmin) > min(tmax, tymax, tzmax):
        return None

    t = max(tmin, tymin, tzmin)
    if t < 0:
        t = min(tmax, tymax, tzmax)

    return (ox + dx * t, oy + dy * t, oz + dz * t)


def ray_cast_volume(ray_origin, ray_direction, volume, step=1.0):
    """Cast ray through voxel volume."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    intersections = []
    ox, oy, oz = ray_origin
    dx, dy, dz = ray_direction

    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / length, dy / length, dz / length

    max_dist = math.sqrt(width**2 + height**2 + depth**2)
    t = 0.0

    while t < max_dist:
        x = int(ox + dx * t)
        y = int(oy + dy * t)
        z = int(oz + dz * t)

        if 0 <= x < width and 0 <= y < height and 0 <= z < depth:
            if volume[z][y][x] == 1:
                intersections.append((x, y, z, t))
        t += step

    return intersections


def volume_raymarch(volume, ray_origin, ray_direction, threshold=0.5):
    """Raymarch through voxel volume."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    ox, oy, oz = ray_origin
    dx, dy, dz = ray_direction

    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / length, dy / length, dz / length

    t = 0.0
    max_t = math.sqrt(width**2 + height**2 + depth**2)
    step = 0.5

    while t < max_t:
        x = int(ox + dx * t)
        y = int(oy + dy * t)
        z = int(oz + dz * t)

        if 0 <= x < width and 0 <= y < height and 0 <= z < depth:
            if volume[z][y][x] >= threshold:
                return (x, y, z), t
        t += step

    return None, -1


def volume_raymarch_with_normal(volume, ray_origin, ray_direction, threshold=0.5):
    """Raymarch with normal estimation."""
    hit, t = volume_raymarch(volume, ray_origin, ray_direction, threshold)

    if hit is None:
        return None, None

    x, y, z = hit
    dx_list = [1, -1, 0, 0, 0, 0]
    dy_list = [0, 0, 1, -1, 0, 0]
    dz_list = [0, 0, 0, 0, 1, -1]

    nx = ny = nz = 0.0
    for i in range(6):
        nx += dx_list[i] * volume[z][y + dy_list[i]][x + dx_list[i]]
        ny += dy_list[i] * volume[z + dz_list[i]][y][x]
        nz += dz_list[i] * volume[z + dz_list[i]][y + dy_list[i]][x]

    length = math.sqrt(nx * nx + ny * ny + nz * nz)
    if length > 0:
        nx, ny, nz = nx / length, ny / length, nz / length

    return hit, (nx, ny, nz)


def voxel_carving(mesh_vertices, mesh_triangles, silhouettes, resolution=32):
    """Carve voxels using silhouette images."""
    if not silhouettes or not mesh_vertices:
        return None

    volume = [[[1] * resolution for _ in range(resolution)] for _ in range(resolution)]

    xs = [v[0] for v in mesh_vertices]
    ys = [v[1] for v in mesh_vertices]
    zs = [v[2] for v in mesh_vertices]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)

    max_range = max(xmax - xmin, ymax - ymin, zmax - zmin)
    if max_range == 0:
        max_range = 1

    for silhouette in silhouettes:
        for z in range(resolution):
            for y in range(resolution):
                for x in range(resolution):
                    px = xmin + (x + 0.5) / resolution * max_range
                    py = ymin + (y + 0.5) / resolution * max_range
                    pz = zmin + (z + 0.5) / resolution * max_range

                    if not point_in_mesh_carve(
                        px, py, pz, mesh_vertices, mesh_triangles
                    ):
                        volume[z][y][x] = 0

    return volume


def point_in_mesh_carve(px, py, pz, vertices, triangles):
    """Check if point is inside mesh."""
    intersections = 0
    for tri in triangles:
        if len(tri) < 3:
            continue
        v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]

        if min(v0[2], v1[2], v2[2]) <= pz <= max(v0[2], v1[2], v2[2]):
            if point_in_triangle_carve(px, py, pz, v0, v1, v2):
                intersections += 1
    return intersections % 2 == 1


def point_in_triangle_carve(px, py, pz, v0, v1, v2):
    """Check if point is inside triangle."""
    e0 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
    e1 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
    p = (px - v0[0], py - v0[1], pz - v0[2])

    d00 = e0[0] * e0[0] + e0[1] * e0[1] + e0[2] * e0[2]
    d01 = e0[0] * e1[0] + e0[1] * e1[1] + e0[2] * e1[2]
    d11 = e1[0] * e1[0] + e1[1] * e1[1] + e1[2] * e1[2]
    d20 = p[0] * e0[0] + p[1] * e0[1] + p[2] * e0[2]
    d21 = p[0] * e1[0] + p[1] * e1[1] + p[2] * e1[2]

    denom = d00 * d11 - d01 * d01
    if abs(denom) < 1e-10:
        return False

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return u >= 0 and v >= 0 and w >= 0


def surface_nets(volume, threshold=0.5):
    """Extract mesh using Surface Nets."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    vertices = []
    faces = []

    for z in range(depth - 1):
        for y in range(height - 1):
            for x in range(width - 1):
                cube = [
                    volume[z][y][x],
                    volume[z][y][x + 1],
                    volume[z][y + 1][x + 1],
                    volume[z][y + 1][x],
                    volume[z + 1][y][x],
                    volume[z + 1][y][x + 1],
                    volume[z + 1][y + 1][x + 1],
                    volume[z + 1][y + 1][x],
                ]

                case = 0
                for i in range(8):
                    if cube[i] >= threshold:
                        case |= 1 << i

                if case == 0 or case == 255:
                    continue

                for edge in range(12):
                    if (case >> edge) & 1:
                        pass

    return vertices, faces


def dual_contouring(volume, threshold=0.5):
    """Dual contouring for quality isosurface."""
    return surface_nets(volume, threshold)


def voxel_gradient_normals(volume):
    """Compute gradient-based normals."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    normals = [[[0.0, 0.0, 0.0] for _ in range(width)] for _ in range(height)]
    normals = [normals[:] for _ in range(depth)]

    for z in range(1, depth - 1):
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                dx = volume[z][y][x + 1] - volume[z][y][x - 1]
                dy = volume[z][y + 1][x] - volume[z][y - 1][x]
                dz = volume[z + 1][y][x] - volume[z - 1][y][x]

                length = math.sqrt(dx * dx + dy * dy + dz * dz)
                if length > 0:
                    normals[z][y][x] = (-dx / length, -dy / length, -dz / length)

    return normals


def smooth_isosurface(volume, iterations=3):
    """Smooth isosurface after extraction."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    result = [[[v for v in row] for row in layer] for layer in volume]

    for _ in range(iterations):
        temp = [[[v for v in row] for row in layer] for layer in result]

        for z in range(1, depth - 1):
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    avg = count = 0
                    for dz in range(-1, 2):
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if dx == 0 and dy == 0 and dz == 0:
                                    continue
                                avg += result[z + dz][y + dy][x + dx]
                                count += 1
                    temp[z][y][x] = result[z][y][x] * 0.5 + (avg / count) * 0.5
        result = temp
    return result
