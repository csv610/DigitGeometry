"""Additional processing utilities."""


def discrete_gradient(grid):
    """Compute discrete gradient of a grid."""
    height = len(grid)
    width = len(grid[0])

    grad_x = [[0] * width for _ in range(height)]
    grad_y = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width - 1):
            grad_x[y][x] = grid[y][x + 1] - grid[y][x]

    for y in range(height - 1):
        for x in range(width):
            grad_y[y][x] = grid[y + 1][x] - grid[y][x]

    return grad_x, grad_y


def discrete_divergence(grad_x, grad_y):
    """Compute discrete divergence from gradient fields."""
    height = len(grad_x)
    width = len(grad_x[0])

    div = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            left = grad_x[y][x - 1] if x > 0 else 0
            right = grad_x[y][x] if x < width - 1 else 0
            up = grad_y[y - 1][x] if y > 0 else 0
            down = grad_y[y][x] if y < height - 1 else 0

            div[y][x] = right - left + down - up

    return div


def discrete_laplacian_grid(grid):
    """Discrete Laplacian on a grid (5-point stencil)."""
    height = len(grid)
    width = len(grid[0])

    laplacian = [[0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            laplacian[y][x] = (
                grid[y - 1][x]
                + grid[y + 1][x]
                + grid[y][x - 1]
                + grid[y][x + 1]
                - 4 * grid[y][x]
            )

    return laplacian


def detect_skeleton_endpoints(skeleton):
    """Detect endpoints in a skeleton."""
    height = len(skeleton)
    width = len(skeleton[0])

    endpoints = []

    neighbors_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for y in range(height):
        for x in range(width):
            if skeleton[y][x] == 1:
                count = 0
                for dx, dy in neighbors_4:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if skeleton[ny][nx] == 1:
                            count += 1

                if count == 1:
                    endpoints.append((x, y))

    return endpoints


def detect_skeleton_junctions(skeleton):
    """Detect junction points in a skeleton."""
    height = len(skeleton)
    width = len(skeleton[0])

    junctions = []

    neighbors_8 = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    for y in range(height):
        for x in range(width):
            if skeleton[y][x] == 1:
                count = 0
                for dx, dy in neighbors_8:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if skeleton[ny][nx] == 1:
                            count += 1

                if count >= 3:
                    junctions.append((x, y))

    return junctions


def prune_skeleton(grid, min_branch_length=3):
    """Prune short branches from skeleton."""
    from digital_geometry.morphology import erode

    height = len(grid)
    width = len(grid[0])

    result = [row[:] for row in grid]

    for _ in range(min_branch_length):
        temp = erode(result)

        for y in range(height):
            for x in range(width):
                if result[y][x] == 1:
                    neighbors = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if (
                                0 <= ny < height
                                and 0 <= nx < width
                                and result[ny][nx] == 1
                            ):
                                neighbors += 1

                    if neighbors <= 1:
                        result[y][x] = 0

    return result


def skeleton_to_graph(skeleton):
    """Convert skeleton to graph representation."""
    height = len(skeleton)
    width = len(skeleton[0])

    graph = {}

    for y in range(height):
        for x in range(width):
            if skeleton[y][x] == 1:
                neighbors = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ny, nx = y + dy, x + dx
                        if (
                            0 <= ny < height
                            and 0 <= nx < width
                            and skeleton[ny][nx] == 1
                        ):
                            neighbors.append((nx, ny))

                graph[(x, y)] = neighbors

    return graph
