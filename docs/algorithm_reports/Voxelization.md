# Voxelization

## 1. Overview
**Voxelization** is the process of converting a 3D model (e.g., triangle mesh, point cloud) into a discrete volumetric representation—a grid of voxels. It is the 3D analog of rasterization in 2D graphics. Voxelization can be "binary" (on/off) or "scalar" (storing density, color, or other attributes).

## 2. Definitions
- **Voxel:** A volume element on a regular grid in 3D space.
- **Surface Voxelization:** Only voxels that intersect the 3D surface are marked.
- **Solid Voxelization:** All voxels that are inside the 3D volume are marked.
- **Voxel Grid Resolution:** The dimensions of the grid ($N_x, N_y, N_z$).

## 3. Theory
### Surface Voxelization
For each triangle in the mesh:
1.  Compute its bounding box in the voxel grid.
2.  For each voxel cell in the bounding box, check if the triangle intersects the voxel's volume (usually a box-triangle intersection test).
3.  Mark intersecting voxels.

### Solid Voxelization
Once the surface is voxelized, the interior can be filled using:
1.  **Scanline Fill:** Process scanlines in one direction (e.g., $z$-axis) and fill voxels between pairs of surface voxels (subject to parity rules).
2.  **Flood Fill:** Start from a known interior point (or from outside and invert) and fill the connected region.
3.  **Winding Number / Parity:** For each voxel center, compute if it's inside by shooting a ray and counting intersections.

### GPU Acceleration
Modern voxelization is often performed on the GPU using a rasterization pipeline: the triangle mesh is rendered into a 3D texture (or multiple 2D texture slices) with a shader that marks the corresponding voxels.

## 4. Pseudo Code (Surface Voxelization)
```python
def voxelize_triangle(v1, v2, v3, grid):
    # 1. Map triangle vertices to grid coordinates
    v1_g = to_grid(v1)
    v2_g = to_grid(v2)
    v3_g = to_grid(v3)
    
    # 2. Get bounding box of the triangle in grid cells
    bbox_min = floor(min(v1_g, v2_g, v3_g))
    bbox_max = ceil(max(v1_g, v2_g, v3_g))
    
    # 3. Check each potential voxel cell for intersection
    for x in range(bbox_min.x, bbox_max.x):
        for y in range(bbox_min.y, bbox_max.y):
            for z in range(bbox_min.z, bbox_max.z):
                if box_triangle_intersect(v1_g, v2_g, v3_g, [x, y, z]):
                    grid[x, y, z] = 1
```

## 5. Parameters Selections
- **Voxel Size ($\epsilon$):** Determines the precision. Too small increases memory exponentially ($O(1/\epsilon^3)$); too large loses geometric detail.
- **Alignment:** Whether the grid is axis-aligned or aligned with the model's principal axes.
- **Conservativeness:** "Conservative Voxelization" ensures every pixel/voxel even partially touched by a primitive is marked (crucial for collision detection).

## 6. Complexity
- **Time Complexity:** $O(T \cdot (R/ \epsilon)^2)$ where $T$ is the number of triangles and $R$ is the size of the triangle relative to voxel size $\epsilon$.
- **Space Complexity:** $O(G^3)$ for a dense grid of resolution $G$, or $O(S)$ where $S$ is the number of surface voxels if using sparse structures like Octrees or Hash Maps.

## 7. Usage
- **Collision Detection:** Fast intersection tests in physics engines.
- **Global Illumination:** Voxel cone tracing for real-time lighting.
- **Medical Imaging:** Reconstructing 3D volumes from 2D slices (e.g., CT scans).
- **Video Games:** 3D environment representation in games like Minecraft or Roblox.

## 9. References
1.  Akenine-Möller, T. (2001). *Fast 3D Triangle-Box Overlap Testing*. Journal of Graphics Tools.
2.  Schwarz, M., & Seidel, H. P. (2010). *Fast Parallel Surface and Solid Voxelization on GPUs*. ACM Transactions on Graphics.
3.  Nießner, M., et al. (2013). *Real-time 3D Reconstruction at Scale using Voxel Hashing*. ACM TOG.
