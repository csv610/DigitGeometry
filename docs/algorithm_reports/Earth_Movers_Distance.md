# Earth Mover's Distance

## 1. Overview
The Earth Mover's Distance (EMD) is a measure of the distance between two probability distributions over a region. It is based on the "transportation problem" from linear programming. Intuitively, if the distributions are interpreted as two different ways of piling up a certain amount of dirt over the region, the EMD is the minimum amount of work needed to transform one pile into the other. Work is defined as the amount of dirt moved multiplied by the distance it is moved.

## 2. Definitions
*   **Signature ($S$):** A representation of a distribution as a set of clusters $\{c_i, w_i\}$, where $c_i$ is the cluster center and $w_i$ is its weight.
*   **Ground Distance ($d_{ij}$):** The distance between two points (e.g., Euclidean distance) in the underlying space.
*   **Flow ($f_{ij}$):** The amount of weight transported from cluster $c_i$ in signature $S_1$ to cluster $c_j$ in signature $S_2$.

## 3. Theory
The EMD is the solution to the following optimization problem:
Minimize the total work:
$\sum_i \sum_j f_{ij} d_{ij}$
Subject to the constraints:
1. $f_{ij} \geq 0$
2. $\sum_j f_{ij} \leq w_{i, 1}$
3. $\sum_i f_{ij} \leq w_{j, 2}$
4. $\sum_i \sum_j f_{ij} = \min(\sum_i w_{i, 1}, \sum_j w_{j, 2})$
The EMD is defined as the total work divided by the total flow:
$EMD(S_1, S_2) = \frac{\sum_{i,j} f_{ij} d_{ij}}{\sum_{i,j} f_{ij}}$
If the distributions are normalized (i.e., total weights are equal), EMD is equivalent to the 1st Wasserstein distance.

## 4. Pseudo Code (Transportation Simplex Method)
```text
function calculateEMD(sig1, sig2, groundDistFunc)
    // Setup cost matrix
    C := matrix(size(sig1), size(sig2))
    for i, j: C[i, j] := groundDistFunc(sig1.c[i], sig2.c[j])
    
    // Solve the transportation problem using linear programming
    // (e.g., North-West Corner Rule + Simplex Method)
    optimal_flow := solveTransportationProblem(sig1.w, sig2.w, C)
    
    total_work := sum(optimal_flow * C)
    total_flow := sum(optimal_flow)
    
    return total_work / total_flow
```

## 5. Parameters Selections
*   **Ground Distance:** Euclidean distance is most common, but other metrics like Manhattan or color distance can be used.
*   **Signature Size:** Reducing the number of clusters in the signatures speeds up the calculation but reduces the precision of the EMD.

## 6. Complexity
*   **Time Complexity:** Generally $O(n^3 \log n)$ where $n$ is the number of clusters, as it is a specific case of the min-cost flow problem. Efficient approximations exist for large distributions.
*   **Space Complexity:** $O(n^2)$ for the cost matrix.

## 7. Usage
*   Content-based image retrieval (comparing color histograms or feature signatures).
*   Comparing point clouds and shapes.
*   Natural language processing (Word Mover's Distance).
*   Transfer learning and domain adaptation.

## 9. References
1.  Rubner, Y., Tomasi, C., & Guibas, L. J. (2000). The Earth Mover's Distance as a Metric for Image Retrieval. International Journal of Computer Vision.
2.  Villani, C. (2009). Optimal Transport: Old and New. Springer.
3.  Peleg, S., Werman, M., & Rom, H. (1989). A Unified Approach to the Change of Resolution: Space and Gray-Level. IEEE Transactions on Pattern Analysis and Machine Intelligence.
