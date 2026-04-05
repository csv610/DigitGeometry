"""Curve analysis operations."""

import math


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


def curve_shortening_flow(points, iterations=1, step_size=0.1, is_closed=False):
    """Curve shortening flow - moves points in direction of curvature."""
    from digital_geometry.curves_basic import compute_tangents

    current = list(points)

    for _ in range(iterations):
        tangents = compute_tangents(current, k=1)

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
    from digital_geometry.curves_dsl import certify_dsls
    is_straight, _, _, _ = certify_dsls(points)
    return is_straight
