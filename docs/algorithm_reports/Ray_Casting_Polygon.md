# Ray-Casting Algorithm (Point-in-Polygon)

## 1. Overview
The Ray-Casting algorithm is a fundamental technique in computational geometry used to determine whether a given point lies inside, outside, or on the boundary of a polygon. It is one of the most widely used methods for the "Point-in-Polygon" (PIP) problem due to its simplicity and efficiency. The algorithm works by counting the number of times a ray starting from the test point intersects the edges of the polygon.

## 2. Definitions
*   **Polygon:** A closed plane figure bounded by a finite chain of straight line segments.
*   **Jordan Curve Theorem:** A theorem stating that every simple closed curve in the plane separates the plane into two regions: an "inside" and an "outside."
*   **Ray:** A semi-infinite line starting at a point and extending infinitely in a specific direction.
*   **Intersection:** A point where the ray crosses an edge of the polygon.

## 3. Theory
The algorithm is based on the Jordan Curve Theorem. For any simple closed curve, a ray starting from a point inside the curve must cross the curve an odd number of times to reach the "outside" (infinity). Conversely, a ray starting from a point outside the curve will cross it an even number of times (or zero).

### Key Logic:
1.  Choose a ray starting at the point $P(x_0, y_0)$ and extending in an arbitrary direction (usually the positive $x$-axis for simplicity).
2.  Count the number of intersections between this ray and the edges of the polygon.
3.  If the number of intersections is **odd**, the point is **inside**.
4.  If the number of intersections is **even**, the point is **outside**.

### Edge Cases:
*   **Ray passing through a vertex:** This can lead to double-counting or missing an intersection. A common solution is to treat the vertex as being slightly "above" the ray or to only count edges where one endpoint is strictly above the ray and the other is at or below it.
*   **Ray collinear with an edge:** Horizontal edges collinear with the ray are typically ignored.
*   **Point on an edge:** Most implementations define whether a point on the boundary is considered "inside" or "outside" based on application requirements.

## 4. Pseudo Code
```text
function isPointInPolygon(point, polygon)
    count := 0
    n := length(polygon)
    x, y := point.x, point.y
    
    for i from 0 to n-1
        p1 := polygon[i]
        p2 := polygon[(i + 1) % n]
        
        // Check if the ray (positive x-direction) intersects the edge (p1, p2)
        if ((p1.y > y) != (p2.y > y)) and 
           (x < (p2.x - p1.x) * (y - p1.y) / (p2.y - p1.y) + p1.x)
            count := count + 1
            
    return (count % 2 == 1)
```

## 5. Parameters Selections
*   **Ray Direction:** While any direction works, the positive $x$-axis simplifies the intersection calculation to a linear interpolation of the $x$-coordinate.
*   **Boundary Inclusion:** Determine if points exactly on the edge should return `true` or `false`. The standard algorithm usually excludes them unless explicitly handled.
*   **Robustness:** Use epsilon values for floating-point comparisons to handle near-vertex or near-edge cases.

## 6. Complexity
*   **Time Complexity:** $O(n)$, where $n$ is the number of vertices in the polygon. Each edge must be checked exactly once.
*   **Space Complexity:** $O(1)$ auxiliary space (excluding the storage for the polygon itself).

## 7. Usage
*   **Geographic Information Systems (GIS):** Determining if a coordinate is within a specific boundary (e.g., city, state).
*   **Computer Graphics:** Hit testing in UI elements and picking objects in a 2D scene.
*   **Collision Detection:** Checking if a character or projectile has entered a restricted zone.
*   **Image Processing:** Masking and region-of-interest (ROI) definition.

## 9. References
1.  Shimrat, M. (1962). Algorithm 112: Position of point relative to polygon. Communications of the ACM.
2.  Haines, E. (1994). Point in Polygon Strategies. In *Graphics Gems IV*. Academic Press.
3.  O'Rourke, J. (1998). *Computational Geometry in C*. Cambridge University Press.
