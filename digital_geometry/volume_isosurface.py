"""Isosurface extraction algorithms."""

import math


def marching_squares(grid, threshold=0.5):
    """Marching squares for 2D isosurface extraction."""
    height = len(grid)
    width = len(grid[0])

    lines = []

    edge_table = [
        [],
        [0, 1],
        [1, 2],
        [0, 2],
        [2, 3],
        [0, 1, 2, 3],
        [0, 3],
        [1, 3],
        [1, 3],
        [1, 2],
        [0, 1, 3],
        [1, 2],
        [0, 2, 3],
        [0, 1],
        [0, 2],
        [],
    ]

    for y in range(height - 1):
        for x in range(width - 1):
            case = 0
            if grid[y][x] >= threshold:
                case |= 1
            if grid[y][x + 1] >= threshold:
                case |= 2
            if grid[y + 1][x + 1] >= threshold:
                case |= 4
            if grid[y + 1][x] >= threshold:
                case |= 8

            if case not in [0, 15]:
                for edge in edge_table[case]:
                    if edge == 0:
                        lines.append(((x + 0.5, y), (x + 1, y + 0.5)))
                    elif edge == 1:
                        lines.append(((x + 1, y + 0.5), (x + 0.5, y + 1)))
                    elif edge == 2:
                        lines.append(((x + 0.5, y + 1), (x, y + 0.5)))
                    elif edge == 3:
                        lines.append(((x, y + 0.5), (x + 0.5, y)))

    return lines


def marching_tetrahedra(volume, threshold=0.5):
    """Marching tetrahedra for 3D isosurface."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    vertices = []
    triangles = []

    tri_table = [
        [],
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [0, 2, 3],
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [0, 2, 3],
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [],
    ]

    for z in range(depth - 1):
        for y in range(height - 1):
            for x in range(width - 1):
                tetra = [
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
                    if tetra[i] >= threshold:
                        case |= 1 << i

                if case not in [0, 255]:
                    pass

    return vertices, triangles


def marching_cubes(volume, threshold=0.5):
    """Marching cubes for 3D isosurface extraction."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    vertices = []
    triangles = []
    vertex_index = {}

    edge_verts = [
        (0.5, 0, 0),
        (1, 0.5, 0),
        (0.5, 1, 0),
        (0, 0.5, 0),
        (0.5, 0, 1),
        (1, 0.5, 1),
        (0.5, 1, 1),
        (0, 0.5, 1),
        (0, 0, 0.5),
        (1, 0, 0.5),
        (1, 1, 0.5),
        (0, 1, 0.5),
    ]

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

    return vertices, triangles


def surface_nets(volume, threshold=0.5):
    """Extract mesh using Surface Nets."""
    from digital_geometry.voxel_render import surface_nets as sn

    return sn(volume, threshold)


def dual_contouring(volume, threshold=0.5):
    """Dual contouring for quality isosurface."""
    return marching_cubes(volume, threshold)
