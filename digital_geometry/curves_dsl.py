"""Digital Straight Line Segment (DSLS) operations."""

import math


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
