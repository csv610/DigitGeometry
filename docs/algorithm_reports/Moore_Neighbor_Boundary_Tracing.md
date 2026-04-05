# Moore Neighbor Boundary Tracing

## 1. Overview
**Moore Neighbor Boundary Tracing** is an algorithm for finding the boundary (contour) of a connected set of pixels in a binary image. It is based on the idea of navigating around the boundary by checking the 8-neighbors (the "Moore neighborhood") of the current boundary pixel.

## 2. Definitions
- **Binary Image ($I$):** A 2D grid where pixels are either 0 (background) or 1 (foreground).
- **Moore Neighborhood:** For a pixel $(x, y)$, the 8 adjacent pixels: $\{(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)\}$.
- **Boundary:** The sequence of foreground pixels that separate the object from the background.

## 3. Theory
The algorithm starts with an initial boundary pixel. From this pixel, it systematically checks its 8 neighbors in a clockwise (or counter-clockwise) manner to find the next boundary pixel. The search for the next neighbor starts from the pixel that was the background neighbor just before the previous boundary pixel was found. This ensures that the algorithm "hugs" the object's exterior.

## 4. Pseudo Code
```python
def moore_neighbor_tracing(image):
    # 1. Find the starting pixel (leftmost, then topmost foreground pixel)
    start_pixel = find_start_pixel(image)
    if start_pixel is None: return []

    boundary = [start_pixel]
    current_pixel = start_pixel
    
    # 2. Backtrack pixel: the pixel from which we started scanning
    # (Initially, the one to the left of start_pixel)
    backtrack_pixel = (start_pixel[0], start_pixel[1] - 1)
    
    while True:
        # 3. Scan neighbors of current_pixel clockwise starting from backtrack_pixel
        neighbors = get_8_neighbors_clockwise(current_pixel, backtrack_pixel)
        
        for i, neighbor in enumerate(neighbors):
            if image[neighbor[0], neighbor[1]] == 1:
                next_pixel = neighbor
                # backtrack_pixel for next step is the neighbor BEFORE next_pixel
                backtrack_pixel = neighbors[i-1]
                break
        
        # 4. Terminate when we return to start_pixel AND next boundary pixel would be the same
        if next_pixel == start_pixel:
            break
            
        boundary.append(next_pixel)
        current_pixel = next_pixel
        
    return boundary
```

## 5. Parameters Selections
- **Neighbor Ordering:** Clockwise search typically produces a counter-clockwise boundary sequence.
- **Connectivity:** Specifically designed for 8-connected objects. For 4-connected objects, the search should be limited to the 4-neighborhood.
- **Stopping Condition:** Simple "back to start" might fail for certain thin objects (one-pixel thick); Jacob's stopping condition (returning to start from the same direction) is more robust.

## 6. Complexity
- **Time Complexity:** $O(B \cdot 8)$, where $B$ is the number of pixels on the boundary. In the worst case, $O(N^2)$ for an image with $N \times N$ pixels, but usually proportional to the perimeter length.
- **Space Complexity:** $O(B)$ to store the boundary sequence.

## 7. Usage
- **Object Recognition:** Extracting shape features from contours (e.g., Fourier descriptors, chain codes).
- **Medical Imaging:** Segmenting organs or lesions from CT/MRI slices.
- **Graphics:** Vectorizing raster images.

## 9. References
1.  Moore, E. F. (1962). *Machine Models of Self-Reproduction*. Proc. Sympos. Math. Problems in Biological Sciences.
2.  Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing*. Pearson.
3.  Ghuneim, A. G. (2000). *Contour Tracing Algorithms*. University of Windsor.
