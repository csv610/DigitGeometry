# Digital Geometry: Algorithms and Applications

## A Comprehensive Textbook

---

# Chapter 1: Introduction to Digital Geometry

## 1.1 What is Digital Geometry?

Digital geometry deals with the study of geometric properties of discrete objects defined on integer grids. Unlike continuous geometry where points have real-valued coordinates, digital geometry operates on pixel (2D) or voxel (3D) lattices where positions are integer tuples.

**Key Distinctions:**
- **Continuous Space**: Points have real coordinates (x, y) ∈ ℝ²
- **Digital Space**: Points have integer coordinates (i, j) ∈ ℤ²

This distinction fundamentally changes how we approach geometric computations, requiring discrete versions of continuous concepts.

## 1.2 Historical Background

Digital geometry emerged from early computer graphics and image processing:

1. **1960s**: Bresenham's line algorithm revolutionized line drawing
2. **1970s**: Mathematical morphology formalized by Serra
3. **1980s**: Digital topology became a rigorous field
4. **1990s**: Level set methods and distance transforms matured
5. **2000s**: Persistent homology and topological data analysis
6. **2010s**: Deep learning integration with geometric features
7. **2020s**: Neural implicit representations and 3D deep learning

## 1.3 Applications

- **Medical Imaging**: CT/MRI segmentation, shape analysis
- **Computer Vision**: Edge detection, feature extraction
- **Robotics**: Path planning, obstacle avoidance
- **Geographic Information Systems**: Terrain analysis
- **Computer Graphics**: Rasterization, surface reconstruction
- **Material Science**: Microstructure analysis

---

# Chapter 2: Rasterization and Drawing

Rasterization is the process of converting continuous geometric shapes into discrete pixel representations.

## 2.1 Bresenham's Line Algorithm

The classic algorithm for drawing lines on a grid:

```
Algorithm: Bresenham Line
Input: (x₀, y₀), (x₁, y₁) - endpoints
Output: Set of grid points approximating the line

1. dx = x₁ - x₀, dy = y₁ - y₀
2. Initialize decision parameter d = 2*dy - dx
3. For each x from x₀ to x₁:
   - Plot (x, y)
   - If d ≥ 0: y = y + 1, d = d + 2*(dy - dx)
   - Else: d = d + 2*dy
```

**Properties:**
- Optimal in terms of plotted points
- Uses only integer arithmetic
- Produces connected 4-connected line

**Supercover Line Variant**: Ensures all grid cells whose interior intersects the line segment are filled, producing 8-connected representation.

## 2.2 Wu's Anti-Aliased Line Algorithm

For smooth, anti-aliased lines using intensity based on distance:

```python
def wu_line(x0, y0, x1, y1):
    """
    Wu's anti-aliased line algorithm.
    Assigns intensity inversely proportional to distance from ideal line.
    """
    points = []
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    if dx == 0 and dy == 0:
        return [(x0, y0, 1.0)]
    
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    
    if dy <= dx:
        e = dx // 2
        y = y0
        for x in range(x0, x1 + sx, sx):
            dist = abs((x - x0) * dy / dx - (y - y0))
            intensity = 1.0 - min(dist, 1.0)
            points.append((x, y, intensity))
            
            e -= dy
            if e < 0:
                y += sy
                e += dx
    else:
        e = dy // 2
        x = x0
        for y in range(y0, y1 + sy, sy):
            dist = abs((x - x0) - (y - y0) * dx / dy)
            intensity = 1.0 - min(dist, 1.0)
            points.append((x, y, intensity))
            
            e -= dx
            if e < 0:
                x += sx
                e += dy
    
    return points
```

**Intensity Calculation**:
- For each grid cell, compute distance to ideal line
- Assign intensity inversely proportional to distance (0-1 range)

## 2.3 Midpoint Circle Algorithm

Drawing circles using decision variables:

```python
def midpoint_circle(xc, yc, r):
    """
    Midpoint circle algorithm using decision variable.
    Plots 8 symmetric points for each iteration.
    
    Args:
        xc, yc: Center coordinates
        r: Radius
    
    Returns:
        List of (x, y) points forming the circle
    """
    points = []
    
    x, y = 0, r
    d = 1 - r  # Decision variable
    
    def plot_circle_points(x, y):
        """Plot all 8 symmetric points."""
        symmetric = [
            (x, y), (-x, y), (x, -y), (-x, -y),
            (y, x), (-y, x), (y, -x), (-y, -x)
        ]
        for px, py in symmetric:
            points.append((xc + px, yc + py))
    
    plot_circle_points(x, y)
    
    while x < y:
        x += 1
        if d < 0:
            # Midpoint is inside the circle
            d += 2 * x + 3
        else:
            # Midpoint is outside or on the circle
            y -= 1
            d += 2 * (x - y) + 5
        
        plot_circle_points(x, y)
    
    return points
```

**Decision Variable**:
- d < 0: Midpoint is inside → next pixel is on arc
- d ≥ 0: Midpoint is outside → next pixel is outside arc

## 2.4 Scanline Polygon Fill

Fills arbitrary polygons using horizontal scanlines:

1. Find intersection of scanline with each edge
2. Sort intersections by x-coordinate
3. Fill pairs of intersections

## Exercises

