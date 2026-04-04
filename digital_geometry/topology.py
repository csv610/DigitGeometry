"""Topological operations on digital images."""

import heapq


def count_connected_components(grid, target_value=1, connectivity=4):
    """Counts connected components of target_value using BFS."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    count = 0

    if connectivity == 8:
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

    for y in range(height):
        for x in range(width):
            if grid[y][x] == target_value and (x, y) not in visited:
                count += 1
                queue = [(x, y)]
                visited.add((x, y))
                while queue:
                    cx, cy = queue.pop(0)
                    for dx, dy in neighbors:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if grid[ny][nx] == target_value and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
    return count


def calculate_topology(grid, connectivity=4):
    """Calculates Betti numbers (b0, b1) and Euler characteristic."""
    b0 = count_connected_components(grid, target_value=1, connectivity=connectivity)

    inverted = [[1 - grid[y][x] for x in range(len(grid[0]))] for y in range(len(grid))]
    bg_components = count_connected_components(
        inverted, target_value=1, connectivity=connectivity
    )
    b1 = bg_components - 1 if b0 > 0 else 0

    return {"b0": b0, "b1": b1, "euler": b0 - b1}


class UnionFindPersistence:
    """Custom Disjoint Set Union for tracking persistent homology features."""

    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.birth = {}

    def make_set(self, i, birth_time):
        self.parent[i] = i
        self.rank[i] = 0
        self.birth[i] = birth_time

    def find(self, i):
        if i not in self.parent:
            return None
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j, death_val):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i is None or root_j is None:
            return

        if root_i == root_j:
            return

        if self.rank[root_i] < self.rank[root_j]:
            root_i, root_j = root_j, root_i

        self.parent[root_j] = root_i
        if self.rank[root_i] == self.rank[root_j]:
            self.rank[root_i] += 1


def compute_h0_persistence(grid, connectivity=4):
    """Compute H0 persistence (connected components)."""
    height = len(grid)
    width = len(grid[0])
    INF = float("inf")
    dist = [[INF] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                dist[y][x] = 0

    uf = UnionFindPersistence()
    edges = []

    neighbors = (
        [(0, 1), (1, 0)] if connectivity == 4 else [(0, 1), (1, 0), (1, 1), (1, -1)]
    )

    for y in range(height):
        for x in range(width):
            idx = y * width + x
            uf.make_set(idx, 0)

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    nidx = ny * width + nx
                    w = abs(grid[y][x] - grid[ny][nx])
                    edges.append((w, idx, nidx))

    edges.sort(key=lambda e: e[0])

    pairs = []
    for w, i, j in edges:
        if uf.find(i) != uf.find(j):
            birth_i = uf.birth[uf.find(i)]
            birth_j = uf.birth[uf.find(j)]
            death = w
            pairs.append((birth_i, death))
            pairs.append((birth_j, death))
            uf.union(i, j, death)

    return sorted(pairs, key=lambda x: x[0])


def compute_h1_persistence(grid, connectivity=4):
    """Compute H1 persistence (holes/loops)."""
    height = len(grid)
    width = len(grid[0])
    INF = float("inf")
    dist = [[INF] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 0:
                dist[y][x] = 0

    uf = UnionFindPersistence()
    edges = []

    neighbors = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for y in range(height):
        for x in range(width):
            idx = y * width + x
            uf.make_set(idx, 0)

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    nidx = ny * width + nx
                    w = max(dist[y][x], dist[ny][nx])
                    edges.append((w, idx, nidx))

    edges.sort(key=lambda e: e[0])

    pairs = []
    for w, i, j in edges:
        if uf.find(i) != uf.find(j):
            birth_i = uf.birth[uf.find(i)]
            birth_j = uf.birth[uf.find(j)]
            death = w
            pairs.append((birth_i, death))
            pairs.append((birth_j, death))
            uf.union(i, j, death)

    return sorted(pairs, key=lambda x: x[0])


def connected_components_3d(volume, target_value=1, connectivity=6):
    """3D connected component labeling."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    if connectivity == 6:
        neighbors = [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]
    else:
        neighbors = [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
            (1, 1, 0),
            (1, -1, 0),
            (-1, 1, 0),
            (-1, -1, 0),
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, 1),
            (-1, 0, -1),
            (0, 1, 1),
            (0, 1, -1),
            (0, -1, 1),
            (0, -1, -1),
            (1, 1, 1),
            (1, -1, 1),
            (-1, 1, 1),
            (-1, -1, 1),
            (1, 1, -1),
            (1, -1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
        ]

    label = [[[0] * width for _ in range(height)] for _ in range(depth)]
    current_label = 0

    def bfs(start_x, start_y, start_z):
        nonlocal current_label
        current_label += 1
        queue = [(start_x, start_y, start_z)]
        label[start_z][start_y][start_x] = current_label

        while queue:
            cx, cy, cz = queue.pop(0)

            for dx, dy, dz in neighbors:
                nx, ny, nz = cx + dx, cy + dy, cz + dz

                if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                    if volume[nz][ny][nx] == target_value and label[nz][ny][nx] == 0:
                        label[nz][ny][nx] = current_label
                        queue.append((nx, ny, nz))

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == target_value and label[z][y][x] == 0:
                    bfs(x, y, z)

    return label, current_label


def compute_surface_curvatures(grid):
    """Compute discrete surface curvatures."""
    height = len(grid)
    width = len(grid[0])
    curvatures = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            laplacian = (
                grid[y - 1][x]
                + grid[y + 1][x]
                + grid[y][x - 1]
                + grid[y][x + 1]
                - 4 * grid[y][x]
            )
            gradient_magnitude = math.sqrt(
                (grid[y][x + 1] - grid[y][x - 1]) ** 2
                + (grid[y + 1][x] - grid[y - 1][x]) ** 2
            )
            curvatures[y][x] = laplacian / (1 + gradient_magnitude)

    return curvatures


import math
