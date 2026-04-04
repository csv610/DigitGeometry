"""Feature detection algorithms for geometry."""

import math


def harris_corner(grid, k=0.04, threshold=0.01):
    """Harris corner detector."""
    from digital_geometry.edge import sobel

    height = len(grid)
    width = len(grid[0])

    Ix = [[0.0] * width for _ in range(height)]
    Iy = [[0.0] * width for _ in range(height)]

    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = 0.0
            gy = 0.0
            for sy in range(3):
                for sx in range(3):
                    gx += grid[y + sy - 1][x + sx - 1] * sobel_x[sy][sx]
                    gy += grid[y + sy - 1][x + sx - 1] * sobel_y[sy][sx]
            Ix[y][x] = gx
            Iy[y][x] = gy

    Ixx = [[Ix[y][x] ** 2 for x in range(width)] for y in range(height)]
    Iyy = [[Iy[y][x] ** 2 for x in range(width)] for y in range(height)]
    Ixy = [[Ix[y][x] * Iy[y][x] for x in range(width)] for y in range(height)]

    result = [[0.0] * width for _ in range(height)]

    window = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            sum_xx = 0.0
            sum_yy = 0.0
            sum_xy = 0.0

            for wy in range(3):
                for wx in range(3):
                    ny, nx = y + wy - 1, x + wx - 1
                    sum_xx += Ixx[ny][nx]
                    sum_yy += Iyy[ny][nx]
                    sum_xy += Ixy[ny][nx]

            det = sum_xx * sum_yy - sum_xy**2
            trace = sum_xx + sum_yy
            result[y][x] = det - k * trace**2

    corners = []
    max_val = max(max(row) for row in result)
    for y in range(height):
        for x in range(width):
            if result[y][x] > threshold * max_val:
                corners.append((x, y))

    return corners


def shi_tomasi_corner(grid, threshold=0.01):
    """Shi-Tomasi corner detector."""
    from digital_geometry.edge import sobel

    height = len(grid)
    width = len(grid[0])

    Ix = [[0.0] * width for _ in range(height)]
    Iy = [[0.0] * width for _ in range(height)]

    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = 0.0
            gy = 0.0
            for sy in range(3):
                for sx in range(3):
                    gx += grid[y + sy - 1][x + sx - 1] * sobel_x[sy][sx]
                    gy += grid[y + sy - 1][x + sx - 1] * sobel_y[sy][sx]
            Ix[y][x] = gx
            Iy[y][x] = gy

    Ixx = [[Ix[y][x] ** 2 for x in range(width)] for y in range(height)]
    Iyy = [[Iy[y][x] ** 2 for x in range(width)] for y in range(height)]
    Ixy = [[Ix[y][x] * Iy[y][x] for x in range(width)] for y in range(height)]

    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            sum_xx = 0.0
            sum_yy = 0.0
            sum_xy = 0.0

            for wy in range(3):
                for wx in range(3):
                    ny, nx = y + wy - 1, x + wx - 1
                    sum_xx += Ixx[ny][nx]
                    sum_yy += Iyy[ny][nx]
                    sum_xy += Ixy[ny][nx]

            eigenvalues = []
            trace = sum_xx + sum_yy
            det = sum_xx * sum_yy - sum_xy**2
            l1 = trace / 2 + math.sqrt(max(trace**2 / 4 - det, 0))
            l2 = trace / 2 - math.sqrt(max(trace**2 / 4 - det, 0))
            result[y][x] = min(l1, l2)

    corners = []
    max_val = max(max(row) for row in result) if result else 0
    for y in range(height):
        for x in range(width):
            if result[y][x] > threshold * max_val:
                corners.append((x, y))

    return corners


def susan_corner(grid, threshold=27):
    """SUSAN corner detector."""
    height = len(grid)
    width = len(grid[0])

    mask = [
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
    ]

    corners = []

    for y in range(3, height - 3):
        for x in range(3, width - 3):
            center = grid[y][x]
            n = 0

            for my in range(7):
                for mx in range(7):
                    if mask[my][mx]:
                        ny, nx = y + my - 3, x + mx - 3
                        if abs(grid[ny][nx] - center) < threshold:
                            n += 1

            if n < 19:
                corners.append((x, y))

    return corners


def fast_corner(grid, threshold=10):
    """FAST corner detector."""
    height = len(grid)
    width = len(grid[0])

    mask_offsets = [
        (-3, 0),
        (-2, -1),
        (-1, -2),
        (0, -3),
        (1, -2),
        (2, -1),
        (3, 0),
        (2, 1),
        (1, 2),
        (0, 3),
        (-1, 2),
        (-2, 1),
    ]

    corners = []

    for y in range(3, height - 3):
        for x in range(3, width - 3):
            center = grid[y][x]

            brighter = 0
            darker = 0

            for dx, dy in mask_offsets:
                ny, nx = y + dy, x + dx
                if grid[ny][nx] > center + threshold:
                    brighter += 1
                elif grid[ny][nx] < center - threshold:
                    darker += 1

            if brighter >= 9 or darker >= 9:
                corners.append((x, y))

    return corners


def structure_tensor(grid, window=3):
    """Compute structure tensor for each pixel."""
    from digital_geometry.edge import sobel

    height = len(grid)
    width = len(grid[0])

    Ix, Iy = sobel(grid), sobel(grid)

    Ixx = [[Ix[y][x] ** 2 for x in range(width)] for y in range(height)]
    Iyy = [[Iy[y][x] ** 2 for x in range(width)] for y in range(height)]
    Ixy = [[Ix[y][x] * Iy[y][x] for x in range(width)] for y in range(height)]

    half = window // 2
    result = [[[0.0, 0.0, 0.0] for _ in range(width)] for _ in range(height)]

    for y in range(half, height - half):
        for x in range(half, width - half):
            sum_xx = 0.0
            sum_yy = 0.0
            sum_xy = 0.0

            for wy in range(window):
                for wx in range(window):
                    ny, nx = y + wy - half, x + wx - half
                    sum_xx += Ixx[ny][nx]
                    sum_yy += Iyy[ny][nx]
                    sum_xy += Ixy[ny][nx]

            result[y][x] = [sum_xx, sum_yy, sum_xy]

    return result


def compute_corner_response(grid, k=0.04):
    """Compute corner response using Harris method."""
    height = len(grid)
    width = len(grid[0])

    st = structure_tensor(grid)

    response = [[0.0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            sum_xx, sum_yy, sum_xy = st[y][x]
            det = sum_xx * sum_yy - sum_xy**2
            trace = sum_xx + sum_yy
            response[y][x] = det - k * trace**2

    return response
