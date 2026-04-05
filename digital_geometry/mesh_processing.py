"""Mesh processing operations."""

import math


def laplacian_mesh_smoothing(vertices, faces, iterations=5, lambda_val=0.5):
    """Laplacian mesh smoothing."""
    if not vertices:
        return vertices, faces

    smoothed = [list(v) for v in vertices]

    for _ in range(iterations):
        new_vertices = [list(v) for v in smoothed]

        for i, (x, y, z) in enumerate(smoothed):
            neighbors = []
            for face in faces:
                if i in face:
                    for j in face:
                        if j != i:
                            neighbors.append(j)

            if neighbors:
                avg_x = avg_y = avg_z = 0.0
                for j in neighbors:
                    avg_x += smoothed[j][0]
                    avg_y += smoothed[j][1]
                    avg_z += smoothed[j][2]
                avg_x /= len(neighbors)
                avg_y /= len(neighbors)
                avg_z /= len(neighbors)

                new_vertices[i][0] = x + lambda_val * (avg_x - x)
                new_vertices[i][1] = y + lambda_val * (avg_y - y)
                new_vertices[i][2] = z + lambda_val * (avg_z - z)

        smoothed = new_vertices

    return smoothed, faces


def mesh_simplification_edge_collapse(vertices, faces, target_count):
    """Simplify mesh using edge collapse."""
    if len(vertices) <= target_count:
        return vertices, faces

    simplified_verts = vertices[:target_count]
    simplified_faces = []

    for face in faces:
        new_face = [min(i, target_count - 1) for i in face]
        if len(set(new_face)) >= 3:
            simplified_faces.append(tuple(new_face))

    return simplified_verts, simplified_faces


def active_contour_snake(
    image, init_points, max_iterations=100, alpha=0.01, beta=0.01, gamma=1.0
):
    """Active contour (snake) algorithm."""
    height = len(image)
    width = len(image[0])

    snake = [list(p) for p in init_points]

    for _ in range(max_iterations):
        new_snake = []
        for i, (x, y) in enumerate(snake):
            prev = snake[(i - 1) % len(snake)]
            next_p = snake[(i + 1) % len(snake)]

            if 0 < x < width - 1 and 0 < y < height - 1:
                ix, iy = int(x), int(y)
                fx = (image[iy][ix + 1] - image[iy][ix - 1]) / 2
                fy = (image[iy + 1][ix] - image[iy - 1][ix]) / 2
                cx = prev[0] - 2 * x + next_p[0]
                cy = prev[1] - 2 * y + next_p[1]

                ex = prev[0] - 2 * prev[0] + next_p[0]
                ey = prev[1] - 2 * prev[1] + next_p[1]

                nx = x - alpha * cx + gamma * fx
                ny = y - alpha * cy + gamma * fy

                nx = max(0, min(width - 1, nx))
                ny = max(0, min(height - 1, ny))

                new_snake.append([nx, ny])
            else:
                new_snake.append([x, y])

        snake = new_snake

    return snake


def mean_curvature_flow_grid(grid, iterations=1, step_size=0.1):
    """Mean curvature flow on grid."""
    height = len(grid)
    width = len(grid[0])

    result = [[float(v) for v in row] for row in grid]

    for _ in range(iterations):
        temp = [[result[y][x] for x in range(width)] for y in range(height)]

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                laplacian = (
                    result[y - 1][x]
                    + result[y + 1][x]
                    + result[y][x - 1]
                    + result[y][x + 1]
                    - 4 * result[y][x]
                )
                temp[y][x] = result[y][x] + step_size * laplacian

        result = temp

    return result
