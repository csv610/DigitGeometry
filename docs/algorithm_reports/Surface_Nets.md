# Surface Nets

## 1. Overview
**Surface Nets** (also known as "Constrained Surface Nets") is an algorithm for generating a mesh from a binary or scalar grid. Unlike Marching Cubes, which creates a separate triangle for each cell configuration, Surface Nets places exactly one vertex per voxel cell that is "on the boundary," resulting in a smoother, more efficient mesh for voxel-based data.

## 2. Definitions
- **Dual Contouring:** A class of algorithms that place vertices within voxel cells rather than on voxel edges. Surface Nets is a simple form of dual contouring.
- **Boundary Cell:** A voxel cell where at least one corner is "inside" the object and at least one corner is "outside."
- **Inside/Outside:** Determined by whether the scalar value at a grid corner is greater than or less than an iso-value $\tau$.

## 3. Theory
The algorithm proceeds in three main steps:
1.  **Voxel Traversal:** Identify all voxel cells that contain a boundary (i.e., corners have differing signs).
2.  **Vertex Placement:** For each boundary cell, place a single vertex at its center, or more precisely, at the average of all intersection points along its edges.
3.  **Face Generation:** For every voxel edge that exhibits a sign change (intersects the surface), generate a quad face connecting the vertices of the four voxel cells that share that edge.

### Smoothing and Constraints
The initial placement (at the cell center) results in a "stair-step" appearance. Surface Nets often involves a relaxation step where vertices are smoothed (e.g., Laplacian smoothing) while being constrained to remain within their original voxel cells to preserve the boundary topology.

## 4. Pseudo Code
```python
def surface_nets(grid, iso_value):
    vertices = {}
    faces = []
    
    # 1. Identify boundary cells and create vertices
    for cell in grid:
        if is_boundary(cell, iso_value):
            # Place vertex at average of edge intersections
            v = compute_centroid(cell, iso_value)
            vertices[cell.id] = v
            
    # 2. Iterate through voxel edges to create quads
    for edge in grid_edges:
        if edge.sign_change():
            # Find the 4 cells sharing this edge
            cells = get_neighbor_cells(edge)
            v_ids = [c.id for c in cells]
            faces.append(create_quad(v_ids))
            
    return vertices, faces
```

## 5. Parameters Selections
- **Iso-value ($\tau$):** The threshold for binary segmentation.
- **Smoothing Iterations:** Number of Laplacian smoothing passes. More iterations result in smoother meshes but potentially lose sharp features.
- **Constraint Strength:** How much a vertex is allowed to move from its initial position.

## 6. Complexity
- **Time Complexity:** $O(N^3)$ to traverse the grid, but $O(S)$ where $S$ is the number of boundary voxels.
- **Space Complexity:** $O(S)$ to store the vertices and faces of the resulting mesh.

## 7. Usage
- **Medical Imaging:** Meshing organ surfaces from segmented MRI/CT voxels.
- **Minecraft-style Engines:** Generating smooth terrain from voxel data while preserving the blocky topology.
- **Molecular Modeling:** Visualizing electron density maps.

## 9. References
1.  Gibson, S. F. (1998). *Constrained Surface Nets: A New Method for Modelling Discretely Sampled Objects to Arbitrary Accuracy*. MICCAI.
2.  Ju, T., et al. (2002). *Dual Contouring of Hermite Data*. SIGGRAPH.
3.  Lorensen, W. E., & Cline, H. E. (1987). *Marching Cubes: A High Resolution 3D Surface Construction Algorithm* (for comparison).
