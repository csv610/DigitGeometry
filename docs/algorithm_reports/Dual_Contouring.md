# Dual Contouring

## 1. Overview
Dual Contouring (DC) is a method for generating a polygonal mesh from a volumetric representation (such as an isosurface or a scalar field). Unlike the traditional Marching Cubes algorithm, Dual Contouring can accurately represent sharp features (corners and edges) and adaptively simplify the mesh. It is widely used in computer graphics and terrain generation.

## 2. Definitions
*   **Hermite Data:** Information consisting of the surface-volume intersection points and their corresponding surface normals.
*   **Dual Grid:** A grid where a vertex is placed inside each cell that is intersected by the surface.
*   **QEF (Quadratic Error Function):** A function that measures the distance from a point to a set of tangent planes, used to find the optimal position for a dual vertex.

## 3. Theory
Marching Cubes creates a vertex on each edge that crosses the surface. Dual Contouring creates a vertex *within each cell* that crosses the surface.
1.  **Identify Boundary Cells:** For each cell in the grid, determine if it crosses the surface (i.e., its corners have different signs).
2.  **Calculate Dual Vertex:** For each boundary cell, find the optimal vertex position $x$ by minimizing the QEF:
    $E(x) = \sum_i (n_i \cdot (x - p_i))^2$
    where $p_i$ and $n_i$ are the intersection points and normals on the cell's edges.
3.  **Generate Polygons:** For each edge in the original grid that crosses the surface, connect the dual vertices from the four adjacent cells to form a quad (or two triangles).

## 4. Pseudo Code
```text
function DualContouring(volume_data)
    vertices := {}
    for cell in volume_data.boundaryCells
        hermite_data := getHermiteData(cell)
        vertex_pos := minimizeQEF(hermite_data)
        vertices[cell.id] := vertex_pos
        
    faces := {}
    for edge in volume_data.boundaryEdges
        cell_ids := getAdjacentCells(edge)
        face := buildFaceFromCellVertices(cell_ids, vertices)
        push(faces, face)
        
    return Mesh(vertices, faces)
```

## 5. Parameters Selections
*   **QEF Solver:** Linear least squares or SVD can be used. Solving the QEF is essential for capturing sharp edges.
*   **Clamping:** The vertex position should be clamped within the cell to avoid self-intersecting meshes.

## 6. Complexity
*   **Time Complexity:** $O(C)$, where $C$ is the number of cells. Each cell and boundary edge is processed a constant number of times.
*   **Space Complexity:** $O(C)$ to store the dual vertices and Hermite data.

## 7. Usage
*   Real-time terrain generation in games (e.g., destructible environments).
*   High-fidelity surface reconstruction from noisy point clouds or scan data.
*   Simulating fluid-structure interaction with sharp interfaces.

## 9. References
1.  Ju, T., Losasso, F., Schaefer, S., & Warren, J. (2002). Dual Contouring of Hermite Data. ACM SIGGRAPH.
2.  Schaefer, S., & Warren, J. (2004). Dual Contouring: The Good, the Bad, and the Ugly. Proceedings of the IEEE.
3.  Lorensen, W. E., & Cline, H. E. (1987). Marching Cubes: A High Resolution 3D Surface Construction Algorithm. ACM SIGGRAPH.
