# Scanline Polygon Fill

## 1. Overview
**Scanline Polygon Fill** is a fundamental algorithm in computer graphics for filling a closed polygon with color. It processes an image line-by-line (scanline) from top to bottom, finding the intersections of the scanline with the polygon's edges and filling the pixels between pairs of intersections.

## 2. Definitions
- **Scanline:** A horizontal line of pixels.
- **Active Edge Table (AET):** A list of all edges intersected by the current scanline, sorted by their current $x$-intersection point.
- **Edge Table (ET):** A pre-built table of all edges, sorted by their minimum $y$-coordinate.
- **Parity Rule (Odd-Even Rule):** A rule stating that a point is inside a polygon if a ray from the point to infinity crosses an odd number of edges.

## 3. Theory
The algorithm follows these steps:
1.  **Preprocessing:** Create an Edge Table (ET). Each entry in ET[y] contains all edges whose minimum $y$ is equal to $y$.
2.  **Iterative Filling:** For each $y$ from the minimum to maximum $y$:
    -   Add edges from ET[y] to the AET.
    -   Remove edges from AET if their maximum $y$ is reached ($y_{max} = y$).
    -   Sort the AET by $x$-coordinate.
    -   Fill pixels between pairs of $x$-intersections in the AET (e.g., between $x_0$ and $x_1$, $x_2$ and $x_3$).
    -   Update the $x$-intersection for each edge in the AET for the next scanline ($x = x + 1/m$, where $m$ is the slope).

### Special Cases (Vertices)
To avoid filling errors at vertices where two edges meet, a common convention is to only count the lower vertex of an edge. If a scanline passes through a vertex, it is counted once if it's a local minimum/maximum and twice if it's on a monotonic path.

## 4. Pseudo Code
```python
def scanline_fill(polygon_edges):
    # 1. Create Edge Table (ET)
    et = build_edge_table(polygon_edges)
    aet = []
    
    # 2. Iterate through all scanlines
    for y in range(min_y, max_y + 1):
        # 3. Move edges from ET[y] to AET
        aet.extend(et[y])
        
        # 4. Remove edges that are no longer active
        aet = [edge for edge in aet if edge.y_max > y]
        
        # 5. Sort AET by current x-intersection
        aet.sort(key=lambda edge: edge.x_curr)
        
        # 6. Fill pixels between pairs of intersections
        for i in range(0, len(aet), 2):
            x_start = ceil(aet[i].x_curr)
            x_end = floor(aet[i+1].x_curr)
            draw_horizontal_line(x_start, x_end, y)
            
        # 7. Update x-intersections for next scanline
        for edge in aet:
            edge.x_curr += edge.inv_slope
```

## 5. Parameters Selections
- **Edge Representation:** Store $y_{max}, x_{curr}$, and $dx/dy$ (inverse slope) for each edge.
- **Anti-aliasing:** Scanline algorithms can be modified to compute sub-pixel coverage for smoother edges.

## 6. Complexity
- **Time Complexity:** $O(Y \cdot E \log E)$ where $Y$ is the number of scanlines and $E$ is the number of edges. The $\log E$ comes from sorting the AET.
- **Space Complexity:** $O(E)$ to store the Edge Table and Active Edge Table.

## 7. Usage
- **Rasterization:** Filling shapes in vector graphics (SVG, PDF, PostScript).
- **Computer Games:** Rendering UI elements and simple 2D shapes.
- **Image Editing:** Implementing the "Paint Bucket" tool for polygons.

## 9. References
1.  Foley, J. D., et al. (1995). *Computer Graphics: Principles and Practice*. Addison-Wesley.
2.  Hearn, D., & Baker, M. P. (2004). *Computer Graphics with OpenGL*. Pearson.
3.  Sutherland, I. E., et al. (1974). *A Characterization of Ten Hidden-Surface Algorithms*. ACM Computing Surveys.
