"""Edge detection algorithms."""

import math


def sobel(grid):
    """Sobel edge detection."""
    height = len(grid)
    width = len(grid[0])

    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = 0.0
            gy = 0.0
            for sy in range(3):
                for sx in range(3):
                    gx += grid[y + sy - 1][x + sx - 1] * sobel_x[sy][sx]
                    gy += grid[y + sy - 1][x + sx - 1] * sobel_y[sy][sx]
            result[y][x] = math.sqrt(gx * gx + gy * gy)

    return result


def prewitt(grid):
    """Prewitt edge detection."""
    height = len(grid)
    width = len(grid[0])

    prewitt_x = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    prewitt_y = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]

    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = 0.0
            gy = 0.0
            for sy in range(3):
                for sx in range(3):
                    gx += grid[y + sy - 1][x + sx - 1] * prewitt_x[sy][sx]
                    gy += grid[y + sy - 1][x + sx - 1] * prewitt_y[sy][sx]
            result[y][x] = math.sqrt(gx * gx + gy * gy)

    return result


def roberts(grid):
    """Roberts cross edge detection."""
    height = len(grid)
    width = len(grid[0])

    result = [[0.0] * width for _ in range(height)]

    for y in range(height - 1):
        for x in range(width - 1):
            gx = grid[y][x] - grid[y + 1][x + 1]
            gy = grid[y][x + 1] - grid[y + 1][x]
            result[y][x] = math.sqrt(gx * gx + gy * gy)

    return result


def laplacian_4(grid):
    """4-neighbor Laplacian edge detection."""
    height = len(grid)
    width = len(grid[0])

    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            result[y][x] = abs(
                4 * grid[y][x]
                - grid[y - 1][x]
                - grid[y + 1][x]
                - grid[y][x - 1]
                - grid[y][x + 1]
            )

    return result


def laplacian_8(grid):
    """8-neighbor Laplacian edge detection."""
    height = len(grid)
    width = len(grid[0])

    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            result[y][x] = abs(
                8 * grid[y][x]
                - grid[y - 1][x - 1]
                - grid[y - 1][x]
                - grid[y - 1][x + 1]
                - grid[y][x - 1]
                - grid[y][x + 1]
                - grid[y + 1][x - 1]
                - grid[y + 1][x]
                - grid[y + 1][x + 1]
            )

    return result


def canny(grid, low_threshold=50, high_threshold=150):
    """Canny edge detector."""
    height = len(grid)
    width = len(grid[0])

    smoothed = gaussian_smooth(grid, sigma=1.4)

    gradient = sobel(smoothed)
    angle = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if gradient[y][x] != 0:
                angle[y][x] = math.degrees(
                    math.atan2(
                        sum(
                            grid[y + sy - 1][x + sx - 1]
                            * [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]][sy][sx]
                            for sy in range(3)
                            for sx in range(3)
                        ),
                        sum(
                            grid[y + sy - 1][x + sx - 1]
                            * [[-1, -2, -1], [0, 0, 0], [1, 2, 1]][sy][sx]
                            for sy in range(3)
                            for sx in range(3)
                        ),
                    )
                )

    edges = non_maximum_suppression(gradient, angle)

    edges = double_threshold(edges, low_threshold, high_threshold)

    edges = hysteresis_threshold(edges)

    return edges


def gaussian_smooth(grid, sigma=1.0):
    """Gaussian smoothing."""
    height = len(grid)
    width = len(grid[0])

    size = int(2 * math.ceil(3 * sigma) + 1)
    half = size // 2

    kernel = []
    for y in range(size):
        row = []
        for x in range(size):
            g = math.exp(-((x - half) ** 2 + (y - half) ** 2) / (2 * sigma * sigma)) / (
                2 * math.pi * sigma * sigma
            )
            row.append(g)
        kernel.append(row)

    result = [[0.0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            total = 0.0
            for ky in range(size):
                for kx in range(size):
                    ny, nx = y + ky - half, x + kx - half
                    if 0 <= ny < height and 0 <= nx < width:
                        result[y][x] += grid[ny][nx] * kernel[ky][kx]

    return result


def non_maximum_suppression(gradient, angle):
    """Non-maximum suppression for Canny."""
    height = len(gradient)
    width = len(gradient[0])

    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            ang = angle[y][x] % 180

            if (0 <= ang < 22.5) or (157.5 <= ang <= 180):
                neighbors = [gradient[y][x - 1], gradient[y][x + 1]]
            elif 22.5 <= ang < 67.5:
                neighbors = [gradient[y - 1][x + 1], gradient[y + 1][x - 1]]
            elif 67.5 <= ang < 112.5:
                neighbors = [gradient[y - 1][x], gradient[y + 1][x]]
            else:
                neighbors = [gradient[y - 1][x - 1], gradient[y + 1][x + 1]]

            if gradient[y][x] >= max(neighbors):
                result[y][x] = gradient[y][x]

    return result


def double_threshold(gradient, low, high):
    """Double thresholding for Canny."""
    height = len(gradient)
    width = len(gradient[0])

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if gradient[y][x] >= high:
                result[y][x] = 2
            elif gradient[y][x] >= low:
                result[y][x] = 1

    return result


def hysteresis_threshold(edges):
    """Hysteresis thresholding for Canny."""
    height = len(edges)
    width = len(edges[0])

    result = [[0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if edges[y][x] == 2:
                result[y][x] = 1
            elif edges[y][x] == 1:
                if (
                    edges[y - 1][x - 1] == 2
                    or edges[y - 1][x] == 2
                    or edges[y - 1][x + 1] == 2
                    or edges[y][x - 1] == 2
                    or edges[y][x + 1] == 2
                    or edges[y + 1][x - 1] == 2
                    or edges[y + 1][x] == 2
                    or edges[y + 1][x + 1] == 2
                ):
                    result[y][x] = 1

    return result