**Exercise 2.1**: Implement Bresenham's line algorithm for all octants (not just shallow lines).

**Exercise 2.2**: Modify Wu's algorithm to handle lines with slope > 1 (steep lines).

**Exercise 2.3**: Add anti-aliasing to the midpoint circle algorithm using distance-based intensity.

**Exercise 2.4**: Implement scanline fill for polygons with holes (multi-component boundaries).

**Exercise 2.5**: Compare the quality of Bresenham's line vs. Wu's anti-aliased line for diagonal lines.

**Exercise 2.6**: Create a function that draws an ellipse using the midpoint algorithm.

---

# Chapter 3: Distance Transforms

The distance transform computes the distance from each pixel to the nearest feature pixel.

## 3.1 Mathematical Background

Given a binary image I with feature pixels F = {p : I(p) = 1}, the distance transform computes:

D(p) = min_{q ∈ F} d(p, q)

where d is a distance metric.

## 3.2 Manhattan Distance (L₁)

Also called "city block" or "taxicab" distance:

d₁((x₁,y₁), (x₂,y₂)) = |x₁ - x₂| + |y₁ - y₂|

**Two-Pass Algorithm**:
- Pass 1 (top-left to bottom-right): Compute forward distances
- Pass 2 (bottom-right to top-left): Compute backward distances

## 3.3 Euclidean Distance (L₂)

True shortest-path distance in continuous space:

d₂((x₁,y₁), (x₂,y₂)) = √((x₁-x₂)² + (y₁-y₂)²)

**Two-Pass Algorithm**:
- Forward pass computes lower bounds
- Backward pass refines estimates

## 3.4 Chamfer Distance

Approximation between L₁ and L₂ using weighted masks:

**3-4 Chamfer**:
```
[0 3 4]
[3 0 3]
[4 3 0]
```

**5-7-11 Chamfer** (better approximation):
```
[7 5 7]
[5 0 5]
[7 5 7]
```

## 3.5 Geodesic Distance

Distance constrained by a mask region:

- Only paths within the mask are considered
- Implements "distance within region"

**Algorithm**:
1. Initialize boundary pixels with zero distance
2. Propagate distances using priority queue (wavefront)

## 3.6 Voronoi Diagram

Computes regions closest to each seed:

```
For each pixel p:
    Find seed s that minimizes d(p, s)
    Assign p to region of s
```

## 3.7 Hausdorff Distance

Measures maximum mismatch between two point sets:

d_H(A, B) = max(max_{a∈A} min_{b∈B} d(a,b), max_{b∈B} min_{a∈A} d(a,b))

Useful for shape matching.

### Complete Distance Transform Implementation

```python
import numpy as np
from collections import deque


def manhattan_distance_transform(binary_image):
    """
    Two-pass Manhattan (L1) distance transform.
    
    Args:
        binary_image: 2D binary array (1 = feature, 0 = background)
    
    Returns:
        Distance field
    """
    h, w = binary_image.shape
    dist = np.full((h, w), np.inf)
    
    # Pass 1: top-left to bottom-right
    for y in range(h):
        for x in range(w):
            if binary_image[y, x] == 1:
                dist[y, x] = 0
            else:
                if y > 0:
                    dist[y, x] = min(dist[y, x], dist[y-1, x] + 1)
                if x > 0:
                    dist[y, x] = min(dist[y, x], dist[y, x-1] + 1)
    
    # Pass 2: bottom-right to top-left
    for y in range(h-1, -1, -1):
        for x in range(w-1, -1, -1):
            if y < h-1:
                dist[y, x] = min(dist[y, x], dist[y+1, x] + 1)
            if x < w-1:
                dist[y, x] = min(dist[y, x], dist[y, x+1] + 1)
    
    return dist


def chamfer_distance_transform(binary_image, weights=(3, 4)):
    """
    Chamfer distance transform using weighted masks.
    
    Args:
        binary_image: 2D binary array
        weights: (d_weight, d_diag) - typically (3, 4) for 3-4 chamfer
    
    Returns:
        Distance field
    """
    h, w = binary_image.shape
    d1, d2 = weights
    dist = np.full((h, w), np.inf)
    
    # Pass 1
    for y in range(h):
        for x in range(w):
            if binary_image[y, x] == 1:
                dist[y, x] = 0
            else:
                if y > 0:
                    dist[y, x] = min(dist[y, x], dist[y-1, x] + d1)
                if x > 0:
                    dist[y, x] = min(dist[y, x], dist[y, x-1] + d1)
                if y > 0 and x > 0:
                    dist[y, x] = min(dist[y, x], dist[y-1, x-1] + d2)
                if y > 0 and x < w-1:
                    dist[y, x] = min(dist[y, x], dist[y-1, x+1] + d2)
    
    # Pass 2
    for y in range(h-1, -1, -1):
        for x in range(w-1, -1, -1):
            if y < h-1:
                dist[y, x] = min(dist[y, x], dist[y+1, x] + d1)
            if x < w-1:
                dist[y, x] = min(dist[y, x], dist[y, x+1] + d1)
            if y < h-1 and x < w-1:
                dist[y, x] = min(dist[y, x], dist[y+1, x+1] + d2)
            if y < h-1 and x > 0:
                dist[y, x] = min(dist[y, x], dist[y+1, x-1] + d2)
    
    return dist


def geodesic_distance_transform(binary_image, mask):
    """
    Geodesic distance transform constrained by mask.
    
    Args:
        binary_image: 2D binary (1 = seeds)
        mask: Binary mask defining valid region
    
    Returns:
        Geodesic distance field
    """
    h, w = binary_image.shape
    dist = np.full((h, w), np.inf)
    queue = deque()
    
    # Initialize with seeds
    for y in range(h):
        for x in range(w):
            if binary_image[y, x] == 1 and mask[y, x]:
                dist[y, x] = 0
                queue.append((y, x))
    
    # Wavefront propagation
    while queue:
        y, x = queue.popleft()
        d = dist[y, x] + 1
        
        for ny, nx in [(y+1,x), (y-1,x), (y,x+1), (y,x-1)]:
            if 0 <= ny < h and 0 <= nx < w:
                if mask[ny, nx] and dist[ny, nx] > d:
                    dist[ny, nx] = d
                    queue.append((ny, nx))
    
    return dist


def hausdorff_distance(points_a, points_b):
    """
    Hausdorff distance between two point sets.
    
    Args:
        points_a: List of (x, y) points
        points_b: List of (x, y) points
    
    Returns:
        Hausdorff distance
    """
    def point_to_set(p, point_set):
        return min(((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5 for q in point_set)
    
    forward = max(point_to_set(a, points_b) for a in points_a)
    backward = max(point_to_set(b, points_a) for b in points_b)
    
    return max(forward, backward)
```

