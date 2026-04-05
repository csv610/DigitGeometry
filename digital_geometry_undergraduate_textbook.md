# Digital Geometry
## A Comprehensive Undergraduate Textbook

---

**Preface**

This textbook presents a systematic introduction to digital geometry, the study of geometric properties of discrete objects defined on integer lattices. Unlike continuous geometry where points have real-valued coordinates, digital geometry operates on pixel (2D) or voxel (3D) grids where positions are integer tuples.

The book is designed for undergraduate students in computer science, mathematics, and engineering who have completed courses in data structures, algorithms, and linear algebra. No prior knowledge of image processing is assumed.

---

# Part I: Foundations

# Chapter 1: Introduction to Digital Geometry

## 1.1 The Digital World

In our increasingly digital world, we represent continuous physical objects using discrete approximations. Photographs become arrays of pixels, 3D objects become voxel grids, and shapes become collections of discrete points. Understanding how geometric properties translate from the continuous to the digital domain is fundamental to computer graphics, computer vision, medical imaging, and many other fields.

**Definition 1.1 (Digital Image)**: A digital image is a function $I: \mathbb{Z}^2 \rightarrow V$ where $\mathbb{Z}^2$ is the integer lattice (the set of all pairs of integers) and $V$ is a set of possible values (typically $\{0, 1\}$ for binary images or $\{0, 1, \ldots, 255\}$ for grayscale images).

**Definition 1.2 (Pixel)**: A pixel is the unit element of a digital image, located at integer coordinates $(i, j) \in \mathbb{Z}^2$. The value $I(i, j)$ represents the intensity or color at that location.

## 1.2 Continuous vs. Digital Geometry

In Euclidean geometry, points have precise real-valued coordinates, lines have zero thickness, and shapes have perfect boundaries. In digital geometry, we work with quantized approximations:

| Continuous | Digital |
|------------|---------|
| Point $(x, y) \in \mathbb{R}^2$ | Pixel $(i, j) \in \mathbb{Z}^2$ |
| Line (1D manifold) | Set of connected pixels |
| Curve (1D) | Digital curve (connected set) |
| Region (2D) | Set of pixels |
| Surface (2D in 3D) | Set of voxels |

**The Grid Cell Model**: Consider a unit square centered at each integer coordinate. This creates a partition of $\mathbb{R}^2$ into unit squares called grid cells or pels (picture elements). A pixel at $(i, j)$ represents the cell $[i-0.5, i+0.5] \times [j-0.5, j+0.5]$.

## 1.3 Historical Development

Digital geometry emerged from the intersection of several fields:

**1960s - Early Computer Graphics**
- Jack Bresenham (1965) developed the famous line algorithm
- Early raster graphics systems enabled screen-based computing

**1970s - Mathematical Morphology**
- Jean Serra formalized mathematical morphology
- Set-theoretic operations on images became systematic

**1980s - Digital Topology**
- Rosenfeld established rigorous foundations
- Connectivity paradoxes resolved (border vs. interior)

**1990s - Level Set Methods**
- Osher and Sethian developed level set framework
- Distance transforms and medial axis matured

**2000s - Topological Data Analysis**
- Persistent homology for multi-scale analysis
- Computational topology became a field

**2010s-2020s - Deep Learning Integration**
- Neural networks for geometric feature learning
- Neural implicit representations

## 1.4 Applications

**Medical Imaging**: CT scans, MRI, and ultrasound produce volumetric data. Digital geometry enables:
- Organ segmentation and identification
- Shape analysis for diagnosis
- Surgical planning and navigation

**Computer Vision**: Understanding images requires geometric reasoning:
- Edge detection and feature extraction
- Object recognition and tracking
- Scene reconstruction from multiple views

**Robotics**: Navigation and manipulation rely on geometric computation:
- Path planning in complex environments
- Obstacle detection and avoidance
- Simultaneous Localization and Mapping (SLAM)

**Geographic Information Systems (GIS)**:
- Terrain modeling and analysis
- Watershed delineation
- Spatial indexing for large datasets

**Computer Graphics**:
- Rasterization and rendering
- Voxel-based modeling
- Surface reconstruction from point clouds

## 1.5 Organization of This Book

This textbook is organized into five parts:

- **Part I (Chapters 1-3)**: Foundations - grid topology, connectivity, and digitizations
- **Part II (Chapters 4-7)**: Transformations - distance, morphology, and registration
- **Part III (Chapters 8-11)**: Analysis - features, contours, curves, and shape
- **Part IV (Chapters 12-15)**: Advanced Topics - 3D geometry, volume processing, and voxels
- **Part V (Chapters 16-17)**: Modern Methods - topological data analysis and neural representations

Each chapter includes:
- Detailed explanations with mathematical foundations
- Pseudocode and implementations
- Worked examples
- Exercises ranging from basic to challenging

---

# Chapter 2: Topology of Digital Images

Understanding the topological properties of digital images is essential before we can analyze their geometric features. Topology studies properties that remain invariant under continuous deformations—stretching and bending without tearing.

## 2.1 Digital Connectivity

In a digital image, pixels are connected to their neighbors. The choice of neighbor definition dramatically affects topological properties.

**Definition 2.1 (4-Neighborhood)**: The 4-neighborhood of a pixel $(i, j)$ is:
$$N_4(i, j) = \{(i-1, j), (i+1, j), (i, j-1), (i, j+1)\}$$

**Definition 2.2 (8-Neighborhood)**: The 8-neighborhood of a pixel $(i, j)$ includes all eight surrounding pixels:
$$N_8(i, j) = \{(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)\}$$

**Example 2.1**: Consider the pixel at the corner of an object:
- Using 4-connectivity, it has 2 neighbors (right and above)
- Using 8-connectivity, it has 3 neighbors (right, above, and above-right)

## 2.2 The Connectivity Paradox

A fundamental challenge in digital topology is the "connectivity paradox." Consider the checkerboard pattern:

```
X . X .
. X . X
X . X .
. X . X
```

Using 4-connectivity, the black squares form four separate components. But using 8-connectivity, they all connect diagonally and form one component. Similarly, white squares (the background) are connected under 4-connectivity but form separate islands under 8-connectivity.

**Theorem 2.1 (Jordan Curve Theorem for Digital Images)**: For a simple closed digital curve, the interior and exterior are 4-connected when the curve is 8-connected, and vice versa.

This theorem justifies using mixed connectivity: 4-connectivity for objects (foreground) and 8-connectivity for background, or the converse.

## 2.3 Connected Components

A connected component is a maximal set of pixels where any two pixels are connected via a path of neighboring pixels.

**Algorithm 2.1: Connected Component Labeling**

```python
function LABEL_COMPONENTS(image):
    label = 0
    for each pixel p in image:
        if p is not visited and p is foreground:
            label += 1
            BFS(p, label)  # Breadth-first search
    return labeled_image
```

**Time Complexity**: $O(n)$ where $n$ is the number of pixels.

**Space Complexity**: $O(n)$ for the label array.

## 2.4 Euler Characteristic

The Euler characteristic is a topological invariant that relates the number of connected components, holes, and other features.

**Definition 2.3 (Euler Characteristic)**: For a binary image, the Euler characteristic is:
$$\chi = \text{(number of connected components)} - \text{(number of holes)}$$

**Theorem 2.2**: For a region in a binary image:
$$\chi = V - E + F$$

where $V$ is the number of voxels, $E$ is the number of edges, and $F$ is the number of faces in the boundary representation.

## 2.5 Betti Numbers

Betti numbers provide a more detailed topological description.

**Definition 2.4 (Betti Numbers)**:
- $\beta_0$: Number of connected components
- $\beta_1$: Number of holes (tunnels, loops)
- $\beta_2$: Number of voids (in 3D)

For a solid disk: $\beta_0 = 1, \beta_1 = 0, \beta_2 = 0$
For an annulus (ring): $\beta_0 = 1, \beta_1 = 1, \beta_2 = 0$
For a torus (donut): $\beta_0 = 1, \beta_1 = 2, \beta_2 = 1$

## 2.6 Digital Topology Properties

