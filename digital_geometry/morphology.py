"""Morphological operations."""

import numpy as np
from scipy import ndimage

SE_SQUARE_3X3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
SE_CROSS_3X3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]


def dilate(grid, se=SE_SQUARE_3X3):
    """Morphological dilation."""
    grid_arr = np.asanyarray(grid)
    se_arr = np.asanyarray(se)
    result = ndimage.binary_dilation(grid_arr, structure=se_arr)
    return result.astype(int).tolist()


def erode(grid, se=SE_SQUARE_3X3):
    """Morphological erosion."""
    grid_arr = np.asanyarray(grid)
    se_arr = np.asanyarray(se)
    # border_value=0 ensures that erosion fails if the SE extends outside the grid
    result = ndimage.binary_erosion(grid_arr, structure=se_arr, border_value=0)
    return result.astype(int).tolist()


def morph_opening(grid, se=SE_SQUARE_3X3):
    """Opening: erosion followed by dilation."""
    grid_arr = np.asanyarray(grid)
    se_arr = np.asanyarray(se)
    result = ndimage.binary_opening(grid_arr, structure=se_arr, iterations=1)
    return result.astype(int).tolist()


def morph_closing(grid, se=SE_SQUARE_3X3):
    """Closing: dilation followed by erosion."""
    grid_arr = np.asanyarray(grid)
    se_arr = np.asanyarray(se)
    result = ndimage.binary_closing(grid_arr, structure=se_arr, iterations=1)
    return result.astype(int).tolist()


def morph_boundary(grid, se=SE_SQUARE_3X3):
    """Extracts the inner boundary of foreground shapes."""
    grid_arr = np.asanyarray(grid)
    eroded = np.asanyarray(erode(grid, se))
    boundary = (grid_arr == 1) & (eroded == 0)
    return boundary.astype(int).tolist()


def tophat(grid, se=SE_SQUARE_3X3):
    """Top-hat transform: extracts small bright features."""
    grid_arr = np.asanyarray(grid)
    opened = np.asanyarray(morph_opening(grid, se))
    result = np.maximum(0, grid_arr - opened)
    return result.tolist()


def bothat(grid, se=SE_SQUARE_3X3):
    """Bottom-hat transform: extracts small dark features."""
    grid_arr = np.asanyarray(grid)
    closed = np.asanyarray(morph_closing(grid, se))
    result = np.maximum(0, closed - grid_arr)
    return result.tolist()


def white_tophat(grid, se=SE_SQUARE_3X3):
    """White top-hat: extracts small bright features."""
    return tophat(grid, se)


def black_tophat(grid, se=SE_SQUARE_3X3):
    """Black top-hat: extracts small dark features."""
    return bothat(grid, se)


def create_square_se(size):
    """Create square structuring element."""
    return np.ones((size, size), dtype=int).tolist()


def morph_erode(grid, se):
    """Morphological erosion with custom SE."""
    return erode(grid, se)


def morphological_skeleton(grid):
    """Morphological skeleton via iterative erosion."""
    from digital_geometry.topology import count_connected_components

    grid_arr = np.asanyarray(grid)
    height, width = grid_arr.shape
    skeleton = np.zeros_like(grid_arr)
    temp_grid = grid_arr.copy()

    while True:
        eroded = np.asanyarray(erode(temp_grid.tolist()))

        if count_connected_components(eroded.tolist(), 1, 4) == 0:
            break

        boundary = np.asanyarray(morph_boundary(temp_grid.tolist()))
        skeleton[boundary == 1] = 1
        temp_grid = eroded

    return skeleton.tolist()


def geodesic_dilation(grid, mask, iterations=1):
    """Geodesic dilation: dilate within mask bounds."""
    grid_arr = np.asanyarray(grid)
    mask_arr = np.asanyarray(mask)
    result = grid_arr.copy()

    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

    for _ in range(iterations):
        dilated = ndimage.binary_dilation(result, structure=structure)
        result = dilated & (mask_arr == 1)

    return result.astype(int).tolist()


def geodesic_erosion(grid, mask, iterations=1):
    """Geodesic erosion: erode, then constrain to mask."""
    grid_arr = np.asanyarray(grid)
    mask_arr = np.asanyarray(mask)
    result = grid_arr.copy()

    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

    for _ in range(iterations):
        eroded = ndimage.binary_erosion(result, structure=structure, border_value=0)
        result = eroded & (mask_arr == 1)

    return result.astype(int).tolist()


def morph_internal_gradient(grid, se=SE_SQUARE_3X3):
    """Internal gradient: foreground - eroded."""
    grid_arr = np.asanyarray(grid)
    eroded = np.asanyarray(erode(grid, se))
    result = np.maximum(0, grid_arr - eroded)
    return result.tolist()


def morph_external_gradient(grid, se=SE_SQUARE_3X3):
    """External gradient: dilated - foreground."""
    grid_arr = np.asanyarray(grid)
    dilated = np.asanyarray(dilate(grid, se))
    result = np.maximum(0, dilated - grid_arr)
    return result.tolist()


