"""Point cloud registration algorithms."""

import math


def iterative_closest_point(source, target, max_iterations=20):
    """Iterative closest point algorithm (vectorized/optimized)."""
    import numpy as np
    from scipy.spatial import cKDTree

    if not source or not target:
        return source

    src = np.array(source, dtype=float)
    tgt = np.array(target, dtype=float)
    
    # Initial translation alignment
    src_center = np.mean(src, axis=0)
    tgt_center = np.mean(tgt, axis=0)
    
    transformed = src - src_center + tgt_center
    tree = cKDTree(tgt)

    for _ in range(max_iterations):
        # Find nearest neighbors
        _, indices = tree.query(transformed)
        correspondences = tgt[indices]
        
        # Compute centers
        new_target_center = np.mean(correspondences, axis=0)
        new_source_center = np.mean(transformed, axis=0)
        
        # Apply translation
        transformed += new_target_center - new_source_center

    # The original implementation doesn't seem to calculate rotation (SVD/Kabsch).
    # We maintain identical behavior (translation only ICP) for test compatibility.
    return transformed.tolist()
