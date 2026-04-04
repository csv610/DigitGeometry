"""Graph cuts and segmentation."""

import heapq


def min_cut_max_flow(capacity, source, sink):
    """Min-cut max-flow algorithm using Edmonds-Karp."""
    height = len(capacity)
    width = len(capacity[0])

    def bfs():
        parent = {source: None}
        visited = {source}
        queue = [source]

        while queue:
            u = queue.pop(0)

            for v in range(height):
                if v not in visited and capacity[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        break

        if sink not in parent:
            return None

        path = []
        v = sink
        while parent[v] is not None:
            path.append(v)
            v = parent[v]
        path.append(source)
        path.reverse()

        return path

    flow = 0

    while True:
        path = bfs()
        if path is None:
            break

        min_capacity = min(capacity[path[i]][path[i + 1]] for i in range(len(path) - 1))

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity[u][v] -= min_capacity
            capacity[v][u] += min_capacity

        flow += min_capacity

    return flow


def graph_cut_segmentation(grid, fg_seeds, bg_seeds):
    """Graph cut segmentation with foreground/background seeds."""
    height = len(grid)
    width = len(grid[0])
    n = height * width

    source = n
    sink = n + 1

    capacity = [[0] * (n + 2) for _ in range(n + 2)]

    for y in range(height):
        for x in range(width):
            idx = y * width + x
            pixel = grid[y][x]

            if (x, y) in fg_seeds:
                capacity[source][idx] = 1000
            elif (x, y) in bg_seeds:
                capacity[idx][sink] = 1000
            else:
                capacity[source][idx] = pixel
                capacity[idx][sink] = 255 - pixel

    neighbors = [(0, 1), (1, 0)]

    for y in range(height):
        for x in range(width):
            idx = y * width + x

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy

                if 0 <= nx < width and 0 <= ny < height:
                    nidx = ny * width + nx
                    diff = abs(grid[y][x] - grid[ny][nx])
                    w = diff + 1

                    capacity[idx][nidx] = w
                    capacity[nidx][idx] = w

    min_cut_max_flow(capacity, source, sink)

    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            idx = y * width + x

            if capacity[idx][source] > 0:
                result[y][x] = 1

    return result


def watershed_transform(grid):
    """Watershed transform for image segmentation."""
    height = len(grid)
    width = len(grid[0])

    labels = [[-1] * width for _ in range(height)]
    label = 0
    heap = []

    for y in range(height):
        for x in range(width):
            heapq.heappush(heap, (grid[y][x], x, y))

    while heap:
        _, x, y = heapq.heappop(heap)

        if labels[y][x] != -1:
            continue

        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and labels[ny][nx] != -1:
                neighbors.append(labels[ny][nx])

        if not neighbors:
            label += 1
            labels[y][x] = label
        else:
            labels[y][x] = min(neighbors)

    return labels