def morph_gradient(grid, se=SE_SQUARE_3X3):
    """Morphological gradient: dilated - eroded."""
    dilated = np.asanyarray(dilate(grid, se))
    eroded = np.asanyarray(erode(grid, se))
    result = dilated - eroded
    return result.tolist()


def hit_or_miss(grid, se_fg, se_bg=None):
    """Hit-or-miss transform for shape detection."""
    grid_arr = np.asanyarray(grid)
    se_fg = np.asanyarray(se_fg)
    if se_bg is None:
        se_bg = np.zeros_like(se_fg)
    else:
        se_bg = np.asanyarray(se_bg)

    result = ndimage.binary_hit_or_miss(grid_arr, structure1=se_fg, structure2=se_bg)
    return result.astype(int).tolist()


def create_cross_se(size):
    """Create cross-shaped structuring element."""
    se = np.zeros((size, size), dtype=int)
    center = size // 2
    se[center, :] = 1
    se[:, center] = 1
    return se.tolist()


def create_diamond_se(size):
    """Create diamond-shaped structuring element."""
    se = np.zeros((size, size), dtype=int)
    center = size // 2
    y, x = np.ogrid[:size, :size]
    mask = np.abs(y - center) + np.abs(x - center) <= center
    se[mask] = 1
    return se.tolist()


def create_disk_se(radius):
    """Create disk-shaped structuring element."""
    size = radius * 2 + 1
    se = np.zeros((size, size), dtype=int)
    center = radius
    y, x = np.ogrid[:size, :size]
    mask = (y - center) ** 2 + (x - center) ** 2 <= radius**2
    se[mask] = 1
    return se.tolist()


