# Fractal Dimension

## 1. Overview
The Fractal Dimension is a statistical measure of the complexity of a shape or pattern, describing how its detail changes with the scale at which it is measured. Unlike Euclidean dimensions (1D lines, 2D planes, 3D volumes), fractal dimensions are often non-integers, reflecting the "roughness" or "irregularity" of natural objects like coastlines, clouds, and vascular systems.

## 2. Definitions
*   **Self-Similarity:** A property where a shape looks similar at different scales.
*   **Hausdorff Dimension ($D_H$):** A theoretical foundation for fractal dimension, based on the measure of a set.
*   **Box-Counting Dimension ($D_b$):** A practical and widely used estimation method that counts the number of boxes of size $\epsilon$ required to cover the shape.
*   **Scaling Factor ($\epsilon$):** The resolution or size of the measuring unit.

## 3. Theory
The fractal dimension $D$ is based on the scaling rule:
$$N(\epsilon) \propto \left( \frac{1}{\epsilon} \right)^D$$
where $N(\epsilon)$ is the number of units of size $\epsilon$ needed to cover the object. Taking the logarithm of both sides gives:
$$\log(N(\epsilon)) \approx D \cdot \log(1/\epsilon) + C$$
The dimension $D$ is then the slope of the line when $\log(N(\epsilon))$ is plotted against $\log(1/\epsilon)$. This is known as the **Box-Counting** method:
$$D = \lim_{\epsilon \to 0} \frac{\log N(\epsilon)}{\log(1/\epsilon)}$$

### Fractal Dimension Examples
*   **Cantor Set:** $D = \log(2)/\log(3) \approx 0.6309$
*   **Sierpinski Gasket:** $D = \log(3)/\log(2) \approx 1.5850$
*   **Koch Snowflake:** $D = \log(4)/\log(3) \approx 1.2619$

## 4. Pseudo Code
### Box-Counting Method
```text
function calculateFractalDimension(image)
    maxScale := min(width, height)
    scales := powerOfTwoSeries(2 to maxScale)
    counts := []
    
    for scale in scales
        count := 0
        grid := divideImageIntoGrid(image, scale)
        for cell in grid
            if cell contains pixels of the shape
                count := count + 1
        counts.append(count)
    
    // Perform linear regression on log(counts) vs log(1/scales)
    D := linearSlope(log(1 / scales), log(counts))
    return D
```

## 5. Parameters Selections
*   **Scale Range:** The range of $\epsilon$ should be large enough to capture the scaling behavior but limited by the image resolution at small scales and the object size at large scales.
*   **Grid Alignment:** The orientation and position of the grid can slightly affect the count. Some algorithms use the minimum possible number of boxes across different grid shifts.

## 6. Complexity
*   **Time Complexity:** $O(N \cdot S)$, where $N$ is the number of pixels and $S$ is the number of scales analyzed.
*   **Space Complexity:** $O(N)$ for image storage or grid masks.

## 7. Usage
*   Analyzing the complexity of biological structures (e.g., lungs, neurons).
*   Surface roughness analysis in material science.
*   Terrain and cloud generation in computer graphics.
*   Time-series analysis (e.g., stock market trends).
*   Image segmentation based on texture.

## 9. References
1.  Mandelbrot, B. B. (1982). *The Fractal Geometry of Nature*.
2.  Falconer, K. (2014). *Fractal Geometry: Mathematical Foundations and Applications*.
3.  Peitgen, H. O., Jürgens, H., & Saupe, D. (2004). *Chaos and Fractals: New Frontiers of Science*.
