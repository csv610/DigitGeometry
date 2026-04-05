"""Boolean operations on voxelized objects using OpenVDB.

This module provides boolean set operations (union, intersection, difference)
on voxelized objects using the OpenVDB library.

Note: OpenVDB must be installed separately. On macOS: brew install openvdb
Then install Python bindings: pip install openvdb-numpy
"""

import numpy as np
from typing import Tuple, Optional

try:
    import openvdb as vdb
    from openvdb import Vec3s, Vec3i

    OPENVDB_AVAILABLE = True
except ImportError:
    OPENVDB_AVAILABLE = False
    vdb = None


def voxel_grid_to_vdb(
    volume: np.ndarray, voxel_size: float = 1.0, name: str = "volume"
) -> Optional[object]:
    """Convert numpy voxel grid to OpenVDB grid.

    Args:
        volume: 3D numpy array (z, y, x) with binary values
        voxel_size: Size of each voxel
        name: Name for the VDB grid

    Returns:
        OpenVDB FloatGrid or None if OpenVDB not available
    """
    if not OPENVDB_AVAILABLE:
        return None

    depth, height, width = volume.shape

    grid = vdb.BoolGrid()
    grid.name = name
    grid.voxelSize = voxel_size

    transform = vdb.createLinearTransform(voxelSize=voxel_size)
    grid.transform = transform

    accessor = grid.getAccessor()

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z, y, x] == 1:
                    accessor.setValueOn((x, y, z), True)

    grid.topologyMin = vdb.Vec3i(0, 0, 0)
    grid.topologyMax = vdb.Vec3i(width - 1, height - 1, depth - 1)

    return grid


def vdb_to_voxel_grid(
    grid: object,
    resolution: Optional[Tuple[int, int, int]] = None,
    threshold: float = 0.5,
) -> np.ndarray:
    """Convert OpenVDB grid to numpy voxel grid.

    Args:
        grid: OpenVDB grid (BoolGrid or FloatGrid)
        resolution: Optional (depth, height, width) - uses grid bbox if None
        threshold: Threshold for FloatGrid values

    Returns:
        3D numpy array (z, y, x) with binary values
    """
    if not OPENVDB_AVAILABLE:
        return None

    if resolution is None:
        bbox = grid.activeBBox()
        depth = bbox.max.z - bbox.min.z + 1
        height = bbox.max.y - bbox.min.y + 1
        width = bbox.max.x - bbox.min.x + 1
    else:
        depth, height, width = resolution

    volume = np.zeros((depth, height, width), dtype=np.uint8)

    it = vdb.BoolGridIterator(grid) if hasattr(grid, "itervoxels") else None

    if hasattr(grid, "tree"):
        for it in grid.tree:
            x, y, z = it.getCoord()
            if 0 <= x < width and 0 <= y < height and 0 <= z < depth:
                if hasattr(grid, "getValue"):
                    val = grid.getValue(it.getCoord())
                else:
                    val = it.value()
                if val > threshold:
                    volume[z, y, x] = 1

    return volume


def vdb_union(grid_a: object, grid_b: object) -> object:
    """Compute boolean union (A OR B) of two VDB grids.

    Args:
        grid_a: First OpenVDB grid
        grid_b: Second OpenVDB grid

    Returns:
        New OpenVDB grid representing union
    """
    if not OPENVDB_AVAILABLE:
        return None

    result = vdb.BoolGrid()
    result.copyMetaFrom(grid_a)
    result.copyMetaFrom(grid_b)

    result = vdb.orBool(grid_a, grid_b)

    return result


def vdb_intersection(grid_a: object, grid_b: object) -> object:
    """Compute boolean intersection (A AND B) of two VDB grids.

    Args:
        grid_a: First OpenVDB grid
        grid_b: Second OpenVDB grid

    Returns:
        New OpenVDB grid representing intersection
    """
    if not OPENVDB_AVAILABLE:
        return None

    result = vdb.andBool(grid_a, grid_b)

    return result