**Theorem 2.3 (Euler's Formula for Digital Images)**: For any simply connected region in a binary image:
$$N_c - N_h = N_v - N_e + N_f$$

where:
- $N_c$ = number of components
- $N_h$ = number of holes
- $N_v$ = number of voxels
- $N_e$ = number of edges
- $N_f$ = number of faces

**Proof Sketch**: The boundary of a digital region can be represented as a 2D manifold. Euler's formula for planar graphs states $V - E + F = 2 - 2g$ where $g$ is the genus (number of holes). Rearranging yields the formula above. $\square$

## 2.7 Path-Based Connectivity

**Definition 2.5 (Digital Path)**: A digital path is a sequence of pixels $P = (p_0, p_1, \ldots, p_k)$ where each consecutive pair $(p_i, p_{i+1})$ are neighbors according to the chosen connectivity.

**Definition 2.6 (Simple Path)**: A path is simple if it does not repeat any pixel.

**Definition 2.7 (Digital Curve)**: A digital curve is a connected set of pixels where each pixel has at most two neighbors in the set (except endpoints).

**Theorem 2.4**: A digital curve with 4-connectivity is simply connected (has no holes).

---

# Chapter 3: Digitization and Grid Representations

When we convert continuous geometric objects into digital form, we must make fundamental decisions about representation. This chapter explores how continuous shapes become discrete pixel or voxel sets.

## 3.1 The Digitization Process

**Definition 3.1 (Grid Intersection Digitization)**: The grid intersection digitization of a continuous set $S \subset \mathbb{R}^2$ is:
$$D(S) = \{(i, j) \in \mathbb{Z}^2 : (i, j) \in S\}$$

This captures exactly which grid points fall inside the shape.

**Definition 3.2 (Grid Cell Digitization)**: The grid cell digitization captures all cells whose centers lie in $S$:
$$D_c(S) = \{(i, j) \in \mathbb{Z}^2 : \text{center}(i, j) \in S\}$$

## 3.2 The Gauss Circle Problem

How many integer lattice points fall inside a circle of radius $r$?

**Theorem 3.1**: Let $N(r)$ be the number of integer points in a circle of radius $r$. Then:
$$N(r) = \pi r^2 + E(r)$$

where the error term $E(r)$ satisfies $|E(r)| \leq 2\sqrt{2}r + 1$.

**Proof Sketch**: The area of the circle is $\pi r^2$. Each grid cell contributes approximately 1 unit of area. The boundary cells form a region whose perimeter is approximately $2\pi r$, and the width of this boundary region is at most $\sqrt{2}$ (the diagonal of a unit square). Thus the error is bounded by the perimeter times the width, giving the stated bound. $\square$

The Gauss circle problem asks for the best possible error bound—this remains an active research area!

## 3.3 Digitization Models

### 3.3.1 Forward Digitization

Each continuous point maps to its nearest integer:
$$D_F(S) = \{\lfloor x + 0.5 \rfloor, \lfloor y + 0.5 \rfloor : (x, y) \in S\}$$

### 3.3.2 Backward Digitization

A pixel belongs to the digitization if its entire cell intersects the shape:
$$D_B(S) = \{(i, j) : [i, i+1] \times [j, j+1] \cap S \neq \emptyset\}$$

### 3.3.3 Area-Based Digitization

The area of intersection determines whether a pixel is included:
$$D_A(S, T) = \{(i, j) : \text{area}([i, i+1] \times [j, j+1] \cap S) \geq T\}$$

where $T$ is a threshold (typically 0.5).

## 3.4 The Paradox of digitization

Digitization inevitably loses information. A circle digitizes to a "staircase" pattern:

**Theorem 3.2 ( digitization Loss)**: For any digitization scheme mapping continuous shapes to discrete sets:
1. The digitization of a connected set may be disconnected
2. The digitization of a convex set may be non-convex
3. Topological properties may not be preserved

This motivates the study of "digital straightness" and other constrained digitizations.

## 3.5 Grid Orientations

The standard grid is aligned with coordinate axes. Other orientations are sometimes used:

**Definition 3.3 (Hexagonal Grid)**: A hexagonal grid uses hexagonal cells rather than squares. Each cell has 6 neighbors at 60° intervals.

**Advantages of Hexagonal Grids**:
- More uniform neighbor distances
- Better angular resolution
- Preferred for certain texture analysis tasks

The coordinate system for hexagonal grids uses axial coordinates $(q, r)$ where $q + r + s = 0$.

## 3.6 Grid Interpolation

When we need to sample continuous functions at grid points, interpolation determines accuracy:

### Nearest Neighbor
$$I_N(i, j) = I(\lfloor i + 0.5 \rfloor, \lfloor j + 0.5 \rfloor)$$

### Bilinear Interpolation
$$I_B(i + u, j + v) = (1-u)(1-v)I(i,j) + u(1-v)I(i+1,j) + (1-u)vI(i,j+1) + uvI(i+1,j+1)$$

where $u, v \in [0, 1]$ are fractional coordinates.

### Bicubic Interpolation
Uses cubic polynomials for smoother results, requiring 16 neighboring pixels.

**Theorem 3.3 (Interpolation Error)**: For a function with bounded second derivatives:
- Nearest neighbor: $O(1)$ error
- Bilinear: $O(h^2)$ error
- Bicubic: $O(h^4)$ error

where $h$ is the grid spacing.

---

# Part II: Transformations

# Chapter 4: Distance Transforms

The distance transform computes, for each pixel, the distance to the nearest feature pixel. This fundamental operation appears in skeletonization, path planning, shape analysis, and many other applications.

## 4.1 Mathematical Foundation

**Definition 4.1 (Distance Transform)**: Given a binary image $I$ with foreground pixels $F = \{p : I(p) = 1\}$ and background pixels $B = \{p : I(p) = 0\}$, the distance transform $D$ is:
$$D(p) = \min_{q \in F} d(p, q)$$

where $d$ is a distance metric.

## 4.2 Distance Metrics

### 4.2.1 Manhattan Distance (L₁)
$$d_1((x_1, y_1), (x_2, y_2)) = |x_1 - x_2| + |y_1 - y_2|$$

Also called "city block" or "taxicab" distance because it measures the distance traveled on a grid.

### 4.2.2 Euclidean Distance (L₂)
$$d_2((x_1, y_1), (x_2, y_2)) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$

The true shortest-path distance.

### 4.2.3 Chebyshev Distance (L∞)
$$d_\infty((x_1, y_1), (x_2, y_2)) = \max(|x_1 - x_2|, |y_1 - y_2|)$$

Measures distance as the maximum of coordinate differences.

### 4.2.4 Properties of Distance Metrics

**Definition 4.2 (Metric)**: A function $d: X \times X \rightarrow \mathbb{R}$ is a metric if for all $x, y, z$:
1. $d(x, y) \geq 0$ (non-negativity)
2. $d(x, y) = 0 \Leftrightarrow x = y$ (identity)
3. $d(x, y) = d(y, x)$ (symmetry)
4. $d(x, z) \leq d(x, y) + d(y, z)$ (triangle inequality)

All four metrics above satisfy these properties.

## 4.3 Chamfer Distance

The Euclidean distance transform is computationally expensive. Chamfer distances approximate Euclidean with integer weights.

**Definition 4.3 (Chamfer Distance)**: Using a mask:
```
[0  a  b]
[a  0  a]
[b  a  0]
```

Common masks:
- 3-4 chamfer: $a=3, b=4$
- 5-7-11 chamfer: $a=5, b=7$ (better approximation)

**Algorithm 4.1: Two-Pass Chamfer Distance**

```python
function CHAMFER_DT(binary_image, weights=(3,4)):
    h, w = binary_image.shape
    dist = array filled with infinity
    
    d1, d2 = weights
    
    # Pass 1: Top-left to bottom-right
    for y in range(h):
        for x in range(w):
            if binary_image[y,x] == 1:
                dist[y,x] = 0
            else:
                if y > 0:     dist[y,x] = min(dist[y,x], dist[y-1,x] + d1)
                if x > 0:     dist[y,x] = min(dist[y,x], dist[y,x-1] + d1)
                if y > 0 and x > 0:   dist[y,x] = min(dist[y,x], dist[y-1,x-1] + d2)
                if y > 0 and x < w-1: dist[y,x] = min(dist[y,x], dist[y-1,x+1] + d2)
    
    # Pass 2: Bottom-right to top-left
    for y in range(h-1, -1, -1):
        for x in range(w-1, -1, -1):
            if y < h-1:     dist[y,x] = min(dist[y,x], dist[y+1,x] + d1)
            if x < w-1:     dist[y,x] = min(dist[y,x], dist[y,x+1] + d1)
            if y < h-1 and x < w-1: dist[y,x] = min(dist[y,x], dist[y+1,x+1] + d2)
            if y < h-1 and x > 0:   dist[y,x] = min(dist[y,x], dist[y+1,x-1] + d2)
    
    return dist
```

**Time Complexity**: $O(n)$ where $n$ is the number of pixels.

**Theorem 4.1**: For the 3-4 chamfer mask, the maximum error from Euclidean distance is 8.3%. For 5-7-11, it's 2.0%.

## 4.4 Euclidean Distance Transform

The exact Euclidean distance transform requires computing $\sqrt{x^2 + y^2}$ for each pixel.

**Algorithm 4.2: Euclidean Distance Transform**

```python
function EUCLIDEAN_DT(binary_image):
    h, w = binary_image.shape
    dist = array filled with infinity
    
    # Pass 1: Compute lower bounds
    for y in range(h):
        for x in range(w):
            if binary_image[y,x] == 1:
                dist[y,x] = 0
            else:
                if y > 0: dist[y,x] = min(dist[y,x], dist[y-1,x] + 1)
                if x > 0: dist[y,x] = min(dist[y,x], dist[y,x-1] + 1)
    
    # Pass 2: Refine estimates
    for y in range(h-1, -1, -1):
        for x in range(w-1, -1, -1):
            if y < h-1: dist[y,x] = min(dist[y,x], dist[y+1,x] + 1)
            if x < w-1: dist[y,x] = min(dist[y,x], dist[y,x+1] + 1)
    
    # True Euclidean: compute sqrt (can use approximation for speed)
    for y in range(h):
        for x in range(w):
            # More accurate: search nearby for true minimum
            pass
    
    return dist
```

More sophisticated algorithms (Felzenszwalb & Huttenlocher, 2004) achieve $O(n)$ time using dynamic programming.

## 4.5 Geodesic Distance

When movement is constrained to a region, we use geodesic distance.

**Definition 4.4 (Geodesic Distance)**: The geodesic distance between two points is the length of the shortest path that stays within the allowed region:
$$d_G(p, q) = \min \{ \text{length}(\pi) : \pi \text{ is a path from } p \text{ to } q, \pi \subset R \}$$

**Algorithm 4.3: Geodesic Distance Transform**

```python
function GEODESIC_DT(seeds, mask):
    h, w = mask.shape
    dist = array filled with infinity
    queue = empty priority queue
    
    for each seed in seeds:
        dist[seed] = 0
        queue.push(seed, 0)
    
    while queue is not empty:
        p = queue.pop()
        for each neighbor n of p:
            if mask[n] and dist[p] + 1 < dist[n]:
                dist[n] = dist[p] + 1
                queue.push(n, dist[n])
    
    return dist
```

**Time Complexity**: $O(n \log n)$ where $n$ is the number of pixels.

## 4.6 Voronoi Diagrams

A Voronoi diagram partitions space based on the nearest seed point.

**Definition 4.5 (Voronoi Cell)**: For a set of seeds $S = \{s_1, s_2, \ldots, s_k\}$, the Voronoi cell of seed $s_i$ is:
$$V(s_i) = \{p : d(p, s_i) \leq d(p, s_j) \text{ for all } j \}$$

**Algorithm 4.4: Distance-Based Voronoi**

```python
function VORONOI(seeds, size):
    dist = array of size × size × len(seeds) filled with infinity
    
    for each seed s_i:
        for each pixel p:
            dist[p, i] = euclidean_distance(p, s_i)
    
    voronoi = array of size × size
    for each pixel p:
        voronoi[p] = argmin_i dist[p, i]
    
    return voronoi
```

## 4.7 Applications

### 4.7.1 Skeletonization
The skeleton (medial axis) consists of points equidistant from multiple boundary points.

### 4.7.2 Shape Matching
Hausdorff distance measures shape dissimilarity.

### 4.7.3 Path Planning
Distance fields guide robot navigation.

---

# Chapter 5: Mathematical Morphology

Mathematical morphology provides a powerful framework for analyzing shape and structure through set operations. Originally developed for analyzing geological and biological images, it now applies widely in industrial inspection, document analysis, and medical imaging.

## 5.1 Set-Theoretic Foundations

Let $A$ be a set representing an image (the set of foreground pixels) and $B$ be a structuring element.

**Definition 5.1 (Translation)**: The translation of $A$ by point $x$:
$$A_x = \{a + x : a \in A\}$$

**Definition 5.2 (Reflection)**: The reflection of $B$:
$$\hat{B} = \{-b : b \in B\}$$

## 5.2 Dilation

**Definition 5.3 (Dilation)**: The dilation of $A$ by $B$ is:
$$A \oplus B = \{z : (\hat{B})_z \cap A \neq \emptyset\}$$

Equivalently:
$$A \oplus B = \bigcup_{b \in B} A_b$$

**Intuition**: Dilation grows the object by "adding" pixels at boundaries.

**Algorithm 5.1: Binary Dilation**

```python
function DILATE(image, se):
    result = zeros_like(image)
    se_points = get_se_points(se)  # Get (dx, dy) for SE
    
    for each foreground pixel p in image:
        for each (dx, dy) in se_points:
            q = (p.x + dx, p.y + dy)
            if q is within image bounds:
                result[q] = 1
    
    return result
```

**Properties**:
- $A \oplus \emptyset = \emptyset$
- $A \oplus \{0\} = A$
- $A \subseteq B \Rightarrow A \oplus C \subseteq B \oplus C$
- Commutative: $A \oplus B = B \oplus A$

## 5.3 Erosion

**Definition 5.4 (Erosion)**: The erosion of $A$ by $B$ is:
$$A \ominus B = \{z : B_z \subseteq A\}$$

**Intuition**: Erosion shrinks the object by "removing" boundary pixels.

**Algorithm 5.2: Binary Erosion**

```python
function ERODE(image, se):
    result = zeros_like(image)
    se_points = get_se_points(se)
    se_origin = get_se_origin(se)
    
    for each pixel p in image:
        fits = True
        for each (dx, dy) in se_points:
            q = (p.x + dx - se_origin.x, p.y + dy - se_origin.y)
            if q is outside image or image[q] == 0:
                fits = False
                break
        if fits:
            result[p] = 1
    
    return result
```

**Duality**: Erosion and dilation are duals:
$$(A \ominus B)^c = A^c \oplus \hat{B}$$
$$(A \oplus B)^c = A^c \ominus \hat{B}$$

## 5.4 Opening and Closing

**Definition 5.5 (Opening)**: The opening of $A$ by $B$:
$$A \circ B = (A \ominus B) \oplus B$$

**Definition 5.6 (Closing)**: The closing of $A$ by $B$:
$$A \bullet B = (A \oplus B) \ominus B$$

**Properties**:
- Opening removes small objects and smooths boundaries
- Closing fills small holes and smooths boundaries
- Both are idempotent: $(A \circ B) \circ B = A \circ B$

## 5.5 Morphological Gradient

**Definition 5.7 (Morphological Gradient)**:
$$\nabla A = (A \oplus B) - (A \ominus B)$$

The gradient highlights boundaries.

## 5.6 Hit-or-Miss Transform

**Definition 5.8 (Hit-or-Miss)**: Finds pixels where the structuring element:
- Matches foreground ($B_1$) exactly
- Matches background ($B_2$) exactly
- $A \otimes B = (A \ominus B_1) \cap (A^c \ominus B_2)$

Used for template matching and shape detection.

## 5.7 Grayscale Morphology

For grayscale images, we use sup (for dilation) and inf (for erosion):

**Definition 5.9 (Grayscale Dilation)**:
$$(f \oplus b)(x, y) = \max_{(i,j) \in b} f(x-i, y-j)$$

**Definition 5.10 (Grayscale Erosion)**:
$$(f \ominus b)(x, y) = \min_{(i,j) \in b} f(x+i, y+j)$$

## 5.8 Structuring Elements

Common structuring elements:

```python
# 3×3 square
SE_SQUARE = [[1,1,1], [1,1,1], [1,1,1]]

# Cross
SE_CROSS = [[0,1,0], [1,1,1], [0,1,0]]

# Diamond
SE_DIAMOND = [[0,1,0], [1,1,1], [0,1,0]]

# 5×5 disk (approximation)
SE_DISK_5 = [
    [0,0,1,0,0],
    [0,1,1,1,0],
    [1,1,1,1,1],
    [0,1,1,1,0],
    [0,0,1,0,0]
]
```

## 5.9 Morphological Algorithms

### 5.9.1 Boundary Extraction
$$\partial A = A - (A \ominus B)$$

### 5.9.2 Region Filling
```python
function FILL(image, seed):
    filled = image.copy()
    queue = [seed]
    
    while queue:
        p = queue.pop()
        if filled[p] == 0:
            filled[p] = 1
            for n in neighbors_4(p):
                if in_bounds(n):
                    queue.append(n)
    
    return filled
```

### 5.9.3 Skeletonization
```python
function SKELETON(image):
    skeleton = zeros_like(image)
    temp = image.copy()
    
    while np.any(temp):
        eroded = ERODE(temp, SE_SQUARE_3X3)
        opened = DILATE(eroded, SE_SQUARE_3X3)
        boundary = temp - opened
        skeleton = skeleton OR boundary
        temp = eroded
    
    return skeleton
```

---

# Chapter 6: Edge Detection

Edges—regions where image intensity changes rapidly—are fundamental to visual perception. This chapter presents classical edge detection algorithms and their theoretical foundations.

## 6.1 The Edge Model

**Definition 6.1 (Step Edge)**: An ideal step edge has constant intensity on each side with an abrupt change.

**Definition 6.2 (Ramp Edge)**: A ramp edge transitions gradually over several pixels.

**Definition 6.3 (Roof Edge)**: A roof edge has a triangular profile, like the ridge of a roof.

**Noise Considerations**: Real edges are corrupted by noise. The signal-to-noise ratio determines detectability.

## 6.2 Gradient-Based Edge Detection

The gradient points in the direction of maximum intensity change.

**Definition 6.4 (Image Gradient)**:
$$\nabla I = \left[ \frac{\partial I}{\partial x}, \frac{\partial I}{\partial y} \right]$$

**Magnitude**:
$$|\nabla I| = \sqrt{I_x^2 + I_y^2}$$

**Direction**:
$$\theta = \arctan\left(\frac{I_y}{I_x}\right)$$

## 6.3 Gradient Operators

### Sobel Operator
$$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix} \quad G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

