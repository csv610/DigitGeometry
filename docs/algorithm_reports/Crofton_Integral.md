# Crofton Integral

## 1. Overview
The Crofton integral (or Cauchy-Crofton formula) is a fundamental result in integral geometry that relates the length of a curve to the expected number of intersections it has with a random line. In digital geometry and image processing, it provides a theoretical basis for estimating the perimeter of objects and the length of digitized boundaries by counting intersections with a discrete set of test lines.

## 2. Definitions
*   **Density of Lines ($d\ell$):** A measure on the set of lines in the plane, typically expressed in polar coordinates as $dp \, d\theta$, where $p$ is the distance from the origin and $\theta$ is the angle of the normal.
*   **Intersection Number ($n(\ell \cap \gamma)$):** The number of points where a line $\ell$ intersects a curve $\gamma$.
*   **Stereology:** The study of 3D structures through 2D slices or 1D probes, heavily relying on Crofton-like formulas.

## 3. Theory
The classical Cauchy-Crofton formula states that the length $L$ of a planar curve $\gamma$ is given by:
$$L = \frac{1}{2} \int \int n(\ell \cap \gamma) \, dp \, d\theta$$
Integrating over $\theta \in [0, \pi]$ and $p \in (-\infty, \infty)$.
In a discrete digital grid, the formula is approximated by counting intersections with grid lines at fixed orientations (e.g., horizontal, vertical, and diagonals).
For a digital curve, the length can be estimated as:
$$L \approx \frac{\pi}{2m} \sum_{i=1}^m \Delta \cdot N_i$$
where $m$ is the number of directions, $\Delta$ is the spacing between parallel lines, and $N_i$ is the number of intersections in direction $i$.

## 4. Pseudo Code (Discrete Perimeter Estimation)
```text
function estimatePerimeter(binary_image, directions)
    total_intersections := 0
    for theta in directions
        rotated_image := rotate(binary_image, theta)
        for row in rotated_image
            total_intersections += countTransitions(row)
    
    m := length(directions)
    // Assuming unit grid spacing delta = 1
    perimeter := (PI / (2 * m)) * total_intersections
    return perimeter

function countTransitions(row)
    count := 0
    for i from 0 to length(row) - 2
        if row[i] != row[i+1]
            count += 1
    return count
```

## 5. Parameters Selections
*   **Number of Directions ($m$):** Using more directions (e.g., 4 or 8 instead of just 2) significantly improves the accuracy of the length estimate.
*   **Grid Spacing ($\Delta$):** The distance between parallel test lines in the discretization.

## 6. Complexity
*   **Time Complexity:** $O(m \cdot N)$, where $N$ is the number of pixels and $m$ is the number of directions.
*   **Space Complexity:** $O(N)$ for rotated images or $O(1)$ if processed on-the-fly.

## 7. Usage
*   Estimating the surface area of 3D objects from 2D cross-sections in medical imaging (CT/MRI).
*   Calculating the perimeter of digital shapes in image analysis.
*   Characterizing the morphology of porous materials.

## 9. References
1.  Santalo, L. A. (2004). Integral Geometry and Geometric Probability. Cambridge University Press.
2.  Klette, R., & Rosenfeld, A. (2004). Digital Geometry: Geometric Methods for Digital Picture Analysis.
3.  Crofton, M. W. (1868). On the Theory of Local Probability. Philosophical Transactions of the Royal Society of London.
