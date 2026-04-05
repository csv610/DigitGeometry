# Bresenham's Line Algorithm

## 1. Overview
Bresenham's line algorithm is an efficient algorithm that determines the points of an $n$-dimensional raster that should be selected in order to form a close approximation to a straight line between two points. It is commonly used to draw line primitives in a bitmap image (e.g., on a computer screen), as it uses only integer addition, subtraction, and bit shifting, all of which are very cheap operations in standard computer architectures.

## 2. Definitions
*   **Raster:** A rectangular pattern of parallel scanning lines, or pixels, that form an image on a display.
*   **Decision Variable ($D$):** A value used to determine which pixel is closer to the true line at each step.
*   **Slope ($m$):** The ratio of the vertical change to the horizontal change ($\Delta y / \Delta x$).
*   **Octant:** One of the eight sectors of the 2D plane divided by the axes and the lines $y=x$ and $y=-x$.

## 3. Theory
The algorithm works by incrementing the independent variable ($x$ or $y$, depending on the slope) and choosing the pixel that is closest to the ideal line. 
For a slope $0 \leq m \leq 1$, at each step $x$, we increment $x$ by 1 and decide whether to keep the same $y$ or increment $y$ by 1.
The decision variable $D$ tracks the error relative to the ideal line. If $D > 0$, we increment $y$ and adjust $D$. Otherwise, we keep $y$ and adjust $D$.
By multiplying the error by $2\Delta x$, the algorithm avoids floating-point arithmetic.

## 4. Pseudo Code
```text
function drawLine(x0, y0, x1, y1)
    dx := abs(x1 - x0)
    dy := -abs(y1 - y0)
    sx := x0 < x1 ? 1 : -1
    sy := y0 < y1 ? 1 : -1
    err := dx + dy

    while true
        plot(x0, y0)
        if x0 == x1 and y0 == y1 break
        e2 := 2 * err
        if e2 >= dy
            err += dy
            x0 += sx
        end if
        if e2 <= dx
            err += dx
            y0 += sy
        end if
    end while
```

## 5. Parameters Selections
*   **Coordinate Precision:** The algorithm operates on integer coordinates.
*   **Line Endpoints:** $(x_0, y_0)$ and $(x_1, y_1)$ define the line segment.
*   **Handling All Octants:** The implementation must account for negative slopes and slopes greater than 1 (often by swapping $x$ and $y$).

## 6. Complexity
*   **Time Complexity:** $O(\max(\Delta x, \Delta y))$, as it iterates through the pixels of the line.
*   **Space Complexity:** $O(1)$ (excluding the output buffer).

## 7. Usage
*   2D graphics rendering engines.
*   Plotters and CNC machines for path interpolation.
*   Ray casting in early 3D games (like Wolfenstein 3D).

## 9. References
1.  Bresenham, J. E. (1965). Algorithm for computer control of a digital plotter. IBM Systems Journal.
2.  Hearn, D., & Baker, M. P. (2004). Computer Graphics with OpenGL.
3.  Foley, J. D., van Dam, A., Feiner, S. K., & Hughes, J. F. (1990). Computer Graphics: Principles and Practice.
