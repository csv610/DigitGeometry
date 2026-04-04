"""Pathfinding algorithms."""

import heapq
from digital_geometry.distance import manhattan_distance, euclidean_distance


def a_star(grid, start, end, allow_diagonal=False):
    """A* Search Algorithm for finding the shortest path in a 2D grid."""
    height = len(grid)
    width = len(grid[0])

    if not (
        0 <= start[0] < width
        and 0 <= start[1] < height
        and grid[start[1]][start[0]] == 0
    ):
        return []
    if not (0 <= end[0] < width and 0 <= end[1] < height and grid[end[1]][end[0]] == 0):
        return []

    heuristic = euclidean_distance if allow_diagonal else manhattan_distance

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    if allow_diagonal:
        neighbors = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
    else:
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        cx, cy = current
        for dx, dy in neighbors:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 0:
                tentative_g = g_score[current] + (
                    math.sqrt(dx * dx + dy * dy) if allow_diagonal else 1
                )

                if tentative_g < g_score.get((nx, ny), float("inf")):
                    came_from[(nx, ny)] = current
                    g_score[(nx, ny)] = tentative_g
                    f_score[(nx, ny)] = tentative_g + heuristic((nx, ny), end)
                    heapq.heappush(open_set, (f_score[(nx, ny)], (nx, ny)))

    return []


def fast_marching_method(grid, seeds):
    """Fast Marching Method for geodesic distance computation."""
    height = len(grid)
    width = len(grid[0])

    INF = float("inf")
    times = [[INF] * width for _ in range(height)]

    for sx, sy in seeds:
        if 0 <= sx < width and 0 <= sy < height:
            times[sy][sx] = 0.0

    heap = []
    for sx, sy in seeds:
        if 0 <= sx < width and 0 <= sy < height:
            heapq.heappush(heap, (0, sx, sy))

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while heap:
        t, x, y = heapq.heappop(heap)

        if t > times[y][x]:
            continue

        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height:
                speed = max(grid[ny][nx], 0.01)
                dist = math.sqrt(dx * dx + dy * dy) / speed
                new_time = t + dist

                if new_time < times[ny][nx]:
                    times[ny][nx] = new_time
                    heapq.heappush(heap, (new_time, nx, ny))

    return times


import math
