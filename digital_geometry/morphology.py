"""Morphological operations."""

SE_SQUARE_3X3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
SE_CROSS_3X3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]


def dilate(grid, se=SE_SQUARE_3X3):
    """Morphological dilation."""
    height = len(grid)
    width = len(grid[0])
    se_height = len(se)
    se_width = len(se[0])
    half_h = se_height // 2
    half_w = se_width // 2

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                for sy in range(se_height):
                    for sx in range(se_width):
                        if se[sy][sx]:
                            ny, nx = y + sy - half_h, x + sx - half_w
                            if 0 <= ny < height and 0 <= nx < width:
                                result[ny][nx] = 1

    return result


def erode(grid, se=SE_SQUARE_3X3):
    """Morphological erosion."""
    height = len(grid)
    width = len(grid[0])
    se_height = len(se)
    se_width = len(se[0])
    half_h = se_height // 2
    half_w = se_width // 2

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            valid = True
            for sy in range(se_height):
                for sx in range(se_width):
                    if se[sy][sx]:
                        ny, nx = y + sy - half_h, x + sx - half_w
                        if not (0 <= ny < height and 0 <= nx < width and grid[ny][nx]):
                            valid = False
                            break
                if not valid:
                    break
            result[y][x] = 1 if valid else 0

    return result


def morph_opening(grid, se=SE_SQUARE_3X3):
    """Opening: erosion followed by dilation."""
    return dilate(erode(grid, se), se)


def morph_closing(grid, se=SE_SQUARE_3X3):
    """Closing: dilation followed by erosion."""
    return erode(dilate(grid, se), se)


def morph_boundary(grid, se=SE_SQUARE_3X3):
    """Extracts the inner boundary of foreground shapes."""
    eroded = erode(grid, se)
    height = len(grid)
    width = len(grid[0])
    boundary = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1 and eroded[y][x] == 0:
                boundary[y][x] = 1
    return boundary


def white_tophat(grid, se=SE_SQUARE_3X3):
    """White top-hat: extracts small bright features."""
    opened = morph_opening(grid, se)
    height = len(grid)
    width = len(grid[0])
    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            result[y][x] = grid[y][x] - opened[y][x]
            if result[y][x] < 0:
                result[y][x] = 0
    return result


def black_tophat(grid, se=SE_SQUARE_3X3):
    """Black top-hat: extracts small dark features."""
    closed = morph_closing(grid, se)
    height = len(grid)
    width = len(grid[0])
    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            result[y][x] = closed[y][x] - grid[y][x]
            if result[y][x] < 0:
                result[y][x] = 0
    return result


def create_square_se(size):
    """Create square structuring element."""
    se = []
    half = size // 2
    for dy in range(-half, half + 1):
        row = []
        for dx in range(-half, half + 1):
            row.append(1)
        se.append(row)
    return se


def morph_erode(grid, se):
    """Morphological erosion with custom SE."""
    if not grid:
        return []

    height = len(grid)
    width = len(grid[0])
    se_height = len(se)
    se_width = len(se[0])
    half_h = se_height // 2
    half_w = se_width // 2

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            valid = True
            for sy in range(se_height):
                for sx in range(se_width):
                    if se[sy][sx]:
                        ny, nx = y + sy - half_h, x + sx - half_w
                        if not (0 <= ny < height and 0 <= nx < width and grid[ny][nx]):
                            valid = False
                            break
                if not valid:
                    break
            result[y][x] = 1 if valid else 0

    return result


def morphological_skeleton(grid):
    """Morphological skeleton via iterative erosion."""
    from digital_geometry.topology import count_connected_components

    height = len(grid)
    width = len(grid[0])
    skeleton = [[0] * width for _ in range(height)]
    temp_grid = [row[:] for row in grid]

    while True:
        eroded = erode(temp_grid)

        if count_connected_components(eroded, 1, 4) == 0:
            break

        boundary = morph_boundary(temp_grid)

        for y in range(height):
            for x in range(width):
                if boundary[y][x] == 1:
                    skeleton[y][x] = 1

        temp_grid = eroded

    return skeleton


def geodesic_dilation(grid, mask, iterations=1):
    """Geodesic dilation: dilate within mask bounds."""
    result = [row[:] for row in grid]
    height = len(grid)
    width = len(grid[0])

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for _ in range(iterations):
        new_result = [row[:] for row in result]
        for y in range(height):
            for x in range(width):
                if result[y][x] == 1:
                    for dx, dy in neighbors:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if mask[ny][nx] == 1:
                                new_result[ny][nx] = 1
        result = new_result

    return result


def geodesic_erosion(grid, mask, iterations=1):
    """Geodesic erosion: erode, then constrain to mask."""
    result = [row[:] for row in grid]
    height = len(grid)
    width = len(grid[0])

    se = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

    for _ in range(iterations):
        eroded = morph_erode(result, se)

        for y in range(height):
            for x in range(width):
                if mask[y][x] == 0:
                    eroded[y][x] = 0

        result = eroded

    return result
