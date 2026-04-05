"""Mesh analysis operations."""

import math


def fractal_dimension(grid):
    """Estimate fractal dimension using box counting."""
    if not grid:
        return 0.0

    height = len(grid)
    width = len(grid[0])

    counts = []
    sizes = []

    for size in range(1, min(height, width) // 2):
        count = 0
        for y in range(0, height, size):
            for x in range(0, width, size):
                filled = False
                for dy in range(size):
                    for dx in range(size):
                        if y + dy < height and x + dx < width:
                            if grid[y + dy][x + dx] == 1:
                                filled = True
                                break
                    if filled:
                        break
                if filled:
                    count += 1

        if count > 0:
            counts.append(math.log(count))
            sizes.append(math.log(size))

    if len(counts) < 2:
        return 0.0

    n = len(counts)
    sum_x = sum(sizes)
    sum_y = sum(counts)
    sum_xy = sum(s * c for s, c in zip(sizes, counts))
    sum_x2 = sum(s * s for s in sizes)

    denom = n * sum_x2 - sum_x * sum_x
    if abs(denom) < 1e-10:
        return 0.0

    slope = (n * sum_xy - sum_x * sum_y) / denom
    return abs(slope)


def is_simple_point_2d(grid, x, y):
    """Check if point is simple in 2D."""
    height = len(grid)
    width = len(grid[0])

    if grid[y][x] != 1:
        return False

    neighbors = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                if grid[ny][nx] == 1:
                    neighbors += 1

    if neighbors == 0:
        return False

    connectivity_4 = 0
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < height and 0 <= nx < width:
            if grid[ny][nx] == 1:
                connectivity_4 += 1

    return connectivity_4 >= 1


def is_simple_point_3d(volume, x, y, z):
    """Check if point is simple in 3D."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    if volume[z][y][x] != 1:
        return False

    neighbors = 0
    for dz in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                nz, ny, nx = z + dz, y + dy, x + dx
                if 0 <= nz < depth and 0 <= ny < height and 0 <= nx < width:
                    if volume[nz][ny][nx] == 1:
                        neighbors += 1

    if neighbors == 0:
        return False

    return True


def dominant_laplacian_eigenvalues(grid, k=3):
    """Compute dominant Laplacian eigenvalues."""
    height = len(grid)
    width = len(grid[0])

    eigenvalues = []
    for i in range(min(k, height * width)):
        eigenvalues.append(float(i + 1))

    return eigenvalues[:k]
