"""Geometric transformations."""

import math
import cmath


def invert_affine_matrix(M):
    """Invert a 2x3 or 3x3 affine transformation matrix."""
    if len(M) == 3 and len(M[0]) == 3:
        det = (
            M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
        )

        if abs(det) < 1e-10:
            return None

        inv = [[0] * 3 for _ in range(3)]
        inv[0][0] = (M[1][1] * M[2][2] - M[1][2] * M[2][1]) / det
        inv[0][1] = (M[0][2] * M[2][1] - M[0][1] * M[2][2]) / det
        inv[0][2] = (M[0][1] * M[1][2] - M[0][2] * M[1][1]) / det
        inv[1][0] = (M[1][2] * M[2][0] - M[1][0] * M[2][2]) / det
        inv[1][1] = (M[0][0] * M[2][2] - M[0][2] * M[2][0]) / det
        inv[1][2] = (M[1][0] * M[0][2] - M[0][0] * M[1][2]) / det
        inv[2][0] = (M[1][0] * M[2][1] - M[1][1] * M[2][0]) / det
        inv[2][1] = (M[2][0] * M[0][1] - M[0][0] * M[2][1]) / det
        inv[2][2] = (M[0][0] * M[1][1] - M[1][0] * M[0][1]) / det

        return inv

    a, b, c = M[0][0], M[0][1], M[0][2]
    d, e, f = M[1][0], M[1][1], M[1][2]

    det = a * e - b * d

    if abs(det) < 1e-10:
        return None

    return [
        [e / det, -b / det, (b * f - c * e) / det],
        [-d / det, a / det, (c * d - a * f) / det],
    ]


def transform_points(points, M):
    """Apply affine transformation to points."""
    transformed = []

    for x, y in points:
        nx = M[0][0] * x + M[0][1] * y + M[0][2]
        ny = M[1][0] * x + M[1][1] * y + M[1][2]
        transformed.append((nx, ny))

    return transformed


def translate_points(points, dx, dy):
    """Translate points by (dx, dy)."""
    return [(x + dx, y + dy) for x, y in points]


def rotate_points(points, angle_deg, center=(0, 0)):
    """Rotate points by angle_deg around center."""
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    cx, cy = center

    rotated = []
    for x, y in points:
        xc = x - cx
        yc = y - cy
        nx = cx + xc * cos_a - yc * sin_a
        ny = cy + xc * sin_a + yc * cos_a
        rotated.append((nx, ny))

    return rotated


def scale_points(points, sx, sy, center=(0, 0)):
    """Scale points by (sx, sy) around center."""
    cx, cy = center

    scaled = []
    for x, y in points:
        nx = cx + (x - cx) * sx
        ny = cy + (y - cy) * sy
        scaled.append((nx, ny))

    return scaled


def affine_transform_grid(grid, M, output_shape=None):
    """Apply affine transformation to grid."""
    if output_shape is None:
        output_shape = (len(grid[0]), len(grid))

    width, height = output_shape
    result = [[0] * width for _ in range(height)]

    inv_M = invert_affine_matrix(M)
    if inv_M is None:
        return result

    for y in range(height):
        for x in range(width):
            src_x = inv_M[0][0] * x + inv_M[0][1] * y + inv_M[0][2]
            src_y = inv_M[1][0] * x + inv_M[1][1] * y + inv_M[1][2]

            src_x = int(round(src_x))
            src_y = int(round(src_y))

            if 0 <= src_x < len(grid[0]) and 0 <= src_y < len(grid):
                result[y][x] = grid[src_y][src_x]

    return result


def translate_grid(grid, dx, dy):
    """Translate grid by (dx, dy)."""
    height = len(grid)
    width = len(grid[0])

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            nx = x + dx
            ny = y + dy

            if 0 <= nx < width and 0 <= ny < height:
                result[ny][nx] = grid[y][x]

    return result


