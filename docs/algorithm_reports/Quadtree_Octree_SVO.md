# Quadtree / Octree / Sparse Voxel Octree (SVO)

## 1. Overview
These are tree-based spatial data structures that recursively partition space into equal-sized sub-cells. A **Quadtree** partitions a 2D space, an **Octree** partitions a 3D space, and a **Sparse Voxel Octree (SVO)** is an Octree where empty sub-volumes are not stored, providing a compact representation of sparse geometry.

## 2. Definitions
- **Leaf Node:** A node that represents a small volume of space (e.g., a single pixel or voxel) and does not have children.
- **Internal Node:** A node that has child nodes (4 for Quadtrees, 8 for Octrees).
- **Subdivision:** The process of splitting a node into its children when it contains more data than a threshold.
- **Voxel:** A value on a regular grid in 3D space.

## 3. Theory
### Recursive Subdivision
The root node represents the entire bounding box of the scene. If a node is "full" (contains too many points) or has "complex geometry," it is split into $2^d$ sub-regions ($d=2$ for 2D, $d=3$ for 3D). This process continues until a maximum depth is reached or the data within a cell is simple enough.

### Sparse Voxel Octree (SVO)
In many 3D models, most of the space is empty. SVOs store only the nodes that contain geometry (voxels). This drastically reduces memory usage from $O(N^3)$ (for a full $N^3$ grid) to something proportional to the surface area $O(N^2)$.

## 4. Pseudo Code (Octree Construction)
```python
class OctreeNode:
    def __init__(self, bounds):
        self.bounds = bounds
        self.points = []
        self.children = None

def insert_point(node, point):
    # 1. Check if point is inside bounds
    if not node.bounds.contains(point):
        return False
        
    # 2. If it's a leaf and has space, add point
    if node.children is None:
        if len(node.points) < THRESHOLD or node.depth >= MAX_DEPTH:
            node.points.append(point)
            return True
        else:
            # 3. Otherwise, subdivide and push points down
            subdivide(node)
            for p in node.points:
                for child in node.children:
                    insert_point(child, p)
            node.points = []

    # 4. Insert into appropriate child
    for child in node.children:
        if insert_point(child, point):
            return True
```

## 5. Parameters Selections
- **Threshold:** The maximum number of points/objects per leaf. Small values lead to deeper trees and more subdivisions.
- **Max Depth:** Prevents infinite recursion and limits memory usage.
- **Bounding Box:** The initial root size should encompass all potential geometry.

## 6. Complexity
- **Time Complexity:**
    - **Construction:** $O(N \log N)$ for $N$ points.
    - **Point Query:** $O(\log N)$ or $O(D)$ where $D$ is max depth.
    - **Range Search:** $O(\text{Output} + D)$.
- **Space Complexity:**
    - **Octree:** $O(N)$ for $N$ points (worst case).
    - **Dense Grid:** $O(R^3)$ for resolution $R$.
    - **SVO:** $O(S)$ where $S$ is the number of surface voxels.

## 7. Usage
- **Collision Detection:** Efficiently narrow down potential collisions between objects.
- **Frustum Culling:** Rapidly eliminate entire sections of a scene not visible to the camera.
- **Global Illumination:** Using SVOs for ray tracing and cone tracing (e.g., in Unreal Engine's Lumen).
- **Terrain Rendering:** Dynamic Level-of-Detail (LOD) for large terrain maps.

## 9. References
1.  Samet, H. (2006). *Foundations of Multidimensional and Metric Data Structures*. Morgan Kaufmann.
2.  Meagher, D. (1982). *Geometric Modeling Using Octree Encoding*. Computer Graphics and Image Processing.
3.  Laine, S., & Karras, T. (2010). *Efficient Sparse Voxel Octrees*. Symposium on Interactive 3D Graphics and Games.
4.  Nießner, M., et al. (2013). *Real-time 3D Reconstruction at Scale using Voxel Hashing*. ACM Transactions on Graphics (TOG).
