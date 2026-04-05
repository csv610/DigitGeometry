# Chamfer Distance Transform

## 1. Overview
The Chamfer Distance Transform (CDT) is a method for approximating the Euclidean distance from every pixel in a binary image to the nearest feature pixel (e.g., edge pixel). While the Euclidean distance transform is computationally expensive, Chamfer distances use local neighborhoods and integer arithmetic to achieve efficient, high-quality approximations.

## 2. Definitions
*   **Distance Transform ($DT$):** A representation of an image where each pixel's value is the distance to the nearest set of object or feature pixels.
*   **Mask:** A small neighborhood of weights used to propagate distances across the image.
*   **Feature Pixel:** A pixel in the binary image that represents the object or boundary of interest (e.g., foreground).

## 3. Theory
Chamfer distances are calculated using a two-pass algorithm (forward and backward). In each pass, a mask is applied that adds relative distances to neighboring pixels and updates the current pixel's value if a smaller distance is found. 
Common masks:
*   **3x3 Chamfer (3, 4):** Approximates distances with weights 3 for orthogonal neighbors and 4 for diagonal neighbors. The final values are divided by 3.
*   **5x5 Chamfer (5, 7, 11):** A more accurate approximation using weights 5, 7, and 11 for orthogonal, diagonal, and "knight's move" neighbors respectively.

The distance $D(p)$ at pixel $p$ is updated as:
$D(p) = \min_{q \in \text{mask}} (D(q) + w(p, q))$, where $w(p, q)$ is the weight in the mask.

## 4. Pseudo Code
```text
function ChamferDistanceTransform(binary_image, mask_weights)
    dist := zeros_like(binary_image)
    dist[binary_image == 0] := 0
    dist[binary_image == 1] := Infinity
    
    // Forward Pass (Top-Left to Bottom-Right)
    for y from 0 to height-1
        for x from 0 to width-1
            if dist[x, y] > 0
                dist[x, y] = min(dist[x, y],
                                 dist[x-1, y] + mask[1, 0],
                                 dist[x, y-1] + mask[0, 1],
                                 dist[x-1, y-1] + mask[1, 1],
                                 dist[x+1, y-1] + mask[-1, 1])
                                 
    // Backward Pass (Bottom-Right to Top-Left)
    for y from height-1 down to 0
        for x from width-1 down to 0
            if dist[x, y] > 0
                dist[x, y] = min(dist[x, y],
                                 dist[x+1, y] + mask[1, 0],
                                 dist[x, y+1] + mask[0, 1],
                                 dist[x+1, y+1] + mask[1, 1],
                                 dist[x-1, y+1] + mask[-1, 1])
    return dist
```

## 5. Parameters Selections
*   **Mask Type:** A larger mask (5x5) provides a better approximation to the Euclidean distance but increases computation.
*   **Weight Scaling:** Using larger integers (e.g., 5, 7, 11) reduces the relative error but requires division at the end to retrieve real distances.

## 6. Complexity
*   **Time Complexity:** $O(N)$, where $N$ is the number of pixels. Each pixel is visited exactly twice.
*   **Space Complexity:** $O(N)$ for the distance map.

## 7. Usage
*   Template matching (e.g., Chamfer matching for object detection).
*   Pathfinding and obstacle avoidance in robotics.
*   Morphological operations and shape analysis.

## 9. References
1.  Borgefors, G. (1986). Distance Transformations in Digital Images. Computer Vision, Graphics, and Image Processing.
2.  Rosenfeld, A., & Pfaltz, J. L. (1966). Sequential Operations in Digital Picture Processing. Journal of the ACM.
3.  Butt, M. A., & Maragos, P. (1998). Optimum Algorithms for Computation of the Chamfer Distance Transform. IEEE Transactions on Image Processing.
