# Douglas-Peucker Simplification

## 1. Overview
The Douglas-Peucker (Ramer-Douglas-Peucker) algorithm is an algorithm for reducing the number of points in a curve that is approximated by a series of points. It aims to find a similar curve with fewer points by recursively subdividing the curve and discarding points that fall within a certain tolerance.

## 2. Definitions
*   **Tolerance ($\epsilon$):** The maximum perpendicular distance that any point in the original curve can be from the simplified line segment.
*   **Perpendicular Distance:** The distance from a point to a line segment defined by its two endpoints.
*   **Simplification:** The process of reducing the number of vertices in a polyline while preserving its shape.

## 3. Theory
The algorithm starts with the line segment connecting the first and last points of the curve.
1.  Find the point $P$ with the maximum perpendicular distance from the line segment.
2.  If this maximum distance is less than $\epsilon$, then the entire curve is replaced by the single line segment.
3.  If the maximum distance is greater than $\epsilon$, recursively apply the algorithm to the two sub-curves formed by dividing at $P$.
The result is a piecewise linear approximation that is within distance $\epsilon$ of the original curve at all points.

## 4. Pseudo Code
```text
function DouglasPeucker(P, epsilon)
    dmax := 0
    index := 0
    end := length(P) - 1
    
    // Find point with max perpendicular distance
    for i from 1 to end-1
        d := perpendicularDistance(P[i], P[0], P[end])
        if d > dmax
            index := i
            dmax := d
            
    // Recursively simplify sub-curves
    if dmax > epsilon
        results1 := DouglasPeucker(P[0..index], epsilon)
        results2 := DouglasPeucker(P[index..end], epsilon)
        return results1[:-1] + results2
    else
        return [P[0], P[end]]
```

## 5. Parameters Selections
*   **$\epsilon$ Selection:** A smaller $\epsilon$ preserves more detail, while a larger $\epsilon$ results in more significant simplification. The choice depends on the scale and noise level of the data.
*   **Distance Metric:** Perpendicular distance is standard, but other metrics (like radial distance) can be used for faster, less accurate results.

## 6. Complexity
*   **Time Complexity:** Average $O(n \log n)$, but worst-case $O(n^2)$ for highly irregular curves. 
*   **Space Complexity:** $O(n)$ in the worst case due to the recursion stack.

## 7. Usage
*   Data compression for vector graphics and map data (e.g., SVG, GIS).
*   Simplifying paths for robotics and pathfinding.
*   Pre-processing for shape recognition and matching.

## 9. References
1.  Douglas, D. H., & Peucker, T. K. (1973). Algorithms for the reduction of the number of points required to represent a digitized line or its caricature. Cartographica.
2.  Ramer, U. (1972). An iterative procedure for the polygonal approximation of plane curves. Computer Graphics and Image Processing.
3.  Hershberger, J., & Snoeyink, J. (1992). Speeding up the Douglas-Peucker Line-Simplification Algorithm. Technical Report.
