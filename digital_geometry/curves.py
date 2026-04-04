"""Curve processing and analysis."""

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


def menger_curvature(p1, p2, p3):
    """Menger curvature for three points."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

    a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    b = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
    c = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    if a * b * c == 0:
        return 0

    return 2 * area / (a * b * c)


def compute_curvature(points, is_closed=False):
    """Compute discrete curvature along a curve."""
    if len(points) < 3:
        return []

    curvatures = []

    for i in range(len(points)):
        if is_closed:
            p1 = points[(i - 1) % len(points)]
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]
        else:
            if i == 0:
                p1 = points[0]
                p2 = points[1]
                p3 = points[2]
            elif i == len(points) - 1:
                p1 = points[-3]
                p2 = points[-2]
                p3 = points[-1]
            else:
                p1 = points[i - 1]
                p2 = points[i]
                p3 = points[i + 1]

        curvatures.append(menger_curvature(p1, p2, p3))

    return curvatures


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


def curve_shortening_flow(points, iterations=1, step_size=0.1, is_closed=False):
    """Curve shortening flow - moves points in direction of curvature."""
    from digital_geometry.curves import estimate_tangents

    current = list(points)

    for _ in range(iterations):
        tangents = estimate_tangents(current, k=1)

        for i in range(len(current)):
            if is_closed or (i > 0 and i < len(current) - 1):
                tangent = tangents[i]
                curvature = compute_curvature(current, is_closed)[i]

                nx = current[i][0] - step_size * curvature * tangent[0]
                ny = current[i][1] - step_size * curvature * tangent[1]
                current[i] = (nx, ny)

    return current


def is_digitally_straight(points):
    """Check if a sequence of points forms a digital straight line."""
    if len(points) < 2:
        return True

    x0, y0 = points[0]
    x1, y1 = points[-1]

    dx = x1 - x0
    dy = y1 - y0

    if dx == 0:
        for x, y in points:
            if x != x0:
                return False
        return True

    if dy == 0:
        for x, y in points:
            if y != y0:
                return False
        return True

    for x, y in points:
        if (y - y0) * dx != (x - x0) * dy:
            return False

    return True


def estimate_tangents(points, k=3):
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


def certify_dsls(points):
    """Certify if points form a digital straight line segment (DSLS).

    Uses the ring arithmetic method to verify DSLS property.
    Returns (is_straight, a, b, mu) where ax - by = mu defines the DSL.
    """
    if len(points) < 2:
        return True, 0, 0, 0

    x0, y0 = points[0]
    xn, yn = points[-1]

    dx = xn - x0
    dy = yn - y0

    if dx == 0 and dy == 0:
        return True, 1, 0, x0

    a = dy
    b = -dx
    mu_min = a * x0 + b * y0
    mu_max = a * xn + b * yn

    if mu_min > mu_max:
        mu_min, mu_max = mu_max, mu_min
        a, b = -a, -b

    mu = mu_min

    for x, y in points:
        val = a * x + b * y
        if val < mu_min or val > mu_max:
            return False, a, b, mu

    return True, a, b, mu


def dsls_Arithmetical_Distance(points):
    """Compute the arithmetical thickness of a DSLS.

    Returns the maximum deviation from the defining straight line.
    """
    if len(points) < 2:
        return 0

    is_straight, a, b, mu = certify_dsls(points)
    if is_straight:
        return 0

    a, b = abs(a), abs(b)

    max_dev = 0
    for x, y in points:
        val = a * x + b * y - mu
        dev = abs(val) / math.sqrt(a * a + b * b)
        max_dev = max(max_dev, dev)

    return max_dev


def naive_dsls_recognition(points, debug=False):
    """Naive DSL recognition algorithm.

    Returns (is_dsl, a, b, mu) or None if not a DSL.
    """
    n = len(points)
    if n < 2:
        return True, 1, 0, 0

    x0, y0 = points[0]
    xn, yn = points[-1]

    dx = xn - x0
    dy = yn - y0

    if dx == 0 and dy == 0:
        return True, 1, 0, 0

    def lower_bracket(x, y, a, b):
        return a * x + b * y

    def upper_bracket(x, y, a, b):
        return a * x + b * y

    a = dy
    b = -dx

    mu1 = a * x0 + b * y0
    mu2 = a * xn + b * yn

    if mu1 > mu2:
        mu1, mu2 = mu2, mu1
        a, b = -a, -b

    mu = mu1

    for x, y in points:
        val = a * x + b * y
        if val < mu1 or val > mu2:
            if debug:
                print(f"Failed at ({x},{y}): {val} not in [{mu1},{mu2}]")
            return None

    return True, a, b, mu
