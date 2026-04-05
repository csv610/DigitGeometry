# Approximate Contour

## 1. Overview
Approximate Contour algorithms are used to simplify a curve composed of line segments to a similar curve with fewer points. The most widely used algorithm for this is the Ramer-Douglas-Peucker (RDP) algorithm, which aims to find a simpler curve by decimation.

## 2. Definitions
*   **Contour:** A sequence of points representing a boundary or curve.
*   **Decimation:** The process of removing points from a sequence.
*   **Epsilon ($\epsilon$):** A distance threshold that determines the level of simplification.
*   **Perpendicular Distance:** The shortest distance from a point to a line segment.

## 3. Theory
The Ramer-Douglas-Peucker algorithm works by recursively subdividing a curve.
1.  Connect the start and end points of the curve with a straight line.
2.  Find the point on the curve that is furthest from this line.
3.  If this point's distance is greater than a user-defined threshold $\epsilon$, the point is kept.
4.  Recursively apply the procedure to the two segments (start to furthest point, furthest point to end).
5.  If no point is further than $\epsilon$, then the intermediate points are discarded, and the original curve is approximated by the straight line segment.

## 4. Pseudo Code
```text
function Douglas_Peucker(points, epsilon)
    max_dist := 0
    index := 0
    
    // Find the point with the maximum distance
    for i from 1 to length(points) - 1
        d := perpendicular_distance(points[i], line(points[0], points[end]))
        if d > max_dist
            index := i
            max_dist := d
            
    // If maximum distance is greater than epsilon, recursively simplify
    if max_dist > epsilon
        results1 := Douglas_Peucker(points[0...index], epsilon)
        results2 := Douglas_Peucker(points[index...end], epsilon)
        return concatenate(results1[0...end-1], results2)
    else
        return [points[0], points[end]]

function perpendicular_distance(p, line_start, line_end)
    // Formula for distance from point (x, y) to line (x1, y1)-(x2, y2)
    return abs((y2-y1)x - (x2-x1)y + x2y1 - y2x1) / sqrt((y2-y1)^2 + (x2-x1)^2)
```

## 5. Parameters Selections
*   **$\epsilon$ (Epsilon):** The most critical parameter. A small $\epsilon$ results in a contour very close to the original (more points). A large $\epsilon$ results in a much simpler, more jagged contour (fewer points).

## 6. Complexity
*   **Time Complexity:** $O(N \log N)$ on average, where $N$ is the number of points. In the worst case (e.g., a circle), it can be $O(N^2)$.
*   **Space Complexity:** $O(N)$ for recursion stack and output.

## 7. Usage
*   Digital cartography and GIS (simplifying coastlines or roads for different zoom levels).
*   Vector graphics (reducing the number of control points in a path).
*   Computer vision (smoothing object boundaries for shape analysis).
*   Data compression for trajectories and sensor data.

## 9. References
1.  Douglas, D., & Peucker, T. (1973). Algorithms for the reduction of the number of points required to represent a digitized line or its caricature. Canadian Cartographer.
2.  Ramer, U. (1972). An iterative procedure for the polygonal approximation of plane curves. Computer Graphics and Image Processing.
3.  Hershberger, J., & Snoeyink, J. (1992). Speeding up the Douglas-Peucker line-simplification algorithm.
