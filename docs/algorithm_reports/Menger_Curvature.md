# Menger Curvature

## 1. Overview
The Menger Curvature is a discrete definition of curvature based on three points in a metric space. While traditional curvature in differential geometry is defined for smooth curves using derivatives, Menger curvature provides a way to quantify the "bending" of any triplet of points. It is particularly useful in geometric measure theory and analysis on non-smooth structures, such as fractals or discrete datasets.

## 2. Definitions
*   **Triangle ($x, y, z$):** Three distinct points in a metric space.
*   **Menger Curvature ($c(x, y, z)$):** Defined as the reciprocal of the radius of the circle passing through the three points (the circumcircle).
*   **Area ($\mathcal{A}$):** The area of the triangle formed by $x, y, z$.

## 3. Theory
For any three points $x, y, z$ in $\mathbb{R}^n$, the Menger curvature is given by:
$$c(x, y, z) = \frac{4 \mathcal{A}(x, y, z)}{|x-y| \cdot |y-z| \cdot |z-x|}$$
where $\mathcal{A}(x, y, z)$ can be calculated using Heron's formula based on the lengths of the sides $a = |x-y|$, $b = |y-z|$, and $c = |z-x|$.

### Properties
1.  If the three points are collinear, their Menger curvature is zero (the circumcircle has an infinite radius).
2.  Menger curvature is symmetric with respect to its three arguments.
3.  As the three points $x, y, z$ on a smooth curve converge to a single point $p$, the Menger curvature $c(x, y, z)$ converges to the standard geometric curvature $\kappa(p)$ of the curve.

## 4. Pseudo Code
```text
function calculateMengerCurvature(x, y, z)
    a := distance(x, y)
    b := distance(y, z)
    c := distance(z, x)
    
    // Check if points are collinear
    if a + b = c or a + c = b or b + c = a
        return 0
    
    // Using Heron's formula for area
    s := (a + b + c) / 2
    area := sqrt(s * (s - a) * (s - b) * (s - c))
    
    curvature := (4 * area) / (a * b * c)
    return curvature
```

## 5. Parameters Selections
*   **Triple Selection:** In practice, choosing the three points is critical. For a discrete curve, one might choose points at equal arc-length intervals.
*   **Scale Sensitivity:** Menger curvature is sensitive to the spacing between the chosen points. Smaller spacing provides a more "local" estimate but is more sensitive to discretization noise.

## 6. Complexity
*   **Time Complexity:** $O(1)$ to calculate the curvature for a single triplet. $O(N)$ for a sequence of points if only adjacent triplets are considered.
*   **Space Complexity:** $O(1)$ to store a triplet and its curvature.

## 7. Usage
*   Estimating curvature for discrete curves and point clouds.
*   Analysis of fractal sets (e.g., Cantor dust).
*   Rectifiability of measures in geometric measure theory.
*   Characterizing the smoothness of paths in machine learning datasets.

## 9. References
1.  Menger, K. (1930). Untersuchungen über allgemeine Metrik. *Mathematische Annalen*.
2.  Léger, J. C. (1999). Menger curvature and rectifiability. *Annals of Mathematics*.
3.  Pajot, H. (2002). *Analytic Capacity, Rectifiability, Menger Curvature and the Cauchy Integral*.
