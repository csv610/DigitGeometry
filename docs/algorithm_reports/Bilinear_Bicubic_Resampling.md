# Bilinear and Bicubic Resampling

## 1. Overview
Bilinear and Bicubic Resampling are popular methods for interpolation in image processing, used to estimate pixel values when resizing an image or performing geometric transformations. They provide a balance between computational efficiency and image quality.

## 2. Definitions
*   **Resampling:** The process of changing the number of pixels in an image (upsampling or downsampling).
*   **Interpolation:** Estimating a value at an unknown point based on known surrounding data points.
*   **Nearest Neighbor:** Selecting the value of the closest pixel (simplest, but creates blocky artifacts).
*   **Bilinear:** Using the 4 nearest pixels to estimate the value.
*   **Bicubic:** Using the 16 nearest pixels to estimate the value.

## 3. Theory
### Bilinear Resampling
For a point $(x, y)$ in the target image, let its floating-point source coordinates be $(u, v)$. Bilinear interpolation performs a weighted average of the 4 surrounding pixels $(Q_{11}, Q_{12}, Q_{21}, Q_{22})$:
1.  Interpolate linearly in the $x$-direction between $Q_{11}$ and $Q_{21}$, and between $Q_{12}$ and $Q_{22}$.
2.  Interpolate linearly in the $y$-direction between those two results.

### Bicubic Resampling
Bicubic interpolation uses a cubic polynomial to smooth the transitions. It considers a $4 \times 4$ neighborhood of 16 pixels. The interpolation kernel is often a Catmull-Rom spline:
$$ W(x) = \begin{cases} (a+2)|x|^3 - (a+3)|x|^2 + 1 & \text{for } |x| \leq 1 \\ a|x|^3 - 5a|x|^2 + 8a|x| - 4a & \text{for } 1 < |x| < 2 \\ 0 & \text{otherwise} \end{cases} $$
Typically, $a = -0.5$. Bicubic produces smoother results and preserves more detail than bilinear but is computationally more expensive.

## 4. Pseudo Code
```text
function Resample(image, new_width, new_height, method)
    new_image := empty_image(new_width, new_height)
    for each pixel (x', y') in new_image
        u := x' * (image.width / new_width)
        v := y' * (image.height / new_height)
        if method == "Bilinear"
            new_image[x', y'] := Bilinear_Interpolate(image, u, v)
        else if method == "Bicubic"
            new_image[x', y'] := Bicubic_Interpolate(image, u, v)
    return new_image
```

## 5. Parameters Selections
*   **Scale Factor:** The ratio between the source and target image sizes.
*   **Cubic Parameter ($a$):** For bicubic interpolation, $a = -0.5$ is a common choice that balances sharpness and ringing.
*   **Edge Handling:** How to handle coordinates outside the source image (clamping, wrapping, or reflecting).

## 6. Complexity
*   **Time Complexity:**
    *   Bilinear: $O(W \cdot H \cdot 4)$ operations.
    *   Bicubic: $O(W \cdot H \cdot 16)$ operations.
*   **Space Complexity:** $O(W \cdot H)$ to store the resampled image.

## 7. Usage
*   **Image Scaling:** Upsampling (zooming in) or downsampling (creating thumbnails).
*   **Geometric Transforms:** Rotating or shearing an image.
*   **Video Playback:** Resizing video frames to fit a screen resolution.
*   **Deep Learning:** Preprocessing images for input into neural networks.

## 9. References
1.  Keys, R. (1981). Cubic convolution interpolation for digital image processing. IEEE Transactions on Acoustics, Speech, and Signal Processing.
2.  Wolberg, G. (1990). Digital Image Warping. IEEE Computer Society Press.
3.  Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing.
