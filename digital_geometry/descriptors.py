"""Shape descriptors and features."""

import math
import cmath


def compute_hu_moments(grid):
    """Compute Hu's 7 invariant moments."""
    height = len(grid)
    width = len(grid[0])

    m00 = sum(sum(row) for row in grid)
    if m00 == 0:
        return [0] * 7

    m10 = sum(y * sum(row) for y, row in enumerate(grid))
    m01 = sum(x * sum(col) for x, col in enumerate(zip(*grid)))

    xc = m10 / m00
    yc = m01 / m00

    def central_moment(p, q):
        total = 0
        for y in range(height):
            for x in range(width):
                total += grid[y][x] * (x - xc) ** p * (y - yc) ** q
        return total

    eta20 = central_moment(2, 0) / m00
    eta02 = central_moment(0, 2) / m00
    eta11 = central_moment(1, 1) / m00
    eta30 = central_moment(3, 0) / m00
    eta03 = central_moment(0, 3) / m00
    eta21 = central_moment(2, 1) / m00
    eta12 = central_moment(1, 2) / m00

    hu = [
        eta20 + eta02,
        (eta20 - eta02) ** 2 + 4 * eta11**2,
        (eta30 - 3 * eta12) ** 2 + (3 * eta21 - eta03) ** 2,
        (eta30 + eta12) ** 2 + (eta21 + eta03) ** 2,
        (eta30 - 3 * eta12)
        * (eta30 + eta12)
        * ((eta30 + eta12) ** 2 - 3 * (eta21 + eta03) ** 2)
        + (3 * eta21 - eta03)
        * (eta21 + eta03)
        * (3 * (eta30 + eta12) ** 2 - (eta21 + eta03) ** 2),
        (eta20 - eta02) * ((eta30 + eta12) ** 2 - (eta21 + eta03) ** 2)
        + 4 * eta11 * (eta30 + eta12) * (eta21 + eta03),
        (3 * eta21 - eta03)
        * (eta30 + eta12)
        * ((eta30 + eta12) ** 2 - 3 * (eta21 + eta03) ** 2)
        - (eta30 - 3 * eta12)
        * (eta21 + eta03)
        * (3 * (eta30 + eta12) ** 2 - (eta21 + eta03) ** 2),
    ]

    return [abs(x) for x in hu]


def compute_zernike_moments(grid, radius, degree=4):
    """Compute Zernike moments."""
    height = len(grid)
    width = len(grid[0])
    cx, cy = width / 2, height / 2

    moments = []

    for n in range(degree + 1):
        for m in range(-n, n + 1, 2):
            if abs(m) <= n:
                moment = 0

                for y in range(height):
                    for x in range(width):
                        if grid[y][x] != 0:
                            nx = (x - cx) / radius
                            ny = (y - cy) / radius

                            rho = math.sqrt(nx**2 + ny**2)
                            theta = math.atan2(ny, nx)

                            if rho <= 1:
                                zernike = zernike_polynomial(n, m, rho, theta)
                                moment += grid[y][x] * zernike

                moments.append(abs(moment))

    return moments


def zernike_polynomial(n, m, rho, theta):
    """Zernike polynomial R_n^m(rho) * exp(i*m*theta)."""
    from math import factorial

    result = 0
    k = (n - abs(m)) // 2

    for s in range(k + 1):
        numerator = ((-1) ** s) * factorial(n - s)
        denominator = (
            factorial(s)
            * factorial((n + abs(m)) // 2 - s)
            * factorial((n - abs(m)) // 2 - s)
        )
        result += (numerator / denominator) * (rho ** (n - 2 * s))

    return result * cmath.exp(1j * m * theta)


def fourier_descriptors(points, n_descriptors=10):
    """Compute Fourier descriptors for a closed contour (vectorized)."""
    import numpy as np
    if len(points) < 2:
        return []

    complex_points = np.array([complex(x, y) for x, y in points])
    dft = np.fft.fft(complex_points)
    
    n = len(points)
    descriptors = np.abs(dft[1:min(n_descriptors + 1, n)])
    
    return descriptors.tolist()


def shape_context_descriptor(points, n_bins_r=5, n_bins_theta=12):
    """Compute shape context descriptor for each point."""
    n = len(points)
    descriptors = []

    for i in range(n):
        histograms = []

        for j in range(n):
            if i == j:
                continue

            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]

            r = math.sqrt(dx**2 + dy**2)
            theta = math.atan2(dy, dx)

            r_bin = min(int(r * n_bins_r), n_bins_r - 1)
            theta_bin = (
                int((theta + math.pi) / (2 * math.pi) * n_bins_theta) % n_bins_theta
            )

            histograms.append((r_bin, theta_bin))

        hist = [[0] * n_bins_theta for _ in range(n_bins_r)]
        for r_bin, theta_bin in histograms:
            hist[r_bin][theta_bin] += 1

        descriptors.append(hist)

    return descriptors


def generalized_hough_transform(grid, template_points):
    """Generalized Hough Transform for shape detection."""
    height = len(grid)
    width = len(grid[0])

    template_cx = int(sum(p[0] for p in template_points) / len(template_points))
    template_cy = int(sum(p[1] for p in template_points) / len(template_points))

    template_vectors = [
        (p[0] - template_cx, p[1] - template_cy) for p in template_points
    ]

    accumulator = [[0] * width for _ in range(height)]

    edge_points = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                if (
                    (y > 0 and grid[y - 1][x] == 0)
                    or (y < height - 1 and grid[y + 1][x] == 0)
                    or (x > 0 and grid[y][x - 1] == 0)
                    or (x < width - 1 and grid[y][x + 1] == 0)
                ):
                    edge_points.append((x, y))

    for ex, ey in edge_points:
        for tx, ty in template_vectors:
            bx, by = ex - tx, ey - ty
            if 0 <= bx < width and 0 <= by < height:
                accumulator[by][bx] += 1

    return accumulator


def detect_critical_points(grid):
    """Detect peaks, pits, and saddles in a grid."""
    height = len(grid)
    width = len(grid[0])

    peaks = []
    pits = []
    saddles = []

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            center = grid[y][x]
            neighbors = [
                grid[y - 1][x - 1],
                grid[y - 1][x],
                grid[y - 1][x + 1],
                grid[y][x - 1],
                grid[y][x + 1],
                grid[y + 1][x - 1],
                grid[y + 1][x],
                grid[y + 1][x + 1],
            ]

            higher = sum(1 for n in neighbors if n > center)
            lower = sum(1 for n in neighbors if n < center)

            if higher == 8:
                pits.append((x, y))
            elif lower == 8:
                peaks.append((x, y))
            elif higher > 0 and lower > 0:
                saddles.append((x, y))

    return {"peaks": peaks, "pits": pits, "saddles": saddles}
