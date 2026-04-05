# Persistent Homology (H0/H1)

## 1. Overview
**Persistent Homology** is a key method in Topological Data Analysis (TDA) for quantifying the topological features of a dataset across multiple scales. It tracks the "birth" and "death" of topological features (like connected components and holes) as a scale parameter (filtration value) changes.

## 2. Definitions
- **Simplicial Complex:** A combinatorial object made of vertices, edges, triangles, etc., used to represent a space.
- **Filtration:** A sequence of nested simplicial complexes $K_0 \subseteq K_1 \subseteq \dots \subseteq K_n$ corresponding to increasing values of a parameter $\epsilon$.
- **Homology Groups:** $H_k(K)$ is the $k$-th homology group. Its rank $\beta_k$ (Betti number) counts $k$-dimensional holes:
    - $\beta_0$: Number of connected components (H0).
    - $\beta_1$: Number of cycles/holes (H1).
    - $\beta_2$: Number of voids/cavities (H2).
- **Persistence:** The interval $[b, d]$ during which a homology class exists in the filtration. $b$ is the "birth" value and $d$ is the "death" value.

## 3. Theory
### Rips Filtration
A common way to construct a filtration from a point cloud is the Vietoris-Rips complex $VR(\epsilon)$: a $k$-simplex is formed if all its vertices are within distance $\epsilon$ of each other.

### Persistence Diagram
A 2D plot where each topological feature is represented by a point $(b, d)$. Points far from the diagonal $b=d$ represent robust topological features, while points near the diagonal represent noise.

### Barcode
An alternative visualization where each feature is a horizontal bar from $b$ to $d$.

## 4. Pseudo Code (Conceptual)
```python
def compute_persistence(point_cloud, max_epsilon):
    # 1. Construct Rips filtration
    filtration = build_rips_filtration(point_cloud, max_epsilon)
    
    # 2. Sort simplices by their birth time (filtration value)
    sorted_simplices = sorted(filtration)
    
    # 3. Reduce the boundary matrix to find birth/death pairs
    boundary_matrix = compute_boundary_matrix(sorted_simplices)
    reduced_matrix = matrix_reduction(boundary_matrix)
    
    # 4. Extract pairs (b, d)
    pairs_H0 = []
    pairs_H1 = []
    for pivot in reduced_matrix:
        birth = sorted_simplices[pivot.row].time
        death = sorted_simplices[pivot.col].time
        dimension = sorted_simplices[pivot.row].dim
        if dimension == 0:
            pairs_H0.append((birth, death))
        elif dimension == 1:
            pairs_H1.append((birth, death))
            
    return pairs_H0, pairs_H1
```

## 5. Parameters Selections
- **Max Epsilon:** The maximum distance for the Rips complex. Larger values increase computation time significantly.
- **Dimension:** Computing $H_2$ and higher is computationally expensive due to the large number of simplices.
- **Simplification:** Using a "witness complex" or "alpha complex" can reduce the number of simplices while preserving topological information.

## 6. Complexity
- **Time Complexity:** Worst-case $O(m^3)$ for $m$ simplices, though sparse matrix implementations are much faster in practice.
- **Space Complexity:** $O(m^2)$ for the boundary matrix, also improved by sparse representations.

## 7. Usage
- **Shape Analysis:** Comparing the topology of 3D models or medical scans.
- **Protein Folding:** Studying the structural evolution of molecules.
- **Noise Filtering:** Distinguishing true geometric features from random point distribution noise.

## 9. References
1.  Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
2.  Zomorodian, A., & Carlsson, G. (2005). *Computing Persistent Homology*. Discrete & Computational Geometry.
3.  Ghrist, R. (2008). *Barcodes: The persistent topology of data*. Bulletin of the American Mathematical Society.
