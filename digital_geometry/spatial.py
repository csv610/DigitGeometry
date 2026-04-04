"""Spatial data structures."""

from digital_geometry.distance import euclidean_distance
from digital_geometry.descriptors import detect_critical_points


class Quadtree:
    """Quadtree for 2D spatial indexing."""

    def __init__(self, bounds, capacity=4):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def insert(self, point):
        x, y = point
        bx, by, bw, bh = self.bounds

        if not (bx <= x < bx + bw and by <= y < by + bh):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        return (
            self.northeast.insert(point)
            or self.northwest.insert(point)
            or self.southeast.insert(point)
            or self.southwest.insert(point)
        )

    def subdivide(self):
        x, y, w, h = self.bounds
        half_w = w // 2
        half_h = h // 2

        self.northeast = Quadtree((x + half_w, y, half_w, half_h), self.capacity)
        self.northwest = Quadtree((x, y, half_w, half_h), self.capacity)
        self.southeast = Quadtree(
            (x + half_w, y + half_h, half_w, half_h), self.capacity
        )
        self.southwest = Quadtree((x, y + half_h, half_w, half_h), self.capacity)
        self.divided = True


class Octree:
    """Octree for 3D spatial indexing."""

    def __init__(self, bounds, capacity=4):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        x, y, z = point
        bx, by, bz, bw, bh, bd = self.bounds

        if not (bx <= x < bx + bw and by <= y < by + bh and bz <= z < bz + bd):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(point):
                return True
        return False

    def subdivide(self):
        x, y, z, w, h, d = self.bounds
        hw, hh, hd = w // 2, h // 2, d // 2

        self.children = []
        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    child_bounds = (x + dx * hw, y + dy * hh, z + dz * hd, hw, hh, hd)
                    self.children.append(Octree(child_bounds, self.capacity))
        self.divided = True


class Quadtree:
    """Quadtree for 2D spatial indexing."""

    def __init__(self, bounds, capacity=4):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        x, y = point
        bx, by, bw, bh = self.bounds

        if not (bx <= x < bx + bw and by <= y < by + bh):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        return (
            self.northeast.insert(point)
            or self.northwest.insert(point)
            or self.southeast.insert(point)
            or self.southwest.insert(point)
        )

    def subdivide(self):
        x, y, w, h = self.bounds
        half_w = w // 2
        half_h = h // 2

        self.northeast = Quadtree((x + half_w, y, half_w, half_h), self.capacity)
        self.northwest = Quadtree((x, y, half_w, half_h), self.capacity)
        self.southeast = Quadtree(
            (x + half_w, y + half_h, half_w, half_h), self.capacity
        )
        self.southwest = Quadtree((x, y + half_h, half_w, half_h), self.capacity)
        self.divided = True


def compute_reeb_graph(grid):
    """Compute Reeb graph from height function."""
    height = len(grid)
    width = len(grid[0])

    nodes = []
    edges = []

    for y in range(height):
        for x in range(width):
            critical = detect_critical_points([[grid[y][x]]])

            if critical["peaks"]:
                nodes.append({"type": "peak", "x": x, "y": y, "value": grid[y][x]})
            elif critical["pits"]:
                nodes.append({"type": "pit", "x": x, "y": y, "value": grid[y][x]})

    return {"nodes": nodes, "edges": edges}


def jump_flooding_dt(grid):
    """Jump Flooding Algorithm for distance transform."""
    height = len(grid)
    width = len(grid[0])

    seeds = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                seeds.append((x, y))

    dist = [[float("inf")] * width for _ in range(height)]
    parent = [[None] * width for _ in range(height)]

    for x, y in seeds:
        dist[y][x] = 0
        parent[y][x] = (x, y)

    for step in [max(1, width // 4), max(1, width // 8), max(1, width // 16), 1]:
        for y in range(height):
            for x in range(width):
                if dist[y][x] == 0:
                    continue

                for dy in [-step, 0, step]:
                    for dx in [-step, 0, step]:
                        if dx == 0 and dy == 0:
                            continue

                        nx, ny = x + dx, y + dy

                        if 0 <= nx < width and 0 <= ny < height:
                            if dist[ny][nx] != float("inf"):
                                d = euclidean_distance((x, y), (nx, ny))

                                if d < dist[y][x]:
                                    dist[y][x] = d
                                    parent[y][x] = (nx, ny)

    return dist


def compute_sdf(grid):
    """Signed Distance Field."""
    height = len(grid)
    width = len(grid[0])

    dist = [[0.0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                dist[y][x] = 0
            else:
                min_dist = float("inf")

                for yy in range(height):
                    for xx in range(width):
                        if grid[yy][xx] == 1:
                            d = euclidean_distance((x, y), (xx, yy))
                            min_dist = min(min_dist, d)

                dist[y][x] = -min_dist

    return dist
