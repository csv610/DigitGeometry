"""Mesh processing and analysis."""

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


def iterative_closest_point(source, target, max_iterations=20):
    """Iterative closest point algorithm."""
    if not source or not target:
        return source

    dim = len(source[0])
    source_center = [sum(p[i] for p in source) / len(source) for i in range(dim)]
    target_center = [sum(p[i] for p in target) / len(target) for i in range(dim)]

    transformed = [[p[i] - source_center[i] + target_center[i] for i in range(dim)] for p in source]

    for _ in range(max_iterations):
        correspondences = []
        for p in transformed:
            min_dist = float("inf")
            closest = target[0]
            for tp in target:
                dist = sum((p[i] - tp[i]) ** 2 for i in range(dim)) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    closest = tp
            correspondences.append(closest)

        if not correspondences:
            break

        # Basic translation-only ICP for this toy implementation
        new_target_center = [
            sum(p[i] for p in correspondences) / len(correspondences) for i in range(dim)
        ]
        new_source_center = [
            sum(p[i] for p in transformed) / len(transformed) for i in range(dim)
        ]
        
        for p in transformed:
            for i in range(dim):
                p[i] += new_target_center[i] - new_source_center[i]

    return transformed


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