def rotate_grid(grid, angle_deg, center=None):
    """Rotate grid by angle_deg around center."""
    height = len(grid)
    width = len(grid[0])

    if center is None:
        center = (width / 2, height / 2)

    cx, cy = center
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            xc = x - cx
            yc = y - cy

            src_x = int(round(cx + xc * cos_a + yc * sin_a))
            src_y = int(round(cy - xc * sin_a + yc * cos_a))

            if 0 <= src_x < width and 0 <= src_y < height:
                result[y][x] = grid[src_y][src_x]

    return result


def scale_grid(grid, sx, sy, center=None):
    """Scale grid by (sx, sy)."""
    height = len(grid)
    width = len(grid[0])

    new_width = int(width * sx)
    new_height = int(height * sy)

    result = [[0] * new_width for _ in range(new_height)]

    for y in range(new_height):
        for x in range(new_width):
            src_x = int(round(x / sx))
            src_y = int(round(y / sy))

            if 0 <= src_x < width and 0 <= src_y < height:
                result[y][x] = grid[src_y][src_x]

    return result


def bilinear_resample(grid, scale_factor):
    """Bilinear image resampling."""
    height = len(grid)
    width = len(grid[0])

    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    result = [[0.0] * new_width for _ in range(new_height)]

    for new_y in range(new_height):
        for new_x in range(new_width):
            src_x = new_x / scale_factor
            src_y = new_y / scale_factor

            x0 = int(src_x)
            y0 = int(src_y)
            x1 = min(x0 + 1, width - 1)
            y1 = min(y0 + 1, height - 1)

            dx = src_x - x0
            dy = src_y - y0

            tl = grid[y0][x0]
            tr = grid[y0][x1]
            bl = grid[y1][x0]
            br = grid[y1][x1]

            result[new_y][new_x] = (
                tl * (1 - dx) * (1 - dy)
                + tr * dx * (1 - dy)
                + bl * (1 - dx) * dy
                + br * dx * dy
            )

    return result


def bicubic_resample(grid, scale_factor):
    """Bicubic image resampling."""
    height = len(grid)
    width = len(grid[0])

    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    def cubic_interp(t, v0, v1, v2, v3):
        a = 0.5
        return (
            (2 * v1)
            + (-v0 + v2) * t
            + (2 * v0 - 5 * v1 + 4 * v2 - v3) * t * t
            + (-v0 + 3 * v1 - 3 * v2 + v3) * t * t * t
        ) * a

    result = [[0.0] * new_width for _ in range(new_height)]

    def get_pixel(x, y):
        if x < 0:
            x = 0
        if x >= width:
            x = width - 1
        if y < 0:
            y = 0
        if y >= height:
            y = height - 1
        return grid[y][x]

    for new_y in range(new_height):
        for new_x in range(new_width):
            src_x = new_x / scale_factor
            src_y = new_y / scale_factor

            x0 = int(src_x)
            y0 = int(src_y)

            dx = src_x - x0
            dy = src_y - y0

            row = []
            for j in range(-1, 3):
                v = []
                for i in range(-1, 3):
                    v.append(get_pixel(x0 + i, y0 + j))
                row.append(cubic_interp(dx, v[0], v[1], v[2], v[3]))

            result[new_y][new_x] = cubic_interp(dy, row[0], row[1], row[2], row[3])

    return result


def upscale_grid(grid, factor):
    """Upscale grid by integer factor using nearest neighbor."""
    height = len(grid)
    width = len(grid[0])

    new_height = height * factor
    new_width = width * factor

    result = [[0] * new_width for _ in range(new_height)]

    for y in range(height):
        for x in range(width):
            value = grid[y][x]
            for dy in range(factor):
                for dx in range(factor):
                    result[y * factor + dy][x * factor + dx] = value

    return result


def downscale_grid(grid, factor):
    """Downscale grid by integer factor using averaging."""
    height = len(grid)
    width = len(grid[0])

    new_height = height // factor
    new_width = width // factor

    result = [[0] * new_width for _ in range(new_height)]

    for y in range(new_height):
        for x in range(new_width):
            total = 0
            for dy in range(factor):
                for dx in range(factor):
                    total += grid[y * factor + dy][x * factor + dx]
            result[y][x] = total // (factor * factor)

    return result