## Exercises

**Exercise 3.1**: Implement the Euclidean distance transform using the two-pass algorithm.

**Exercise 3.2**: Create a 5-7-11 chamfer mask and compare results with 3-4 chamfer.

**Exercise 3.3**: Compute the Voronoi diagram from the distance transform results.

**Exercise 3.4**: Modify the geodesic distance transform for 8-connected paths.

**Exercise 3.5**: Implement the directed Hausdorff distance (not symmetric).

---

# Chapter 4: Mathematical Morphology

Mathematical morphology studies the shape and structure of objects through set operations.

## 4.1 Basic Operations

### Dilation
Expands the object by adding pixels at boundaries:

A ⊕ B = {z | (B̂)_z ∩ A ≠ ∅}

Where B̂ is the reflection of structuring element B.

### Erosion
Shrinks the object by removing boundary pixels:

A ⊖ B = {z | (B)_z ⊆ A}

## 4.2 Compound Operations

### Opening
Erosion followed by dilation:

A ○ B = (A ⊖ B) ⊕ B

Removes small objects and smooths boundaries.

### Closing
Dilation followed by erosion:

A • B = (A ⊕ B) ⊖ B

Fills small holes and smooths boundaries.

### Boundary
∂A = A - (A ⊖ B)

## 4.3 Top-Hat Transforms

### White Top-Hat
A - (A ○ B)

Extracts small bright features.

### Black Top-Hat
(A • B) - A

Extracts small dark features.

## 4.4 Morphological Skeleton

The skeleton (medial axis) preserves topology while reducing dimension:

```python
def morphological_skeleton(image):
    skeleton = zeros_like(image)
    while True:
        eroded = erode(image)
        opened = dilate(eroded)
        boundary = image - opened
        skeleton = skeleton + boundary
        image = eroded
        if no pixels remain:
            break
    return skeleton
```

**Properties**:
- Preserves connectivity
- Centers objects
- Useful for shape analysis

## 4.5 Structuring Elements

Predefined shapes:

```python
SE_SQUARE_3X3 = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]

SE_CROSS_3X3 = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

## Exercises

**Exercise 4.1**: Implement grayscale dilation and erosion (not binary).

**Exercise 4.2**: Create a top-hat transform that extracts objects of a specific size.

**Exercise 4.3**: Compare the morphological skeleton with the skeleton from distance transform.

**Exercise 4.4**: Implement geodesic morphological operations (dilation constrained by mask).

**Exercise 4.5**: Design a structuring element for corner detection using morphological operations.

**Exercise 4.6**: Implement opening-by-reconstruction and closing-by-reconstruction.

---

# Chapter 5: Topology

Topology studies properties preserved under continuous deformations.

## 5.1 Connected Components

**4-Connectivity**: Neighbors are N, S, E, W

**8-Connectivity**: Includes diagonals

### Union-Find Algorithm

```python
def count_connected_components(image):
    n = width * height
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    # Union all foreground pixels
    for each foreground pixel:
        union with 4-connected neighbors
    
    # Count unique components
    return len(set(find(i) for i in range(n)))
```

## 5.2 Euler Characteristic

For 2D objects:

χ = C - H

where C = components, H = holes

For voxels in 3D:

χ = V - E + F

where V = voxels, E = edges, F = faces

## 5.3 Betti Numbers

Topological invariants:

- **β₀**: Number of connected components
- **β₁**: Number of holes/loops
- **β₂**: Number of voids (3D)

## 5.4 Persistent Homology

Tracks topological features across scales:

```python
def compute_h0_persistence(image):
    # Track connected components as threshold changes
    # Birth = first appearance
    # Death = merge with another component
    # Persistence = death - birth
