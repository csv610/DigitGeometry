# Jump Flooding Algorithm (JFA)

## 1. Overview
The Jump Flooding Algorithm (JFA) is an efficient technique for calculating the Voronoi diagram or the Distance Transform of a set of seed points on a grid. Unlike traditional flood fill algorithms that visit neighboring pixels one by one, JFA uses a "jumping" strategy to propagate seed information across the entire grid in a logarithmic number of passes. It is highly parallelizable and primarily used in GPU-based image processing.

## 2. Definitions
*   **Seed Point ($s$):** A starting point in the grid with a known property (e.g., location, color).
*   **Step Size ($k$):** The distance in pixels between the current pixel and the neighbors being queried.
*   **Voronoi Diagram:** A partition of the grid into regions, where each region consists of points closest to a particular seed.
*   **Distance Transform:** An image where each pixel value is the distance to the nearest seed point.

## 3. Theory
JFA operates on a grid of size $N \times N$. In each pass, every pixel $(x, y)$ queries its neighbors at distance $k$. The neighbors are at $(x \pm k, y \pm k)$, $(x \pm k, y)$, and $(x, y \pm k)$. If a neighbor knows of a seed point that is closer to $(x, y)$ than its current closest seed, the pixel $(x, y)$ updates its record.
The step size $k$ starts at $N/2$ and is halved in each subsequent pass ($k = N/4, N/8, \dots, 1$).
Although JFA is a heuristic and can occasionally produce small errors in the Voronoi boundaries, it is extremely fast and accurate enough for most computer graphics applications. The errors can be mitigated using an additional $1 \times 1$ pass or a "JFA+1" variant.

## 4. Pseudo Code
```text
function JumpFlooding(seeds, width, height)
    grid := initializeGridWithInfinity()
    for each (x, y) in seeds
        grid[x, y] := (x, y) // Store its own coordinates as the closest seed
        
    k := max(width, height) / 2
    while k >= 1
        for each pixel p = (x, y) in parallel
            for each offset dx, dy in {-k, 0, k}
                neighbor := (x + dx, y + dy)
                if neighbor within bounds
                    seed_n := grid[neighbor]
                    if distance(p, seed_n) < distance(p, grid[p])
                        grid[p] := seed_n
        k := k / 2
        
    return grid
```

## 5. Parameters Selections
*   **Initial Step Size ($k$):** Usually set to $2^{\lceil \log_2 N \rceil - 1}$ for a grid of size $N$.
*   **Pass Variations:** JFA+1 or JFA+2 (additional passes with $k=1$ or $k=2$) can be used to resolve precision issues at Voronoi boundaries.

## 6. Complexity
*   **Time Complexity:** $O(\log N)$ parallel passes on a grid of size $N \times N$. Total sequential operations are $O(N^2 \log N)$.
*   **Space Complexity:** $O(N^2)$ to store the closest seed coordinates for each pixel.

## 7. Usage
*   GPU-accelerated Voronoi diagram generation.
*   Calculating Euclidean distance transforms.
*   Generating high-quality drop shadows and halos in real-time.
*   Morphological operations (dilation, erosion) with large kernels.
*   Path planning and obstacle avoidance in games.

## 9. References
1.  Rong, G., & Tan, T. S. (2006). Jump Flooding in GPU with Applications to Voronoi Diagram and Distance Transform. *Symposium on Interactive 3D Graphics and Games*.
2.  Schneider, J., & Westermann, R. (2001). GPU-based calculation of distance fields. *Technical Report*.
3.  Guodong, R., & Tiow-Seng, T. (2007). Variants of Jump Flooding Algorithm for Computing Discrete Voronoi Diagrams. *International Symposium on Voronoi Diagrams in Science and Engineering*.
