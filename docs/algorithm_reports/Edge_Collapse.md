# Edge Collapse Mesh Simplification

## 1. Overview
Edge collapse is a fundamental operation in mesh simplification that reduces the number of vertices and faces in a 3D model. It works by merging two adjacent vertices into a single vertex, thereby removing one edge and two faces (in a triangle manifold). By repeatedly applying this operation to edges that cause the least error, a simplified version of the original mesh can be generated while preserving its overall shape.

## 2. Definitions
*   **Edge Collapse ($v_1, v_2 \rightarrow \bar{v}$):** The operation of replacing vertices $v_1$ and $v_2$ with a single vertex $\bar{v}$.
*   **Quadric Error Metric (QEM):** A distance measure representing the sum of squared distances from a vertex to the planes of its adjacent faces.
*   **Priority Queue:** A data structure used to store all potential edge collapses, ordered by their estimated error.

## 3. Theory
The most popular algorithm for edge collapse simplification uses the **Quadric Error Metric (QEM)**. Each vertex $v$ is assigned a 4x4 matrix $Q$ such that the error at $v$ is $v^T Q v$.
1.  **Initialize Quadrics:** For each vertex, $Q$ is the sum of the matrices $(n_i n_i^T, -d_i n_i, d_i^2)$ for each adjacent face with plane equation $n_i \cdot x + d_i = 0$.
2.  **Estimate Collapse Error:** For an edge $(v_1, v_2)$, the new quadric is $Q = Q_1 + Q_2$. The optimal position $\bar{v}$ is found by solving $\nabla (\bar{v}^T Q \bar{v}) = 0$.
3.  **Iterative Simplification:** Repeatedly collapse the edge with the minimum error, update the quadrics and errors of affected edges, and re-order the priority queue.

## 4. Pseudo Code
```text
function SimplifyMesh(mesh, target_vertex_count)
    initializeQuadrics(mesh)
    queue := empty priority queue
    
    for each edge (v1, v2) in mesh
        computeOptimalCollapse(v1, v2, v_new, error)
        queue.push({v1, v2, v_new, error})
        
    while mesh.vertexCount > target_vertex_count
        {v1, v2, v_new, error} := queue.popMin()
        if isCollapseValid(v1, v2)
            collapseEdge(v1, v2, v_new)
            updateAffectedEdges(v_new, queue)
            
    return mesh
```

## 5. Parameters Selections
*   **Optimal Vertex Position:** If the Q matrix is singular, the midpoint or one of the endpoints is chosen as $\bar{v}$.
*   **Boundary Constraints:** Edges on the boundary of the mesh can be weighted more heavily to prevent the boundary from shrinking or distorting.
*   **Topological Checks:** Prevent collapses that would cause non-manifold geometry or face flips.

## 6. Complexity
*   **Time Complexity:** $O(E \log E)$ where $E$ is the number of edges, primarily due to the priority queue operations.
*   **Space Complexity:** $O(V + E)$ to store the mesh, quadric matrices, and queue.

## 7. Usage
*   LOD (Level of Detail) generation for video games and real-time visualization.
*   Simplifying complex models for faster simulation or 3D printing.
*   Pre-processing for geometric analysis.

## 9. References
1.  Garland, M., & Heckbert, P. S. (1997). Surface Simplification Using Quadric Error Metrics. ACM SIGGRAPH.
2.  Hoppe, H. (1996). Progressive Meshes. ACM SIGGRAPH.
3.  Botsch, M., et al. (2010). Polygon Mesh Processing.
