"""Thinning and skeleton algorithms."""

import math


def zhang_suen_thinning(grid):
    """Zhang-Suen thinning algorithm for binary grid."""
    height = len(grid)
    width = len(grid[0])
    thinned = [row[:] for row in grid]

    def neighbors_8(x, y):
        n = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    n.append(thinned[ny][nx])
        return n

    def step(step_num):
        to_del = []
        for y in range(height):
            for x in range(width):
                if thinned[y][x] != 1:
                    continue
                n = neighbors_8(x, y)
                p = n.count(1)
                if p < 2 or p > 6:
                    continue
                transitions = 0
                for i in range(7):
                    if n[i] == 0 and n[i + 1] == 1:
                        transitions += 1
                if n[7] == 0 and n[0] == 1:
                    transitions += 1

                if step_num == 1:
                    cond1 = transitions == 1
                    cond2 = n[0] * n[2] * n[4] == 0
                    cond3 = n[2] * n[4] * n[6] == 0
                    if cond1 and cond2 and cond3:
                        to_del.append((x, y))
                else:
                    cond1 = transitions == 1
                    cond2 = n[0] * n[2] * n[6] == 0
                    cond3 = n[0] * n[4] * n[6] == 0
                    if cond1 and cond2 and cond3:
                        to_del.append((x, y))

        for x, y in to_del:
            thinned[y][x] = 0
        return len(to_del) > 0

    while step(1) or step(2):
        pass
    return thinned


def thinning_3d(volume):
    """3D thinning algorithm."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])
    result = [[[v for v in row] for row in layer] for layer in volume]

    neighbors = [
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

    while True:
        to_remove = []
        for z in range(1, depth - 1):
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if result[z][y][x] != 1:
                        continue

                    n_count = 0
                    for dx, dy, dz in neighbors:
                        if result[z + dz][y + dy][x + dx] == 1:
                            n_count += 1

                    if n_count >= 2 and n_count <= 26:
                        border_count = 0
                        for dx, dy, dz in [
                            (-1, 0, 0),
                            (1, 0, 0),
                            (0, -1, 0),
                            (0, 1, 0),
                            (0, 0, -1),
                            (0, 0, 1),
                        ]:
                            if (
                                0 <= z + dz < depth
                                and 0 <= y + dy < height
                                and 0 <= x + dx < width
                            ):
                                if result[z + dz][y + dy][x + dx] == 0:
                                    border_count += 1
                        if border_count > 0:
                            to_remove.append((x, y, z))

        if not to_remove:
            break

        for x, y, z in to_remove:
            result[z][y][x] = 0

    return result


def morphological_skeleton(grid):
    """Morphological skeletonization."""
    from digital_geometry.morphology import erode, morph_boundary

    height = len(grid)
    width = len(grid[0])
    skeleton = [[0] * width for _ in range(height)]
    temp = [row[:] for row in grid]
    se = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    while True:
        eroded = erode(temp, se)
        if sum(sum(row) for row in eroded) == 0:
            break
        boundary = morph_boundary(temp, se)
        for y in range(height):
            for x in range(width):
                if boundary[y][x] == 1:
                    skeleton[y][x] = 1
        temp = eroded

    return skeleton


def skeleton_3d_medial(volume):
    """Extract 3D skeleton using medial axis approach."""
    from digital_geometry.voxel import voxel_sdf_3d

    sdf = voxel_sdf_3d(volume)
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    from digital_geometry.voxel_core import NEIGHBOR_6

    skeleton = [[[0] * width for _ in range(height)] for _ in range(depth)]

    for z in range(1, depth - 1):
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if volume[z][y][x] == 1:
                    neighbors = []
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            neighbors.append(sdf[nz][ny][nx])

                    center_dist = sdf[z][y][x]
                    is_min = all(center_dist <= n for n in neighbors)

                    if is_min:
                        skeleton[z][y][x] = 1

    return skeleton


def medial_axis_transform(grid):
    """Medial axis (skeleton) transform."""
    from digital_geometry.morphology import dilate, erode, morph_boundary

    height = len(grid)
    width = len(grid[0])
    se = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    result = [[0] * width for _ in range(height)]
    temp = [row[:] for row in grid]

    while True:
        eroded = erode(temp, se)
        if sum(sum(row) for row in eroded) == 0:
            break
        boundary = morph_boundary(temp, se)
        for y in range(height):
            for x in range(width):
                if boundary[y][x] == 1:
                    result[y][x] = grid[y][x]
        temp = eroded

    return result


def medial_axis_transform_3d(volume):
    """3D medial axis transform."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    from digital_geometry.voxel_core import NEIGHBOR_6

    result = [[[0] * width for _ in range(height)] for _ in range(depth)]
    temp = [[row[:] for row in layer] for layer in volume]

    while True:
        eroded = voxel_erode_iteration(temp)
        
        # Identify current boundary
        boundary = []
        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if temp[z][y][x] == 1:
                        is_boundary = False
                        for dx, dy, dz in NEIGHBOR_6:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            if not (0 <= nx < width and 0 <= ny < height and 0 <= nz < depth) or temp[nz][ny][nx] == 0:
                                is_boundary = True
                                break
                        if is_boundary:
                            boundary.append((x, y, z))

        if sum(sum(sum(p) for p in row) for row in eroded) == 0:
            # All current voxels are medial axis if they can't be eroded further
            for z in range(depth):
                for y in range(height):
                    for x in range(width):
                        if temp[z][y][x] == 1:
                            result[z][y][x] = volume[z][y][x]
            break
            
        for x, y, z in boundary:
            result[z][y][x] = volume[z][y][x]
        temp = eroded

    return result


def voxel_erode_iteration(volume):
    """Single iteration of 3D erosion."""
    from digital_geometry.voxel_core import NEIGHBOR_6

    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    result = [[[v for v in row] for row in layer] for layer in volume]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 1:
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if not (
                            0 <= nx < width and 0 <= ny < height and 0 <= nz < depth
                        ):
                            result[z][y][x] = 0
                            break
                        if volume[nz][ny][nx] == 0:
                            result[z][y][x] = 0
                            break

    return result