def vdb_difference(grid_a: object, grid_b: object) -> object:
    """Compute boolean difference (A NOT B) of two VDB grids.

    Args:
        grid_a: First OpenVDB grid (minuend)
        grid_b: Second OpenVDB grid (subtrahend)

    Returns:
        New OpenVDB grid representing A - B
    """
    if not OPENVDB_AVAILABLE:
        return None

    result = vdb.andNotBool(grid_a, grid_b)

    return result


def vdb_symmetric_difference(grid_a: object, grid_b: object) -> object:
    """Compute symmetric difference (XOR) of two VDB grids.

    Args:
        grid_a: First OpenVDB grid
        grid_b: Second OpenVDB grid

    Returns:
        New OpenVDB grid representing elements in either grid but not both
    """
    if not OPENVDB_AVAILABLE:
        return None

    result = vdb.xorBool(grid_a, grid_b)

    return result


def voxel_boolean_union(
    volume_a: np.ndarray, volume_b: np.ndarray, voxel_size: float = 1.0
) -> np.ndarray:
    """Compute boolean union of two voxel grids.

    Args:
        volume_a: First 3D voxel grid
        volume_b: Second 3D voxel grid
        voxel_size: Size of each voxel

    Returns:
        Resulting voxel grid
    """
    if not OPENVDB_AVAILABLE:
        return _voxel_boolean_fallback(volume_a, volume_b, "union")

    grid_a = voxel_grid_to_vdb(volume_a, voxel_size)
    grid_b = voxel_grid_to_vdb(volume_b, voxel_size)

    result_grid = vdb_union(grid_a, grid_b)

    return vdb_to_voxel_grid(result_grid)


def voxel_boolean_intersection(
    volume_a: np.ndarray, volume_b: np.ndarray, voxel_size: float = 1.0
) -> np.ndarray:
    """Compute boolean intersection of two voxel grids.

    Args:
        volume_a: First 3D voxel grid
        volume_b: Second 3D voxel grid
        voxel_size: Size of each voxel

    Returns:
        Resulting voxel grid
    """
    if not OPENVDB_AVAILABLE:
        return _voxel_boolean_fallback(volume_a, volume_b, "intersection")

    grid_a = voxel_grid_to_vdb(volume_a, voxel_size)
    grid_b = voxel_grid_to_vdb(volume_b, voxel_size)

    result_grid = vdb_intersection(grid_a, grid_b)

    return vdb_to_voxel_grid(result_grid)


def voxel_boolean_difference(
    volume_a: np.ndarray, volume_b: np.ndarray, voxel_size: float = 1.0
) -> np.ndarray:
    """Compute boolean difference (A - B) of two voxel grids.

    Args:
        volume_a: First 3D voxel grid (minuend)
        volume_b: Second 3D voxel grid (subtrahend)
        voxel_size: Size of each voxel

    Returns:
        Resulting voxel grid
    """
    if not OPENVDB_AVAILABLE:
        return _voxel_boolean_fallback(volume_a, volume_b, "difference")

    grid_a = voxel_grid_to_vdb(volume_a, voxel_size)
    grid_b = voxel_grid_to_vdb(volume_b, voxel_size)

    result_grid = vdb_difference(grid_a, grid_b)

    return vdb_to_voxel_grid(result_grid)


