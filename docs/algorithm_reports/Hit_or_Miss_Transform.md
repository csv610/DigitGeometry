# Hit-or-Miss Transform

## 1. Overview
The Hit-or-Miss Transform (HMT) is a basic tool in mathematical morphology used for shape detection and pattern matching in binary images. It allows for identifying specific configurations of pixels (a "hit") while also ensuring that certain surrounding pixels are not present (a "miss"). It is a powerful operation for detecting features such as corners, endpoints, isolated pixels, and more complex structures.

## 2. Definitions
*   **Foreground ($A$):** The set of white pixels in a binary image.
*   **Background ($A^c$):** The set of black pixels.
*   **Composite Structuring Element ($B = (B_1, B_2)$):** A pair of disjoint structuring elements, where $B_1$ represents the "hit" pattern (must match foreground) and $B_2$ represents the "miss" pattern (must match background).
*   **Erosion ($\ominus$):** A morphological operation that shrinks foreground regions.

## 3. Theory
The hit-or-miss transform of a set $A$ by $B = (B_1, B_2)$ is defined as the intersection of the erosion of $A$ by $B_1$ and the erosion of the complement of $A$ by $B_2$:
$$A \otimes B = (A \ominus B_1) \cap (A^c \ominus B_2)$$
A pixel $(x, y)$ in the result will be 1 only if:
1.  The structuring element $B_1$ centered at $(x, y)$ is entirely contained within the foreground $A$.
2.  The structuring element $B_2$ centered at $(x, y)$ is entirely contained within the background $A^c$.

Since $B_1$ and $B_2$ must be disjoint for the transform to be non-empty, HMT is fundamentally a template matching operation.

## 4. Pseudo Code
```text
function hitOrMissTransform(image, kernel1, kernel2)
    hit := erosion(image, kernel1)
    
    // Complement the image (invert pixels)
    image_complement := invert(image)
    miss := erosion(image_complement, kernel2)
    
    // Point-wise AND (intersection)
    result := hit AND miss
    return result
```

## 5. Parameters Selections
*   **Structuring Element Design:** $B_1$ should represent the object shape you want to detect, and $B_2$ should define the required empty space around it.
*   **Example (Detecting an Isolated Pixel):** $B_1$ is a single pixel at the origin, and $B_2$ is its 8-neighbors.

## 6. Complexity
*   **Time Complexity:** $O(N \cdot |B|)$, where $N$ is the number of pixels and $|B|$ is the size of the structuring element (number of pixels in $B_1$ and $B_2$).
*   **Space Complexity:** $O(N)$ for image storage.

## 7. Usage
*   Feature detection (corners, junctions, endpoints).
*   Thinning and thickening (as building blocks for these operations).
*   Pruning to remove small branches from skeletons.
*   Object location within an image (e.g., finding specific characters in a text).

## 9. References
1.  Serra, J. (1982). *Image Analysis and Mathematical Morphology*.
2.  Heijmans, H. J. (1994). *Morphological Image Operators*.
3.  Soille, P. (2003). *Morphological Image Analysis: Principles and Applications*.