### Prewitt Operator
$$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix} \quad G_y = \begin{bmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix}$$

### Roberts Cross
$$G_x = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \quad G_y = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$$

**Algorithm 6.1: Gradient Edge Detection**

```python
function GRADIENT_EDGE(image, kernel_x, kernel_y):
    # Apply convolution
    gx = convolve(image, kernel_x)
    gy = convolve(image, kernel_y)
    
    # Compute magnitude
    magnitude = sqrt(gx^2 + gy^2)
    
    # Compute direction
    direction = arctan2(gy, gx)
    
    return magnitude, direction
```

## 6.4 Laplacian Operator

The Laplacian is the second derivative:

**Definition 6.5 (Laplacian)**:
$$\nabla^2 I = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}$$

**Laplacian kernels**:
$$L_4 = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix} \quad L_8 = \begin{bmatrix} 1 & 1 & 1 \\ 1 & -8 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

**Properties**:
- Zero-crossings indicate edges
- More sensitive to noise than first derivatives
- Detects edges regardless of orientation

## 6.5 The Canny Edge Detector

John Canny's 1986 algorithm remains the most widely used edge detector. It optimizes three criteria: good detection, good localization, and single response.

**Algorithm 6.2: Canny Edge Detector**

```python
function CANNY(image, low_threshold, high_threshold):
    # Step 1: Gaussian smoothing
    smoothed = gaussian(image, sigma=1.4)
    
    # Step 2: Compute gradients
    magnitude, direction = compute_gradient_sobel(smoothed)
    
    # Step 3: Non-maximum suppression
    thinned = non_maximum_suppression(magnitude, direction)
    
    # Step 4: Double thresholding
    strong, weak = double_threshold(thinned, low_threshold, high_threshold)
    
    # Step 5: Hysteresis thresholding
    edges = hysteresis(strong, weak)
    
    return edges


function NON_MAX_SUPPRESSION(magnitude, direction):
    result = zeros_like(magnitude)
    
    for each pixel p:
        angle = direction[p]
        
        # Determine neighbors along gradient direction
        neighbors = get_neighbors_along_angle(angle)
        
        if magnitude[p] >= magnitude[neighbors[0]] and \
           magnitude[p] >= magnitude[neighbors[1]]:
            result[p] = magnitude[p]
        else:
            result[p] = 0
    
    return result
```

