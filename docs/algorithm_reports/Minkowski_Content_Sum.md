# Minkowski Content and Minkowski Sum

## 1. Overview
The **Minkowski Sum** is a fundamental operation in convex geometry and mathematical morphology, representing the set of all possible sums of vectors from two sets $A$ and $B$. In digital geometry and motion planning, it is used to "expand" one shape by another. **Minkowski Content** is a related concept in geometric measure theory that generalizes the notion of boundary measure (surface area or perimeter) by considering the volume of a neighborhood of the set.

## 2. Definitions
### Minkowski Sum
For two sets $A, B \subset \mathbb{R}^n$, the Minkowski sum $A \oplus B$ is defined as:
$$A \oplus B = \{a + b \mid a \in A, b \in B\}$$
Geometrically, it can be viewed as the union of translates of $A$ by every point in $B$, or vice-versa.

### Minkowski Content
The $k$-dimensional Minkowski content of a set $A \subset \mathbb{R}^n$ is defined as the limit:
$$\mathcal{M}^k(A) = \lim_{\epsilon \to 0} \frac{\text{vol}_n(A \oplus B_\epsilon)}{\alpha_{n-k} \epsilon^{n-k}}$$
where $B_\epsilon$ is a ball of radius $\epsilon$ and $\alpha_{n-k}$ is the volume of the unit $(n-k)$-ball. For a surface in 3D, the 2D Minkowski content corresponds to its surface area.

## 3. Theory
### Properties of Minkowski Sum
1.  **Commutativity:** $A \oplus B = B \oplus A$
2.  **Associativity:** $(A \oplus B) \oplus C = A \oplus (B \oplus C)$
3.  **Distributivity over Union:** $A \oplus (B \cup C) = (A \oplus B) \cup (A \oplus C)$
4.  **Convexity:** If $A$ and $B$ are convex, $A \oplus B$ is convex.

### Steiner Formula
For a convex body $K \subset \mathbb{R}^n$, the volume of its $\epsilon$-neighborhood $K \oplus B_\epsilon$ is given by a polynomial in $\epsilon$:
$$\text{vol}_n(K \oplus B_\epsilon) = \sum_{i=0}^n \binom{n}{i} W_i(K) \epsilon^i$$
where $W_i(K)$ are the Quermassintegrals or intrinsic volumes.

## 4. Pseudo Code (Minkowski Sum of Polygons)
Computing the Minkowski sum of two convex polygons $P$ and $Q$ with $n$ and $m$ vertices can be done in $O(n+m)$ time by reordering edges.

```python
def minkowski_sum_convex_polygons(P, Q):
    # P, Q are lists of vertices in CCW order
    # 1. Reorder vertices so that the one with smallest y (then smallest x) is first
    # 2. Compute edges as vectors
    edges_P = [P[i+1] - P[i] for i in range(len(P)-1)] + [P[0] - P[-1]]
    edges_Q = [Q[i+1] - Q[i] for i in range(len(Q)-1)] + [Q[0] - Q[-1]]
    
    # 3. Sort edges by polar angle
    all_edges = sorted(edges_P + edges_Q, key=lambda v: atan2(v.y, v.x))
    
    # 4. Reconstruct the resulting polygon
    result = [P[0] + Q[0]]
    for e in all_edges:
        result.append(result[-1] + e)
    return result[:-1] # Remove last redundant point
```

## 5. Parameters Selections
-   **$\epsilon$ (Radius):** In Minkowski Content calculation, $\epsilon$ must be small enough to capture local boundary details but large enough to avoid numerical instability.
-   **Decomposition:** For non-convex shapes, the Minkowski sum is typically computed by decomposing them into convex parts, summing the parts, and taking the union.

## 6. Complexity
-   **Convex Polygons (2D):** $O(n + m)$, where $n, m$ are vertex counts.
-   **Convex Polyhedra (3D):** $O(nm)$ in the worst case.
-   **Non-Convex Shapes:** Can be exponential without decomposition; with convex decomposition, it depends on the number of convex pieces.

## 7. Usage
-   **Collision Detection:** Checking if $A \cap B \neq \emptyset$ is equivalent to checking if the origin is inside $A \oplus (-B)$.
-   **Motion Planning:** Robot pathfinding in an environment with obstacles.
-   **Image Processing:** Dilation in mathematical morphology is a Minkowski sum with a structuring element.

## 9. References
1.  Schneider, R. (1993). *Convex Bodies: The Brunn-Minkowski Theory*. Cambridge University Press.
2.  de Berg, M., et al. (2008). *Computational Geometry: Algorithms and Applications*. Springer.
3.  Federer, H. (1969). *Geometric Measure Theory*. Springer.
