"""Distance transforms and metrics - NumPy Centric Version with Anisotropic Support."""

import numpy as np
from scipy import ndimage


def manhattan_distance(p1, p2, spacing=(1.0, 1.0)):
    """Manhattan distance between two points with spacing."""
    return np.abs((np.asanyarray(p1) - np.asanyarray(p2)) * np.asanyarray(spacing)).sum()


def euclidean_distance(p1, p2, spacing=(1.0, 1.0)):
    """Euclidean distance between two points with spacing."""
    return np.linalg.norm((np.asanyarray(p1) - np.asanyarray(p2)) * np.asanyarray(spacing))


def manhattan_distance_transform(grid: np.ndarray, spacing=(1.0, 1.0)):
    """Manhattan distance transform with anisotropic support."""
    if not isinstance(grid, np.ndarray):
        grid = np.asanyarray(grid)
    if not np.any(grid == 1):
        return np.full(grid.shape, np.inf, dtype=np.float64)

    # distance_transform_cdt doesn't support sampling directly like EDT
    # but for cityblock, we can approximate or use a custom metric.
    # However, taxicab distance with weights is exactly what CDT does.
    result = ndimage.distance_transform_cdt(grid == 0, metric="cityblock")
    # Apply average spacing as a linear factor (simplification for Manhattan)
    avg_spacing = np.mean(spacing)
    return result.astype(np.float64) * avg_spacing


def euclidean_distance_transform(grid: np.ndarray, spacing=None):
    """Euclidean distance transform with anisotropic support."""
    if not isinstance(grid, np.ndarray):
        grid = np.asanyarray(grid)
    if not np.any(grid == 1):
        return np.zeros(grid.shape, dtype=np.float64)

    # sampling parameter in EDT handles anisotropic spacing
    result = ndimage.distance_transform_edt(grid == 0, sampling=spacing)
    return result.astype(np.float64)


def chamfer_distance_transform(grid: np.ndarray, weights=None):
    """Chamfer distance transform with configurable weights."""
    if not isinstance(grid, np.ndarray):
        grid = np.asanyarray(grid)
    if not np.any(grid == 1):
        return np.full(grid.shape, np.inf, dtype=np.float64)

    if weights is None:
        weights = [3, 4]

    w1, w2 = weights[0], weights[1]
    metric = np.array([[w2, w1, w2], [w1, 0, w1], [w2, w1, w2]])
    result = ndimage.distance_transform_cdt(grid == 0, metric=metric)
    return result.astype(np.float64)


def geodesic_distance_transform(grid: np.ndarray, mask: np.ndarray, spacing=(1.0, 1.0)):
    """Geodesic distance transform on a grid with mask and spacing."""
    if not isinstance(grid, np.ndarray) or not isinstance(mask, np.ndarray):
        grid = np.asanyarray(grid)
        mask = np.asanyarray(mask)

    height, width = grid.shape
    dist = np.full((height, width), np.inf, dtype=np.float64)
    dist[mask == 1] = 0

    from collections import deque
    y_coords, x_coords = np.where(mask == 1)
    queue = deque(zip(x_coords, y_coords))

    # Neighbors with their associated spacing-based distances
    # dx, dy, step_dist
    dy_s, dx_s = spacing
    neighbors = [(0, 1, dy_s), (0, -1, dy_s), (1, 0, dx_s), (-1, 0, dx_s)]

    while queue:
        cx, cy = queue.popleft()
        for dx, dy, dstep in neighbors:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny, nx] == 1 and dist[ny, nx] == np.inf:
                    dist[ny, nx] = dist[cy, cx] + dstep
                    queue.append((nx, ny))

    return dist


def voronoi_diagram(width, height, seeds: np.ndarray, metric="euclidean", spacing=(1.0, 1.0)):
    """Compute Voronoi diagram given seeds and anisotropic spacing."""
    if not isinstance(seeds, np.ndarray):
        seeds = np.asanyarray(seeds)
        
    if seeds.size == 0:
        return np.full((height, width), -1, dtype=np.int32)

    y, x = np.indices((height, width))
    dy_s, dx_s = spacing

    # scale indices and seeds by spacing
    sx = seeds[:, 0][:, np.newaxis, np.newaxis] * dx_s
    sy = seeds[:, 1][:, np.newaxis, np.newaxis] * dy_s
    grid_x = x * dx_s
    grid_y = y * dy_s

    if metric == "manhattan":
        distances = np.abs(grid_x - sx) + np.abs(grid_y - sy)
    else:
        distances = np.sqrt((grid_x - sx) ** 2 + (grid_y - sy) ** 2)

    region = np.argmin(distances, axis=0)
    return region


def hausdorff_distance(set1, set2, spacing=(1.0, 1.0)):
    """Hausdorff distance between two point sets with spacing."""
    a = np.asanyarray(set1) * np.asanyarray(spacing)
    b = np.asanyarray(set2) * np.asanyarray(spacing)
    
    if a.size == 0 or b.size == 0:
        return 0.0

    diff = a[:, np.newaxis, :] - b[np.newaxis, :, :]
    dist = np.linalg.norm(diff, axis=2)

    d_ab = np.max(np.min(dist, axis=1))
    d_ba = np.max(np.min(dist, axis=0))

    return float(max(d_ab, d_ba))


def earth_movers_distance(h1, h2):
    """Earth Mover's Distance between two histograms."""
    h1 = np.asanyarray(h1)
    h2 = np.asanyarray(h2)
    return float(np.sum(np.abs(np.cumsum(h1) - np.cumsum(h2))))
