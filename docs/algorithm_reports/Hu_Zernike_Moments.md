# Hu and Zernike Moments

## 1. Overview
Image moments are statistical measures that describe the properties and shape of an object in a digital image. They are widely used for shape representation, recognition, and classification. **Hu Moments** are based on standard geometric moments and are invariant to translation, scale, and rotation. **Zernike Moments** are based on orthogonal Zernike polynomials over a unit disk, providing superior shape representation and reconstruction capabilities compared to Hu moments.

## 2. Definitions
*   **Geometric Moment ($m_{pq}$):** The projection of an image onto a polynomial basis.
*   **Central Moment ($\mu_{pq}$):** Moments calculated with respect to the centroid $(\bar{x}, \bar{y})$ of the object, making them translation-invariant.
*   **Normalized Central Moment ($\eta_{pq}$):** Moments that are further scaled to be invariant to magnification.
*   **Hu Invariants ($\phi_i$):** A set of 7 non-linear combinations of normalized central moments that provide invariance to translation, rotation, and scaling.
*   **Zernike Moment ($A_{nm}$):** The projection of the image onto the Zernike complex polynomials $V_{nm}(x, y)$.

## 3. Theory
### Hu Moments
The Hu set consists of seven moments $\phi_1$ through $\phi_7$. The first few are:
$$\phi_1 = \eta_{20} + \eta_{02}$$
$$\phi_2 = (\eta_{20} - \eta_{02})^2 + 4\eta_{11}^2$$
Hu moments are based on the theory of algebraic invariants and have been a standard in shape analysis for decades.

### Zernike Moments
Zernike moments are defined on a unit disk. The $(n, m)$-th Zernike moment is:
$$A_{nm} = \frac{n+1}{\pi} \iint_{x^2+y^2 \leq 1} f(x, y) [V_{nm}(\rho, \theta)]^* dx dy$$
*   **Orthogonality:** Since Zernike polynomials are orthogonal, the moments provide independent information about the shape.
*   **Robustness:** They are more robust to noise than Hu moments and can perfectly reconstruct the image given enough moments.

## 4. Pseudo Code
### Central Moments
```text
function calculateCentralMoments(image)
    m00, m10, m01 := calculateGeometricMoments(image)
    x_bar := m10 / m00, y_bar := m01 / m00
    
    for each pixel (x, y) in image
        mu_pq := sum((x - x_bar)^p * (y - y_bar)^q * f(x, y))
    return mu
```

### Hu Moments
```text
function calculateHuMoments(mu)
    eta := calculateNormalizedMoments(mu)
    phi1 := eta[2,0] + eta[0,2]
    phi2 := (eta[2,0] - eta[0,2])^2 + 4 * eta[1,1]^2
    // ... calculate phi3 through phi7
    return {phi1, ..., phi7}
```

## 5. Parameters Selections
*   **Scale Normalization:** Critical for Hu moments to ensure scale invariance.
*   **Image Centering:** The object must be centered within a unit disk before calculating Zernike moments.
*   **Order ($n$):** Higher-order Zernike moments capture more detail but are more computationally expensive and noise-sensitive. Typically, $n$ is chosen between 5 and 20.

## 6. Complexity
*   **Hu Moments:** $O(N \cdot P)$, where $N$ is the number of pixels and $P$ is the number of moment types (a constant 7).
*   **Zernike Moments:** $O(N \cdot M)$, where $M$ is the number of Zernike polynomials. Computing the polynomials can be expensive.

## 7. Usage
*   Shape recognition and classification (e.g., aircraft, characters).
*   Medical imaging for lesion shape analysis.
*   Content-based image retrieval.
*   Digital watermarking.
*   Object tracking by matching moment signatures between frames.

## 9. References
1.  Hu, M. K. (1962). Visual pattern recognition by moment invariants. *IRE Transactions on Information Theory*.
2.  Teague, M. R. (1980). Image analysis via the general theory of moments. *Journal of the Optical Society of America*.
3.  Khotanzad, A., & Hong, Y. H. (1990). Invariant image recognition by Zernike moments. *IEEE Transactions on Pattern Analysis and Machine Intelligence*.
