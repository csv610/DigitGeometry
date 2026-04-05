# Graph Cut Segmentation

## 1. Overview
Graph Cut Segmentation is a powerful technique in computer vision that treats image segmentation as an energy minimization problem on a graph. The image is mapped onto a graph where nodes represent pixels and edges represent the relationships between them. By finding the "minimum cut" of the graph, the algorithm optimally partitions the image into background and foreground (or multiple regions) while minimizing a cost function that balances regional properties and boundary consistency.

## 2. Definitions
*   **Source ($S$):** A terminal node representing the foreground (object).
*   **Sink ($T$):** A terminal node representing the background.
*   **$n$-links:** Edges between neighboring pixels, representing boundary smoothness (regional cost).
*   **$t$-links:** Edges connecting each pixel to the source $S$ or sink $T$, representing the likelihood of a pixel belonging to the foreground or background (unary cost).
*   **Minimum Cut:** A set of edges that, when removed, separate the source from the sink such that the sum of their weights is minimized.

## 3. Theory
The segmentation problem is formulated as minimizing an energy function:
$$E(L) = \sum_{p \in P} R_p(L_p) + \sum_{(p, q) \in N} B_{p, q}(L_p, L_q)$$
where $L = \{L_p | p \in P\}$ is the labeling of each pixel $p$ as foreground or background.
*   **Regional Term ($R_p$):** Measures how well the label $L_p$ fits the pixel $p$. For example, if $p$ has a color similar to the foreground model, $R_p(\text{foreground})$ will be small.
*   **Boundary Term ($B_{p, q}$):** Measures the similarity between neighboring pixels $p$ and $q$. If $p$ and $q$ have similar properties (e.g., intensity), $B_{p, q}$ will be high to discourage a cut between them.

The **Max-Flow Min-Cut Theorem** states that the maximum flow through a network is equal to the capacity of the minimum cut. This allows us to use efficient max-flow algorithms (e.g., Boykov-Kolmogorov, Edmonds-Karp) to find the optimal segmentation.

## 4. Pseudo Code
```text
function graphCut(image, foregroundModel, backgroundModel)
    G := createEmptyGraph()
    source := newNode(), sink := newNode()
    
    for each pixel p
        // Add t-links
        weightToSource := likelihood(p, foregroundModel)
        weightToSink := likelihood(p, backgroundModel)
        G.addEdge(source, p, weightToSource)
        G.addEdge(p, sink, weightToSink)
        
        for each neighbor q of p
            // Add n-links
            weight := boundarySimilarity(p, q)
            G.addEdge(p, q, weight)
            
    // Solve the Max-Flow problem
    maxFlow, minCut := solveMaxFlow(G, source, sink)
    
    for each pixel p
        if p is connected to source in minCut
            label(p) := foreground
        else
            label(p) := background
            
    return labels
```

## 5. Parameters Selections
*   **Regional Likelihood:** Often modeled using histograms or Gaussian Mixture Models (GMMs) based on user-provided markers (seeds).
*   **Boundary Term ($\lambda$):** A weighting factor that controls the "smoothness" of the segmentation. Larger $\lambda$ results in smoother boundaries.
*   **Connectivity:** 4-way or 8-way connectivity between pixels.

## 6. Complexity
*   **Time Complexity:** $O(V \cdot E^2)$ or $O(V^2 \cdot E)$ for general max-flow, but the specialized **Boykov-Kolmogorov algorithm** used in vision typically runs in $O(N)$ for grid-like graphs in practice.
*   **Space Complexity:** $O(N)$ to store the graph (nodes and edges).

## 7. Usage
*   Interactive image segmentation (e.g., GrabCut).
*   Stereo matching (disparity estimation).
*   Object recognition.
*   Image stitching and panorama creation.
*   Medical image analysis (organ segmentation).

## 9. References
1.  Boykov, Y., & Jolly, M. P. (2001). Interactive graph cuts for optimal boundary & region segmentation of objects in N-D images. *ICCV*.
2.  Boykov, Y., & Kolmogorov, V. (2004). An experimental comparison of min-cut/max-flow algorithms for energy minimization in vision. *PAMI*.
3.  Rother, C., Kolmogorov, V., & Blake, A. (2004). "GrabCut": interactive foreground extraction using iterated graph cuts. *SIGGRAPH*.