**Step Details**:

1. **Gaussian Smoothing**: Reduces noise. Standard deviation $\sigma = 1.4$ balances noise reduction with edge preservation.

2. **Non-Maximum Suppression**: Thins edges by keeping only local maxima in the gradient direction.

3. **Double Threshold**: 
   - High threshold: Strong edges (keep)
   - Low threshold: Weak edges (potential)
   
4. **Hysteresis**: Connect weak edges to strong edges; discard isolated weak pixels.

**Theorem 6.1**: Canny's detector is optimal for step edges in the sense of maximizing the product of detection probability and localization.

## 6.6 Edge Linking

After initial detection, edges often need linking:

### 6.6.1 Local Linking
Connect edges within a neighborhood if direction and magnitude are consistent.

### 6.6.2 Hough Transform
Detect parametric curves (lines, circles, ellipses) through voting in parameter space.

```python
function HOUGH_LINES(edge_image, threshold):
    accumulator = zeros((rho_range, theta_range))
    
    for each edge pixel (x, y):
        for theta in theta_range:
            rho = x * cos(theta) + y * sin(theta)
            accumulator[rho, theta] += 1
    
    # Find peaks above threshold
    peaks = find_local_maxima(accumulator, threshold)
    
    return peaks
```

---

# Chapter 7: Image Registration and Transformations

Image registration—the alignment of two or more images—is fundamental to medical imaging, remote sensing, and computer vision. This chapter covers geometric transformations and the Iterative Closest Point algorithm.

## 7.1 Geometric Transformations

**Definition 7.1 (Affine Transformation)**: An affine transformation preserves parallel lines:
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} t_x \\ t_y \end{bmatrix}$$

Properties:
- Translation (shifting)
- Rotation
- Scaling
- Shearing
- Any combination of above

**Definition 7.2 (Homogeneous Coordinates)**: Using homogeneous coordinates:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} a & b & t_x \\ c & d & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

## 7.2 Image Resampling

When we transform an image, we need to sample at new pixel locations.

**Algorithm 7.1: Forward Mapping**

```python
function FORWARD_TRANSFORM(image, T):
    output = zeros_like(image)
    
    for y in range(height):
        for x in range(width):
            new_coords = T(x, y)
            if in_bounds(new_coords):
                output[new_coords] = image[y, x]
    
    return output
```

Problem: Output may have holes!

**Algorithm 7.2: Inverse Mapping**

```python
function INVERSE_TRANSFORM(image, T):
    output = zeros_like(image)
    T_inv = inverse(T)
    
    for y in range(output_height):
        for x in range(output_width):
            orig_coords = T_inv(x, y)
            if in_bounds(orig_coords):
                output[y, x] = interpolate(image, orig_coords)
    
    return output
```

### Interpolation Methods

**Nearest Neighbor**: Use the closest integer coordinate.

**Bilinear**:
```python
def bilinear_interp(image, x, y):
    x0, y0 = floor(x), floor(y)
    x1, y1 = x0 + 1, y0 + 1
    
    fx, fy = x - x0, y - y0
    
    return (1-fx)*(1-fy)*image[y0,x0] + \
           fx*(1-fy)*image[y0,x1] + \
           (1-fx)*fy*image[y1,x0] + \
           fx*fy*image[y1,x1]
```

**Bicubic**: Uses 16 neighboring pixels with cubic polynomials.

## 7.3 Iterative Closest Point (ICP)

ICP aligns point sets by iteratively finding correspondences and computing transformations.

