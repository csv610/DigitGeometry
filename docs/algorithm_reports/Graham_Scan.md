# Graham Scan (Convex Hull)

## 1. Overview
Graham scan is an efficient algorithm for computing the convex hull of a finite set of points in the plane with a time complexity of $O(n \log n)$. It was proposed by Ronald Graham in 1972 and remains one of the most popular algorithms for this task due to its relative simplicity and performance. The algorithm uses a stack to build the hull iteratively while visiting points in order of their polar angle relative to a pivot point.

## 2. Definitions
*   **Convex Hull:** The smallest convex set that contains all points in a set $S$.
*   **Pivot Point:** The point with the lowest $y$-coordinate (and lowest $x$-coordinate in case of ties) used as the origin for polar sorting.
*   **Polar Angle:** The angle formed between the positive $x$-axis and the line segment connecting the pivot point to another point.
*   **Left Turn (Counter-Clockwise):** A sequence of three points $A, B, C$ where $C$ lies to the left of the directed line $AB$.

## 3. Theory
The Graham scan algorithm follows a systematic process to identify the vertices of the convex hull:
1.  **Pivot Selection:** Find the point with the lowest $y$-coordinate. This point is guaranteed to be on the convex hull.
2.  **Polar Sorting:** Sort all other points by their polar angle relative to the pivot. If two points have the same angle, the one further from the pivot is kept (or just keep both and handle duplicates).
3.  **Hull Construction:** Iterate through the sorted points. Maintain a stack of points that potentially form the hull. For each new point:
    *   While the new point and the top two points on the stack form a right turn (clockwise) or are collinear, the top point on the stack is removed (backtracked).
    *   Push the new point onto the stack.

The "cross product" of vectors $(B-A)$ and $(C-B)$ is used to determine the orientation (left turn, right turn, or collinear).

## 4. Pseudo Code
```text
function grahamScan(P)
    // Find the pivot point (lowest y-coordinate, then lowest x)
    pivot := P[0]
    for p in P:
        if p.y < pivot.y or (p.y == pivot.y and p.x < pivot.x):
            pivot = p
            
    // Sort points by polar angle with pivot
    // (If angles are equal, distance from pivot is tie-breaker)
    sortedP := sort(P \ {pivot}, by: polar_angle(pivot, p))
    
    stack := [pivot]
    for p in sortedP:
        while length(stack) >= 2 and orientation(stack[-2], stack[-1], p) <= 0:
            pop(stack)
        push(stack, p)
        
    return stack

function orientation(a, b, c)
    val := (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0: return 0  // collinear
    return (val > 0) ? -1 : 1 // 1 for counter-clockwise, -1 for clockwise
```

## 5. Parameters Selections
*   **Pivot Selection:** Using the lowest $y$-coordinate ensures the pivot is an extreme point and simplifies polar sorting to a range of $[0, \pi]$.
*   **Handling Collinear Points:** Depending on the application, you might want to include or exclude collinear points on the hull edges.
*   **Numerical Stability:** Geometric predicates (orientation tests) are sensitive to floating-point errors. Using exact arithmetic or robust predicates is recommended for degenerate cases.

## 6. Complexity
*   **Time Complexity:** $O(n \log n)$, dominated by the sorting step. The scan itself is $O(n)$ because each point is pushed onto and popped from the stack at most once.
*   **Space Complexity:** $O(n)$ to store the sorted points and the stack.

## 7. Usage
*   **Collision Detection:** Determining the bounding volume for physics objects.
*   **Clustering:** Finding the boundary of a group of points.
*   **Optimization:** Reducing a large set of points to its most extreme members before further processing.
*   **Geographic Analysis:** Calculating the extent of a set of GPS coordinates.

## 9. References
1.  Graham, R. L. (1972). *An Efficient Algorithm for Determining the Convex Hull of a Finite Planar Set*. Information Processing Letters.
2.  Cormen, T. H., et al. (2009). *Introduction to Algorithms*. MIT Press.
3.  O'Rourke, J. (1998). *Computational Geometry in C*. Cambridge University Press.
