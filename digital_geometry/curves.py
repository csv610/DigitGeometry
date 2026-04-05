"""Curve processing and analysis - compatibility module.

This module imports from the split curve submodules for backward compatibility.
"""

from digital_geometry.curves_basic import (
    point_in_polygon,
    convex_hull,
    smooth_points,
    douglas_peucker,
    perpendicular_distance,
    compute_tangents,
)

from digital_geometry.curves_analysis import (
    menger_curvature,
    compute_curvature,
    curve_shortening_flow,
    is_digitally_straight,
)

from digital_geometry.curves_dsl import (
    certify_dsls,
    dsls_Arithmetical_Distance,
    naive_dsls_recognition,
)
