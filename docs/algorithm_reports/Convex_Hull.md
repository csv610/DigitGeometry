# Convex Hull

## 1. Overview
The convex hull of a set of points is the smallest convex set that contains all of them. Intuitively, if the points are thought of as nails in a board, the convex hull is the shape formed by a rubber band stretched around all of them. It is a fundamental construction in computational geometry.

## 2. Definitions
*   **Convex Set:** A set where for any two points in the set, the line segment joining them is also within the set.
*   **Extreme Point:** A point in a set that does not lie on any open line segment between two points in the set.
*   **Monotone Chain:** A sequence of points where the $x$-coordinates are strictly increasing or decreasing.

## 3. Theory
There are several algorithms for computing the convex hull in 2D:
1.  **Graham Scan:** Sorts points by polar angle and uses a stack to keep track of the hull.
2.  **Monotone Chain (Andrew's Algorithm):** Sorts points by $x$-coordinate and builds upper and lower hulls separately. It is generally preferred due to its numerical stability and simpler sorting.
3.  **Jarvis March (Gift Wrapping):** Starts at an extreme point and "wraps" around the set.
4.  **Quickhull:** A divide-and-conquer approach similar to quicksort.
5.  **Chan's Algorithm:** An optimal output-sensitive algorithm that combines Graham scan and Jarvis march.

## 4. Pseudo Code (Monotone Chain)
```text
function monotoneChain(P)
    sort(P) by x-coordinate (and y for ties)
    
    // Build lower hull
    lower := []
    for p in P
        while size(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0
            pop(lower)
        push(lower, p)
        
    // Build upper hull
    upper := []
    for p in reversed(P)
        while size(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0
            pop(upper)
        push(upper, p)
        
    // Concatenate hulls (removing last point of each to avoid duplicates)
    return lower[:-1] + upper[:-1]
```

## 5. Parameters Selections
*   **Precision:** Use robust geometric predicates to avoid issues with floating-point errors (e.g., orientation tests).
*   **Sorting:** Efficient $O(n \log n)$ sorting is the bottleneck for most algorithms.

## 6. Complexity
*   **Time Complexity:** $O(n \log n)$ for sorting-based algorithms (Graham, Monotone Chain) or $O(nh)$ for Jarvis March, where $h$ is the number of points on the hull. Chan's algorithm is $O(n \log h)$.
*   **Space Complexity:** $O(n)$ for storing the sorted points and the hull.

## 7. Usage
*   Collision detection in physics engines and robotics.
*   Pattern recognition and image processing (shape analysis).
*   Geographic information systems (GIS).
*   Statistics (outlier detection).

## 9. References
1.  Graham, R. L. (1972). An Efficient Algorithm for Determining the Convex Hull of a Finite Planar Set. Information Processing Letters.
2.  Andrew, A. M. (1979). Another Efficient Algorithm for Convex Hulls in Two Dimensions. Information Processing Letters.
3.  Chan, T. M. (1996). Optimal Output-Sensitive Convex Hull Algorithms in Two and Three Dimensions. Discrete & Computational Geometry.
4.  Preparata, F. P., & Shamos, M. I. (1985). Computational Geometry: An Introduction.
