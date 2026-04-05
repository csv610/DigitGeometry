"""Basic topology operations."""

import math


def count_connected_components(grid, target_value=1, connectivity=4):
    """Counts connected components of target_value using BFS."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    count = 0

    if connectivity == 8:
        neighbors = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
    else:
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == target_value and (x, y) not in visited:
                count += 1
                queue = [(x, y)]
                visited.add((x, y))
                while queue:
                    cx, cy = queue.pop(0)
                    for dx, dy in neighbors:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if grid[ny][nx] == target_value and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
    return count


def compute_topology(grid, connectivity=4):
    """Calculates Betti numbers (b0, b1) and Euler characteristic."""
    b0 = count_connected_components(grid, target_value=1, connectivity=connectivity)

    inverted = [[1 - grid[y][x] for x in range(len(grid[0]))] for y in range(len(grid))]
    bg_components = count_connected_components(
        inverted, target_value=1, connectivity=connectivity
    )
    b1 = bg_components - 1 if b0 > 0 else 0

    return {"b0": b0, "b1": b1, "euler": b0 - b1}


def connected_components_3d(volume, target_value=1, connectivity=6):
    """3D connected component labeling."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    if connectivity == 6:
        neighbors = [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]
    else:
        neighbors = [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
            (1, 1, 0),
            (1, -1, 0),
            (-1, 1, 0),
            (-1, -1, 0),
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, 1),
            (-1, 0, -1),
            (0, 1, 1),
            (0, 1, -1),
            (0, -1, 1),
            (0, -1, -1),
            (1, 1, 1),
            (1, -1, 1),
            (-1, 1, 1),
            (-1, -1, 1),
            (1, 1, -1),
            (1, -1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
        ]

    label = [[[0] * width for _ in range(height)] for _ in range(depth)]
    current_label = 0

    def bfs(start_x, start_y, start_z):
        nonlocal current_label
        current_label += 1
        queue = [(start_x, start_y, start_z)]
        label[start_z][start_y][start_x] = current_label

        while queue:
            cx, cy, cz = queue.pop(0)

            for dx, dy, dz in neighbors:
                nx, ny, nz = cx + dx, cy + dy, cz + dz

                if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                    if volume[nz][ny][nx] == target_value and label[nz][ny][nx] == 0:
                        label[nz][ny][nx] = current_label
                        queue.append((nx, ny, nz))

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == target_value and label[z][y][x] == 0:
                    bfs(x, y, z)

    return label, current_label


def compute_surface_curvatures(grid):
    """Compute discrete surface curvatures."""
    height = len(grid)
    width = len(grid[0])
    curvatures = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            laplacian = (
                grid[y - 1][x]
                + grid[y + 1][x]
                + grid[y][x - 1]
                + grid[y][x + 1]
                - 4 * grid[y][x]
            )
            gradient_magnitude = math.sqrt(
                (grid[y][x + 1] - grid[y][x - 1]) ** 2
                + (grid[y + 1][x] - grid[y - 1][x]) ** 2
            )
            curvatures[y][x] = laplacian / (1 + gradient_magnitude)

    return curvatures