**Algorithm 7.3: ICP**

```python
function ICP(source, target, max_iterations=20):
    transformed = source.copy()
    
    for iteration in range(max_iterations):
        # Step 1: Find closest points
        correspondences = []
        for p in transformed:
            closest = find_closest(p, target)
            correspondences.append(closest)
        
        # Step 2: Compute transformation
        T = compute_rigid_transform(transformed, correspondences)
        
        # Step 3: Apply transformation
        transformed = apply_transform(transformed, T)
        
        # Step 4: Check convergence
        if change_in_transformation < threshold:
            break
    
    return transformed
```

**Computing Rigid Transformation**:
1. Compute centroids
2. Center point clouds
3. Compute cross-covariance matrix
4. Use SVD to find rotation
5. Extract translation

**Time Complexity**: $O(k \cdot n \cdot m)$ where $k$ is iterations, $n$ and $m$ are point set sizes.

## 7.4 Registration Metrics

**Definition 7.3 (Sum of Squared Differences)**:
$$SSD = \sum_{i} \|p_i - q_i\|^2$$

**Definition 7.4 (Hausdorff Distance)**:
$$d_H(A, B) = \max\left(\max_{a \in A} \min_{b \in B} \|a-b\|, \max_{b \in B} \min_{a \in A} \|a-b\|\right)$$

**Definition 7.5 (Mutual Information)** (for multi-modal):
$$MI(A, B) = \sum_{a,b} p(a,b) \log \frac{p(a,b)}{p(a)p(b)}$$

---

# Part III: Analysis

# Chapter 8: Feature Detection

Features are distinctive image elements that can be reliably detected and matched. Corners, blobs, and ridges are fundamental to tracking, matching, and 3D reconstruction.

## 8.1 Corners and Interest Points

**Definition 8.1 (Corner)**: A corner is an image point where intensity changes in multiple directions.

**Why Corners?**:
- Rich in information
- Stable under viewpoint changes
- Easy to detect reliably
- Good for matching

## 8.2 Harris Corner Detector

The Harris detector uses the structure tensor to detect corners.

**Algorithm 8.1: Harris Corner Detector**

```python
function HARRIS(image, k=0.04, threshold=0.01):
    # Step 1: Compute gradients
    Ix = sobel_x(image)
    Iy = sobel_y(image)
    
    # Step 2: Compute structure tensor components
    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy
    
    # Step 3: Gaussian smoothing
    Ixx = gaussian(Ixx, sigma=1)
    Iyy = gaussian(Iyy, sigma=1)
    Ixy = gaussian(Ixy, sigma=1)
    
    # Step 4: Compute corner response
    corners = zeros_like(image)
    for each pixel:
        M = [[Ixx[p], Ixy[p]], [Ixy[p], Iyy[p]]]
        det = Ixx[p] * Iyy[p] - Ixy[p]^2
        trace = Ixx[p] + Iyy[p]
        response = det - k * trace^2
        
        if response > threshold:
            corners[p] = response
    
    # Step 5: Non-maximum suppression
    corners = nms(corners, window=3)
    
    return corners
```

**Mathematical Foundation**:

For a window $W$, compute the second moment matrix:
$$M = \begin{bmatrix} \sum I_x^2 & \sum I_x I_y \\ \sum I_x I_y & \sum I_y^2 \end{bmatrix}$$

**Corner Response**:
$$R = \det(M) - k \cdot \text{tr}(M)^2 = \lambda_1 \lambda_2 - k(\lambda_1 + \lambda_2)^2$$

where $\lambda_1, \lambda_2$ are eigenvalues of $M$.

- $R > 0$: Corner (both eigenvalues large)
- $R \approx 0$: Flat (both eigenvalues small)
- $R < 0$: Edge (one eigenvalue large, one small)

**Theorem 8.1**: For a step edge, the Harris detector response is proportional to the edge strength squared.

## 8.3 Shi-Tomasi Corner Detector

A simpler variant that directly checks eigenvalues:

**Algorithm 8.2: Shi-Tomasi**

```python
function SHI_TOMASI(image, quality=0.01):
    # Compute gradients and structure tensor (same as Harris)
    ...
    
    # Compute minimum eigenvalue
    for each pixel:
        lambda_min = (trace - sqrt(trace^2 - 4*det)) / 2
        
        if lambda_min > quality:
            corners[p] = lambda_min
    
    # Non-maximum suppression
    corners = nms(corners)
    
    return corners
```

## 8.4 FAST (Features from Accelerated Segment Test)

Extremely fast corner detection based on intensity comparison.

**Algorithm 8.3: FAST**

```python
function FAST(image, threshold=20):
    corners = []
    
    for each pixel p:
        Ip = image[p]
        
        # Check 4 neighbors at distance 3
        if not all(abs(image[p + offset] - Ip) > threshold for offset in [(-3,0), (3,0), (0,-3), (0,3)]):
            continue
        
        # Check 8 outer neighbors
        count = sum(1 for offset in outer_ring if abs(image[p + offset] - Ip) > threshold)
        
        if count >= 12:
            corners.append(p)
    
    return corners
```

**Time Complexity**: $O(n)$ where $n$ is the number of pixels—extremely fast in practice.

## 8.5 Scale Selection

Features need to be detected at appropriate scales.

**Definition 8.2 (Scale Space)**: The scale space of an image is:
$$L(x, y, \sigma) = G(x, y, \sigma) * I(x, y)$$

where $G$ is a Gaussian kernel with standard deviation $\sigma$.

**Definition 8.3 (Blob Detection)**: Use the Laplacian of Gaussian:
$$LoG(x, y, \sigma) = \sigma^2 \left( \frac{\partial^2 L}{\partial x^2} + \frac{\partial^2 L}{\partial y^2} \right)$$

Local maxima of $|LoG|$ indicate blobs at scale $\sigma$.

---

# Chapter 9: Contour Processing

Contours (boundaries) encode the shape of objects. This chapter covers contour extraction, representation, and analysis.

## 9.1 Contour Tracing

**Algorithm 9.1: Moore Neighbor Tracing**

```python
function MOORE_BOUNDARY(start, image):
    contour = [start]
    current = start
    neighbor_idx = 0  # Start searching from first neighbor
    
    while True:
        # Search neighbors in clockwise order starting from neighbor_idx
        found = False
        for i in range(8):
            idx = (neighbor_idx + i) % 8
            neighbor = current.neighbor[idx]
            
            if is_boundary(neighbor, image):
                contour.append(neighbor)
                current = neighbor
                neighbor_idx = (idx + 5) % 8  # Next search starts here
                found = True
                break
        
        if not found or current == start:
            break
    
    return contour
```

## 9.2 Chain Codes

A chain code represents a contour as a sequence of directions.

**Definition 9.1 (Freeman Chain Code)**: Direction encoding:
- 0: East (1, 0)
- 1: Northeast (1, -1)
- 2: North (0, -1)
- 3: Northwest (-1, -1)
- 4: West (-1, 0)
- 5: Southwest (-1, 1)
- 6: South (0, 1)
- 7: Southeast (1, 1)

**Algorithm 9.2: Chain Code Extraction**

```python
function EXTRACT_CHAIN_CODE(contour):
    code = []
    
    for i in range(len(contour)):
        dx = contour[(i+1)%len][0] - contour[i][0]
        dy = contour[(i+1)%len][1] - contour[i][1]
        
        direction = find_direction(dx, dy)
        code.append(direction)
    
    return code
```

**Normalization**: Rotation normalization uses "first difference":
$$d_i = (c_i - c_{i-1}) \mod 8$$

Translation is inherently invariant; scale requires normalization.

## 9.3 Polygon Approximation

**Algorithm 9.3: Douglas-Peucker**

```python
function DOUGLAS_PEUCKER(points, epsilon):
    if len(points) < 3:
        return points
    
    # Find point with maximum distance
    max_dist = 0
    max_idx = 0
    for i in range(1, len(points)-1):
        d = perpendicular_distance(points[i], points[0], points[-1])
        if d > max_dist:
            max_dist = d
            max_idx = i
    
    if max_dist > epsilon:
        left = DOUGLAS_PEUCKER(points[:max_idx+1], epsilon)
        right = DOUGLAS_PEUCKER(points[max_idx:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]
```

