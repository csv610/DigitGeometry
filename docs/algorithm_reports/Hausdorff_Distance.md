# Hausdorff Distance

## 1. Overview
The Hausdorff Distance is a mathematical measure of the distance between two subsets in a metric space. Unlike standard distance measures between points, the Hausdorff distance measures how far two shapes or point clouds are from each other. It represents the greatest of all the distances from a point in one set to the closest point in the other set. It is widely used in computer vision, computer graphics, and digital geometry for shape comparison, object matching, and quality assessment.

## 2. Definitions
Given two non-empty subsets $A$ and $B$ of a metric space $(M, d)$:
*   **Directed Hausdorff Distance ($h(A, B)$):** The maximum distance from a point in $A$ to the nearest point in $B$:
    $$h(A, B) = \sup_{a \in A} \inf_{b \in B} d(a, b)$$
*   **Bidirectional (Symmetric) Hausdorff Distance ($H(A, B)$):** The maximum of the two directed distances:
    $$H(A, B) = \max \{ h(A, B), h(B, A) \}$$
    It captures the overall mismatch between two sets.

## 3. Theory
The Hausdorff distance $H(A, B) = \delta$ implies that:
1.  Every point in $A$ is within distance $\delta$ of some point in $B$.
2.  Every point in $B$ is within distance $\delta$ of some point in $A$.

### Partial (Modified) Hausdorff Distance
To improve robustness against outliers, the directed distance can be redefined using the $k$-th largest value (quantile) instead of the maximum:
$$h_k(A, B) = k\text{-th } \sup_{a \in A} \inf_{b \in B} d(a, b)$$
This is particularly useful in noisy image data where a single outlier point could lead to an erroneously large distance.

## 4. Pseudo Code
### Brute-Force Algorithm
```text
function hausdorffDistance(setA, setB)
    hAtoB := -Infinity
    for each point a in setA
        minDist := Infinity
        for each point b in setB
            minDist := min(minDist, distance(a, b))
        hAtoB := max(hAtoB, minDist)
        
    hBtoA := -Infinity
    for each point b in setB
        minDist := Infinity
        for each point a in setA
            minDist := min(minDist, distance(a, b))
        hBtoA := max(hBtoA, minDist)
        
    return max(hAtoB, hBtoA)
```

## 5. Parameters Selections
*   **Metric $d$:** Usually the Euclidean distance, but Manhattan or Chebyshev distances can also be used.
*   **Quantile (Modified Hausdorff):** Choosing a quantile like 95% makes the measure robust to noise.
*   **Efficient Calculation:** Using KD-trees or Distance Transforms (e.g., Chamfer Distance) to find the nearest neighbors can significantly speed up the computation.

## 6. Complexity
*   **Brute-Force:** $O(N_A \cdot N_B)$, where $N_A$ and $N_B$ are the number of points in each set.
*   **Optimized (e.g., KD-Tree):** $O((N_A + N_B) \log N_B)$.
*   **Space Complexity:** $O(N_A + N_B)$.

## 7. Usage
*   Shape matching and recognition (e.g., comparing a template against an image).
*   Quality control in manufacturing (e.g., comparing a scanned object against a CAD model).
*   Medical imaging for comparing segmented organ boundaries.
*   Estimating the error between a mesh and its simplification in computer graphics.

## 9. References
1.  Huttenlocher, D. P., Klanderman, G. A., & Rucklidge, W. J. (1993). Comparing images using the Hausdorff distance. *IEEE Transactions on Pattern Analysis and Machine Intelligence*.
2.  Dubuisson, M. P., & Jain, A. K. (1994). A modified Hausdorff distance for object matching. *International Conference on Pattern Recognition*.
3.  Rockafellar, R. T., & Wets, R. J. B. (1998). *Variational Analysis*.
