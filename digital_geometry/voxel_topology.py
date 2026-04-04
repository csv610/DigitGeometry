"""Voxel topology and boundary operations."""

from digital_geometry.voxel_core import NEIGHBOR_6, NEIGHBOR_18, NEIGHBOR_26


def find_voxel_borders(volume):
    """Find border voxels (adjacent to background)."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    borders = []
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        if volume[nz][ny][nx] == 0:
                            borders.append((x, y, z))
                            break
    return borders


def find_voxel_edges(volume):
    """Find edge voxels (adjacent to exactly 2 foreground voxels)."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    edges = []
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue
                fg_count = 0
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        if volume[nz][ny][nx] == 1:
                            fg_count += 1
                if fg_count == 2:
                    edges.append((x, y, z))
    return edges


def find_voxel_vertices(volume):
    """Find vertex voxels (corners where 3 axes meet)."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    vertices = []
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue
                neighbors = []
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        if volume[nz][ny][nx] == 1:
                            neighbors.append((dx, dy, dz))

                has_x = any(dx != 0 for dx, dy, dz in neighbors)
                has_y = any(dy != 0 for dx, dy, dz in neighbors)
                has_z = any(dz != 0 for dx, dy, dz in neighbors)

                if has_x and has_y and has_z:
                    vertices.append((x, y, z))
    return vertices


def classify_voxel_grid(volume):
    """Classify voxels as interior/exterior/boundary."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    result = [[["exterior"] * width for _ in range(height)] for _ in range(depth)]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    result[z][y][x] = "exterior"
                    continue
                is_boundary = False
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if not (0 <= nx < width and 0 <= ny < height and 0 <= nz < depth):
                        is_boundary = True
                        break
                    if volume[nz][ny][nx] == 0:
                        is_boundary = True
                        break
                result[z][y][x] = "boundary" if is_boundary else "interior"
    return result


def is_voxel_surface_manifold(volume):
    """Check if voxel surface is manifold."""
    borders = find_voxel_borders(volume)
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    for x, y, z in borders:
        neighbor_count = 0
        for dx, dy, dz in NEIGHBOR_6:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                if volume[nz][ny][nx] == 1:
                    neighbor_count += 1
        if neighbor_count != 2 and neighbor_count != 3:
            return False
    return True


def voxel_junction_count(volume):
    """Count junction voxels."""
    borders = find_voxel_borders(volume)
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    junction_count = 0
    for x, y, z in borders:
        neighbor_count = 0
        for dx, dy, dz in NEIGHBOR_6:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                if volume[nz][ny][nx] == 1:
                    neighbor_count += 1
        if neighbor_count >= 4:
            junction_count += 1
    return junction_count


def voxel_endpoint_count(volume):
    """Count endpoint voxels."""
    borders = find_voxel_borders(volume)
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    endpoint_count = 0
    for x, y, z in borders:
        neighbor_count = 0
        for dx, dy, dz in NEIGHBOR_6:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                if volume[nz][ny][nx] == 1:
                    neighbor_count += 1
        if neighbor_count == 1:
            endpoint_count += 1
    return endpoint_count


def extract_boundary_faces(volume):
    """Extract boundary faces."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    faces = []
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if not (0 <= nx < width and 0 <= ny < height and 0 <= nz < depth):
                        faces.append((x, y, z, dx, dy, dz))
                    elif volume[nz][ny][nx] == 0:
                        faces.append((x, y, z, dx, dy, dz))
    return faces


def voxel_contour_3d(volume):
    """Get 3D contour voxels."""
    borders = find_voxel_borders(volume)
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    contour = [[[0] * width for _ in range(height)] for _ in range(depth)]
    for x, y, z in borders:
        contour[z][y][x] = 1
    return contour
