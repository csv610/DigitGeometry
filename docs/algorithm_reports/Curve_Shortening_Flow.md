# Curve Shortening Flow

## 1. Overview
The Curve Shortening Flow (CSF) is a geometric process that evolves a curve by moving each point along its inward normal vector with a speed proportional to its local curvature. This flow minimizes the arc length of the curve and is essentially the "heat equation" for curves. In image processing, it is used for boundary smoothing and noise reduction.

## 2. Definitions
*   **Curvature ($\kappa$):** A measure of how much a curve deviates from being a straight line.
*   **Normal Vector ($\mathbf{N}$):** A vector perpendicular to the curve, pointing toward the "center" of the curve.
*   **Velocity Vector ($\mathbf{V}$):** The rate of change of the curve's position over time, defined as $\mathbf{V} = \kappa \mathbf{N}$.

## 3. Theory
The evolution of a curve $\gamma(u, t)$ under CSF is described by the partial differential equation:
$$\frac{\partial \gamma}{\partial t} = \kappa \mathbf{N}$$
A simple closed curve in the plane will eventually become convex and then shrink to a round point before disappearing. In a discrete setting, the curve is represented as a sequence of vertices $P_i$. The discrete curvature vector can be approximated by the central difference:
$$\mathbf{V}_i = P_{i-1} - 2P_i + P_{i+1}$$
This discrete flow is equivalent to applying a Laplacian filter to the vertices of the curve.

## 4. Pseudo Code
```text
function CurveShorteningFlow(vertices, iterations, dt)
    n := size(vertices)
    for iter from 1 to iterations
        new_vertices := []
        for i from 0 to n-1
            prev := vertices[(i - 1 + n) % n]
            curr := vertices[i]
            next := vertices[(i + 1) % n]
            
            // Laplacian approximation of curvature vector
            curvature_vec := (prev + next) / 2 - curr
            new_pos := curr + dt * curvature_vec
            push(new_vertices, new_pos)
            
        vertices := resample(new_vertices) // Maintain vertex spacing
    return vertices
```

## 5. Parameters Selections
*   **Time Step ($dt$):** Must be small enough to ensure stability ($dt < 0.5$ for the explicit scheme).
*   **Resampling Frequency:** As the curve shrinks, vertices may cluster. Equidistant resampling is crucial for maintaining numerical accuracy.
*   **Iterations:** The number of steps determines the level of smoothing.

## 6. Complexity
*   **Time Complexity:** $O(M \cdot V)$ where $M$ is iterations and $V$ is vertices.
*   **Space Complexity:** $O(V)$ for storing the vertex coordinates.

## 7. Usage
*   Smoothing of boundaries in medical image segmentation.
*   Removing artifacts from digitized shapes.
*   Shape evolution and simplification in computer vision.

## 9. References
1.  Grayson, M. A. (1987). The shape of a planar curve evolves to a circle under its curvature flow. Journal of Differential Geometry.
2.  Bruckstein, A. M., Sapiro, G., & Shaked, D. (1995). Evolution of Planar Polygons. International Journal of Computer Vision.
3.  Sethian, J. A. (1999). Level Set Methods and Fast Marching Methods. Cambridge University Press.