```

**Use Cases**:
- Shape clustering
- Feature selection
- Data simplification

---

# Chapter 6: Edge Detection

Edge detection identifies boundaries in images.

## 6.1 Gradient-Based Operators

### Sobel Operator

Two 3×3 kernels:

```
Gx = [[-1, 0, 1],      Gy = [[-1, -2, -1],
       [-2, 0, 2],           [ 0,  0,  0],
       [-1, 0, 1]]          [ 1,  2,  1]]
```

Magnitude: G = √(Gx² + Gy²)
Direction: θ = arctan(Gy/Gx)

### Prewitt Operator

Similar to Sobel but with different weights:

```
Gx = [[-1, 0, 1],      Gy = [[-1, -1, -1],
       [-1, 0, 1],           [ 0,  0,  0],
       [-1, 0, 1]]           [ 1,  1, 1]]
```

### Roberts Cross

2×2 operators for diagonal edges:

```
Gx = [[1, 0],      Gy = [[0, 1],
       [0, -1]]         [-1, 0]]
```

## 6.2 Laplacian Operator

Second derivative operator:

```
L4  = [[0, 1, 0],      L8 = [[1, 1, 1],
       [1, -4, 1],          [1, -8, 1],
       [0, 1, 0]]           [1, 1, 1]]
```

**Properties**:
- Detects edges regardless of direction
- Sensitive to noise

## 6.3 Canny Edge Detector

Multi-stage algorithm:

1. **Gaussian Smoothing**: Reduce noise
2. **Gradient Computation**: Find magnitude and direction
3. **Non-Maximum Suppression**: Thin edges
4. **Double Thresholding**: Identify strong/weak edges
5. **Hysteresis**: Connect weak edges to strong edges

```python
def canny(image, low=50, high=150):
    # Step 1: Smooth
    smoothed = gaussian_smooth(image, sigma=1.4)
    
    # Step 2: Gradient
    G, theta = compute_gradient(sobel(smoothed))
    
    # Step 3: Non-maximum suppression
    thinned = non_max_suppress(G, theta)
    
    # Step 4: Double threshold
    strong, weak = threshold(thinned, low, high)
    
    # Step 5: Hysteresis
    edges = hysteresis(strong, weak)
    
    return edges
```

## Exercises

**Exercise 6.1**: Implement the full Canny edge detector including non-maximum suppression.

**Exercise 6.2**: Compare edge detection results using Sobel, Prewitt, and Roberts operators.

**Exercise 6.3**: Add hysteresis thresholding to connect broken edges.

**Exercise 6.4**: Implement Laplacian of Gaussian (LoG) edge detection.

**Exercise 6.5**: Create a multi-scale edge detector using Gaussian pyramids.

**Exercise 6.6**: Compare Canny with Laplacian for edge localization accuracy.

---

# Chapter 7: Feature Detection

Interest point detection finds distinctive image locations.

## 7.1 Harris Corner Detector

Detects corners using local structure tensor:

**Structure Tensor**:
M = [I_x²  I_x I_y]
    [I_x I_y  I_y²]

**Corner Response**:
R = det(M) - k · tr(M)²
  = (I_x²·I_y² - I_xy²) - k(I_x² + I_y²)²

Where k is typically 0.04-0.06.

## 7.2 Shi-Tomasi Corner Detector

Simpler than Harris, uses minimum eigenvalue:

λ_min > threshold

## 7.3 SUSAN Detector

Uses local brightness similarity:

- For each pixel, compare to center
- Count similar pixels (USAN)
- Corners have small USAN

## 7.4 FAST Detector

Tree-based corner test:

1. Test 4 neighbors at distance 3
2. If ≥ 3 are brighter/darker, continue
3. Check 8 outer ring
4. Full corner test if passed

Very fast but may have false positives.

## 7.5 Structure Tensor

Second-order moment matrix:

```
M = Σ [I_x²  I_x I_y]
      [I_x I_y  I_y²]
```

Used for:
- Corner detection
- Edge detection
- Orientation estimation

---

# Chapter 8: Contour Processing

Contours represent boundaries of objects.

## 8.1 Flood Fill

Fills connected region from seed:

```python
def flood_fill(image, seed, fill_value):
    stack = [seed]
    while stack:
        x, y = stack.pop()
        if image[x, y] == original_value:
            image[x, y] = fill_value
            for neighbor in 4-connected:
                stack.append(neighbor)
```

## 8.2 Moore Neighbor Tracing

Boundary following algorithm:

1. Start at leftmost boundary pixel
2. Visit neighbors in clockwise order
3. Mark visited pixels
4. Stop when returning to start

## 8.3 Suzuki Contour Tracing

Ordered contour extraction for binary images:

- Assigns hierarchy to contours (parent/child)
- Handles holes correctly
- Used in many standards (ITU-T, ISO)

## 8.4 Freeman Chain Code

Encodes contour as direction sequence:

```
0 = N, 1 = NE, 2 = E, 3 = SE
4 = S, 5 = SW, 6 = W, 7 = NW
```

Example: `0011122234566677`

**Properties**:
- Compact representation
- Invariant to translation
- Rotation requires normalization

## 8.5 Run-Length Encoding

Compact representation of binary images:

```python
def run_length_encode(image):
    # Consecutive same-value pixels grouped
    # Format: [(value, count), ...]
