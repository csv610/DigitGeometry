"""Core voxel utilities."""

import math

NEIGHBOR_6 = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

NEIGHBOR_18 = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
    (-1, -1, 0),
    (-1, 1, 0),
    (1, -1, 0),
    (1, 1, 0),
    (-1, 0, -1),
    (-1, 0, 1),
    (1, 0, -1),
    (1, 0, 1),
    (0, -1, -1),
    (0, -1, 1),
    (0, 1, -1),
    (0, 1, 1),
]

NEIGHBOR_26 = [
    (-1, -1, -1),
    (-1, -1, 0),
    (-1, -1, 1),
    (-1, 0, -1),
    (-1, 0, 0),
    (-1, 0, 1),
    (-1, 1, -1),
    (-1, 1, 0),
    (-1, 1, 1),
    (0, -1, -1),
    (0, -1, 0),
    (0, -1, 1),
    (0, 0, -1),
    (0, 0, 1),
    (0, 1, -1),
    (0, 1, 0),
    (0, 1, 1),
    (1, -1, -1),
    (1, -1, 0),
    (1, -1, 1),
    (1, 0, -1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, -1),
    (1, 1, 0),
    (1, 1, 1),
]


def get_neighbors_6(x, y, z):
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in NEIGHBOR_6]


def get_neighbors_18(x, y, z):
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in NEIGHBOR_18]


def get_neighbors_26(x, y, z):
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in NEIGHBOR_26]


def voxel_euler_number(volume):
    """Compute Euler number (topological invariant)."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    v = e = f = 0

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1:
                    v += 1
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            if volume[nz][ny][nx] == 1:
                                if dx > 0:
                                    e += 1
                                if dy > 0:
                                    e += 1
                                if dz > 0:
                                    e += 1
                    for dx, dy in [(1, 0), (0, 1), (1, 1)]:
                        nx1, ny1 = x + dx, y + dy
                        if 0 <= nx1 < width and 0 <= ny1 < height:
                            if volume[z][ny1][nx1] == 1:
                                f += 1

    return v - e / 2 + f / 4


def voxel_connectivity_count(volume):
    """Count connected components."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    visited = [[[False] * width for _ in range(height)] for _ in range(depth)]
    count = 0

    def dfs(x, y, z):
        stack = [(x, y, z)]
        while stack:
            cx, cy, cz = stack.pop()
            if visited[cz][cy][cx]:
                continue
            visited[cz][cy][cx] = True
            for dx, dy, dz in NEIGHBOR_6:
                nx, ny, nz = cx + dx, cy + dy, cz + dz
                if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                    if volume[nz][ny][nx] == 1 and not visited[nz][ny][nx]:
                        stack.append((nx, ny, nz))

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1 and not visited[z][y][x]:
                    dfs(x, y, z)
                    count += 1

    return count


def voxel_coloring(volume):
    """Color voxels to detect separation."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    colors = [[[-1] * width for _ in range(height)] for _ in range(depth)]
    current_color = 0

    def flood_fill(start_x, start_y, start_z, color):
        stack = [(start_x, start_y, start_z)]
        while stack:
            x, y, z = stack.pop()
            if not (0 <= x < width and 0 <= y < height and 0 <= z < depth):
                continue
            if volume[z][y][x] == 0 or colors[z][y][x] != -1:
                continue
            colors[z][y][x] = color
            for dx, dy, dz in NEIGHBOR_6:
                stack.append((x + dx, y + dy, z + dz))

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1 and colors[z][y][x] == -1:
                    flood_fill(x, y, z, current_color)
                    current_color += 1

    return colors, current_color


def voxel_separated(volume):
    """Check if voxel volume has separate components."""
    colors, count = voxel_coloring(volume)
    return count > 1
