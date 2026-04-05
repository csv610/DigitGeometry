# Black and White Top-hat Transforms

## 1. Overview
The Top-hat transform is an operation that extracts small elements and details from given images. There are two types: the **White Top-hat** transform, which extracts bright features smaller than the structuring element, and the **Black Top-hat** transform, which extracts dark features.

## 2. Definitions
*   **Structuring Element ($B$):** A small shape (like a disk or square) used to probe the image.
*   **Opening ($\gamma_B(f)$):** $f \circ B = (f \ominus B) \oplus B$, removes small bright features.
*   **Closing ($\phi_B(f)$):** $f \bullet B = (f \oplus B) \ominus B$, fills small dark holes.
*   **White Top-hat ($T_w(f)$):** The difference between the original image and its opening.
*   **Black Top-hat ($T_b(f)$):** The difference between the closing of the image and the original.

## 3. Theory
*   **White Top-hat ($T_w = f - \gamma_B(f)$):** This operation removes the background and extracts objects that are smaller than the structuring element and brighter than their surroundings. It's often used for background normalization and feature extraction.
*   **Black Top-hat ($T_b = \phi_B(f) - f$):** This extracts dark objects that are smaller than the structuring element and darker than their surroundings.

Both transforms are useful when the background is not uniform (e.g., uneven lighting), as they effectively perform a high-pass filter that removes low-frequency background variations.

## 4. Pseudo Code
```text
function White_Tophat(image, kernel)
    background := Opening(image, kernel)
    result := image - background
    return result

function Black_Tophat(image, kernel)
    closed := Closing(image, kernel)
    result := closed - image
    return result

function Opening(image, kernel)
    eroded := Erode(image, kernel)
    return Dilate(eroded, kernel)

function Closing(image, kernel)
    dilated := Dilate(image, kernel)
    return Erode(dilated, kernel)
```

## 5. Parameters Selections
*   **Structuring Element Shape:** Usually a disk for general features or a line for linear structures (e.g., blood vessels).
*   **Structuring Element Size:** Should be slightly larger than the maximum size of the features to be extracted. If the element is too small, no features are extracted; if too large, background noise might be captured.

## 6. Complexity
*   **Time Complexity:** $O(W \cdot H \cdot |B|)$, where $|B|$ is the size of the structuring element. For separable or rectangular elements, this can be reduced to $O(W \cdot H)$.
*   **Space Complexity:** $O(W \cdot H)$ to store intermediate opening/closing results.

## 7. Usage
*   **Extracting small objects:** Detecting cells in medical images or stars in astronomical images.
*   **Illumination Correction:** Removing shading or uneven lighting from scanned documents.
*   **Feature Enhancement:** Highlighting ridges or valleys in digital elevation models (DEMs).
*   **Preprocessing:** For segmentation or object counting.

## 9. References
1.  Meyer, F. (1978). Contrast feature extraction. Special Issues of Practical Metallography.
2.  Serra, J. (1982). Image Analysis and Mathematical Morphology. Academic Press.
3.  Soille, P. (2003). Morphological Image Analysis: Principles and Applications.
