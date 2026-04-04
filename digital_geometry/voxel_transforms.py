"""Voxel transforms and conversions."""

from digital_geometry.voxel_core import NEIGHBOR_6, NEIGHBOR_18, NEIGHBOR_26


def voxelize_triangle_mesh(vertices, triangles, resolution=32):
    """Voxelize a triangle mesh."""
    if not vertices or not triangles:
        return [
            [[0] * resolution for _ in range(resolution)] for _ in range(resolution)
        ]

    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)

    max_range = max(xmax - xmin, ymax - ymin, zmax - zmin)
    if max_range == 0:
        max_range = 1

    volume = [[[0] * resolution for _ in range(resolution)] for _ in range(resolution)]

    for tri in triangles:
        if len(tri) < 3:
            continue
        v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]

        min_x = int(((min(v0[0], v1[0], v2[0]) - xmin) / max_range) * resolution)
        max_x = int(((max(v0[0], v1[0], v2[0]) - xmin) / max_range) * resolution)
        min_y = int(((min(v0[1], v1[1], v2[1]) - ymin) / max_range) * resolution)
        max_y = int(((max(v0[1], v1[1], v2[1]) - ymin) / max_range) * resolution)
        min_z = int(((min(v0[2], v1[2], v2[2]) - zmin) / max_range) * resolution)
        max_z = int(((max(v0[2], v1[2], v2[2]) - zmin) / max_range) * resolution)

        min_x, max_x = max(0, min_x), min(resolution - 1, max_x)
        min_y, max_y = max(0, min_y), min(resolution - 1, max_y)
        min_z, max_z = max(0, min_z), min(resolution - 1, max_z)

        for z in range(min_z, max_z + 1):
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    px = xmin + (x + 0.5) / resolution * max_range
                    py = ymin + (y + 0.5) / resolution * max_range
                    pz = zmin + (z + 0.5) / resolution * max_range
                    if point_in_triangle(px, py, pz, v0, v1, v2):
                        volume[z][y][x] = 1

    return volume


def point_in_triangle(px, py, pz, v0, v1, v2):
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


def voxelize_surface_mesh(vertices, triangles, resolution=32):
    """Voxelize only the surface."""
    return voxelize_triangle_mesh(vertices, triangles, resolution)


def merge_voxels(volume, level=2):
    """Merge voxels at given level."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    new_depth = (depth + level - 1) // level
    new_height = (height + level - 1) // level
    new_width = (width + level - 1) // level

    result = [[[0] * new_width for _ in range(new_height)] for _ in range(new_depth)]

    for z in range(new_depth):
        for y in range(new_height):
            for x in range(new_width):
                for dz in range(level):
                    for dy in range(level):
                        for dx in range(level):
                            sz = z * level + dz
                            sy = y * level + dy
                            sx = x * level + dx
                            if sz < depth and sy < height and sx < width:
                                if volume[sz][sy][sx] == 1:
                                    result[z][y][x] = 1
                                    break
                        else:
                            continue
                        break
    return result


def minkowski_sum_voxel(volume1, volume2):
    """Compute Minkowski sum."""
    d1, h1, w1 = len(volume1), len(volume1[0]), len(volume1[0][0])
    d2, h2, w2 = len(volume2), len(volume2[0]), len(volume2[0][0])

    result = [[[0] * (w1 + w2) for _ in range(h1 + h2)] for _ in range(d1 + d2)]

    for z1 in range(d1):
        for y1 in range(h1):
            for x1 in range(w1):
                if volume1[z1][y1][x1] == 0:
                    continue
                for z2 in range(d2):
                    for y2 in range(h2):
                        for x2 in range(w2):
                            if volume2[z2][y2][x2] == 0:
                                continue
                            nx, ny, nz = x1 + x2, y1 + y2, z1 + z2
                            if (
                                nz < len(result)
                                and ny < len(result[0])
                                and nx < len(result[0][0])
                            ):
                                result[nz][ny][nx] = 1
    return result


def voxel_dilate_3d(volume, iterations=1):
    """3D morphological dilation."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    result = [[[v for v in row] for row in layer] for layer in volume]

    for _ in range(iterations):
        temp = [[[v for v in row] for row in layer] for layer in result]
        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if result[z][y][x] == 1:
                        for dx, dy, dz in NEIGHBOR_6:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                                temp[nz][ny][nx] = 1
        result = temp
    return result


def voxel_erode_3d(volume, iterations=1):
    """3D morphological erosion."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    result = [[[v for v in row] for row in layer] for layer in volume]

    for _ in range(iterations):
        temp = [[[v for v in row] for row in layer] for layer in result]
        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if result[z][y][x] == 1:
                        for dx, dy, dz in NEIGHBOR_6:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            if not (
                                0 <= nx < width and 0 <= ny < height and 0 <= nz < depth
                            ):
                                temp[z][y][x] = 0
                                break
                            if result[nz][ny][nx] == 0:
                                temp[z][y][x] = 0
                                break
        result = temp
    return result


def fill_voxel_holes(volume):
    """Fill holes in voxel volume."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    visited = [[[False] * width for _ in range(height)] for _ in range(depth)]
    stack = []

    for x in range(width):
        for y in range(height):
            if volume[0][y][x] == 0:
                stack.append((x, y, 0))
                visited[0][y][x] = True
            if volume[depth - 1][y][x] == 0:
                stack.append((x, y, depth - 1))
                visited[depth - 1][y][x] = True

    for z in range(depth):
        for x in range(width):
            if volume[z][0][x] == 0:
                stack.append((x, 0, z))
                visited[z][0][x] = True
            if volume[z][height - 1][x] == 0:
                stack.append((x, height - 1, z))
                visited[z][height - 1][x] = True
        for y in range(height):
            if volume[z][y][0] == 0:
                stack.append((0, y, z))
                visited[z][y][0] = True
            if volume[z][y][width - 1] == 0:
                stack.append((width - 1, y, z))
                visited[z][y][width - 1] = True

    while stack:
        cx, cy, cz = stack.pop()
        for dx, dy, dz in NEIGHBOR_6:
            nx, ny, nz = cx + dx, cy + dy, cz + dz
            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                if not visited[nz][ny][nx] and volume[nz][ny][nx] == 0:
                    visited[nz][ny][nx] = True
                    stack.append((nx, ny, nz))

    return [
        [
            [
                1 if not visited[z][y][x] and volume[z][y][x] == 0 else volume[z][y][x]
                for x in range(width)
            ]
            for y in range(height)
        ]
        for z in range(depth)
    ]


def voxel_pyramid(volume, levels=3):
    """Build multi-resolution voxel pyramid."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    pyramid = [volume]

    for level in range(1, levels):
        prev = pyramid[level - 1]
        d, h, w = len(prev), len(prev[0]), len(prev[0][0])
        new_d, new_h, new_w = max(1, d // 2), max(1, h // 2), max(1, w // 2)

        current = [
            [[0.0 for _ in range(new_w)] for _ in range(new_h)] for _ in range(new_d)
        ]

        for z in range(new_d):
            for y in range(new_h):
                for x in range(new_w):
                    sum_val = count = 0
                    for dz in range(2):
                        for dy in range(2):
                            for dx in range(2):
                                sz, sy, sx = z * 2 + dz, y * 2 + dy, x * 2 + dx
                                if sz < d and sy < h and sx < w:
                                    sum_val += prev[sz][sy][sx]
                                    count += 1
                    current[z][y][x] = sum_val / count if count > 0 else 0.0
        pyramid.append(current)
    return pyramid
