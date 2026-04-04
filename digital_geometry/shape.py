"""Polygon operations and shape analysis."""

import math


def polygon_area(polygon):
    """Calculate polygon area using Shoelace formula."""
    n = len(polygon)
    if n < 3:
        return 0.0

    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i][0] * polygon[j][1]
        area -= polygon[j][0] * polygon[i][1]

    return abs(area) / 2.0


def polygon_centroid(polygon):
    """Calculate polygon centroid."""
    n = len(polygon)
    if n < 3:
        return (0.0, 0.0)

    cx = 0.0
    cy = 0.0
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        cross = polygon[i][0] * polygon[j][1] - polygon[j][0] * polygon[i][1]
        area += cross
        cx += (polygon[i][0] + polygon[j][0]) * cross
        cy += (polygon[i][1] + polygon[j][1]) * cross

    area = abs(area) / 2.0
    if area == 0:
        return (polygon[0][0], polygon[0][1])

    cx /= 6 * area
    cy /= 6 * area

    return (cx, cy)


def point_to_segment_distance(px, py, x1, y1, x2, y2):
    """Calculate distance from point to line segment."""
    dx = x2 - x1
    dy = y2 - y1
    length_sq = dx * dx + dy * dy

    if length_sq == 0:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return math.sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)


def point_to_polygon_distance(px, py, polygon):
    """Calculate minimum distance from point to polygon boundary."""
    if len(polygon) < 3:
        return 0.0

    min_dist = float("inf")
    for i in range(len(polygon)):
        j = (i + 1) % len(polygon)
        x1, y1 = polygon[i]
        x2, y2 = polygon[j]
        dist = point_to_segment_distance(px, py, x1, y1, x2, y2)
        min_dist = min(min_dist, dist)

    return min_dist


def polygon_perimeter(polygon):
    """Calculate polygon perimeter."""
    n = len(polygon)
    if n < 3:
        return 0.0

    perimeter = 0.0
    for i in range(n):
        j = (i + 1) % n
        dx = polygon[j][0] - polygon[i][0]
        dy = polygon[j][1] - polygon[i][1]
        perimeter += math.sqrt(dx * dx + dy * dy)

    return perimeter


def bounding_box(points):
    """Calculate axis-aligned bounding box."""
    if not points:
        return (0, 0, 0, 0)

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    return (min(xs), min(ys), max(xs), max(ys))


def bounding_box_area(points):
    """Calculate bounding box area."""
    xmin, ymin, xmax, ymax = bounding_box(points)
    return (xmax - xmin) * (ymax - ymin)


def shape_circularity(polygon):
    """Calculate circularity: 4*pi*area / perimeter^2."""
    area = polygon_area(polygon)
    perimeter = polygon_perimeter(polygon)

    if perimeter == 0:
        return 0.0

    return 4 * math.pi * area / (perimeter**2)


def shape_solidity(polygon):
    """Calculate solidity: area / convex_hull_area."""
    area = polygon_area(polygon)
    from digital_geometry import convex_hull

    hull = convex_hull(polygon)

    if hull and len(hull) >= 3:
        hull_area = polygon_area(hull)
        if hull_area > 0:
            return area / hull_area

    return 1.0


def shape_aspect_ratio(points):
    """Calculate aspect ratio of bounding box."""
    xmin, ymin, xmax, ymax = bounding_box(points)
    width = xmax - xmin
    height = ymax - ymin

    if height == 0:
        return 0.0

    return width / height


def shape_eccentricity(points):
    """Calculate eccentricity of shape (ratio of major/minor axes)."""
    if len(points) < 3:
        return 0.0

    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    mean_x = sum(x_coords) / len(points)
    mean_y = sum(y_coords) / len(points)

    xx = sum((x - mean_x) ** 2 for x in x_coords)
    yy = sum((y - mean_y) ** 2 for y in y_coords)
    xy = sum((x - mean_x) * (y - mean_y) for x, y in points)

    eigenvalue_1 = (xx + yy) / 2 + math.sqrt(((xx - yy) / 2) ** 2 + xy**2)
    eigenvalue_2 = (xx + yy) / 2 - math.sqrt(((xx - yy) / 2) ** 2 + xy**2)

    if eigenvalue_2 == 0:
        return 0.0

    return math.sqrt(eigenvalue_1 / eigenvalue_2)


def shape_extent(points, bounding_rect=None):
    """Calculate extent: area / bounding_box_area."""
    area = 0
    for i in range(len(points)):
        j = (i + 1) % len(points)
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2

    if bounding_rect is None:
        bounding_rect = bounding_box(points)

    xmin, ymin, xmax, ymax = bounding_rect
    bbox_area = (xmax - xmin) * (ymax - ymin)

    if bbox_area == 0:
        return 0.0

    return area / bbox_area


def convex_hull_perimeter(polygon):
    """Calculate convex hull perimeter."""
    from digital_geometry import convex_hull

    hull = convex_hull(polygon)
    return polygon_perimeter(hull)


def shape_compactness(polygon):
    """Calculate compactness: perimeter^2 / area."""
    area = polygon_area(polygon)
    perimeter = polygon_perimeter(polygon)

    if area == 0:
        return 0.0

    return (perimeter**2) / (4 * math.pi * area)
