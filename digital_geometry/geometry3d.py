"""3D geometry utilities."""

import math


def compute_surface_normals(grid, voxel_size=1.0):
    """Estimate surface normals from a depth/height grid."""
    height = len(grid)
    width = len(grid[0])

    normals = [[[0.0, 0.0, 0.0] for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            dz_dx = (grid[y][x + 1] - grid[y][x - 1]) / (2 * voxel_size)
            dz_dy = (grid[y + 1][x] - grid[y - 1][x]) / (2 * voxel_size)

            nx = -dz_dx
            ny = -dz_dy
            nz = 1.0

            length = math.sqrt(nx * nx + ny * ny + nz * nz)
            if length > 0:
                normals[y][x] = [nx / length, ny / length, nz / length]

    return normals


def compute_normals_cross_product(grid):
    """Compute normals using cross product of gradients."""
    height = len(grid)
    width = len(grid[0])

    normals = [[[0.0, 0.0, 0.0] for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            dx = grid[y][x + 1] - grid[y][x - 1]
            dy = grid[y + 1][x] - grid[y - 1][x]

            nx = -dx
            ny = -dy
            nz = 2.0

            length = math.sqrt(nx * nx + ny * ny + nz * nz)
            if length > 0:
                normals[y][x] = [nx / length, ny / length, nz / length]

    return normals


def fit_plane_least_squares(points):
    """Fit a plane to points using least squares.

    Returns (a, b, c, d) where ax + by + cz = d is the plane equation.
    """
    n = len(points)
    if n < 3:
        return (0, 0, 1, 0)

    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    sum_z = sum(p[2] for p in points)
    sum_xx = sum(p[0] ** 2 for p in points)
    sum_xy = sum(p[0] * p[1] for p in points)
    sum_xz = sum(p[0] * p[2] for p in points)
    sum_yy = sum(p[1] ** 2 for p in points)
    sum_yz = sum(p[1] * p[2] for p in points)

    mean_x = sum_x / n
    mean_y = sum_y / n
    mean_z = sum_z / n

    uxx = sum_xx - sum_x * mean_x
    uxy = sum_xy - sum_x * mean_y
    uxz = sum_xz - sum_x * mean_z
    uyy = sum_yy - sum_y * mean_y
    uyz = sum_yz - sum_y * mean_z

    a = uyz * uxy - uxz * uyy
    b = uxz * uxy - uyz * uxx
    c = uxx * uyy - uxy * uxy

    length = math.sqrt(a * a + b * b + c * c)
    if length > 0:
        a /= length
        b /= length
        c /= length

    d = a * mean_x + b * mean_y + c * mean_z

    return (a, b, c, d)


def compute_curvature_2d(grid):
    """Estimate mean curvature on a grid."""
    height = len(grid)
    width = len(grid[0])

    curvature = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            f = grid[y][x]
            fx = (grid[y][x + 1] - grid[y][x - 1]) / 2
            fy = grid[y + 1][x] - grid[y - 1][x] / 2
            fxx = grid[y][x + 1] - 2 * f + grid[y][x - 1]
            fyy = grid[y + 1][x] - 2 * f + grid[y - 1][x]
            fxy = (
                grid[y + 1][x + 1]
                - grid[y + 1][x - 1]
                - grid[y - 1][x + 1]
                + grid[y - 1][x - 1]
            ) / 4

            denom = (1 + fx * fx + fy * fy) ** 1.5
            if denom > 0:
                curvature[y][x] = (
                    abs(fxx * (1 + fy * fy) - 2 * fx * fy * fxy + fyy * (1 + fx * fx))
                    / denom
                )

    return curvature


def voxel_volume(mesh_vertices, mesh_triangles):
    """Calculate volume of a mesh using voxel method."""
    if not mesh_vertices or not mesh_triangles:
        return 0.0

    xs = [v[0] for v in mesh_vertices]
    ys = [v[1] for v in mesh_vertices]
    zs = [v[2] for v in mesh_vertices]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)

    resolution = 20
    dx = (xmax - xmin) / resolution
    dy = (ymax - ymin) / resolution
    dz = (zmax - zmin) / resolution

    volume = 0.0
    for zi in range(resolution):
        for yi in range(resolution):
            for xi in range(resolution):
                px = xmin + (xi + 0.5) * dx
                py = ymin + (yi + 0.5) * dy
                pz = zmin + (zi + 0.5) * dz

                if point_in_mesh(px, py, pz, mesh_vertices, mesh_triangles):
                    volume += dx * dy * dz

    return volume


def point_in_mesh(px, py, pz, vertices, triangles):
    """Check if point is inside mesh using ray casting."""
    from digital_geometry.curves import point_in_polygon

    intersections = 0
    for tri in triangles:
        if len(tri) < 3:
            continue
        v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]

        if min(v0[2], v1[2], v2[2]) <= pz <= max(v0[2], v1[2], v2[2]):
            if pz < max(v0[2], v1[2], v2[2]):
                polygon = [(v0[0], v0[1]), (v1[0], v1[1]), (v2[0], v2[1])]
                if point_in_polygon((px, py), polygon):
                    intersections += 1

    return intersections % 2 == 1
