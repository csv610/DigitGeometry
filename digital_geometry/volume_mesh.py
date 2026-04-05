"""Mesh processing and analysis - compatibility module.

This module imports from the split mesh submodules for backward compatibility.
"""

from digital_geometry.mesh_processing import (
    laplacian_mesh_smoothing,
    mesh_simplification_edge_collapse,
    active_contour_snake,
    mean_curvature_flow_grid,
)

from digital_geometry.mesh_analysis import (
    fractal_dimension,
    is_simple_point_2d,
    is_simple_point_3d,
    dominant_laplacian_eigenvalues,
)

from digital_geometry.registration import (
    iterative_closest_point,
)