**Time Complexity**: $O(n)$ average, $O(n^2)$ worst case.

## 9.4 Shape Signatures

**Definition 9.2 (Centroid Distance Signature)**:
$$r(\theta) = \sqrt{(x(\theta) - c_x)^2 + (y(\theta) - c_y)^2}$$

**Definition 9.3 (Curvature Signature)**:
$$k(\theta) = \frac{d\theta}{ds}$$

where $s$ is arc length.

---

# Chapter 10: Curve Analysis

Curves—1D digital objects—require specialized analysis. This chapter covers curvature, smoothing, and digital straightness.

## 10.1 Curve Representations

A digital curve can be represented as:
1. A sequence of pixel coordinates
2. Chain code
3. Parametric function $P(t) = (x(t), y(t))$

## 10.2 Curvature

**Definition 10.1 (Curvature)**: For a parametric curve:
$$\kappa = \frac{x' y'' - y' x''}{(x'^2 + y'^2)^{3/2}}$$

**Discrete Curvature**:
```python
function DISCRETE_CURVATURE(p1, p2, p3):
    # Three consecutive points
    v1 = (p1.x - p2.x, p1.y - p2.y)
    v2 = (p3.x - p2.x, p3.y - p2.y)
    
    # Angle at p2
    angle = acos(dot(v1, v2) / (norm(v1) * norm(v2)))
    
    return 2 * sin(angle/2) / norm(v2)
```

## 10.3 Curve Smoothing

**Gaussian Smoothing**:
```python
function SMOOTH_CURVE(curve, sigma):
    x_coords = [p.x for p in curve]
    y_coords = [p.y for p in curve]
    
    x_smooth = gaussian_convolution(x_coords, sigma)
    y_smooth = gaussian_convolution(y_coords, sigma)
    
    return [(x_smooth[i], y_smooth[i]) for i in range(len(curve))]
```

**Moving Average**:
```python
function MOVING_AVERAGE(curve, window):
    smoothed = []
    for i in range(len(curve)):
        start = max(0, i - window//2)
        end = min(len(curve), i + window//2 + 1)
        
        avg_x = sum(p.x for p in curve[start:end]) / (end - start)
        avg_y = sum(p.y for p in curve[start:end]) / (end - start)
        smoothed.append((avg_x, avg_y))
    
    return smoothed
```

## 10.4 Digital Straight Lines

**Definition 10.2 (Digital Straight Line)**: A set of pixels $S$ is a digital straight line (DSL) if there exists a real straight line $L$ such that $S$ is the grid-intersection digitization of $L$.

**Theorem 10.1 (Arithmetic Sequence Characterization)**: A set of pixels is a DSL if and only if the y-coordinates of its pixels form an arithmetic progression when sorted by x-coordinate.

**Algorithm 10.1: DSL Recognition**

```python
function IS_DSL(points):
    if len(points) < 3:
        return True
    
    # Sort by x-coordinate
    sorted_pts = sorted(points, key=lambda p: p[0])
    
    # Check if y-values form arithmetic progression
    dx1 = sorted_pts[1][0] - sorted_pts[0][0]
    dy1 = sorted_pts[1][1] - sorted_pts[0][1]
    
    for i in range(2, len(sorted_pts)):
        dx = sorted_pts[i][0] - sorted_pts[i-1][0]
        dy = sorted_pts[i][1] - sorted_pts[i-1][1]
        
        if dx * dy1 != dy * dx1:
            return False
    
    return True
```

## 10.5 Convex Hull

**Algorithm 10.4: Graham Scan**

```python
function GRAHAM_SCAN(points):
    # Find point with minimum y (and x for ties)
    base = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort by polar angle from base
    sorted_pts = sorted(points, 
                       key=lambda p: atan2(p[1]-base[1], p[0]-base[0]))
    
    # Build hull
    hull = []
    for p in sorted_pts:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    
    return hull
```

**Time Complexity**: $O(n \log n)$ due to sorting.

---

# Chapter 11: Shape Analysis

Quantitative shape analysis enables comparison, classification, and retrieval. This chapter presents geometric measures and descriptors.

## 11.1 Basic Geometric Properties

### Area
**Theorem 11.1 (Shoelace Formula)**: For polygon with vertices $(x_i, y_i)$:
$$A = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$$

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
$$C_x = \frac{1}{6A} \sum (x_i + x_{i+1})(x_i y_{i+1} - x_{i+1} y_i)$$
$$C_y = \frac{1}{6A} \sum (y_i + y_{i+1})(x_i y_{i+1} - x_{i+1} y_i)$$

### Perimeter
$$P = \sum \sqrt{(x_{i+1} - x_i)^2 + (y_{i+1} - y_i)^2}$$

## 11.2 Shape Descriptors

### Circularity
$$C = \frac{4\pi A}{P^2}$$

- Circle: $C = 1$
- Square: $C = \frac{\pi}{4} \approx 0.785$
- Triangle: $C \approx 0.6$

### Solidity
$$S = \frac{A}{A_{convex}}$$

### Aspect Ratio
$$AR = \frac{width}{height}$$

### Eccentricity
$$E = \frac{a - b}{a}$$

where $a$ and $b$ are major and minor axes.

### Compactness
$$K = \frac{P^2}{A}$$

## 11.3 Shape Moments

**Definition 11.1 (Raw Moment)**:
$$M_{pq} = \sum_x \sum_y x^p y^q I(x, y)$$

**Definition 11.2 (Central Moment)**:
$$\mu_{pq} = \sum_x \sum_y (x - \bar{x})^p (y - \bar{y})^q I(x, y)$$

where $\bar{x} = M_{10}/M_{00}$, $\bar{y} = M_{01}/M_{00}$

**Definition 11.3 (Normalized Central Moment)**:
$$\eta_{pq} = \frac{\mu_{pq}}{M_{00}^{(p+q)/2 + 1}}$$

## 11.4 Hu Moments

**Theorem 11.2**: The seven Hu moments are invariant under translation, rotation, and scaling.

```python
def hu_moments(moments):
    # Compute from central moments
    # Log transform for numerical stability
    hu = []
    for i in range(7):
        hu.append(-sign(moments[i]) * log10(abs(moments[i]) + 1e-10))
    return hu
```

**The seven Hu moments**:
- $\eta_{20} + \eta_{02}$
- $(\eta_{20} - \eta_{02})^2 + 4\eta_{11}^2$
- $(\eta_{30} - 3\eta_{12})^2 + (3\eta_{21} - \eta_{03})^2$
- $(\eta_{30} + \eta_{12})^2 + (\eta_{21} + \eta_{03})^2$
- $(3\eta_{30} - \eta_{12})(\eta_{30} + \eta_{12})((\eta_{30} + \eta_{12})^2 - 3(\eta_{21} + \eta_{03})^2) + (3\eta_{21} - \eta_{03})(\eta_{21} + \eta_{03})(3(\eta_{30} + \eta_{12})^2 - (\eta_{21} + \eta_{03})^2)$
- $(\eta_{20} - \eta_{02})((\eta_{30} + \eta_{12})^2 - (\eta_{21} + \eta_{03})^2) + 4\eta_{11}(\eta_{30} + \eta_{12})(\eta_{21} + \eta_{03})$
- $(3\eta_{21} - \eta_{03})(\eta_{30} + \eta_{12})((\eta_{30} + \eta_{12})^2 - 3(\eta_{21} + \eta_{03})^2) - (3\eta_{30} - \eta_{12})(\eta_{21} + \eta_{03})(3(\eta_{30} + \eta_{12})^2 - (\eta_{21} + \eta_{03})^2)$

---

# Part IV: Advanced Topics

# Chapter 12: 3D Geometry and Volumetric Processing

Moving to three dimensions, we analyze volumetric data from CT scans, MRI, and other imaging modalities.

## 12.1 Voxel Representations

**Definition 12.1 (Voxel)**: A voxel (volume pixel) is the 3D equivalent of a pixel, representing a value on a regular grid in 3D space.

**Definition 12.2 (Binary Volume)**: A binary volume $V: \mathbb{Z}^3 \rightarrow \{0, 1\}$ where $V(x,y,z) = 1$ indicates occupied space.

## 12.2 3D Connectivity

**Definition 12.3 (6-Connectivity)**: Neighbors in 6 directions (±x, ±y, ±z).

