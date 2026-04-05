# Image Filters: Gaussian, Laplacian, Sobel, Prewitt, and Roberts

## 1. Overview
In digital image processing, filters are used to transform images for tasks such as smoothing, sharpening, and edge detection. These filters are applied using a process called convolution, where a small matrix (kernel) is moved across the image pixels to calculate new pixel values. Linear filters like **Gaussian** are used for noise reduction, while differential filters like **Sobel**, **Prewitt**, **Roberts**, and **Laplacian** are used for edge enhancement and boundary detection.

## 2. Definitions
*   **Convolution ($*$):** A mathematical operation on two functions (image and kernel) that produces a third function representing the filtered image.
*   **Kernel:** A small square matrix that defines the filter's operation (e.g., $3 \times 3$ or $5 \times 5$).
*   **Gaussian Filter:** A smoothing filter that uses a kernel with weights following a 2D Gaussian distribution.
*   **Laplacian Filter:** A second-order derivative filter used to detect regions of rapid intensity change (edges).
*   **Gradient Filters (Sobel, Prewitt, Roberts):** First-order derivative filters that estimate the image gradient in horizontal and vertical directions.

## 3. Theory
### Gaussian Filter (Smoothing)
Used to blur the image and reduce noise. The kernel values are calculated using:
$$G(x, y) = \frac{1}{2 \pi \sigma^2} e^{-(x^2 + y^2) / 2 \sigma^2}$$

### Sobel and Prewitt (Edge Detection)
These filters use two $3 \times 3$ kernels ($G_x$ and $G_y$) to detect horizontal and vertical edges.
**Sobel Kernels:**
$$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$
The Sobel filter provides a smoothing effect, making it more robust to noise than the Prewitt filter.

### Roberts Cross (Edge Detection)
Uses two $2 \times 2$ kernels for diagonal edge detection. It is fast but sensitive to noise.
$$G_x = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}, \quad G_y = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$$

### Laplacian Filter (Edge Enhancement)
Calculates the sum of the second derivatives. A common discrete approximation is:
$$L = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix} \text{ or } \begin{bmatrix} 1 & 1 & 1 \\ 1 & -8 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

## 4. Pseudo Code
```text
function applyFilter(image, kernel)
    result := createEmptyImage(image.width, image.height)
    k_size := kernel.size // (e.g., 3 for a 3x3 kernel)
    offset := k_size / 2
    
    for each pixel (x, y) in image
        sum := 0
        for each (kx, ky) in kernel
            sum += image[x + kx - offset, y + ky - offset] * kernel[kx, ky]
        result[x, y] := sum
        
    return result
```

## 5. Parameters Selections
*   **$\sigma$ (Gaussian):** Controls the degree of smoothing. Larger $\sigma$ values result in more blur.
*   **Kernel Size:** Larger kernels (e.g., $5 \times 5, 7 \times 7$) can better smooth noise but may blur edges more.
*   **Combined Filters:** The **Laplacian of Gaussian (LoG)** combines Gaussian smoothing and Laplacian edge detection to find edges more robustly in noisy images.

## 6. Complexity
*   **Time Complexity:** $O(W \cdot H \cdot K^2)$ for an image of size $W \times H$ and a kernel of size $K \times K$. For separable kernels like Gaussian, it can be reduced to $O(W \cdot H \cdot K)$.
*   **Space Complexity:** $O(W \cdot H)$ to store the filtered image.

## 7. Usage
*   Noise reduction (Gaussian).
*   Edge detection and feature extraction (Sobel, Prewitt, Roberts).
*   Image sharpening (using the Laplacian filter).
*   Pre-processing step for more advanced algorithms like the Canny edge detector.

## 9. References
1.  Sobel, I., & Feldman, G. (1968). A $3 \times 3$ isotropic gradient operator for image processing. *Stanford Artificial Intelligence Project*.
2.  Prewitt, J. M. (1970). Object detection and extraction. *In Picture Processing and Psychopictorics*.
3.  Roberts, L. G. (1963). Machine Perception Of Three-Dimensional Solids. *Ph.D. Thesis, MIT*.
4.  Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing*.