```

```python
def run_length_decode(rle_data, width, height):
    """Decode run-length encoding back to image."""
    result = []
    for value, count in rle_data:
        result.extend([value] * count)
    return np.array(result).reshape(height, width)


def freeman_chain_code(contour):
    """
    Compute Freeman chain code from contour points.
    
    Args:
        contour: List of (x, y) points in order
    
    Returns:
        Chain code as list of integers 0-7
    """
    if len(contour) < 2:
        return []
    
    code = []
    directions = [
        (-1, 0), (-1, 1), (0, 1), (1, 1),
        (1, 0), (1, -1), (0, -1), (-1, -1)
    ]
    
    for i in range(len(contour) - 1):
        dx = contour[i+1][0] - contour[i][0]
        dy = contour[i+1][1] - contour[i][1]
        
        for j, (dxd, dyd) in enumerate(directions):
            if dxd == dx and dyd == dy:
                code.append(j)
                break
    
    return code
```

## Exercises

**Exercise 8.1**: Implement 8-connected flood fill using a queue.

**Exercise 8.2**: Modify the chain code to be rotation-normalized using first difference.

**Exercise 8.3**: Implement the Moore neighbor boundary tracing algorithm.

**Exercise 8.4**: Add hole handling to the contour extraction algorithm.

**Exercise 8.5**: Compare RLE with chain codes for contour compression ratio.

**Exercise 8.6**: Implement chain code smoothing to reduce noise.

---

# Chapter 9: Pathfinding

Finding paths through digital spaces.

## 9.1 A* Algorithm

Optimal pathfinding using heuristics:

```python
def a_star(start, goal, grid):
    open_set = PriorityQueue()
    open_set.add(start, 0)
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        current = open_set.pop_lowest()
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + d(current, neighbor)
            if tentative_g < g_score.get(neighbor, ∞):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor, goal)
                open_set.add(neighbor, f_score)
    
    return None  # No path
```

**Heuristics**:
- Manhattan distance for 4-connected
- Euclidean distance for 8-connected

## 9.2 Fast Marching Method

Eikonal equation solver:

∂u/∂x = |∇u|

Propagates wavefront from seeds:

```python
def fast_marching(seeds, grid):
    distances = ∞
    active = PriorityQueue()
    
    for seed in seeds:
        distances[seed] = 0
        active.add(seed, 0)
    
    while active:
        current = active.pop_lowest()
        for neighbor in neighbors(current):
            if distances[neighbor] > distances[current] + 1:
                distances[neighbor] = distances[current] + 1
                active.add(neighbor, distances[neighbor])
    
    return distances
