"""Distance transforms and metrics."""

import math


def manhattan_distance(p1, p2):
    """Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1, p2):
    """Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def manhattan_distance_transform(grid):
    """Manhattan distance transform."""
    height = len(grid)
    width = len(grid[0])
    INF = float("inf")
    dist = [[INF] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                dist[y][x] = 0
            elif x > 0 and y > 0:
                dist[y][x] = 1 + min(dist[y][x - 1], dist[y - 1][x], dist[y - 1][x - 1])
            elif x > 0:
                dist[y][x] = 1 + dist[y][x - 1]
            elif y > 0:
                dist[y][x] = 1 + dist[y - 1][x]

    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            if x < width - 1:
                dist[y][x] = min(dist[y][x], 1 + dist[y][x + 1])
            if y < height - 1:
                dist[y][x] = min(dist[y][x], 1 + dist[y + 1][x])
            if x < width - 1 and y < height - 1:
                dist[y][x] = min(dist[y][x], 1 + dist[y + 1][x + 1])
            if x > 0 and y < height - 1:
                dist[y][x] = min(dist[y][x], 1 + dist[y + 1][x - 1])

    return dist


def euclidean_distance_transform(grid):
    """Euclidean distance transform using two-pass algorithm."""
    height = len(grid)
    width = len(grid[0])
    INF = float("inf")
    dist = [[INF] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                dist[y][x] = 0
            else:
                if x > 0 and dist[y][x - 1] != INF:
                    dist[y][x] = min(dist[y][x], dist[y][x - 1] + 1)
                if y > 0 and dist[y - 1][x] != INF:
                    dist[y][x] = min(dist[y][x], dist[y - 1][x] + 1)

    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            if x < width - 1 and dist[y][x + 1] != INF:
                dist[y][x] = min(dist[y][x], dist[y][x + 1] + 1)
            if y < height - 1 and dist[y + 1][x] != INF:
                dist[y][x] = min(dist[y][x], dist[y + 1][x] + 1)

            if x < width - 1 and y < height - 1:
                dist[y][x] = min(
                    dist[y][x],
                    (dist[y + 1][x + 1] + 1.414) if dist[y + 1][x + 1] != INF else INF,
                )
            if x > 0 and y < height - 1:
                dist[y][x] = min(
                    dist[y][x],
                    (dist[y + 1][x - 1] + 1.414) if dist[y + 1][x - 1] != INF else INF,
                )

    for y in range(height):
        for x in range(width):
            if dist[y][x] == INF:
                dist[y][x] = 0

    return dist


def chamfer_distance_transform(grid, weights=None):
    """Chamfer distance transform with configurable weights."""
    height = len(grid)
    width = len(grid[0])

    if weights is None:
        weights = [3, 4]

    w1, w2 = weights[0], weights[1]
    INF = float("inf")
    dist = [[INF] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                dist[y][x] = 0

    for y in range(height):
        for x in range(width):
            if dist[y][x] > 0:
                if x > 0 and dist[y][x - 1] + w1 < dist[y][x]:
                    dist[y][x] = dist[y][x - 1] + w1
                if y > 0 and dist[y - 1][x] + w1 < dist[y][x]:
                    dist[y][x] = dist[y - 1][x] + w1
                if x > 0 and y > 0 and dist[y - 1][x - 1] + w2 < dist[y][x]:
                    dist[y][x] = dist[y - 1][x - 1] + w2
                if x < width - 1 and y > 0 and dist[y - 1][x + 1] + w2 < dist[y][x]:
                    dist[y][x] = dist[y - 1][x + 1] + w2

    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            if dist[y][x] > 0:
                if x < width - 1 and dist[y][x + 1] + w1 < dist[y][x]:
                    dist[y][x] = dist[y][x + 1] + w1
                if y < height - 1 and dist[y + 1][x] + w1 < dist[y][x]:
                    dist[y][x] = dist[y + 1][x] + w1
                if (
                    x < width - 1
                    and y < height - 1
                    and dist[y + 1][x + 1] + w2 < dist[y][x]
                ):
                    dist[y][x] = dist[y + 1][x + 1] + w2
                if x > 0 and y < height - 1 and dist[y + 1][x - 1] + w2 < dist[y][x]:
                    dist[y][x] = dist[y + 1][x - 1] + w2

    return dist


def geodesic_distance_transform(grid, mask):
    """Geodesic distance transform on a grid with mask."""
    height = len(grid)
    width = len(grid[0])

    INF = float("inf")
    dist = [[INF] * width for _ in range(height)]

    queue = []

    for y in range(height):
        for x in range(width):
            if mask[y][x] == 1:
                dist[y][x] = 0
                queue.append((x, y))

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        queue.sort(key=lambda p: dist[p[1]][p[0]])
        cx, cy = queue.pop(0)

        for dx, dy in neighbors:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == 1 and dist[ny][nx] == INF:
                    dist[ny][nx] = dist[cy][cx] + 1
                    queue.append((nx, ny))

    return dist


def voronoi_diagram(width, height, seeds, metric="euclidean"):
    """Compute Voronoi diagram given seeds."""
    INF = float("inf")
    region = [[-1] * width for _ in range(height)]
    dist_grid = [[INF] * width for _ in range(height)]

    def dist(p1, p2):
        if metric == "manhattan":
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    for y in range(height):
        for x in range(width):
            min_dist = INF
            nearest = -1
            for i, seed in enumerate(seeds):
                d = dist(seed, (x, y))
                if d < min_dist:
                    min_dist = d
                    nearest = i
            region[y][x] = nearest
            dist_grid[y][x] = min_dist

    return region


def hausdorff_distance(set1, set2):
    """Hausdorff distance between two point sets."""
    if not set1 or not set2:
        return 0.0

    def directed_distance(A, B):
        max_dist = 0
        for a in A:
            min_dist = min(
                math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for b in B
            )
            max_dist = max(max_dist, min_dist)
        return max_dist

    return max(directed_distance(set1, set2), directed_distance(set2, set1))


def earth_movers_distance(h1, h2):
    """Earth Mover's Distance between two histograms."""
    total = 0
    for i in range(len(h1)):
        total += abs(sum(h1[: i + 1]) - sum(h2[: i + 1]))
    return total
