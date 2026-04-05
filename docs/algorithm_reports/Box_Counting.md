# Box-Counting Method (Fractal Dimension)

## 1. Overview
The Box-Counting method (also known as the Minkowski-Bouligand dimension) is a practical and widely used algorithm for estimating the fractal dimension of a set in Euclidean space. It is particularly useful for analyzing the complexity of irregular shapes found in nature, such as coastlines, cloud structures, and biological systems. The algorithm estimates how much space a set occupies at increasingly fine scales.

## 2. Definitions
*   **Grid:** A mesh of cells (boxes) of side length $\epsilon$ that covers the set of interest.
*   **$N(\epsilon)$:** The number of boxes of size $\epsilon$ that contain at least one point of the set.
*   **Scaling Limit:** The theoretical limit as $\epsilon$ approaches zero.
*   **Fractal Dimension ($D$):** A non-integer dimension that characterizes the "roughness" or "detail" of a set.

## 3. Theory
The core idea is that for a fractal object, the number of boxes $N(\epsilon)$ required to cover the object scales with the box size $\epsilon$ according to a power law:
$$N(\epsilon) \approx C \cdot \epsilon^{-D}$$
where $D$ is the fractal dimension and $C$ is a constant. Taking the logarithm of both sides gives a linear relationship:
$$\log(N(\epsilon)) \approx D \cdot \log(1/\epsilon) + \log(C)$$
The dimension $D$ can thus be estimated by finding the slope of the line in a log-log plot (logarithm of the count vs. logarithm of the inverse scale).

### Mathematical Definition:
The box-counting dimension is defined as:
$$D_b = \lim_{\epsilon \to 0} \frac{\log N(\epsilon)}{\log(1/\epsilon)}$$

## 4. Pseudo Code
```text
function calculateBoxCountingDimension(image)
    // 1. Determine the range of box sizes (epsilon)
    minScale := 1 (pixel size)
    maxScale := min(width, height)
    scales := powerSeries(start=maxScale, ratio=0.5, end=minScale)
    
    counts := []
    for epsilon in scales:
        count := 0
        // 2. Partition space into a grid of size epsilon
        grid := createGrid(image.width, image.height, epsilon)
        for box in grid:
            // 3. Count boxes that intersect the shape
            if box.containsPointFrom(image):
                count += 1
        counts.append(count)
    
    // 4. Perform linear regression on log(counts) vs log(1/scales)
    D := computeSlope(log(1/scales), log(counts))
    return D
```

## 5. Parameters Selections
*   **Scale Range:** The range of $\epsilon$ is critical. Using too large an $\epsilon$ results in poor resolution, while too small an $\epsilon$ is limited by the pixel size of the digital image.
*   **Grid Offset:** The count $N(\epsilon)$ can vary depending on where the grid is placed. To find the "true" minimum $N(\epsilon)$, some implementations shift the grid by small amounts and take the minimum count.
*   **Ratio:** A common choice for the sequence of scales is powers of two (e.g., $1, 2, 4, 8 \dots$).

## 6. Complexity
*   **Time Complexity:** $O(S \cdot N)$, where $S$ is the number of scales and $N$ is the total number of pixels in the image. For each scale, we scan the entire image once.
*   **Space Complexity:** $O(N)$ to store the image or the grid representation.

## 7. Usage
*   **Texture Analysis:** Distinguishing between different textures in satellite imagery or medical scans.
*   **Ecology:** Measuring the complexity of habitats or the branching patterns of trees.
*   **Geology:** Characterizing the roughness of fault lines or the distribution of mineral deposits.
*   **Neuroscience:** Quantifying the branching complexity of neurons.

## 9. References
1.  Mandelbrot, B. B. (1982). *The Fractal Geometry of Nature*. W. H. Freeman.
2.  Russell, D. A., Hanson, J. D., & Ott, E. (1980). *Dimension of strange attractors*. Physical Review Letters.
3.  Liebovitch, L. S., & Toth, T. (1989). *A fast algorithm to determine fractal dimension by box counting*. Physics Letters A.