def _voxel_boolean_fallback(
    volume_a: np.ndarray, volume_b: np.ndarray, operation: str
) -> np.ndarray:
    """Fallback boolean operations using numpy when OpenVDB unavailable.

    Args:
        volume_a: First 3D voxel grid
        volume_b: Second 3D voxel grid
        operation: 'union', 'intersection', or 'difference'

    Returns:
        Resulting voxel grid
    """
    da, ha, wa = volume_a.shape
    db, hb, wb = volume_b.shape

    max_d = max(da, db)
    max_h = max(ha, hb)
    max_w = max(wa, wb)

    padded_a = np.zeros((max_d, max_h, max_w), dtype=np.uint8)
    padded_b = np.zeros((max_d, max_h, max_w), dtype=np.uint8)

    padded_a[:da, :ha, :wa] = volume_a
    padded_b[:db, :hb, :wb] = volume_b

    if operation == "union":
        result = np.logical_or(padded_a, padded_b).astype(np.uint8)
    elif operation == "intersection":
        result = np.logical_and(padded_a, padded_b).astype(np.uint8)
    elif operation == "difference":
        result = np.logical_and(padded_a, np.logical_not(padded_b)).astype(np.uint8)
    elif operation == "symmetric_difference":
        result = np.logical_xor(padded_a, padded_b).astype(np.uint8)
    else:
        raise ValueError(f"Unknown operation: {operation}")

    return result


def voxel_symmetric_difference(
    volume_a: np.ndarray, volume_b: np.ndarray, voxel_size: float = 1.0
) -> np.ndarray:
    """Compute symmetric difference (XOR) of two voxel grids.

    Args:
        volume_a: First 3D voxel grid
        volume_b: Second 3D voxel grid
        voxel_size: Size of each voxel

    Returns:
        Resulting voxel grid
    """
    if not OPENVDB_AVAILABLE:
        return _voxel_boolean_fallback(volume_a, volume_b, "symmetric_difference")

    grid_a = voxel_grid_to_vdb(volume_a, voxel_size)
    grid_b = voxel_grid_to_vdb(volume_b, voxel_size)

    result_grid = vdb_symmetric_difference(grid_a, grid_b)

    return vdb_to_voxel_grid(result_grid)


def vdb_dilate(grid: object, iterations: int = 1) -> object:
    """Dilate (expand) a boolean VDB grid.

    Args:
        grid: Input OpenVDB grid
        iterations: Number of dilation iterations

    Returns:
        Dilated grid
    """
    if not OPENVDB_AVAILABLE:
        return None

    from openvdb import tools

    result = grid
    for _ in range(iterations):
        result = tools.dilate(result)

    return result


def vdb_erode(grid: object, iterations: int = 1) -> object:
    """Erode (shrink) a boolean VDB grid.

    Args:
        grid: Input OpenVDB grid
        iterations: Number of erosion iterations

    Returns:
        Eroded grid
    """
    if not OPENVDB_AVAILABLE:
        return None

    from openvdb import tools

    result = grid
    for _ in range(iterations):
        result = tools.erode(result)

    return result


def voxel_dilate(
    volume: np.ndarray, iterations: int = 1, voxel_size: float = 1.0
) -> np.ndarray:
    """Dilate a voxel grid using morphological dilation.

    Args:
        volume: 3D voxel grid
        iterations: Number of dilation iterations
        voxel_size: Size of each voxel

    Returns:
        Dilated voxel grid
    """
    if not OPENVDB_AVAILABLE:
        return _numpy_morphology_dilate(volume, iterations)

    grid = voxel_grid_to_vdb(volume, voxel_size)
    dilated = vdb_dilate(grid, iterations)

    return vdb_to_voxel_grid(dilated)


def voxel_erode(
    volume: np.ndarray, iterations: int = 1, voxel_size: float = 1.0
) -> np.ndarray:
    """Erode a voxel grid using morphological erosion.

    Args:
        volume: 3D voxel grid
        iterations: Number of erosion iterations
        voxel_size: Size of each voxel

    Returns:
        Eroded voxel grid
    """
    if not OPENVDB_AVAILABLE:
        return _numpy_morphology_erode(volume, iterations)

    grid = voxel_grid_to_vdb(volume, voxel_size)
    eroded = vdb_erode(grid, iterations)

    return vdb_to_voxel_grid(eroded)


def _numpy_morphology_dilate(volume: np.ndarray, iterations: int = 1) -> np.ndarray:
    """Fallback numpy-based dilation."""
    from scipy.ndimage import binary_dilation

    result = volume.copy()
    structure = np.ones((3, 3, 3), dtype=np.uint8)

    for _ in range(iterations):
        result = binary_dilation(result, structure).astype(np.uint8)

    return result


