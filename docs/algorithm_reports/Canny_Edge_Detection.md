# Canny Edge Detection

## 1. Overview
The Canny edge detector is an edge detection operator that uses a multi-stage algorithm to detect a wide range of edges in images. It was developed by John F. Canny in 1986. Canny also produced a computational theory of edge detection explaining why the technique works.

## 2. Definitions
*   **Gaussian Smoothing:** A process of blurring an image by convolving it with a Gaussian function to reduce noise.
*   **Gradient Magnitude ($G$):** The strength of the edge at a pixel.
*   **Gradient Orientation ($\theta$):** The direction of the edge at a pixel.
*   **Non-Maximum Suppression (NMS):** A technique to "thin" edges by keeping only the local maxima in the direction of the gradient.
*   **Hysteresis Thresholding:** A dual-thresholding method used to connect "weak" edges that are adjacent to "strong" edges.

## 3. Theory
The Canny algorithm consists of five main steps:
1.  **Noise Reduction:** Convolution with a Gaussian filter: $G_\sigma(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$.
2.  **Gradient Calculation:** Computing the image gradients $G_x$ and $G_y$ using Sobel or similar operators. The magnitude $G = \sqrt{G_x^2 + G_y^2}$ and angle $\theta = \arctan(G_y / G_x)$.
3.  **Non-Maximum Suppression:** For each pixel, check if it is a local maximum in the direction of its gradient. If not, suppress it (set to zero).
4.  **Double Thresholding:** Categorize pixels into "strong" (above high threshold $T_H$), "weak" (between low $T_L$ and high $T_H$), and "suppressed" (below $T_L$).
5.  **Edge Tracking by Hysteresis:** Retain weak edges only if they are connected to strong edges.

## 4. Pseudo Code
```text
function CannyEdgeDetection(image, sigma, T_L, T_H)
    smoothed := GaussianBlur(image, sigma)
    Gx, Gy := ComputeGradients(smoothed)
    magnitude := sqrt(Gx^2 + Gy^2)
    theta := atan2(Gy, Gx)
    
    nms_magnitude := NonMaximumSuppression(magnitude, theta)
    
    edges := zeros(size(image))
    for pixel in nms_magnitude
        if pixel >= T_H
            edges[pixel] := strong
        else if pixel >= T_L
            edges[pixel] := weak
            
    final_edges := HysteresisTracking(edges)
    return final_edges
```

## 5. Parameters Selections
*   **$\sigma$ (Gaussian Blur):** Larger $\sigma$ reduces noise but blurs edges. Typically $1.0$ to $2.0$.
*   **$T_L$ and $T_H$:** The thresholds for hysteresis. $T_H$ controls the initial sensitivity, and $T_L$ controls the continuity of edges. A common ratio $T_H / T_L$ is between 2:1 and 3:1.

## 6. Complexity
*   **Time Complexity:** $O(N)$, where $N$ is the number of pixels. Each step (convolution, gradient, NMS, thresholding) is linear with respect to the image size.
*   **Space Complexity:** $O(N)$ to store gradients, magnitude, and intermediate edge maps.

## 7. Usage
*   Object detection and recognition.
*   Image segmentation.
*   Feature extraction in computer vision pipelines.

## 9. References
1.  Canny, J. (1986). A Computational Approach to Edge Detection. IEEE Transactions on Pattern Analysis and Machine Intelligence.
2.  Trucco, E., & Verri, A. (1998). Introductory Techniques for 3-D Computer Vision.
3.  Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing.
