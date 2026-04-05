# Connected Components Labeling

## 1. Overview
Connected-component labeling (CCL), also known as connected-component analysis (CCA) or region labeling, is an algorithmic application of graph theory used to uniquely label connected regions in a binary (or grayscale) image. It is a fundamental step in many image processing applications to group pixels that share the same characteristics and are spatially connected.

## 2. Definitions
*   **Connectivity:** The spatial relationship between pixels. Common types include 4-connectivity (horizontal and vertical) and 8-connectivity (horizontal, vertical, and diagonal).
*   **Background Pixel:** Pixels in an image with a value of 0.
*   **Foreground Pixel:** Pixels in an image with a non-zero value (usually 1).
*   **Region/Component:** A set of foreground pixels that are connected according to the chosen connectivity rule.
*   **Equivalence Table:** A data structure used to track labels that are discovered to belong to the same component during the labeling process.

## 3. Theory
CCL algorithms can be categorized into two main types:
1.  **Multi-pass Algorithms:** These scan the image multiple times. The first pass assigns temporary labels and records equivalences. Subsequent passes resolve these equivalences using a Disjoint-Set Union (DSU) or a lookup table.
2.  **One-pass Algorithms (Recursive or Iterative):** These use depth-first search (DFS) or breadth-first search (BFS) to traverse each component fully as soon as it is encountered. While conceptually simpler, they can suffer from stack overflow in large components if implemented recursively.

Modern efficient CCL algorithms (like Grana's or He's algorithms) use decision trees to minimize the number of operations per pixel.

## 4. Pseudo Code (Two-pass Algorithm)
```text
function ConnectedComponents(binary_image, connectivity)
    labels := zeros_like(binary_image)
    next_label := 1
    dsu := DisjointSetUnion()
    
    // First Pass: Assign temporary labels
    for y from 0 to height-1
        for x from 0 to width-1
            if image[x, y] is foreground
                neighbors := getNeighbors(x, y, connectivity)
                if neighbors are empty
                    labels[x, y] := next_label
                    next_label += 1
                else
                    labels[x, y] := min(neighbors.labels)
                    for L in neighbors.labels
                        dsu.union(L, labels[x, y])
                        
    // Second Pass: Resolve labels
    for y from 0 to height-1
        for x from 0 to width-1
            if image[x, y] is foreground
                labels[x, y] := dsu.find(labels[x, y])
                
    return labels
```

## 5. Parameters Selections
*   **Connectivity Type:** Choosing 4-connectivity results in more regions, while 8-connectivity merges regions that touch only at corners. 4-connectivity is generally faster.
*   **Foreground Value:** The value that distinguishes the object from the background.

## 6. Complexity
*   **Time Complexity:** $O(N \cdot \alpha(N))$ for two-pass using DSU, where $N$ is the number of pixels and $\alpha$ is the inverse Ackermann function. In practice, it is nearly $O(N)$.
*   **Space Complexity:** $O(N)$ to store the label image and equivalence data.

## 7. Usage
*   Object counting and identification in manufacturing.
*   Character recognition (OCR).
*   Medical imaging for identifying anatomical structures.
*   Tracking objects in video sequences.

## 9. References
1.  Rosenfeld, A., & Pfaltz, J. L. (1966). Sequential Operations in Digital Picture Processing. Journal of the ACM.
2.  He, L., Chao, Y., & Suzuki, K. (2008). A Run-Based Two-Scan Labeling Algorithm. IEEE Transactions on Image Processing.
3.  Grana, C., Borghesani, D., & Cucchiara, R. (2010). Optimized Block-Based Connected Components Labeling with Decision Trees. IEEE Transactions on Image Processing.
