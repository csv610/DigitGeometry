# Mesh Manifoldness Verification

## 1. Overview
Mesh manifoldness is a critical property in computational geometry and computer graphics that ensures a 3D surface is well-behaved and topologically sound. A "manifold" mesh is one where the local neighborhood of every point is topologically equivalent to a disk (for interior points) or a half-disk (for boundary points). Manifoldness is essential for many algorithms, including boolean operations, 3D printing, and physics simulations, which often fail on "non-manifold" geometry.

## 2. Definitions
*   **Edge Manifoldness:** Every edge in the mesh must be shared by exactly one or two faces.
*   **Vertex Manifoldness:** The set of faces sharing a vertex must form a single, connected "fan" (or "star") of faces.
*   **Watertight (Closed) Mesh:** A manifold mesh with no boundary edges (every edge is shared by exactly two faces).
*   **Non-manifold Edge:** An edge shared by three or more faces (T-junction) or a lone edge with no face.
*   **Degenerate Face:** A face with zero area or duplicate vertices.

## 3. Theory
Verification involves checking several local and global topological constraints:

1.  **Edge-Face Incidence:** For each edge in the mesh, count the number of faces that contain it.
    *   **0 faces:** Isolated edge (invalid in most face-based meshes).
    *   **1 face:** Boundary edge (allowed in manifold meshes with boundaries).
    *   **2 faces:** Manifold interior edge.
    *   **3+ faces:** Non-manifold edge (prohibited).
2.  **Vertex Star Connectivity:** For each vertex, the neighboring faces must be reachable from one another by traversing across shared edges that also share that vertex. If a vertex belongs to two separate "clusters" of faces that only touch at that vertex (like a bowtie), it is non-manifold.
3.  **Orientation Consistency:** In a manifold mesh, the orientation of adjacent faces must be consistent. If face A and face B share an edge, they should traverse that edge in opposite directions to ensure a consistent "inside" and "outside."

## 4. Pseudo Code
```text
function verifyMeshManifoldness(vertices, faces)
    edge_to_faces := {} // Map of edge (u, v) to face IDs
    vertex_to_faces := {} // Map of vertex ID to face IDs
    
    // 1. Check Edge Manifoldness
    for f in faces:
        for each edge (u, v) in f:
            edge := canonicalOrder(u, v)
            edge_to_faces[edge].append(f.id)
            vertex_to_faces[u].append(f.id)
            
    for edge, face_list in edge_to_faces:
        if length(face_list) > 2:
            return false, "Non-manifold edge: " + edge
            
    // 2. Check Vertex Manifoldness
    for v, face_list in vertex_to_faces:
        if not isConnectedFan(v, face_list, edge_to_faces):
            return false, "Non-manifold vertex: " + v
            
    // 3. Check Orientation
    for edge, face_list in edge_to_faces:
        if length(face_list) == 2:
            if not isConsistent(edge, face_list[0], face_list[1]):
                return false, "Inconsistent orientation at edge: " + edge
                
    return true, "Mesh is manifold"
```

## 5. Parameters Selections
*   **Tolerance ($\epsilon$):** Small epsilon values may be needed to merge nearly-coincident vertices that were intended to be the same (vertex welding) before checking manifoldness.
*   **Boundary Policy:** Specify whether open boundaries (1-face edges) are acceptable or if the mesh must be strictly watertight (2-face edges only).

## 6. Complexity
*   **Time Complexity:** $O(F)$, where $F$ is the number of faces. Each face is visited once to populate maps, and then each edge/vertex is checked.
*   **Space Complexity:** $O(F + V)$ to store the edge-to-face and vertex-to-face adjacency maps.

## 7. Usage
*   **3D Printing (STL files):** Slicing software requires manifold, watertight meshes to distinguish between the "material" and "air."
*   **Boolean Operations:** Algorithms for union, intersection, and subtraction of 3D objects (e.g., CGAL, OpenSCAD) require manifold input.
*   **Subdivision Surfaces:** Many subdivision schemes (e.g., Catmull-Clark) assume manifold topology.
*   **Finite Element Analysis (FEA):** Simulation meshes must be topologically sound to ensure numerical stability.

## 9. References
1.  Botsch, M., et al. (2010). *Polygon Mesh Processing*. CRC Press.
2.  Gueziec, A., et al. (1998). *Cutting and Stitching: Converting Sets of Polygons to Manifold Surfaces*. IEEE Computer Graphics and Applications.
3.  Attene, M. (2010). *A lightweight approach to repairing non-manifold polygon meshes*. IEEE International Conference on Shape Modeling and Applications.
