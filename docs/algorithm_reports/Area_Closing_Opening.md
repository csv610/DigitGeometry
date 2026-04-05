# Area Closing and Opening

## 1. Overview
Area Opening and Area Closing are morphological filters that operate based on the size (area) of connected components in an image. Unlike standard morphological opening/closing with a fixed structuring element, area-based filters preserve the shape of objects while removing components that are smaller than a specified area threshold.

## 2. Definitions
*   **Opening:** A morphological operation that removes small foreground objects (white on black) while keeping larger ones.
*   **Closing:** A morphological operation that fills small background holes (black on white) in foreground objects.
*   **Connected Component:** A group of pixels where each pixel is reachable from any other pixel in the group through a path of adjacent pixels.
*   **Area ($A$):** The number of pixels in a connected component.
*   **Lambda ($\lambda$):** The area threshold; components with an area less than $\lambda$ are removed.

## 3. Theory
*   **Area Opening ($AO_\lambda$):** Removes all connected components of the foreground whose area is less than $\lambda$. It is an "attribute opening."
*   **Area Closing ($AC_\lambda$):** Is the dual of area opening. It fills all background components (holes) whose area is less than $\lambda$.

These operations are idempotent (applying them twice gives the same result as once) and increasing (if image $A \subseteq B$, then $AO_\lambda(A) \subseteq AO_\lambda(B)$). They are particularly powerful because they do not distort the boundaries of the objects that are kept, unlike opening with a large disk or square structuring element.

## 4. Pseudo Code
```text
function Area_Opening(image, lambda, connectivity)
    labels := find_connected_components(image, connectivity)
    for each component in labels
        if size(component) < lambda
            set_all_pixels(component, background_value)
    return image

function Area_Closing(image, lambda, connectivity)
    inverted_image := invert(image)
    opened_inverted := Area_Opening(inverted_image, lambda, connectivity)
    return invert(opened_inverted)
```

## 5. Parameters Selections
*   **Area Threshold ($\lambda$):** The minimum number of pixels for an object (or hole) to be preserved. Selection depends on the resolution and the expected size of objects of interest.
*   **Connectivity:** Usually 4-way or 8-way for 2D images. 8-way connectivity is more common for foreground objects.

## 6. Complexity
*   **Time Complexity:** $O(W \cdot H \cdot \alpha(W \cdot H))$, where $\alpha$ is the inverse Ackermann function, arising from the Disjoint Set Union (DSU) used in labeling. For practical purposes, it is essentially $O(W \cdot H)$.
*   **Space Complexity:** $O(W \cdot H)$ for storing component labels and pixel data.

## 7. Usage
*   Denoising binary and grayscale images (removing "salt and pepper" noise).
*   Filtering small artifacts from segmented medical images.
*   Extracting meaningful objects while ignoring negligible noise in satellite imagery.
*   Document image analysis (removing small flecks from scanned text).

## 9. References
1.  Vincent, L. (1992). Morphological Area Openings and Closings for Grayscale Images. Proc. NATO Shape in Picture Workshop.
2.  Soille, P. (2003). Morphological Image Analysis: Principles and Applications.
3.  Heijmans, H. J. A. M. (1994). Morphological Image Operators.
