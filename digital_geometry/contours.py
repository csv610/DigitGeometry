"""Contour extraction and tracing."""

MOORE_NEIGHBORS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


def flood_fill(grid, start_x, start_y, replacement_color):
    """Flood Fill Algorithm using 4-way connectivity."""
    if not grid or not grid[0]:
        return

    height = len(grid)
    width = len(grid[0])

    if start_y < 0 or start_y >= height or start_x < 0 or start_x >= width:
        return

    target_color = grid[start_y][start_x]
    if target_color == replacement_color:
        return

    queue = [(start_x, start_y)]
    while queue:
        cx, cy = queue.pop(0)

        if grid[cy][cx] == target_color:
            grid[cy][cx] = replacement_color

            if cx > 0:
                queue.append((cx - 1, cy))
            if cx < width - 1:
                queue.append((cx + 1, cy))
            if cy > 0:
                queue.append((cx, cy - 1))
            if cy < height - 1:
                queue.append((cx, cy + 1))


def moore_neighbor_boundary_trace(grid, start_x, start_y):
    """Moore neighbor boundary tracing algorithm."""
    height = len(grid)
    width = len(grid[0])

    if grid[start_y][start_x] != 1:
        return []

    boundary = []
    visited = set()

    current = (start_x, start_y)
    direction = 0

    while True:
        boundary.append(current)
        visited.add(current)

        found = False
        for i in range(8):
            dir_idx = (direction + i + 1) % 8
            dx, dy = MOORE_NEIGHBORS[dir_idx]
            nx, ny = current[0] + dx, current[1] + dy

            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
                current = (nx, ny)
                direction = dir_idx
                found = True
                break

        if not found or current in visited:
            break

    return boundary


def suzuki_contour_trace(grid):
    """Suzuki's algorithm for contour tracing."""
    height = len(grid)
    width = len(grid[0])

    visited = [[False] * width for _ in range(height)]
    contours = []

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1 and not visited[y][x]:
                contour = [(x, y)]
                visited[y][x] = True
                direction = 7

                curr_x, curr_y = x, y

                while True:
                    next_x, next_y, direction = get_next_boundary_point(
                        curr_x, curr_y, direction, grid, visited, width, height
                    )

                    if next_x is None:
                        break

                    contour.append((next_x, next_y))
                    visited[next_y][next_x] = True
                    curr_x, curr_y = next_x, next_y

                if len(contour) > 1:
                    contours.append(contour)

    return contours


def get_next_boundary_point(x, y, prev_direction, grid, visited, width, height):
    """Helper to find next boundary point in Suzuki's algorithm."""
    for i in range(8):
        idx = (prev_direction + i + 1) % 8
        dx, dy = MOORE_NEIGHBORS[idx]
        nx, ny = x + dx, y + dy

        if 0 <= nx < width and 0 <= ny < height:
            if grid[ny][nx] == 1 and not visited[ny][nx]:
                return nx, ny, idx

    return None, None, None


def run_length_encode(grid):
    """Run-length encoding of a binary grid."""
    height = len(grid)
    width = len(grid[0])

    rle = []

    for y in range(height):
        row_rle = []
        count = 1

        for x in range(1, width):
            if grid[y][x] == grid[y][x - 1]:
                count += 1
            else:
                row_rle.append((grid[y][x - 1], count))
                count = 1

        row_rle.append((grid[y][-1], count))
        rle.append(row_rle)

    return rle


def run_length_decode(rle, width):
    """Decode run-length encoded data back to grid."""
    grid = []

    for row_rle in rle:
        row = []
        for value, count in row_rle:
            row.extend([value] * count)

        if len(row) < width:
            row.extend([0] * (width - len(row)))
        elif len(row) > width:
            row = row[:width]

        grid.append(row)

    return grid


def freeman_chain_code(points):
    """Compute Freeman chain code for a contour."""
    if len(points) < 2:
        return []

    chain = []

    for i in range(len(points) - 1):
        dx = points[i + 1][0] - points[i][0]
        dy = points[i + 1][1] - points[i][1]

        if dx == 1 and dy == 0:
            chain.append(0)
        elif dx == 1 and dy == 1:
            chain.append(1)
        elif dx == 0 and dy == 1:
            chain.append(2)
        elif dx == -1 and dy == 1:
            chain.append(3)
        elif dx == -1 and dy == 0:
            chain.append(4)
        elif dx == -1 and dy == -1:
            chain.append(5)
        elif dx == 0 and dy == -1:
            chain.append(6)
        elif dx == 1 and dy == -1:
            chain.append(7)

    return chain
