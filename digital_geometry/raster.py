"""Rasterization algorithms."""

import math


SE_SQUARE_3X3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
SE_CROSS_3X3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]


def bresenham_line(x0, y0, x1, y1):
    """Bresenham's Line Algorithm."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points


def midpoint_circle(x0, y0, radius):
    """Bresenham's Circle Algorithm (Midpoint Circle)."""
    points = set()
    x = radius
    y = 0
    err = 0

    while x >= y:
        points.add((x0 + x, y0 + y))
        points.add((x0 + y, y0 + x))
        points.add((x0 - y, y0 + x))
        points.add((x0 - x, y0 + y))
        points.add((x0 - x, y0 - y))
        points.add((x0 - y, y0 - x))
        points.add((x0 + y, y0 - x))
        points.add((x0 + x, y0 - y))

        if err <= 0:
            y += 1
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

    return list(points)


def wu_line(x0, y0, x1, y1):
    """Wu's Anti-Aliased Line Algorithm."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    if dx == 0 and dy == 0:
        return [(x0, y0, 1.0)]

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx >= dy:
        x, y = x0, y0
        x_end = x1
        t = dy / dx if dx != 0 else 0

        while x != x_end:
            x += sx
            t += dy / dx if dx != 0 else 0
            intensity = 1 - abs(t - round(t))
            points.append((x, y, intensity))
            if abs(t - round(t)) < 1e-9:
                y += sy
                t -= sy
    else:
        x, y = x0, y0
        y_end = y1
        t = dx / dy if dy != 0 else 0

        while y != y_end:
            y += sy
            t += dx / dy if dy != 0 else 0
            intensity = 1 - abs(t - round(t))
            points.append((x, y, intensity))
            if abs(t - round(t)) < 1e-9:
                x += sx
                t -= sx

    points.insert(0, (x0, y0, 1.0))
    return points


def supercover_line_2d(x0, y0, x1, y1):
    """Supercover line algorithm for 2D grids."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    x, y = x0, y0
    points.append((x, y))

    if dx == 0:
        for _ in range(dy):
            y += sy
            points.append((x, y))
        return points

    if dy == 0:
        for _ in range(dx):
            x += sx
            points.append((x, y))
        return points

    error = dx - dy

    while x != x1 or y != y1:
        e2 = 2 * error
        if e2 > -dy:
            error -= dy
            x += sx
            points.append((x, y))
        if e2 < dx:
            error += dx
            y += sy
            points.append((x, y))

    return points


def supercover_line_3d(x0, y0, z0, x1, y1, z1):
    """Supercover line algorithm for 3D voxel grids."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    sz = 1 if z0 < z1 else -1

    x, y, z = x0, y0, z0
    points.append((x, y, z))

    if dx == 0 and dy == 0:
        for _ in range(dz):
            z += sz
            points.append((x, y, z))
        return points

    if dx == 0 and dz == 0:
        for _ in range(dy):
            y += sy
            points.append((x, y, z))
        return points

    if dy == 0 and dz == 0:
        for _ in range(dx):
            x += sx
            points.append((x, y, z))
        return points

    err_xy = dx - dy
    err_xz = dx - dz
    err_yz = dy - dz

    while x != x1 or y != y1 or z != z1:
        e2_xy = 2 * err_xy
        e2_xz = 2 * err_xz
        e2_yz = 2 * err_yz

        if e2_xy > -dy and e2_xz > -dz:
            err_xy -= dy
            err_xz -= dz
            x += sx
            points.append((x, y, z))
        if e2_xy < dx and e2_yz < dz:
            err_xy += dx
            err_yz -= dz
            y += sy
            points.append((x, y, z))
        if e2_xz < dx and e2_yz < dy:
            err_xz += dx
            err_yz += dy
            z += sz
            points.append((x, y, z))

    return points


def scanline_polygon_fill(polygon, width, height, fill_value=1):
    """Scanline polygon fill algorithm."""
    if len(polygon) < 3:
        return [[0] * width for _ in range(height)]

    grid = [[0] * width for _ in range(height)]
    min_y = min(p[1] for p in polygon)
    max_y = max(p[1] for p in polygon)

    for y in range(max(min_y, 0), min(max_y, height)):
        intersections = []
        n = len(polygon)

        for i in range(n):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % n]

            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                if p2[1] != p1[1]:
                    x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    intersections.append(x)

        intersections.sort()

        for i in range(0, len(intersections) - 1, 2):
            x_start = max(int(math.ceil(intersections[i])), 0)
            x_end = min(int(math.floor(intersections[i + 1])), width - 1)

            for x in range(x_start, x_end + 1):
                grid[y][x] = fill_value

    return grid
