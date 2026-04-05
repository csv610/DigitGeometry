"""Basic curve operations."""

import math


def point_in_polygon(point, polygon):
    """Ray Casting Algorithm for Point in Polygon."""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def convex_hull(points):
    """Convex hull using Graham scan."""
    if len(points) < 3:
        return list(points)

    points = sorted(set(points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def smooth_points(points, window_size=3, is_closed=False):
    """Smooth points using moving average."""
    if len(points) <= window_size:
        return points

    smoothed = []
    half = window_size // 2

    for i in range(len(points)):
        neighbors = []

        for j in range(-half, half + 1):
            if is_closed:
                idx = (i + j) % len(points)
            else:
                if 0 <= i + j < len(points):
                    idx = i + j
                else:
                    continue

            neighbors.append(points[idx])

        if neighbors:
            avg_x = sum(p[0] for p in neighbors) / len(neighbors)
            avg_y = sum(p[1] for p in neighbors) / len(neighbors)
            smoothed.append((avg_x, avg_y))

    return smoothed


def douglas_peucker(points, epsilon):
    """Douglas-Peucker Algorithm for polyline simplification."""
    if len(points) < 3:
        return points

    dmax = 0
    index = 0
    end = len(points) - 1

    for i in range(1, end):
        d = perpendicular_distance(points[i], points[0], points[end])
        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        rec_results1 = douglas_peucker(points[: index + 1], epsilon)
        rec_results2 = douglas_peucker(points[index:], epsilon)
        result = rec_results1[:-1] + rec_results2
    else:
        result = [points[0], points[end]]

    return result


def perpendicular_distance(point, line_start, line_end):
    """Calculates perpendicular distance from point to a line segment."""
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end

    if x1 == x2 and y1 == y2:
        return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

    numerator = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1))
    denominator = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return denominator and numerator / denominator or 0


def compute_tangents(points, k=3):
    """Estimate tangent vectors using local fitting."""
    n = len(points)
    tangents = []

    for i in range(n):
        start = max(0, i - k)
        end = min(n - 1, i + k)

        if start == end:
            tangents.append((0, 0))
            continue

        dx = points[end][0] - points[start][0]
        dy = points[end][1] - points[start][1]
        length = math.sqrt(dx * dx + dy * dy)

        if length > 0:
            tangents.append((dx / length, dy / length))
        else:
            tangents.append((0, 0))

    return tangents