**Definition 12.4 (18-Connectivity)**: 6-connectivity plus 12 face diagonals.

**Definition 12.5 (26-Connectivity)**: All 26 neighbors.

**Theorem 12.1**: For 3D objects, use 26-connectivity for the object and 6-connectivity for background (or vice versa) to avoid paradoxes.

## 12.3 Marching Cubes

The marching cubes algorithm extracts isosurfaces from volumetric data.

**Algorithm 12.1: Marching Cubes**

```python
function MARCHING_CUBES(volume, isolevel):
    vertices = []
    faces = []
    
    for each cube in volume:
        # Determine which corners are above isolevel
        cube_index = 0
        for i in range(8):
            if cube.corner[i].value > isolevel:
                cube_index |= (1 << i)
        
        if cube_index == 0 or cube_index == 255:
            continue  # All inside or all outside
        
        # Get edge table entries
        edge_vertices = get_edge_vertices(cube, cube_index, isolevel)
        
        # Get face table entries  
        face_indices = get_face_indices(cube_index)
        
        # Add vertices and faces
        for edge in edge_vertices:
            vertices.append(interpolate(edge, isolevel))
        
        for face in face_indices:
            faces.append(tuple(face + len(vertices)))
    
    return vertices, faces
```

**Edge Table**: 256 entries (2^8 corner configurations), each specifying which of the 12 edges intersect the isosurface.

**Face Table**: Specifies how to triangulate each configuration.

**Time Complexity**: $O(n)$ where $n$ is the number of voxels.

## 12.4 Distance Transform in 3D

```python
function DT_3D(volume):
    # Three-pass algorithm
    # Pass 1: Face neighbors
    # Pass 2: Edge neighbors  
    # Pass 3: Corner neighbors
    
    dist = zeros_like(volume) + infinity
    
    # Forward pass
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z,y,x]:
                    dist[z,y,x] = 0
                else:
                    # Check neighbors and add 1
                    pass
    
    # Backward pass similar
    
    return dist
```

## 12.5 Skeletonization in 3D

**Algorithm 12.2: 3D Thinning**

```python
function THIN_3D(volume):
    current = volume.copy()
    changed = True
    
    while changed:
        changed = False
        
        # First pass: remove 6-connected border points
        to_remove = []
        for each voxel p in current:
            if is_border(p, current) and not is_endpoint(p, current):
                if remove_preserves_topology(p, current):
                    to_remove.append(p)
        
        for p in to_remove:
            current[p] = 0
            changed = True
        
        # Second pass: similar but different direction
    
    return current
```

**Topological Thinning Condition**: A voxel can be removed if its removal does not change the number of connected components or create new holes.

---

# Chapter 13: Spatial Data Structures

Efficient spatial indexing is crucial for large-scale geometric computation.

## 13.1 Quadtree

A quadtree recursively divides 2D space into four quadrants.

**Algorithm 13.1: Quadtree Insertion**

```python
class QuadtreeNode:
    def __init__(self, bounds, capacity=4):
        self.bounds = bounds  # (x, y, width, height)
        self.capacity = capacity
        self.points = []
        self.children = None
    
    def insert(self, point):
        if not contains(self.bounds, point):
            return False
        
        if len(self.points) < self.capacity and self.children is None:
            self.points.append(point)
            return True
        
        if self.children is None:
            self.subdivide()
        
        return any(child.insert(point) for child in self.children)
    
    def subdivide(self):
        x, y, w, h = self.bounds
        hw, hh = w/2, h/2
        
        self.children = [
            QuadtreeNode((x+hw, y, hw, hh), self.capacity),
            QuadtreeNode((x, y, hw, hh), self.capacity),
            QuadtreeNode((x, y+hh, hw, hh), self.capacity),
            QuadtreeNode((x+hw, y+hh, hw, hh), self.capacity),
        ]
        
        for p in self.points:
            for child in self.children:
                if child.insert(p):
                    break
        
        self.points = []
```

**Time Complexity**:
- Insert: $O(\log n)$ average
- Query: $O(\sqrt{n} + k)$ where $k$ is results

## 13.2 Octree

The octree extends the quadtree to 3D, dividing each node into eight children.

**Time Complexity**: $O(\log n)$ for insert/query.

## 13.3 Voxel Hashing

For very large scenes, hash tables provide better memory efficiency.

```python
class VoxelHash:
    def __init__(self, table_size=2**20):
        self.table = {}
        self.table_size = table_size
    
    def _hash(self, x, y, z):
        p1, p2, p3 = 73856093, 19349663, 83492791
        return (abs(x)*p1 ^ abs(y)*p2 ^ abs(z)*p3) % self.table_size
    
    def insert(self, x, y, z, data):
        h = self._hash(x, y, z)
        self.table[h] = (x, y, z, data)
    
    def query(self, x, y, z):
        h = self._hash(x, y, z)
        return self.table.get(h)
```

## 13.4 Signed Distance Fields

**Definition 13.1 (Signed Distance Field)**: A function $S: \mathbb{R}^3 \rightarrow \mathbb{R}$ where $S(p) > 0$ outside a surface, $S(p) < 0$ inside, and $|S(p)|$ equals the distance to the surface.

**Algorithm 13.2: Jump Flooding Algorithm**

```python
function JFA(seeds):
    # Initialize with seed positions
    # For k = 1, 2, 4, 8, ...:
    #   Each pixel checks 8 neighbors at distance k
    #   Update if closer seed found
    
    pass
```

---

# Chapter 14: Segmentation

Segmentation partitions an image into meaningful regions.

## 14.1 Thresholding

**Global Thresholding**: Find single threshold $T$ such that:
$$I(x,y) > T \rightarrow \text{foreground}$$

**Otsu's Method**: Maximize between-class variance:
$$\sigma^2_B = w_0(\mu_0 - \mu_T)^2 + w_1(\mu_1 - \mu_T)^2$$

**Algorithm 14.1: Otsu's Threshold**

```python
def OTSU(image):
    # Compute histogram
    hist = compute_histogram(image)
    
    # Try all thresholds
    best_threshold = 0
    best_variance = 0
    
    for t in range(256):
        w0 = sum(hist[:t])
        w1 = sum(hist[t:])
        
        if w0 == 0 or w1 == 0:
            continue
        
        mu0 = sum(i * hist[i] for i in range(t)) / w0
        mu1 = sum(i * hist[i] for i in range(t, 256)) / w1
        
        variance = w0 * w1 * (mu0 - mu1)^2
        
        if variance > best_variance:
            best_variance = variance
            best_threshold = t
    
    return best_threshold
```

## 14.2 Region Growing

**Algorithm 14.2: Region Growing**

```python
def REGION_GROW(image, seeds, threshold):
    regions = {}
    for seed in seeds:
        regions[seed] = [seed]
    
    for seed in seeds:
        queue = [seed]
        visited = set()
        
        while queue:
            p = queue.pop()
            if p in visited:
                continue
            visited.add(p)
            
            for neighbor in neighbors_4(p):
                if neighbor not in visited and \
                   abs(image[neighbor] - image[seed]) < threshold:
                    regions[seed].append(neighbor)
                    queue.append(neighbor)
    
    return regions
```

## 14.3 Graph Cuts

**Algorithm 14.3: Min-Cut Max-Flow**

```python
def MIN_CUT(image, seeds, lambda_param):
    # Build graph
    # Nodes: pixels + source + sink
    # Edges: n-links (neighbor to neighbor) and t-links (pixel to source/sink)
    
    # Find max flow
    flow = FORD_FULKERSON(graph)
    
    # Cut separates source set from sink set
    return segmentation
```

## 14.4 Watershed

**Algorithm 14.4: Watershed**

```python
def WATERSHED(gradient):
    # Initialize with markers
    # Priority queue with distances
    # Flood from markers
    
    pass
```

---

# Chapter 15: Shape Descriptors and Recognition

This chapter presents advanced techniques for describing and recognizing shapes.

## 15.1 Fourier Descriptors

**Algorithm 15.1: Fourier Descriptor**

```python
def FOURIER_DESCRIPTOR(contour, num_coeffs=10):
    # Convert to complex coordinates
    complex_pts = [c[0] + 1j*c[1] for c in contour]
    
    # Compute FFT
    fft = np.fft.fft(complex_pts)
    
    # Take first num_coeffs (low frequency)
    return fft[:num_coeffs]
```

