# Distance Transforms: Manhattan and Euclidean

## 1. Overview
A Distance Transform (DT) converts a binary image into a grayscale image where each pixel's intensity represents its distance to the nearest foreground (or background) pixel. It is a fundamental tool in digital geometry for shape representation, skeletonization, and path planning. Common distance metrics include the **Manhattan (L1)**, **Chebyshev (L-infinity)**, and **Euclidean (L2)** distances.

## 2. Definitions
*   **Metric Space ($X, d$):** A set $X$ with a distance function $d(p, q)$ that satisfies the triangle inequality.
*   **Binary Image ($I$):** A set of points representing foreground ($S$) and background ($S^c$).
*   **Distance Transform ($DT$):** For each pixel $p$, $DT(p) = \min_{q \in S} d(p, q)$.
*   **Manhattan Distance ($L_1$):** $d(p, q) = |x_p - x_q| + |y_p - y_q|$. Also called the taxicab or city block distance.
*   **Euclidean Distance ($L_2$):** $d(p, q) = \sqrt{(x_p - x_q)^2 + (y_p - y_q)^2}$. The true straight-line distance.

## 3. Theory
The distance transform is equivalent to finding the minimum value of a cost function across the entire image.
### Manhattan Distance Transform
Can be calculated using a two-pass raster scan (forward and backward) over the image. This is extremely efficient and results in a rhombic shape for equidistant points.
### Euclidean Distance Transform
More complex because the Euclidean metric does not directly decompose into simple local operations in the same way as $L_1$. Efficient algorithms like **Meijster's** or **Fabbri's** achieve exact Euclidean distance in $O(N)$ time using the concept of lower envelopes of parabolas or sequential scans.

## 4. Pseudo Code
### Two-Pass Manhattan Distance Transform
```text
function manhattanDT(image)
    dist := initializeWithInfinity(image)
    for p in foreground: dist[p] := 0
    
    // Forward pass
    for each pixel (x, y) from top-left to bottom-right
        dist[x, y] := min(dist[x, y], 
                          dist[x-1, y] + 1, 
                          dist[x, y-1] + 1)
                          
    // Backward pass
    for each pixel (x, y) from bottom-right to top-left
        dist[x, y] := min(dist[x, y], 
                          dist[x+1, y] + 1, 
                          dist[x, y+1] + 1)
    return dist
```

## 5. Parameters Selections
*   **Distance Metric:** $L_1$ is fastest; $L_2$ is most accurate. Chamfer distance is an approximation to $L_2$ that can be computed using similar scanning passes as $L_1$.
*   **Background/Foreground:** Define whether you are measuring the distance *to* objects or the distance *within* objects.

## 6. Complexity
*   **Time Complexity:** $O(N)$ for both Manhattan and modern Euclidean distance transform algorithms (where $N$ is the number of pixels).
*   **Space Complexity:** $O(N)$ to store the distance values.

## 7. Usage
*   Shape skeletonization and medial axis transform.
*   Pathfinding and obstacle avoidance.
*   Image segmentation (e.g., Watershed algorithm seeds).
*   Distance-based morphological operations (dilation/erosion).
*   Font rendering (SDF - Signed Distance Fields).

## 9. References
1.  Rosenfeld, A., & Pfaltz, J. L. (1966). Sequential operations in digital picture processing. *Journal of the ACM*.
2.  Meijster, A., Roerdink, J. B., & Hesselink, W. H. (2002). A general algorithm for computing distance transforms in linear time. *Mathematical Morphology and its Applications to Image and Signal Processing*.
3.  Fabbri, R., Costa, L. D. F., Torelli, J. C., & Bruno, O. M. (2008). 2D Euclidean Distance Transform Algorithms: A Comparative Survey. *ACM Computing Surveys*.
