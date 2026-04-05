# Surface Curvatures: Principal, Gaussian, and Mean

## 1. Overview
Curvature is a fundamental concept in differential geometry that describes the local bending of a surface. On a smooth 3D surface, curvature is not a single number but depends on the direction of travel. By analyzing the maximum and minimum curvatures (principal curvatures), we can calculate the **Gaussian** and **Mean** curvatures. These measures are used to classify surface regions into shapes such as flat, spherical, cylindrical, or saddle-like.

## 2. Definitions
*   **Normal Curvature ($k_n$):** The curvature of a curve on the surface formed by the intersection of the surface and a plane containing the normal vector.
*   **Principal Curvatures ($\kappa_1, \kappa_2$):** The maximum and minimum values of the normal curvature at a point.
*   **Gaussian Curvature ($K$):** The product of the principal curvatures ($K = \kappa_1 \cdot \kappa_2$).
*   **Mean Curvature ($H$):** The average of the principal curvatures ($H = \frac{1}{2}(\kappa_1 + \kappa_2)$).
*   **Principal Directions:** The orthogonal directions corresponding to $\kappa_1$ and $\kappa_2$.

## 3. Theory
### Surface Classification based on $K$ and $H$:
*   **$K > 0$:** Elliptic (spherical) point.
*   **$K < 0$:** Hyperbolic (saddle) point.
*   **$K = 0$:** Parabolic (flat or cylindrical) point.
*   **$H = 0$:** Minimal surface (the surface area is locally minimized).

The Gaussian curvature $K$ is an intrinsic property of the surface (Theorema Egregium), meaning it can be determined by measuring lengths and angles on the surface without reference to the 3D space in which it is embedded. In contrast, the Mean curvature $H$ is extrinsic.

## 4. Pseudo Code
### Estimating Curvature on a Discrete Mesh
```text
function estimateCurvature(mesh, point)
    neighbors := getKNearestNeighbors(mesh, point)
    // Fit a quadratic surface (paraboloid) to neighbors
    z = a*x^2 + b*x*y + c*y^2
    
    // Calculate derivatives
    fxx := 2*a, fyy := 2*c, fxy := b
    
    // Construct the Weingarten matrix (Shape Operator)
    W := [[fxx, fxy], [fxy, fyy]]
    
    // Solve for eigenvalues (Principal Curvatures)
    kappa1, kappa2 := eigenvalues(W)
    
    K := kappa1 * kappa2
    H := 0.5 * (kappa1 + kappa2)
    return K, H
```

## 5. Parameters Selections
*   **Neighborhood Size ($k$):** The number of neighbors used for surface fitting. Small $k$ is sensitive to noise; large $k$ can over-smooth the surface and lose detail.
*   **Discrete Operators:** In digital geometry, curvatures are often estimated using the **Cotangent formula** or **Angle Deficit** (for Gaussian curvature).

## 6. Complexity
*   **Time Complexity:** $O(N \cdot k^2)$, where $N$ is the number of points and $k$ is the neighborhood size for least-squares fitting.
*   **Space Complexity:** $O(N)$ for storing curvature values.

## 7. Usage
*   Object recognition and shape analysis.
*   Surface fairing and smoothing in CAD.
*   Identifying features such as creases, ridges, and valleys in meshes.
*   Medical imaging for analyzing organ surface complexity (e.g., brain gyrification).
*   Segmenting 3D scans based on surface type.

## 9. References
1.  Do Carmo, M. P. (2016). *Differential Geometry of Curves and Surfaces*.
2.  Meyer, M., Desbrun, M., Schröder, P., & Barr, A. H. (2003). Discrete Differential-Geometry Operators for Triangulated 2-Manifolds. *Visualization and Mathematics*.
3.  Taubin, G. (1995). Estimating the tensor of curvature of a surface from a discrete set of points. *ICCV*.
