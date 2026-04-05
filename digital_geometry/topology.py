"""Topological operations on digital images - compatibility module.

This module imports from the split topology submodules for backward compatibility.
"""

from digital_geometry.topology_basic import (
    count_connected_components,
    compute_topology,
    connected_components_3d,
    compute_surface_curvatures,
)

from digital_geometry.topology_persistent import (
    UnionFindPersistence,
    compute_h0_persistence,
    compute_h1_persistence,
)
