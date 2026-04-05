# Skeletonization

## 1. Overview
**Skeletonization** (or "thining") is a morphological operation that reduces a binary image to its "skeleton"—a set of thin lines that are equidistant from the object's boundaries. The resulting skeleton captures the essential topology and structure of the shape, making it easier to analyze and recognize.

## 2. Definitions
- **Skeleton:** The set of centers of all maximal inscribed balls in the object. Also known as the **Medial Axis**.
- **Maximal Inscribed Ball:** A ball contained within the object that is not a subset of any other ball contained within the same object.
- **Topological Invariance:** The requirement that the skeleton has the same number of connected components and holes (Euler characteristic) as the original shape.

## 3. Theory
### Distance-Based Skeletonization
The Medial Axis Transform (MAT) is computed using a distance transform. Points in the skeleton are those where the distance to the boundary is locally maximal in at least two directions.

### Thinning Algorithms (e.g., Zhang-Suen)
These are iterative methods that remove ("peel off") outer pixels layer-by-layer. A pixel is removed if it:
1.  Is a boundary pixel.
2.  Is not an end-point (has more than 1 neighbor).
3.  Its removal does not break connectivity (does not change the Euler characteristic).

## 4. Pseudo Code (Zhang-Suen Thinning)
The Zhang-Suen algorithm uses two sub-iterations per pass to remove pixels from different directions.

```python
def zhang_suen_thinning(image):
    while True:
        # Sub-iteration 1
        to_remove = []
        for p in foreground_pixels(image):
            n = neighbors(p) # 8-neighbors
            B = count_foreground(n) # Number of 1s in 8-neighbors
            A = count_transitions(n) # Number of 0->1 transitions in clockwise order
            # Conditions for removal:
            # 1. 2 <= B <= 6
            # 2. A == 1 (connectivity preserving)
            # 3. p_north * p_east * p_south == 0
            # 4. p_east * p_south * p_west == 0
            if condition1 and condition2 and condition3 and condition4:
                to_remove.append(p)
        for p in to_remove: image[p] = 0
        if not to_remove: break
        
        # Sub-iteration 2 (similar, with conditions 3 and 4 slightly changed)
        # ... repeat similar process ...
    return image
```

## 5. Parameters Selections
- **Connectivity:** 4-connected vs. 8-connected. Standard algorithms usually target 8-connectivity.
- **Pruning:** Post-processing step to remove small, noisy branches (spurs) that often appear in skeletons due to small boundary irregularities.
- **Thresholding:** Before skeletonization, the image must be cleanly binarized.

## 6. Complexity
- **Time Complexity:** $O(I \cdot N)$ where $I$ is the number of iterations (proportional to the width of the object) and $N$ is the number of pixels.
- **Space Complexity:** $O(N)$ to store the image and temporary removal list.

## 7. Usage
- **Optical Character Recognition (OCR):** Reducing characters to thin strokes for feature extraction.
- **Biometrics:** Fingerprint ridge analysis and vein pattern recognition.
- **Graphics:** Extracting control skeletons for mesh animation (rigging).
- **Medical Imaging:** Analyzing the branching patterns of blood vessels or neurons.

## 9. References
1.  Blum, H. (1967). *A Transformation for Extracting New Descriptors of Shape*. Models for the Perception of Speech and Visual Form.
2.  Zhang, T. Y., & Suen, C. Y. (1984). *A Fast Parallel Algorithm for Thinning Digital Patterns*. Communications of the ACM.
3.  Lam, L., et al. (1992). *Thinning Algorithms - A Comprehensive Survey*. IEEE Transactions on Pattern Analysis and Machine Intelligence.
