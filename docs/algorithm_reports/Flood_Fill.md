# Flood Fill Algorithm

## 1. Overview
The Flood Fill algorithm is a classic technique used in computer graphics and image processing to determine the area connected to a given node in a multi-dimensional array. It is the core algorithm behind the "bucket" fill tool in paint programs. The algorithm starts at a "seed" node and spreads to all neighboring nodes that share a common attribute (e.g., color), replacing that attribute with a new one.

## 2. Definitions
*   **Seed Point ($x, y$):** The starting coordinate for the fill operation.
*   **Target Color ($C_t$):** The original color of the seed point that needs to be replaced.
*   **Replacement Color ($C_r$):** The new color to be applied to the connected region.
*   **Connectivity:** Defines which neighbors are considered connected. Common types are 4-connectivity (up, down, left, right) and 8-connectivity (includes diagonals).

## 3. Theory
Flood fill is essentially a graph traversal problem. The image is treated as a grid graph where pixels are nodes and adjacent pixels are connected by edges. The algorithm explores the connected component containing the seed point.
There are two main approaches:
1.  **Stack-based (Recursive or Iterative):** Uses a stack or recursion to visit neighbors. Simple to implement but can lead to stack overflow on large images if implemented recursively.
2.  **Queue-based (Breadth-First Search):** Uses a queue to explore the region level by level.
3.  **Scanline Fill:** An optimized version that fills horizontal spans of pixels at once, reducing the number of stack/queue operations and improving cache locality.

## 4. Pseudo Code
### Recursive 4-way Flood Fill
```text
function floodFill(x, y, targetColor, replacementColor)
    if targetColor = replacementColor then return
    if getPixel(x, y) != targetColor then return
    
    setPixel(x, y, replacementColor)
    
    floodFill(x + 1, y, targetColor, replacementColor)
    floodFill(x - 1, y, targetColor, replacementColor)
    floodFill(x, y + 1, targetColor, replacementColor)
    floodFill(x, y - 1, targetColor, replacementColor)
```

### Stack-based Iterative Flood Fill
```text
function floodFill(x, y, targetColor, replacementColor)
    if targetColor = replacementColor then return
    if getPixel(x, y) != targetColor then return
    
    stack := { (x, y) }
    while stack is not empty
        (x, y) := stack.pop()
        if getPixel(x, y) = targetColor
            setPixel(x, y, replacementColor)
            stack.push(x + 1, y)
            stack.push(x - 1, y)
            stack.push(x, y + 1)
            stack.push(x, y - 1)
```

## 5. Parameters Selections
*   **Connectivity:** Choose 4-connectivity for simple grid-aligned regions or 8-connectivity if diagonal connections are required.
*   **Tolerance:** In real-world images (e.g., photos), pixels may not have the *exact* same color. A tolerance parameter allows filling pixels within a certain distance in color space (e.g., Euclidean distance in RGB).

## 6. Complexity
*   **Time Complexity:** $O(N)$, where $N$ is the number of pixels in the connected region. Each pixel is visited a constant number of times.
*   **Space Complexity:** $O(N)$ in the worst case for the stack or queue. Scanline variants can reduce the space complexity to $O(W)$, where $W$ is the width of the image.

## 7. Usage
*   "Paint Bucket" tools in image editors.
*   Finding connected components in binary images.
*   Solving mazes (by filling the path).
*   Game AI for determining reachable areas.

## 9. References
1.  Smith, A. R. (1979). Tint Fill. *ACM SIGGRAPH Computer Graphics*.
2.  Heckbert, P. S. (1990). A Seed Fill Algorithm. *Graphics Gems*.
3.  Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing*.
