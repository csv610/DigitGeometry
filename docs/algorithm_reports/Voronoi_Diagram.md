# Voronoi Diagram

## 1. Overview
A **Voronoi Diagram** is a partition of space into regions based on distance to a set of points (seeds). For each seed, there is a corresponding region (Voronoi cell) consisting of all points that are closer to that seed than to any other. It is the dual of the Delaunay Triangulation.

## 2. Definitions
- **Seed ($p_i$):** A point in a set $P = \{p_1, p_2, \dots, p_n\}$.
- **Voronoi Cell ($V_i$):** The set of all points $x$ such that $\text{dist}(x, p_i) \leq \text{dist}(x, p_j)$ for all $j \neq i$.
- **Voronoi Edge:** The boundary between two adjacent Voronoi cells. It is a subset of the perpendicular bisector of the two seeds.
- **Voronoi Vertex:** A point where three or more Voronoi cells meet. It is the center of the circumcircle of three seeds (Delaunay triangle).

## 3. Theory
### Properties
1.  **Convexity:** Each Voronoi cell is a convex region.
2.  **Number of Elements:** For $n$ seeds in 2D, there are at most $n$ cells, $2n-5$ vertices, and $3n-6$ edges.
3.  **Duality:** The Delaunay triangulation is obtained by connecting seeds whose Voronoi cells share an edge.

### Construction Algorithms
1.  **Fortune's Algorithm (Sweep-line):** $O(n \log n)$ time. Uses a "beach line" that sweeps across the plane to build the diagram.
2.  **Divide and Conquer:** $O(n \log n)$ time. Recursively divides the seeds and merges the diagrams.
3.  **Incremental Construction:** $O(n^2)$ worst-case, $O(n \log n)$ average.
4.  **Jump Flooding Algorithm (JFA):** $O(N \log N)$ where $N$ is the number of pixels. GPU-optimized method for discrete grids.

## 4. Pseudo Code (Conceptual Incremental)
```python
def incremental_voronoi(seeds):
    voronoi = create_initial_bounding_box()
    for p in seeds:
        # 1. Find the cell containing point p
        target_cell = find_cell(voronoi, p)
        
        # 2. Compute the new cell boundaries
        # Intersection of perpendicular bisectors with existing cells
        new_cell = compute_bisector_intersections(voronoi, p)
        
        # 3. Update the diagram topology
        update_voronoi(voronoi, new_cell)
    return voronoi
```

## 5. Parameters Selections
- **Distance Metric:** Usually Euclidean ($L_2$), but can be Manhattan ($L_1$), Chebyshev ($L_\infty$), or others, leading to different cell shapes.
- **Bounding Box:** Essential for handling infinite cells on the diagram's periphery.
- **Weighting:** In a "Weighted Voronoi Diagram," the distance is scaled by a weight for each seed.

## 6. Complexity
- **Time Complexity:** $O(n \log n)$ for optimal 2D algorithms. Higher for higher dimensions ($O(n^{\lceil d/2 \rceil})$).
- **Space Complexity:** $O(n)$ in 2D to store the vertices and edges.

## 7. Usage
- **Spatial Planning:** Locating facilities (e.g., cell towers, hospitals) to serve regions.
- **Computer Graphics:** Procedural texturing (cracks, stones), pathfinding for robots.
- **Biology:** Modeling cell growth and tissue structures.
- **Physics:** Analyzing crystal structures (Wigner-Seitz cells).

## 9. References
1.  Fortune, S. (1987). *A sweep-line algorithm for Voronoi diagrams*. Algorithmica.
2.  Aurenhammer, F. (1991). *Voronoi diagrams - a survey of a fundamental geometric data structure*. ACM Computing Surveys.
3.  de Berg, M., et al. (2008). *Computational Geometry: Algorithms and Applications*. Springer.