def _numpy_morphology_erode(volume: np.ndarray, iterations: int = 1) -> np.ndarray:
    """Fallback numpy-based erosion."""
    from scipy.ndimage import binary_erosion

    result = volume.copy()
    structure = np.ones((3, 3, 3), dtype=np.uint8)

    for _ in range(iterations):
        result = binary_erosion(result, structure).astype(np.uint8)

    return result


def voxel_open(
    volume: np.ndarray, iterations: int = 1, voxel_size: float = 1.0
) -> np.ndarray:
    """Perform opening (erosion followed by dilation) on voxel grid.

    Args:
        volume: 3D voxel grid
        iterations: Number of iterations for each operation
        voxel_size: Size of each voxel

    Returns:
        Opened voxel grid
    """
    eroded = voxel_erode(volume, iterations, voxel_size)
    opened = voxel_dilate(eroded, iterations, voxel_size)

    return opened


def voxel_close(
    volume: np.ndarray, iterations: int = 1, voxel_size: float = 1.0
) -> np.ndarray:
    """Perform closing (dilation followed by erosion) on voxel grid.

    Args:
        volume: 3D voxel grid
        iterations: Number of iterations for each operation
        voxel_size: Size of each voxel

    Returns:
        Closed voxel grid
    """
    dilated = voxel_dilate(volume, iterations, voxel_size)
    closed = voxel_erode(dilated, iterations, voxel_size)

    return closed


def compute_voxel_volume(grid: object, voxel_size: float = 1.0) -> float:
    """Compute volume of voxels in a grid.

    Args:
        grid: OpenVDB BoolGrid
        voxel_size: Size of each voxel

    Returns:
        Volume in cubic units
    """
    if not OPENVDB_AVAILABLE:
        return 0.0

    from openvdb import tools

    voxel_count = tools.activeVoxelCount(grid)
    return voxel_count * (voxel_size**3)


def compute_voxel_centroid(
    grid: object, voxel_size: float = 1.0
) -> Tuple[float, float, float]:
    """Compute centroid of voxels in a grid.

    Args:
        grid: OpenVDB BoolGrid
        voxel_size: Size of each voxel

    Returns:
        (x, y, z) centroid coordinates
    """
    if not OPENVDB_AVAILABLE:
        return (0.0, 0.0, 0.0)

    from openvdb import tools

    sum_x = sum_y = sum_z = 0.0
    count = 0

    for it in grid:
        x, y, z = it.getCoord()
        sum_x += x
        sum_y += y
        sum_z += z
        count += 1

    if count == 0:
        return (0.0, 0.0, 0.0)

    return (
        sum_x / count * voxel_size,
        sum_y / count * voxel_size,
        sum_z / count * voxel_size,
    )


def voxel_slice(volume: np.ndarray, axis: int, index: int) -> np.ndarray:
    """Extract a 2D slice from a 3D voxel volume.

    Args:
        volume: 3D voxel grid
        axis: 0=z, 1=y, 2=x
        index: Index along the axis

    Returns:
        2D numpy array
    """
    if axis == 0:
        return volume[index, :, :]
    elif axis == 1:
        return volume[:, index, :]
    elif axis == 2:
        return volume[:, :, index]
    else:
        raise ValueError(f"Invalid axis: {axis}")


def voxel_project(volume: np.ndarray, axis: int) -> np.ndarray:
    """Project voxel volume along an axis (max projection).

    Args:
        volume: 3D voxel grid
        axis: 0=z, 1=y, 2=x

    Returns:
        2D numpy array
    """
    if axis == 0:
        return np.max(volume, axis=0)
    elif axis == 1:
        return np.max(volume, axis=1)
    elif axis == 2:
        return np.max(volume, axis=2)
    else:
        raise ValueError(f"Invalid axis: {axis}")
