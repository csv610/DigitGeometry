# Affine Transform

## 1. Overview
An Affine Transform is a linear mapping method that preserves points, straight lines, and planes. It is a fundamental operation in computer graphics and image processing, allowing for combinations of translation, rotation, scaling, and shearing.

## 2. Definitions
*   **Affine Mapping:** A function $f: X \to Y$ between two affine spaces which consists of a linear transformation followed by a translation.
*   **Parallelism:** One of the key properties of affine transforms is that parallel lines remain parallel after transformation.
*   **Collinearity:** Points lying on the same line before transformation will remain collinear after transformation.
*   **Homogeneous Coordinates:** A system used to represent translation as a matrix multiplication, often using $3 \times 3$ matrices for 2D transforms.

## 3. Theory
In 2D, an affine transform can be represented by a matrix $A$:
$$ \begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} a & b & t_x \\ c & d & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix} $$
where:
*   $a, b, c, d$ define rotation, scaling, and shearing.
*   $t_x, t_y$ define translation.

An affine transform can be uniquely determined by its effect on three non-collinear points.

## 4. Pseudo Code
```text
function Affine_Transform(image, M)
    new_image := empty_image(image.size)
    for each pixel (x, y) in image
        [x', y'] := M * [x, y, 1]
        if (x', y') is within new_image.bounds
            new_image[x', y'] := image[x, y]
    return new_image

// Note: In practice, inverse mapping is used to avoid holes
function Affine_Transform_Inverse(image, M)
    new_image := empty_image(image.size)
    M_inv := inverse(M)
    for each pixel (x', y') in new_image
        [x, y] := M_inv * [x', y', 1]
        if (x, y) is within image.bounds
            new_image[x', y'] := Interpolate(image, x, y)
    return new_image
```

## 5. Parameters Selections
*   **Scaling Factors ($s_x, s_y$):** These determine the size change along the $x$ and $y$ axes.
*   **Rotation Angle ($\theta$):** The angle by which the object is rotated.
*   **Translation Offsets ($t_x, t_y$):** The distance the object is shifted.
*   **Shear Factors ($sh_x, sh_y$):** These determine the "slanting" of the object.
*   **Interpolation Method:** Nearest-neighbor, bilinear, or bicubic. Bilinear is a common default.

## 6. Complexity
*   **Time Complexity:** $O(W \cdot H)$, where $W$ and $H$ are the width and height of the target image. Each pixel is computed once.
*   **Space Complexity:** $O(W \cdot H)$ to store the transformed image.

## 7. Usage
*   Image registration (aligning images from different sources).
*   Correcting geometric distortions in cameras and scanners.
*   Character recognition (normalizing text samples).
*   Computer graphics for moving and scaling objects in 2D and 3D scenes.

## 9. References
1.  Foley, J. D., & Van Dam, A. (1995). Computer Graphics: Principles and Practice.
2.  Hartley, R., & Zisserman, A. (2003). Multiple View Geometry in Computer Vision.
3.  Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing.
