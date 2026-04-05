# Fourier Descriptors

## 1. Overview
Fourier Descriptors are powerful features used in shape analysis and pattern recognition to represent the boundary of a 2D object. By treating the boundary as a periodic signal and applying the Fourier Transform, the boundary can be described in terms of its frequency components. This representation is invariant to translation, rotation, and scaling (when normalized).

## 2. Definitions
*   **Boundary Sequence:** A sequence of complex numbers $z(k) = x(k) + i y(k)$, representing the $(x, y)$ coordinates of points on the boundary.
*   **Discrete Fourier Transform (DFT):** A transformation that converts the spatial boundary sequence into a set of Fourier coefficients $Z(u)$.
*   **Low-Frequency Components:** Capture the general shape of the object.
*   **High-Frequency Components:** Capture the fine details and noise of the boundary.

## 3. Theory
The object boundary can be expressed as a periodic sequence of $N$ points. The $u$-th Fourier descriptor is calculated as:
$$Z(u) = \frac{1}{N} \sum_{k=0}^{N-1} z(k) e^{-i 2 \pi u k / N}, \quad u = 0, 1, \dots, N-1$$
The original shape can be reconstructed from the descriptors:
$$z(k) = \sum_{u=0}^{N-1} Z(u) e^{i 2 \pi u k / N}$$
By using only the first $M < N$ descriptors (low-frequency components), we can achieve a smoothed approximation of the shape.
### Invariances
1.  **Translation:** $Z(0)$ is the centroid. Removing $Z(0)$ makes the descriptors translation-invariant.
2.  **Rotation:** Rotating the shape by $\theta$ multiplies each $Z(u)$ by $e^{i\theta}$. Taking the magnitude $|Z(u)|$ makes the descriptors rotation-invariant.
3.  **Scaling:** Scaling by $\alpha$ multiplies each $Z(u)$ by $\alpha$. Dividing all coefficients by $|Z(1)|$ makes the descriptors scale-invariant.

## 4. Pseudo Code
```text
function getFourierDescriptors(boundaryPoints, numDescriptors)
    N := length(boundaryPoints)
    z := array of N complex numbers (x + iy)
    
    // Compute DFT
    Z := DFT(z)
    
    // Normalize (Optional)
    Z[0] := 0 // Translation invariance
    scale := absoluteValue(Z[1])
    for i from 1 to N-1
        Z[i] := Z[i] / scale // Scale invariance
        
    return Z[0:numDescriptors]
```

## 5. Parameters Selections
*   **Number of Descriptors ($M$):** Smaller $M$ captures the overall shape and is robust to noise. Larger $M$ includes more fine details but may become sensitive to discretization noise. Typically, $M$ is chosen between 10 and 32.
*   **Boundary Extraction:** The boundary must be sampled uniformly or resampled to $N$ equidistant points to ensure consistent frequency analysis.

## 6. Complexity
*   **Time Complexity:** $O(N \log N)$ if using the Fast Fourier Transform (FFT).
*   **Space Complexity:** $O(N)$ to store the boundary and descriptors.

## 7. Usage
*   Shape recognition and classification (e.g., character recognition).
*   Shape retrieval in databases.
*   Medical imaging for organ contour analysis.
*   Object tracking by matching descriptors between frames.

## 9. References
1.  Zahn, C. T., & Roskies, R. Z. (1972). Fourier Descriptors for Plane Closed Curves. *IEEE Transactions on Computers*.
2.  Persoon, E., & Fu, K. S. (1977). Shape Discrimination Using Fourier Descriptors. *IEEE Transactions on Systems, Man, and Cybernetics*.
3.  Zhang, D., & Lu, G. (2002). A comparative study of Fourier descriptors for shape representation and retrieval. *Visual Communication and Image Representation*.
