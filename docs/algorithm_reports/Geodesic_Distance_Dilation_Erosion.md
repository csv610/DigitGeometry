# Geodesic Distance, Dilation, and Erosion

## 1. Overview
Geodesic transformations are morphological operations that are performed within a constrained space, usually defined by a "mask" image. Unlike standard morphological operations that use a structuring element of fixed shape, geodesic operations adapt to the topology of the mask. These tools are fundamental in mathematical morphology for tasks such as object reconstruction, hole filling, and marker-based segmentation.

## 2. Definitions
*   **Mask Image ($M$):** A binary or grayscale image that acts as the constraint for the operation.
*   **Marker Image ($I$):** An initial seed image that will be propagated within the mask.
*   **Geodesic Distance ($d_M(p, q)$):** The shortest path between pixels $p$ and $q$ that remains entirely within the mask $M$.
*   **Geodesic Dilation ($\delta_M(I)$):** Propagation of the marker $I$ within the mask $M$.
*   **Geodesic Erosion ($\epsilon_M(I)$):** Shrinking of the marker $I$ constrained by the mask $M$.

## 3. Theory
### Geodesic Dilation
The geodesic dilation of a marker image $I$ with respect to a mask image $M$ is defined as the point-wise minimum of the standard dilation and the mask:
$$\delta_M^{(1)}(I) = (I \oplus B) \cap M$$
where $B$ is a small structuring element (typically 4- or 8-connectivity).
Repeating this operation until stability is reached results in the **Reconstruction by Dilation**:
$$\delta_M^{(\infty)}(I) = \lim_{n \to \infty} \delta_M^{(n)}(I)$$

### Geodesic Erosion
Similarly, geodesic erosion is defined as:
$$\epsilon_M^{(1)}(I) = (I \ominus B) \cup M$$
The result of repeated applications is the **Reconstruction by Erosion**.

### Geodesic Distance
The geodesic distance $d_M(p, q)$ is the shortest path between $p$ and $q$ that stays within the set $M$. If no such path exists, the distance is infinite.

## 4. Pseudo Code
### Reconstruction by Dilation
```text
function reconstructByDilation(marker, mask)
    current := marker
    repeat
        previous := current
        current := dilate(current, kernel)
        current := pointwiseMinimum(current, mask)
    until current = previous
    return current
```

## 5. Parameters Selections
*   **Structuring Element ($B$):** Usually a $3 \times 3$ cross (4-connectivity) or a $3 \times 3$ square (8-connectivity).
*   **Mask Image ($M$):** Defines the boundary of the region of interest. For hole filling, $M$ is the original image, and $I$ is a marker placed on the border.

## 6. Complexity
*   **Time Complexity:** $O(N \cdot K)$, where $N$ is the number of pixels and $K$ is the number of iterations until convergence. In the worst case, $K$ can be the diameter of the largest object.
*   **Space Complexity:** $O(N)$ for image storage and intermediate buffers.

## 7. Usage
*   **Morphological Reconstruction:** Isolating objects of interest by markers.
*   **Hole Filling:** Automatically filling interior gaps in objects.
*   **Removing Border Objects:** Removing objects that touch the edge of the image.
*   **Watershed Segmentation:** Markers are often used to initialize the watershed lines.
*   **Distance Transform:** Calculating distances that respect object boundaries.

## 9. References
1.  Vincent, L. (1993). Morphological Grayscale Reconstruction in Image Analysis: Applications and Efficient Algorithms. *IEEE Transactions on Image Processing*.
2.  Lantuéjoul, C., & Beucher, S. (1981). On the use of geodesic metrics in image analysis. *Journal of Microscopy*.
3.  Soille, P. (2003). *Morphological Image Analysis: Principles and Applications*.
