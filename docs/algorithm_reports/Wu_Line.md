# Wu Line (Xiaolin Wu's Line Algorithm)

## 1. Overview
**Wu Line** is an algorithm for drawing anti-aliased lines on a pixel grid. While Bresenham's algorithm produces "stair-step" lines (aliasing), Wu's algorithm calculates the intensity of two adjacent pixels for each point along the line, resulting in a much smoother appearance.

## 2. Definitions
- **Anti-aliasing:** A technique for smoothing jagged edges by using multiple shades/colors for each pixel based on how much it is covered by a shape.
- **Fractional Coordinate:** The actual mathematical position of the line as it passes through a pixel row/column.
- **Coverage:** The percentage of a pixel's area that the line covers.

## 3. Theory
Bresenham's algorithm only chooses the pixel closest to the line and colors it 100%. Wu's algorithm calculates the distance from the line's exact path to the centers of the two closest pixels. It then distributes the intensity between these two pixels:
- The pixel closer to the line gets a higher intensity.
- The pixel further away gets a lower intensity.
- The total intensity of the two pixels remains constant.

This is essentially a linear interpolation of the pixel values along the $x$ or $y$ axis (whichever is the "driving" axis).

## 4. Pseudo Code
```python
def wu_line(x0, y0, x1, y1):
    # 1. Handle steep lines by swapping x and y
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        
    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1.0
    
    # 2. Iterate through pixels along x-axis
    y = float(y0)
    for x in range(round(x0), round(x1) + 1):
        # 3. Compute intensity for two adjacent pixels
        intensity1 = 1.0 - (y - floor(y))
        intensity2 = y - floor(y)
        
        if steep:
            plot(floor(y), x, intensity1)
            plot(floor(y) + 1, x, intensity2)
        else:
            plot(x, floor(y), intensity1)
            plot(x, floor(y) + 1, intensity2)
        
        # 4. Advance y by the gradient
        y += gradient
```

## 5. Parameters Selections
- **Intensity Mapping:** Intensities are typically mapped to a grayscale range (0-255).
- **Gamma Correction:** For optimal visual results, the calculated intensities should be gamma-corrected before display.
- **Line Width:** While the standard algorithm draws 1-pixel wide lines, it can be extended to thicker lines with a similar anti-aliasing principle.

## 6. Complexity
- **Time Complexity:** $O(L)$ where $L$ is the number of pixels along the longest axis. It is slightly slower than Bresenham's due to the floating-point operations (or fixed-point arithmetic) and drawing twice as many pixels.
- **Space Complexity:** $O(L)$ or $O(1)$ depending on whether pixels are stored or directly plotted.

## 7. Usage
- **Graphics Libraries:** Used in libraries like Cairo or early versions of Windows GDI for high-quality 2D line drawing.
- **Computer-Aided Design (CAD):** Rendering blueprints and technical drawings where smoothness is critical.
- **Fonts:** Part of the rasterization process for vector fonts (TrueType, OpenType).

## 9. References
1.  Wu, X. (1991). *An Efficient Antialiasing Technique*. ACM SIGGRAPH Computer Graphics.
2.  Bresenham, J. E. (1965). *Algorithm for Computer Control of a Digital Plotter*. IBM Systems Journal (for comparison).
3.  Foley, J. D., et al. (1995). *Computer Graphics: Principles and Practice*. Addison-Wesley.