```

## Exercises

**Exercise 9.1**: Implement A* with diagonal movement (8-connected) and proper heuristic.

**Exercise 9.2**: Add obstacle avoidance using collision detection.

**Exercise 9.3**: Compare A* with Dijkstra's algorithm (zero heuristic).

**Exercise 9.4**: Implement the Fast Marching Method for irregular grids.

**Exercise 9.5**: Add path smoothing (reduce jagged edges) using curve simplification.

**Exercise 9.6**: Implement dynamic obstacle avoidance (re-plan when obstacle appears).

---

# Chapter 10: Curve Analysis

## 10.1 Point in Polygon

Ray casting algorithm:

```python
def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        
        if ((y1 > y) != (y2 > y)) and \
           (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    
    return inside
```

## 10.2 Convex Hull

### Graham Scan Algorithm

1. Find bottom-left point
2. Sort others by polar angle
3. Build hull by checking turn direction

### Monotone Chain
O(n log n) algorithm

## 10.3 Douglas-Peucker Simplification

Iterative polyline simplification using perpendicular distance:

```python
def perpendicular_distance(point, line_start, line_end):
    """
    Calculate perpendicular distance from point to line segment.
    
    Args:
        point: (x, y) tuple
        line_start: (x, y) tuple for line start
        line_end: (x, y) tuple for line end
    
    Returns:
        Perpendicular distance
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    dx = x2 - x1
    dy = y2 - y1
    
    if dx == 0 and dy == 0:
        return ((px - x1)**2 + (py - y1)**2) ** 0.5
    
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    
    return ((px - proj_x)**2 + (py - proj_y)**2) ** 0.5


def douglas_peucker(points, epsilon):
    """
    Douglas-Peucker polyline simplification algorithm.
    
    Args:
        points: List of (x, y) points
        epsilon: Maximum distance threshold
    
    Returns:
        Simplified point list
    """
    if len(points) < 3:
        return points[:]
    
    dmax = 0
    index = 0
    for i in range(1, len(points) - 1):
        d = perpendicular_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    
    if dmax > epsilon:
        left = douglas_peucker(points[:index+1], epsilon)
        right = douglas_peucker(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]


def simplify_curve(points, epsilon=1.0):
    """
    Simplify a curve using Douglas-Peucker algorithm.
    
    Args:
        points: List of (x, y) tuples
        epsilon: Tolerance distance
    
    Returns:
        Simplified point list
    """
    if len(points) < 3:
        return points[:]
    
    return douglas_peucker(points, epsilon)
```

**How it works**:
1. Find the point with maximum distance from the line between endpoints
2. If max distance > epsilon, recursively simplify both segments
3. Otherwise, discard all intermediate points

## 10.4 Curve Curvature

### Menger Curvature

κ = 4 * Area / (|AB| · |BC| · |AC|)

### Discrete Curvature

κ(p_i) = 2 * sin(θ/2) / |p_i - p_{i-1}|

## 10.5 Digital Straight Lines (DSL)

A digital straight line satisfies:

- 4-connected: line where ∂f/∂x ∈ {0, ±1}
- 8-connected: line where |∂f/∂x| ≤ 1

**DSL Recognition**: Arithmetical DSL detection uses arithmetic sequences.

## Exercises

**Exercise 10.1**: Implement the convex hull using both Graham scan and monotone chain.

**Exercise 10.2**: Compare Douglas-Peucker simplification at different epsilon values.

**Exercise 10.3**: Implement Menger curvature for a polyline.

**Exercise 10.4**: Add tangent estimation using local fitting.

**Exercise 10.5**: Implement point-in-polygon using winding number algorithm.

**Exercise 10.6**: Test digital straight line recognition with arithmetic sequences.

---

# Chapter 11: Shape Analysis

Quantitative description of shape properties.

## 11.1 Basic Measures

### Area (Shoelace Formula)

```python
def polygon_area(points):
    area = 0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2
```

### Centroid

```
C_x = (1/6A) Σ(x_i + x_{i+1})(x_i y_{i+1} - x_{i+1} y_i)
C_y = (1/6A) Σ(y_i + y_{i+1})(x_i y_{i+1} - x_{i+1} y_i)
```

### Perimeter

Sum of edge lengths.

## 11.2 Derived Metrics

### Circularity

C = 4πA / P²

- Circle: C = 1
- Complex shapes: C < 1

### Solidity

S = A / A_convex

Ratio of area to convex hull area.

### Aspect Ratio

AR = width / height

### Eccentricity

E = (a² - b²) / (a² + b²)

Where a, b are major/minor axes.

### Extent

E = A / (w × h)

### Compactness

K = P² / A

## Exercises

**Exercise 11.1**: Implement all shape metrics (circularity, solidity, aspect ratio, eccentricity, extent, compactness).

**Exercise 11.2**: Compare shape metrics for different shapes (circle, square, triangle, L-shape).

**Exercise 11.3**: Add shape moment computation (central moments, normalized moments).

**Exercise 11.4**: Implement bounding box (minimum area rectangle, not axis-aligned).

**Exercise 11.5**: Test shape similarity metrics on rotated and scaled versions of the same shape.

**Exercise 11.6**: Implement shape signature (distance from centroid vs. angle).

---

# Chapter 12: 3D Geometry

## 12.1 Surface Normals

### Gradient-Based

```python
def estimate_surface_normals(grid):
    normals = []
    for z in range(1, depth-1):
        for y in range(1, height-1):
            for x in range(1, width-1):
                # Central differences
                dz = grid[z+1,y,x] - grid[z-1,y,x]
                dy = grid[z,y+1,x] - grid[z,y-1,x]
                dx = grid[z,y,x+1] - grid[z,y,x-1]
                
                normal = normalize((-dx, -dy, -dz))
                normals.append(normal)
    return normals
```

### Cross Product

For triangle meshes:

n = (v2 - v1) × (v3 - v1)

Normalized for unit normal.

## 12.2 Plane Fitting

Least squares plane fitting:

```python
def fit_plane_least_squares(points):
    # Solve: Ax = b
    # where A = [xi, yi, 1], x = [a,b,c]
    # Minimize ||Ax - b||²
```

## 12.3 Curvature Estimation

### Mean Curvature (2D grid)

H = (∂²f/∂x² + ∂²f/∂y²) / 2

### Gaussian Curvature

K = (∂²f/∂x² · ∂²f/∂y² - (∂²f/∂x∂y)²)

---

# Chapter 13: Spatial Data Structures

## 13.1 Quadtree

2D hierarchical spatial indexing:

```python
class Quadtree:
    def __init__(self, bounds, capacity=4):
        self.bounds = bounds  # (x, y, w, h)
        self.capacity = capacity
        self.points = []
        self.divided = False
    
    def subdivide(self):
        # Create 4 children
        x, y, w, h = self.bounds
        hw, hh = w/2, h/2
        
        self.northeast = Quadtree((x+hw, y, hw, hh), self.capacity)
        self.northwest = Quadtree((x, y, hw, hh), self.capacity)
        self.southeast = Quadtree((x+hw, y+hh, hw, hh), self.capacity)
        self.southwest = Quadtree((x, y+hh, hw, hh), self.capacity)
        self.divided = True
```

## Exercises

**Exercise 13.1**: Implement full Quadtree with insert, query, and range search operations.

**Exercise 13.2**: Compare Quadtree vs. brute force for nearest neighbor search.

**Exercise 13.3**: Implement the Jump Flooding Algorithm for distance fields.

**Exercise 13.4**: Add point removal to the octree implementation.

**Exercise 13.5**: Implement Reeb graph computation from a scalar field.

**Exercise 13.6**: Compare SDF computation using JFA vs. chamfer distance.

---

# Chapter 14: Segmentation

## 14.1 Graph Cuts

### Min-Cut Max-Flow

Formulates segmentation as energy minimization:

```python
def min_cut_max_flow(capacity_matrix):
    # Ford-Fulkerson algorithm
    # Find maximum flow
    # Min cut = saturated edges
```

### Energy Function

E = λ · Data(s) + Smooth(s)

- **Data term**: Fit to seeds
- **Smooth term**: Boundary smoothness

## 14.2 Watershed Transform

Region growing from markers:

1. Compute gradient magnitude
2. Identify local minima (markers)
3. Flood from markers
4. Merge at boundaries
```

## Exercises

**Exercise 14.1**: Implement the min-cut/max-flow algorithm using Ford-Fulkerson.

**Exercise 14.2**: Add energy function with data and smoothness terms for graph cuts.

**Exercise 14.3**: Implement watershed with markers (not automatic detection).

**Exercise 14.4**: Compare graph cut segmentation with and without boundary term.

**Exercise 14.5**: Add spatial coherence to watershed to reduce over-segmentation.

**Exercise 14.6**: Implement interactive segmentation with user-provided seeds.

---

# Chapter 15: Shape Descriptors

Invariant features for shape recognition.

## 15.1 Hu Moments

7 rotation/translation/scale invariant moments:

```python
def calculate_hu_moments(image):
    # Compute raw moments m_ij
    # Compute central moments η_ij
    # Compute normalized moments η_ij'
    # Compute 7 Hu moments
```

**Properties**:
- Invariant to rotation, translation, scale
- Used for shape matching

## 15.2 Zernike Moments

Orthogonal polynomials on unit circle:

- Higher order than Hu moments
- Can reconstruct image from moments
- Rotation invariant

## 15.3 Fourier Descriptors

Frequency domain shape representation:

1. Trace boundary → complex sequence
2. Apply FFT
3. Use low-frequency coefficients

**Properties**:
- Scale invariance (normalize)
- Rotation invariance (phase)
- Translation invariance (centroid subtraction)

## 15.4 Shape Context

Point-based descriptor:

- For each point, compute distribution of other points
- Captures local structure
- Used for matching

## 15.5 Generalized Hough Transform

Template matching for arbitrary shapes:

- Build R-table from template
- Vote in parameter space
- Find peaks

---

# Chapter 16: Image Pyramids

Multi-resolution representation.

## 16.1 Gaussian Pyramid

Downsampling with smoothing:

```python
def build_gaussian_pyramid(image, levels):
    pyramid = [image]
    for i in range(levels - 1):
        # Gaussian blur
        blurred = gaussian_smooth(pyramid[i])
        # Downsample
        downsampled = blurred[::2, ::2]
        pyramid.append(downsampled)
    return pyramid
```

## 16.2 Laplacian Pyramid

Difference of Gaussians:

```python
def build_laplacian_pyramid(gaussian_pyramid):
    laplacian = []
    for i in range(len(gaussian_pyramid) - 1):
        # Upsample
        upsampled = upsample(gaussian_pyramid[i+1])
        # Compute difference
        diff = gaussian_pyramid[i] - upsampled
        laplacian.append(diff)
    laplacian.append(gaussian_pyramid[-1])
    return laplacian
```

**Applications**:
- Image blending
- Compression
- Multi-scale analysis
```

## Exercises

**Exercise 16.1**: Implement multi-resolution blending using Laplacian pyramids.

**Exercise 16.2**: Compare Gaussian pyramid vs. downsampling without smoothing.

**Exercise 16.3**: Use Laplacian pyramid for image compression.

**Exercise 16.4**: Implement hybrid image creation (combine low/high freq from different images).

**Exercise 16.5**: Add frequency-based pyramid construction (wavelet transform).

**Exercise 16.6**: Compare pyramid-based edge detection vs. single-scale Canny.

---

# Chapter 17: 3D Volume Processing

## 17.1 Marching Cubes

Isosurface extraction from 3D volume:

1. For each cell, determine configuration (256 possibilities)
2. Look up edge intersection table
3. Interpolate vertices
4. Generate triangles

```python
def marching_cubes(volume, isolevel):
    # Process all cubes
    # Generate vertices on edges where values cross isolevel
    # Connect vertices into triangles
    # Return (vertices, faces)
```

## 17.2 Thinning

### Zhang-Suen Thinning

Two-step iterative algorithm:

1. Delete pixels satisfying conditions
2. Repeat until stable

Preserves topology while reducing to skeleton.

## 17.3 Medial Axis Transform

Skeleton from distance transform:

```python
def medial_axis_transform(binary):
    # Compute distance transform
    # Find local maxima (skeleton)
    # Preserve distance values
```

## 17.4 Volume Meshes

### Laplacian Mesh Smoothing

```
v' = v + λ Δv
```

Where Δ is the Laplacian operator.

### Mesh Simplification

Edge collapse to reduce polygon count.

---

# Chapter 18: Voxel Processing

## 18.1 Voxel Data Structures

### Sparse Voxel Octree

Hierarchical 3D structure:

- Nodes divide into 8 children
- Only stores occupied cells
- Efficient for large volumes

### Voxel Hashing

Hash-based spatial indexing:

```python
class VoxelHash:
    def _hash_position(self, x, y, z):
        p1, p2, p3 = 73856093, 19349663, 83492791
        return (abs(x)*p1 ^ abs(y)*p2 ^ abs(z)*p3) % table_size
```

## 18.2 Voxel Operations

### Voxelization

Converts mesh to voxel grid:

```python
def voxelize_triangle_mesh(vertices, triangles, resolution):
    # For each triangle, fill voxels along edges
    # Use projection methods
```

### Morphological 3D

- Dilation/Erosion in 3D
- Opening/Closing
- Hole filling

## 18.3 Surface Extraction

### Surface Nets

- Extract vertices at cell corners
- Generate mesh with fewer vertices than marching cubes

### Dual Contouring

- Sample on both inside and outside
- Produces sharper features

## 18.4 Signed Distance Fields

```python
def voxel_sdf_3d(volume):
    # Compute distance to surface
    # Positive outside, negative inside
```

## 18.5 Ray Marching

Volume rendering through ray casting:

```python
def volume_raymarch(volume, origin, direction):
    for step in range(max_steps):
        pos = origin + direction * step
        density = sample(volume, pos)
        if density > threshold:
            return pos
    return None
```

## Exercises

**Exercise 17.1**: Implement the full marching cubes algorithm with edge table lookup.

**Exercise 17.2**: Compare marching cubes with marching tetrahedra for the same volume.

**Exercise 17.3**: Implement the Zhang-Suen thinning algorithm.

**Exercise 17.4**: Add mesh smoothing using Laplacian smoothing.

**Exercise 17.5**: Implement mesh simplification using edge collapse.

**Exercise 17.6**: Compare skeleton from thinning vs. medial axis transform.

---

# Chapter 19: Advanced Topics

## 19.1 Persistent Homology

Multi-scale topological analysis:

- Track birth/death of features
- Construct persistence diagram
- Filter noise

## 19.2 Neural Implicit Representations

Feature volumes for learning:

```python
class FeatureVolume:
    def query_features(self, x, y, z):
        # Trilinear interpolation
        # Returns feature vector
```

## 19.3 Semantic Voxels

Multi-class voxel grids:

```python
class SemanticVoxelGrid:
    # Stores class ID per voxel
    # Supports instance IDs
    # Confidence values
```

## 19.4 Adaptive Octrees

Resolution-adaptive spatial structures:

- Refine near surfaces
- Variable depth based on geometry
- Efficient for complex scenes

## Exercises

**Exercise 18.1**: Implement voxel hashing with hash collision handling.

**Exercise 18.2**: Compare sparse voxel octree vs. dense 3D array for large models.

**Exercise 18.3**: Implement ray marching with early termination.

**Exercise 18.4**: Add normal estimation to volume ray marching.

**Exercise 18.5**: Implement dual contouring for better feature preservation.

**Exercise 18.6**: Compare surface nets vs. marching cubes mesh quality.

---

# Chapter 20: Practical Applications

## 20.1 Medical Imaging

- Organ segmentation
- Shape analysis
- Path planning for surgery

## 20.2 Computer Vision

- Feature matching
- Object recognition
- Scene understanding

## 20.3 Robotics

- Obstacle detection
- Path planning
- SLAM

## 20.4 Computer Graphics

- Surface reconstruction
- Voxel rendering
- Procedural generation

---

# Appendix A: Module Reference

| Module | Description |
|--------|-------------|
| raster | Bresenham, Wu, circle algorithms |
| distance | Distance transforms, Voronoi |
| morphology | Dilation, erosion, skeleton |
| topology | Connected components, Betti numbers |
| edge | Sobel, Canny, Laplacian |
| features | Harris, FAST, SUSAN |
| transforms | Affine, rotation, resampling |
| contours | Flood fill, chain codes |
| pathfinding | A*, fast marching |
| curves | Curvature, simplification |
| shape | Area, perimeter, metrics |
| geometry3d | Normals, plane fitting |
| spatial | Quadtree, octree, SDF |
| segmentation | Graph cuts, watershed |
| descriptors | Hu moments, Zernike, Fourier |
| pyramids | Gaussian, Laplacian |

---

# Appendix B: Algorithm Complexity

| Algorithm | Time | Space |
|-----------|------|-------|
| Bresenham Line | O(n) | O(1) |
| Distance Transform | O(n) | O(n) |
| A* Search | O(b^d) | O(b^d) |
| Connected Components | O(n) | O(n) |
| Marching Cubes | O(n) | O(n) |
| Quadtree Insert | O(log n) | O(n) |

Where n = number of pixels/voxels, b = branching factor, d = depth

---

# Appendix C: References

1. Rosenfeld, A., & Pfaltz, J. L. (1966). Sequential operations in digital picture processing. JACM.

2. Serra, J. (1982). Image Analysis and Mathematical Morphology. Academic Press.

3. Canny, J. (1986). A computational approach to edge detection. TPAMI.

4. Harris, C., & Stephens, M. (1988). A combined corner and edge detector. Alvey Vision Conference.

5. Montanari, O. (1968). On the optimal detection of curves in noisy pictures. Communications of the ACM.

6. Zadeh, L. A. (1969). Fuzzy sets. Information and Control.

---

*This textbook was generated from the Digital Geometry Library codebase, containing 170+ functions across 45 modules covering the full spectrum of digital geometry algorithms.*