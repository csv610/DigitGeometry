"""Persistent homology operations."""

import heapq


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
