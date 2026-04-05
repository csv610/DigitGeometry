"""Edge detection algorithms."""

import math
import numpy as np
from scipy import ndimage


def sobel(grid):
    """Sobel edge detection."""
    grid_arr = np.asanyarray(grid, dtype=float)
    height, width = grid_arr.shape

    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)

    gx = ndimage.convolve(grid_arr, sobel_x, mode="constant", cval=0.0)
    gy = ndimage.convolve(grid_arr, sobel_y, mode="constant", cval=0.0)

    result = np.sqrt(gx**2 + gy**2)

    # Match original implementation's border behavior (1 to height-1)
    res_final = np.zeros_like(result)
    res_final[1 : height - 1, 1 : width - 1] = result[1 : height - 1, 1 : width - 1]

    return res_final.tolist()


def prewitt(grid):
    """Prewitt edge detection."""
    grid_arr = np.asanyarray(grid, dtype=float)
    height, width = grid_arr.shape

    prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
    prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float)

    gx = ndimage.convolve(grid_arr, prewitt_x, mode="constant", cval=0.0)
    gy = ndimage.convolve(grid_arr, prewitt_y, mode="constant", cval=0.0)

    result = np.sqrt(gx**2 + gy**2)

    # Match original implementation's border behavior
    res_final = np.zeros_like(result)
    res_final[1 : height - 1, 1 : width - 1] = result[1 : height - 1, 1 : width - 1]

    return res_final.tolist()


def roberts(grid):
    """Roberts cross edge detection."""
    grid_arr = np.asanyarray(grid, dtype=float)
    height, width = grid_arr.shape

    result = np.zeros_like(grid_arr)

    # gx = grid[y][x] - grid[y + 1][x + 1]
    # gy = grid[y][x + 1] - grid[y + 1][x]
    gx = grid_arr[:-1, :-1] - grid_arr[1:, 1:]
    gy = grid_arr[:-1, 1:] - grid_arr[1:, :-1]

    result[:-1, :-1] = np.sqrt(gx**2 + gy**2)

    return result.tolist()


def laplacian_4(grid):
    """4-neighbor Laplacian edge detection."""
    grid_arr = np.asanyarray(grid, dtype=float)
    height, width = grid_arr.shape

    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=float)
    result = np.abs(ndimage.convolve(grid_arr, kernel, mode="constant", cval=0.0))

    res_final = np.zeros_like(result)
    res_final[1 : height - 1, 1 : width - 1] = result[1 : height - 1, 1 : width - 1]

    return res_final.tolist()


def laplacian_8(grid):
    """8-neighbor Laplacian edge detection."""
    grid_arr = np.asanyarray(grid, dtype=float)
    height, width = grid_arr.shape

    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float)
    result = np.abs(ndimage.convolve(grid_arr, kernel, mode="constant", cval=0.0))

    res_final = np.zeros_like(result)
    res_final[1 : height - 1, 1 : width - 1] = result[1 : height - 1, 1 : width - 1]

    return res_final.tolist()


def canny(grid, low_threshold=50, high_threshold=150):
    """Canny edge detector."""
    grid_arr = np.asanyarray(grid, dtype=float)
    height, width = grid_arr.shape

    smoothed = np.array(gaussian_smooth(grid_arr, sigma=1.4))

    # Sobel for gradient
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)

    gx = ndimage.convolve(grid_arr, sobel_x, mode="constant", cval=0.0)
    gy = ndimage.convolve(grid_arr, sobel_y, mode="constant", cval=0.0)

    gradient = np.sqrt(gx**2 + gy**2)
    angle = np.rad2deg(np.arctan2(gx, gy))

    # Borders for gradient
    gradient[0, :] = 0
    gradient[-1, :] = 0
    gradient[:, 0] = 0
    gradient[:, -1] = 0

    edges = non_maximum_suppression(gradient.tolist(), angle.tolist())
    edges = double_threshold(edges, low_threshold, high_threshold)
    edges = hysteresis_threshold(edges)

    return edges


def gaussian_smooth(grid, sigma=1.0):
    """Gaussian smoothing."""
    grid_arr = np.asanyarray(grid, dtype=float)

    size = int(2 * math.ceil(3 * sigma) + 1)
    half = size // 2

    y, x = np.mgrid[-half : half + 1, -half : half + 1]
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2)) / (2 * np.pi * sigma**2)

    result = ndimage.convolve(grid_arr, kernel, mode="constant", cval=0.0)

    return result.tolist()


def non_maximum_suppression(gradient, angle):
    """Non-maximum suppression for Canny."""
    gradient = np.asanyarray(gradient)
    angle = np.asanyarray(angle)
    height, width = gradient.shape
    result = np.zeros_like(gradient)

    angle = angle % 180

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            ang = angle[y, x]

            if (0 <= ang < 22.5) or (157.5 <= ang <= 180):
                neighbors = [gradient[y, x - 1], gradient[y, x + 1]]
            elif 22.5 <= ang < 67.5:
                neighbors = [gradient[y - 1, x + 1], gradient[y + 1, x - 1]]
            elif 67.5 <= ang < 112.5:
                neighbors = [gradient[y - 1, x], gradient[y + 1, x]]
            else:
                neighbors = [gradient[y - 1, x - 1], gradient[y + 1, x + 1]]

            if gradient[y, x] >= max(neighbors):
                result[y, x] = gradient[y, x]

    return result.tolist()


def double_threshold(gradient, low, high):
    """Double thresholding for Canny."""
    gradient = np.asanyarray(gradient)
    result = np.zeros(gradient.shape, dtype=int)

    result[gradient >= high] = 2
    result[(gradient >= low) & (gradient < high)] = 1

    return result.tolist()


def hysteresis_threshold(edges):
    """Hysteresis thresholding for Canny."""
    edges = np.asanyarray(edges)
    height, width = edges.shape
    result = np.zeros_like(edges)

    # A simple way to do hysteresis is using binary_dilation on high pixels restricted to weak pixels
    # but to maintain exact behavior we might need to be careful.
    # The original implementation only does ONE pass.

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if edges[y, x] == 2:
                result[y, x] = 1
            elif edges[y, x] == 1:
                if np.any(edges[y - 1 : y + 2, x - 1 : x + 2] == 2):
                    result[y, x] = 1

    return result.tolist()