**Properties**:
- Translation: First coefficient represents centroid
- Scale: Normalize by first coefficient
- Rotation: Phase changes, magnitude stays

## 15.2 Zernike Moments

Zernike polynomials form an orthogonal basis on the unit circle.

**Algorithm 15.2: Zernike Moments**

```python
def ZERNIKE_MOMENTS(image, order):
    # Compute polynomial values for each pixel
    # Sum weighted pixel values
    # Return complex moments
    pass
```

**Advantages**:
- Rotation invariant
- Can reconstruct image from moments
- More discriminative than Hu moments

## 15.3 Shape Context

**Algorithm 15.3: Shape Context**

```python
def SHAPE_CONTEXT(point, all_points, bins=(5, 12)):
    # For each other point, compute relative position
    # Bin into polar histogram
    # Return histogram
    
    pass
```

## 15.4 Template Matching

**Normalized Cross-Correlation**:
$$NCC = \frac{\sum (I - \bar{I})(T - \bar{T})}{\sqrt{\sum (I - \bar{I})^2 \sum (T - \bar{T})^2}}$$

---

# Part V: Modern Methods

# Chapter 16: Topological Data Analysis

Topological Data Analysis (TDA) provides tools for understanding the shape of data at multiple scales.

## 16.1 Persistent Homology

**Definition 16.1 (Filtration)**: A filtration is a sequence of nested spaces:
$$K_0 \subseteq K_1 \subseteq K_2 \subseteq \cdots$$

**Definition 16.2 (Persistence)**: A homology class "born" at filtration value $b$ and "die" at $d$ has persistence $d - b$.

**Algorithm 16.1: Persistent Homology**

```python
def PERSISTENT_HOMOLOGY(distance_matrix):
    # Build Vietoris-Rips complex
    # Compute persistence using union-find
    
    pass
```

## 16.2 Persistence Diagrams

**Definition 16.3 (Persistence Diagram)**: A multiset of points $(b, d)$ representing birth-death pairs.

## 16.3 Applications

- Shape clustering
- Feature selection
- Data simplification

---

# Chapter 17: Neural Implicit Representations

Modern machine learning approaches represent geometry through neural networks.

## 17.1 Signed Distance Functions

**Definition 17.1 (Neural SDF)**: A function $f_\theta(x, y, z) \rightarrow \mathbb{R}$ learned by a neural network to approximate signed distance.

**Architecture**: Typically uses positional encoding + MLP:
- Input: 3D coordinates
- Positional encoding: $\sin, \cos$ at multiple frequencies
- MLP: Several hidden layers (e.g., 4 layers of 256 units)
- Output: Single scalar (distance)

## 17.2 Feature Volumes

```python
class FeatureVolume:
    def __init__(self, resolution, feature_dim):
        self.resolution = resolution
        self.feature_dim = feature_dim
        self.features = zeros(resolution, resolution, resolution, feature_dim)
    
    def query(self, x, y, z):
        # Trilinear interpolation
        return interpolate_3d(self.features, x, y, z)
```

## 17.3 Multi-Resolution Hash Encoding

```python
class MultiResolutionHash:
    def __init__(self, num_levels=16):
        self.levels = []
        for i in range(num_levels):
            resolution = 2**i * 16
            self.levels.append(HashTable(resolution))
    
    def get_feature(self, x, y, z):
        feature = zeros(self.feature_dim)
        for level in self.levels:
            feature += level.query(x, y, z)
        return feature
```

---

# Appendix A: Exercise Sets

## Chapter 2 Exercises

**Exercise 2.1**: Prove that 4-connected components can be found using union-find in $O(n)$ time.

**Exercise 2.2**: Write a program to compute the Euler characteristic of a binary image and verify it on several test images.

**Exercise 2.3**: Explain the connectivity paradox and how mixed connectivity resolves it.

**Exercise 2.4**: Show that the Jordan curve theorem fails for certain connectivity choices.

## Chapter 4 Exercises

**Exercise 4.1**: Implement the Euclidean distance transform and compare its output with the chamfer distance transform.

**Exercise 4.2**: Prove that the 3-4 chamfer distance satisfies the triangle inequality.

**Exercise 4.3**: Modify the geodesic distance transform to work with weighted costs.

**Exercise 4.4**: Use the distance transform to find the skeleton of a shape and compare with morphological skeletonization.

## Chapter 5 Exercises

**Exercise 5.1**: Prove the duality between erosion and dilation.

**Exercise 5.2**: Implement grayscale morphological operations.

**Exercise 5.3**: Show that morphological opening satisfies $A \circ B \subseteq A$.

**Exercise 5.4**: Design a structuring element to detect corners.

## Chapter 6 Exercises

**Exercise 6.1**: Derive the response of the Sobel operator to a step edge.

**Exercise 6.2**: Show that the Laplacian is more sensitive to noise than the gradient.

**Exercise 6.3**: Modify Canny's detector for sub-pixel edge localization.

**Exercise 6.4**: Compare edge detection results using different gradient operators.

## Chapter 8 Exercises

**Exercise 8.1**: Prove that Harris corner response is invariant to additive intensity changes.

**Exercise 8.2**: Implement the Shi-Tomasi corner detector and compare with Harris.

**Exercise 8.3**: Modify FAST for scale invariance.

**Exercise 8.4**: Design a feature detector for specific shapes (circles, lines).

## Chapter 11 Exercises

**Exercise 11.1**: Prove that Hu moments are scale invariant.

**Exercise 11.2**: Use shape moments to classify simple shapes.

**Exercise 11.3**: Compare shape matching using different descriptors.

**Exercise 11.4**: Implement a simple shape retrieval system.

## Chapter 12 Exercises

**Exercise 12.1**: Implement marching cubes and test on various volumetric data.

**Exercise 12.2**: Compare 3D skeletonization with 2D skeletonization.

**Exercise 12.3**: Implement a distance transform in 3D.

**Exercise 12.4**: Design an algorithm to extract the medial axis of a 3D object.

---

# Appendix B: Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Connected Components | $O(n)$ | $O(n)$ |
| Distance Transform (Chamfer) | $O(n)$ | $O(n)$ |
| Euclidean DT (Felzenszwalb) | $O(n)$ | $O(n)$ |
| Morphological Operations | $O(n \cdot m)$ | $O(n)$ |
| Canny Edge Detection | $O(n)$ | $O(n)$ |
| Harris Corner | $O(n)$ | $O(n)$ |
| Marching Cubes | $O(n)$ | $O(n)$ |
| Quadtree Insert | $O(\log n)$ | $O(n)$ |
| ICP | $O(k \cdot n \cdot m)$ | $O(n + m)$ |

---

# Appendix C: References

1. Rosenfeld, A., & Pfaltz, J. L. (1966). Sequential operations in digital picture processing. Journal of the ACM, 13(4), 471-494.

2. Serra, J. (1982). Image Analysis and Mathematical Morphology. Academic Press.

3. Canny, J. (1986). A computational approach to edge detection. IEEE TPAMI, 8(6), 679-698.

4. Harris, C., & Stephens, M. (1988). A combined corner and edge detector. Alvey Vision Conference, 147-151.

5. Bresenham, J. E. (1965). Algorithm for computer control of a digital plotter. IBM Systems Journal, 4(1), 25-30.

6. Rosenfeld, A. (1979). Digital picture analysis. Springer.

7. Soille, P. (2003). Morphological Image Analysis: Principles and Applications. Springer.

8. Montanari, O. (1968). On the optimal detection of curves in noisy pictures. Communications of the ACM, 11(5), 335-345.

9. Felzenszwalb, P. F., & Huttenlocher, D. P. (2004). Distance transforms of sampled functions. Cornell University.

10. Edelsbrunner, H., & Harer, J. (2010). Computational Topology: An Introduction. American Mathematical Society.

11. Müller, T., et al. (2022). Instant Neural Graphics Primitives with a Multiresolution Hash Encoding. ACM Transactions on Graphics.

---

*This textbook provides a comprehensive introduction to digital geometry for undergraduate students. The material covers foundational concepts, practical algorithms, and modern techniques, with emphasis on both mathematical theory and implementation.*