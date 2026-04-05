import pytest
import numpy as np
from digital_geometry.geometric_measure_theory import (
    compute_imt_2d, 
    compute_imt_3d, 
    minkowski_synthesis_2d
)
from digital_geometry.voxel_render import fast_winding_number

def test_imt_2d_square():
    square = [(0,0), (1,0), (1,1), (0,1)]
    res = compute_imt_2d(square, rank=2)
    assert res['beta'] < 0.1  # Square is symmetric, beta_2 should be near 0

def test_imt_2d_rectangle():
    rect = [(0,0), (4,0), (4,1), (0,1)]
    res = compute_imt_2d(rect, rank=2)
    assert res['beta'] > 0.5  # Elongated, beta_2 should be high

def test_minkowski_synthesis():
    # Simple circle-ish
    tensors = {0: 6.28, 2: 0.1+0j}
    pts = minkowski_synthesis_2d(tensors)
    assert len(pts) == 100
    assert pts.shape[1] == 2

def test_fast_winding_number():
    vol = np.zeros((5, 5, 5))
    vol[1:4, 1:4, 1:4] = 1
    # Point inside (2, 2, 2)
    res = fast_winding_number(vol, [(2, 2, 2), (0, 0, 0)])
    assert res[0] > 0.8  # Inside ~ 1.0
    assert res[1] < 0.2  # Outside ~ 0.0

def test_surface_manifold_integrity():
    from digital_geometry.voxel_render import surface_nets
    from digital_geometry.voxel_topology import verify_mesh_manifold
    # Create a 4x4x4 cube
    vol = np.zeros((6, 6, 6), dtype=np.uint8)
    vol[1:5, 1:5, 1:5] = 1
    verts, faces = surface_nets(vol)
    is_manifold, msg = verify_mesh_manifold(verts, faces)
    assert is_manifold, f"Surface Nets failed manifold QC: {msg}"

def test_imt_3d_basic():
    # Small 3x3x3 block
    vol = np.zeros((5, 5, 5))
    vol[1:4, 1:4, 1:4] = 1
    import scipy.special
    res = compute_imt_3d(vol, l=2)
    assert 'beta' in res
    assert res['area'] > 0
