# Bounding Box

## 1. Overview
A bounding box is a simple geometric container that completely encloses a given set of objects or a single object in a given space. It is commonly used as a first-order approximation to the actual shape of an object to simplify spatial queries, collision detection, and rendering.

## 2. Definitions
*   **Axis-Aligned Bounding Box (AABB):** A bounding box whose sides are parallel to the coordinate axes.
*   **Oriented Bounding Box (OBB):** A bounding box that is rotated to better fit the object, not necessarily aligned with the axes.
*   **Minimum Bounding Box:** The smallest possible box (in terms of area, volume, or perimeter) that contains the object.
*   **Bounding Volume Hierarchy (BVH):** A tree structure where each node is a bounding volume enclosing its children.

## 3. Theory
The most common type is the **AABB**, which for a set of points $P = \{p_1, p_2, ..., p_n\}$ is defined by the minimum and maximum coordinates along each axis:
$$ x_{min} = \min_{i} p_{ix}, \quad x_{max} = \max_{i} p_{ix} $$
$$ y_{min} = \min_{i} p_{iy}, \quad y_{max} = \max_{i} p_{iy} $$

For **OBBs**, the box is often computed using Principal Component Analysis (PCA) to find the main axes of the object. The first principal component becomes the primary axis of the OBB, the second the secondary, and so on.

## 4. Pseudo Code
```text
function Calculate_AABB(points)
    x_min := Infinity, x_max := -Infinity
    y_min := Infinity, y_max := -Infinity
    
    for each point p in points
        if p.x < x_min then x_min := p.x
        if p.x > x_max then x_max := p.x
        if p.y < y_min then y_min := p.y
        if p.y > y_max then y_max := p.y
        
    return {min: [x_min, y_min], max: [x_max, y_max]}

function Calculate_OBB(points)
    center := Mean(points)
    cov_matrix := Covariance_Matrix(points, center)
    eigenvectors := Eigenvectors(cov_matrix)
    
    // Project points onto eigenvectors to find bounds
    // ...
    return OBB_Matrix
```

## 5. Parameters Selections
*   **Alignment (AABB vs. OBB):** AABBs are extremely fast to calculate and test for intersection but are often "loose." OBBs are "tight" but computationally more expensive to calculate and use in intersection tests.
*   **Expansion Factor:** Sometimes, a small "epsilon" margin is added to the bounding box to ensure numerical stability during intersection tests.

## 6. Complexity
*   **Time Complexity (AABB):** $O(N)$ for $N$ points, as each point is visited once.
*   **Time Complexity (OBB):** $O(N \cdot D + D^3)$ for $N$ points in $D$ dimensions, due to the covariance matrix and eigendecomposition.
*   **Space Complexity:** $O(1)$ to store the AABB (2 points); $O(D^2)$ to store the OBB matrix.

## 7. Usage
*   **Collision Detection:** Fast "broad phase" check to see if two complex objects *might* be colliding.
*   **Frustum Culling:** Ignoring objects that are outside the camera's field of view in graphics engines.
*   **R-trees and Quadtrees:** Building spatial indexes for efficient database queries.
*   **Object Detection (AI):** Bounding boxes are the standard output format for many neural networks (e.g., YOLO, Faster R-CNN) to localize objects in an image.

## 9. References
1.  Ericson, C. (2004). Real-Time Collision Detection. Morgan Kaufmann.
2.  Gottschalk, S., Lin, M. C., & Manocha, D. (1996). OBBTree: A Hierarchical Structure for Rapid Interference Detection. SIGGRAPH.
3.  Barequet, G., & Har-Peled, S. (2001). Efficiently approximating the minimum-volume bounding box of a point set in three dimensions. Journal of Algorithms.
