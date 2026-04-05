# Corner Detection: FAST, Harris, Shi-Tomasi, and SUSAN

## 1. Overview
Corner detection is an approach used within computer vision systems to extract certain kinds of features and infer the contents of an image. Corner detection is frequently used in motion detection, image registration, video tracking, image mosaicing, panorama stitching, and object recognition. This report summarizes four fundamental corner detection algorithms: FAST, Harris, Shi-Tomasi, and SUSAN.

## 2. Definitions
*   **Corner:** A point in an image that has high intensity variation in all directions.
*   **Autocorrelation:** A measure of the self-similarity of an image signal under small shifts.
*   **Eigenvalues ($\lambda_1, \lambda_2$):** Values that describe the principal components of the intensity gradient distribution in a local window.
*   **Response Function ($R$):** A value calculated for each pixel to determine if it is a corner.

## 3. Theory
### A. Harris Corner Detector
Uses the autocorrelation matrix $M$ of the gradients $G_x, G_y$ in a window $W$:
$M = \sum_{x,y \in W} w(x, y) \begin{bmatrix} G_x^2 & G_x G_y \\ G_x G_y & G_y^2 \end{bmatrix}$
The response $R = \det(M) - k \cdot (\text{trace}(M))^2$. Corners are points where both $\lambda_1$ and $\lambda_2$ are large.

### B. Shi-Tomasi (Good Features to Track)
A modification of Harris that uses a simpler response function: $R = \min(\lambda_1, \lambda_2)$. It is generally more robust for tracking.

### C. FAST (Features from Accelerated Segment Test)
A high-speed detector that checks a circle of 16 pixels around a candidate pixel $P$. If $n$ contiguous pixels are all brighter or darker than $P$ (by a threshold $t$), $P$ is a corner. It is optimized using machine learning (ID3 tree).

### D. SUSAN (Smallest Univalue Segment Assimilating Nucleus)
A method that does not use image gradients. It compares the intensity of every pixel in a circular mask to the central pixel. Corners are points where the "USAN" area (the set of pixels with similar intensity to the center) is small.

## 4. Pseudo Code (Harris Corner Detector)
```text
function HarrisCorner(image, k, threshold)
    Ix, Iy := ComputeGradients(image)
    Ixx := GaussianBlur(Ix^2)
    Iyy := GaussianBlur(Iy^2)
    Ixy := GaussianBlur(Ix * Iy)
    
    R := (Ixx * Iyy - Ixy^2) - k * (Ixx + Iyy)^2
    
    corners := []
    for each pixel in R
        if R[pixel] > threshold and isLocalMaximum(R, pixel)
            push(corners, pixel)
            
    return corners
```

## 5. Parameters Selections
*   **Sensitivity Factor ($k$):** In Harris, typically $0.04 \leq k \leq 0.06$.
*   **FAST Threshold ($t$):** Higher values result in fewer, more distinct corners.
*   **Window Size:** A larger window (e.g., 5x5) provides more robustness to noise but can blur the corner's exact location.

## 6. Complexity
*   **FAST:** $O(N)$ with a very low constant factor, making it suitable for real-time mobile applications.
*   **Harris/Shi-Tomasi:** $O(N)$ with higher computation due to gradients and Gaussian blurring.
*   **Space Complexity:** $O(N)$ to store intermediate derivative and response maps.

## 7. Usage
*   Real-time SLAM (Simultaneous Localization and Mapping).
*   Structure from Motion (SfM) for 3D reconstruction.
*   Image stitching and panorama creation.
*   Object tracking in video.

## 9. References
1.  Harris, C., & Stephens, M. (1988). A Combined Corner and Edge Detector. Alvey Vision Conference.
2.  Shi, J., & Tomasi, C. (1994). Good Features to Track. IEEE Conference on Computer Vision and Pattern Recognition.
3.  Rosten, E., & Drummond, T. (2006). Machine learning for high-speed corner detection. European Conference on Computer Vision.
4.  Smith, S. M., & Brady, J. M. (1997). SUSAN—A New Approach to Low Level Image Processing. International Journal of Computer Vision.
