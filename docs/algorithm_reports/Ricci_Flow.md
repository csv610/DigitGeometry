# Ricci Flow

## 1. Overview
**Ricci Flow** is a geometric flow—a process that deforms a Riemannian manifold's metric over time to smooth out curvature irregularities. It is analogous to the heat equation but for geometry, and it is most famous for its role in Grisha Perelman's proof of the Poincaré Conjecture and Thurston's Geometrization Conjecture.

## 2. Definitions
- **Riemannian Metric ($g$):** A symmetric (0,2)-tensor that defines the distance between points and the geometry of the manifold.
- **Ricci Curvature ($Rc$):** A symmetric (0,2)-tensor that represents the "average" sectional curvature at a point in different directions.
- **Flow Equation:** The evolution of the metric $g(t)$ is governed by:
$$\frac{\partial}{\partial t} g(t) = -2 Rc(g(t))$$
This means the metric shrinks in directions of positive curvature and expands in directions of negative curvature.

## 3. Theory
### Geometric Interpretation
Just as the heat equation $u_t = \Delta u$ smooths a temperature distribution, the Ricci flow smooths the "geometry" of a manifold. If a manifold has constant positive sectional curvature (like a sphere), it will shrink uniformly to a point. If it has constant negative curvature (like a hyperbolic space), it will expand.

### Singularities and Surgery
During the flow, parts of the manifold may become extremely thin or "pinch off," forming singularities. Perelman developed "Ricci flow with surgery," where singular parts are carefully cut and capped with spheres before continuing the flow, allowing the global topology to be analyzed.

### Discrete Ricci Flow
In digital geometry, particularly for 2D meshes, **Discrete Ricci Flow** (e.g., Circle Packing Ricci Flow) is used to compute conformal mappings (parameterizations). For a triangulation, one can evolve edge lengths or "circle radii" to achieve a target curvature (e.g., zero for a flat parameterization).

## 4. Pseudo Code (Discrete Ricci Flow for Surface Parameterization)
```python
def surface_ricci_flow(mesh, target_curvatures):
    # mesh: vertices, edges, faces
    # target_curvatures: zero for flat (Euclidean) parameterization
    
    phi = initial_log_radii(mesh) # Log-radii of circles at each vertex
    for iter in range(MAX_ITER):
        # 1. Compute current angles from log-radii using Cosine Law
        angles = compute_angles(mesh, phi)
        
        # 2. Compute Gaussian curvature at each vertex
        K = compute_vertex_curvature(mesh, angles)
        
        # 3. Update log-radii to minimize curvature error
        grad = K - target_curvatures
        phi -= step_size * grad # Simple gradient descent
        
        if norm(grad) < TOLERANCE:
            break
            
    return phi # Final metric representation
```

## 5. Parameters Selections
- **Time Step ($\Delta t$):** Small enough for stability. In the discrete case, adaptive steps (Newton's method) are often used for faster convergence.
- **Target Curvature:** For parameterizing a disk to a rectangle, $K=0$ inside and $K$ sum to $2\pi$ on the boundary.
- **Mesh Resolution:** Higher resolution leads to better approximation but increased computational cost.

## 6. Complexity
- **Time Complexity:** $O(I \cdot V)$ or $O(I \cdot V^3)$ depending on the optimization method (Gradient Descent vs. Newton/Hessian).
- **Space Complexity:** $O(V + E)$ to store the mesh and curvature data.

## 7. Usage
- **Topology:** Proving the Poincaré Conjecture (3D manifolds).
- **Computer Graphics:** Conformal surface parameterization (UV mapping) for textures and remeshing.
- **Medical Imaging:** Flattening the cerebral cortex or colon surface for visualization and analysis.

## 9. References
1.  Hamilton, R. S. (1982). *Three-manifolds with positive Ricci curvature*. Journal of Differential Geometry.
2.  Perelman, G. (2002). *The entropy formula for the Ricci flow and its geometric applications*. arXiv.
3.  Gu, X., & Yau, S. T. (2008). *Computational Conformal Geometry*. International Press.
4.  Chow, B., & Knopf, D. (2004). *The Ricci Flow: An Introduction*. American Mathematical Society.