def create_line_se(length, angle=0):
    """Create line-shaped structuring element."""
    se = np.zeros((length, length), dtype=int)
    if angle == 0:
        se[:, length // 2] = 1
    elif angle == 90:
        se[length // 2, :] = 1
    elif angle == 45:
        for i in range(length):
            se[i, i] = 1
    elif angle == 135:
        for i in range(length):
            se[i, length - 1 - i] = 1
    return se.tolist()


def area_opening(grid, threshold):
    """Area opening: removes connected components smaller than threshold."""
    grid_arr = np.asanyarray(grid)
    labeled, num_features = ndimage.label(grid_arr)
    if num_features == 0:
        return grid_arr.tolist()

    component_sizes = np.bincount(labeled.ravel())
    too_small = component_sizes < threshold
    too_small_mask = too_small[labeled]
    result = grid_arr.copy()
    result[too_small_mask] = 0
    return result.tolist()


def area_closing(grid, threshold):
    """Area closing: fills holes smaller than threshold."""
    grid_arr = np.asanyarray(grid)
    inverted = 1 - grid_arr
    opened = np.asanyarray(area_opening(inverted.tolist(), threshold))
    result = 1 - opened
    return result.tolist()


def opening_by_reconstruction(grid, se=SE_SQUARE_3X3):
    """Opening by reconstruction: erosion followed by geodesic dilation."""
    eroded = np.asanyarray(erode(grid, se))
    # marker = eroded, mask = grid
    # geodesic dilation until convergence
    result = ndimage.binary_propagation(eroded, mask=np.asanyarray(grid))
    return result.astype(int).tolist()


def closing_by_reconstruction(grid, se=SE_SQUARE_3X3):
    """Closing by reconstruction: dilation followed by geodesic erosion."""
    dilated = np.asanyarray(dilate(grid, se))
    # marker = dilated, mask = grid
    # We want to fill holes but not outside the original shapes?
    # Actually reconstruction by dilation of marker under mask.
    # For closing, it's reconstruction by erosion of marker above mask.
    # binary_propagation is for dilation.
    # For erosion, we can use binary_propagation on inverted images.
    inverted_marker = 1 - dilated
    inverted_mask = 1 - np.asanyarray(grid)
    reconstructed_inverted = ndimage.binary_propagation(
        inverted_marker, mask=inverted_mask
    )
    result = 1 - reconstructed_inverted
    return result.astype(int).tolist()


def morphological_close_holes(grid, se=SE_SQUARE_3X3):
    """Close small holes in binary image."""
    grid_arr = np.asanyarray(grid)
    # Using binary_fill_holes might be better but let's stick to the requested logic if possible.
    # The original was dilate then erode (closing).
    return morph_closing(grid, se)


def remove_small_components(grid, min_size):
    """Remove connected components smaller than min_size."""
    return area_opening(grid, min_size)



class Morphology:
    """High-level wrapper for morphological operations."""

    def __init__(self, grid=None, se=None):
        """Initialize with optional grid and structuring element.

        Args:
            grid: Input binary/grayscale grid (2D list)
            se: Structuring element (default: 3x3 square)
        """
        self.grid = grid
        self.se = se if se is not None else SE_SQUARE_3X3

    def set_grid(self, grid):
        """Set the input grid."""
        self.grid = grid
        return self

    def set_se(self, se):
        """Set the structuring element."""
        self.se = se
        return self

    def dilate(self, iterations=1):
        """Apply dilation."""
        if self.grid is None:
            raise ValueError("Grid not set")
        result = self.grid
        for _ in range(iterations):
            result = dilate(result, self.se)
        self.grid = result
        return self

    def erode(self, iterations=1):
        """Apply erosion."""
        if self.grid is None:
            raise ValueError("Grid not set")
        result = self.grid
        for _ in range(iterations):
            result = erode(result, self.se)
        self.grid = result
        return self

    def open(self):
        """Apply opening (erosion + dilation)."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morph_opening(self.grid, self.se)
        return self

    def close(self):
        """Apply closing (dilation + erosion)."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morph_closing(self.grid, self.se)
        return self

    def tophat(self):
        """Apply white top-hat transform."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = tophat(self.grid, self.se)
        return self

    def bothat(self):
        """Apply black bottom-hat transform."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = bothat(self.grid, self.se)
        return self

    def boundary(self):
        """Extract morphological boundary."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morph_boundary(self.grid, self.se)
        return self

    def skeleton(self):
        """Extract morphological skeleton."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morphological_skeleton(self.grid)
        return self

    def internal_gradient(self):
        """Apply internal gradient."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morph_internal_gradient(self.grid, self.se)
        return self

    def external_gradient(self):
        """Apply external gradient."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morph_external_gradient(self.grid, self.se)
        return self

    def gradient(self):
        """Apply morphological gradient."""
        if self.grid is None:
            raise ValueError("Grid not set")
        self.grid = morph_gradient(self.grid, self.se)
        return self

    def get(self):
        """Get the result grid."""
        return self.grid


def apply_morphology(grid, operation, se=None, iterations=1):
    """Apply a morphological operation with a single function call."""
    m = Morphology(grid, se)

    if operation == "dilate":
        return m.dilate(iterations).get()
    elif operation == "erode":
        return m.erode(iterations).get()
    elif operation == "open":
        return m.open().get()
    elif operation == "close":
        return m.close().get()
    elif operation == "tophat":
        return m.tophat().get()
    elif operation == "bothat":
        return m.bothat().get()
    elif operation == "boundary":
        return m.boundary().get()
    elif operation == "skeleton":
        return m.skeleton().get()
    elif operation == "internal_gradient":
        return m.internal_gradient().get()
    elif operation == "external_gradient":
        return m.external_gradient().get()
    elif operation == "gradient":
        return m.gradient().get()
    else:
        raise ValueError(f"Unknown operation: {operation}")


def morphological_filter(grid, operations, se=None):
    """Apply a sequence of morphological operations."""
    m = Morphology(grid, se)
    for op in operations:
        if op == "dilate":
            m.dilate()
        elif op == "erode":
            m.erode()
        elif op == "open":
            m.open()
        elif op == "close":
            m.close()
        elif op == "tophat":
            m.tophat()
        elif op == "bothat":
            m.bothat()
        elif op == "boundary":
            m.boundary()
        elif op == "skeleton":
            m.skeleton()
        elif op == "internal_gradient":
            m.internal_gradient()
        elif op == "external_gradient":
            m.external_gradient()
        elif op == "gradient":
            m.gradient()
        else:
            raise ValueError(f"Unknown operation: {op}")
    return m.get()


def remove_small_holes(grid, max_size):
    """Remove holes smaller than max_size using area closing."""
    return area_closing(grid, max_size)


def remove_small_regions(grid, min_size):
    """Remove connected components smaller than min_size."""
    return remove_small_components(grid, min_size)


def extract_peaks(grid, se=None):
    """Extract bright peaks using top-hat transform."""
    return tophat(grid, se if se is not None else SE_SQUARE_3X3)


def extract_valleys(grid, se=None):
    """Extract dark valleys using bottom-hat transform."""
    return bothat(grid, se if se is not None else SE_SQUARE_3X3)


def remove_white_dots(grid, se=None):
    """Remove small white (bright) dots/noise using opening.

    This is useful for cleaning salt noise or small bright artifacts.

    Args:
        grid: Input binary/grayscale grid
        se: Structuring element (default: 3x3 square)

    Returns:
        Grid with small white dots removed
    """
    return morph_opening(grid, se if se is not None else SE_SQUARE_3X3)


def remove_black_dots(grid, se=None):
    """Remove small black (dark) dots/holes using closing.

    This is useful for cleaning pepper noise or small dark artifacts.

    Args:
        grid: Input binary/grayscale grid
        se: Structuring element (default: 3x3 square)

    Returns:
        Grid with small black dots removed
    """
    return morph_closing(grid, se if se is not None else SE_SQUARE_3X3)
