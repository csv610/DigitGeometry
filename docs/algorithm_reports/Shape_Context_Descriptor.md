# Shape Context Descriptor

## 1. Overview
The **Shape Context Descriptor** is a global shape descriptor used for object recognition and shape matching. For a point $p$ on a shape, the shape context is a coarse-grained histogram of the relative coordinates of all other points on the shape. It captures the distribution of the shape relative to $p$, making it powerful for point-set matching under deformation.

## 2. Definitions
- **Shape Point Set:** A set $P = \{p_1, p_2, \dots, p_n\}$ of points sampled from the shape boundary.
- **Log-Polar Binning:** A system where bins are defined by ranges of log-distance $\log(r)$ and angle $\theta$ from a reference point $p$.
- **Shape Context at $p_i$ ($h_i$):** A histogram of the remaining points $P \setminus \{p_i\}$ in log-polar bins.

## 3. Theory
### Histogram Construction
For a point $p_i$, the vector to another point $p_j$ is $(r_{ij}, \theta_{ij})$. The shape context $h_i(k)$ for bin $k$ is:
$$h_i(k) = \#\{p_j \neq p_i : (p_j - p_i) \in \text{bin } k\}$$
Usually, 5 distance bins (logarithmically spaced) and 12 angle bins (uniformly spaced) are used, resulting in a 60-dimensional descriptor per point.

### Matching Cost
The cost of matching point $p_i$ on shape $P$ to point $q_j$ on shape $Q$ is computed using the $\chi^2$ test:
$$C_{ij} = \frac{1}{2} \sum_{k=1}^K \frac{(h_i(k) - g_j(k))^2}{h_i(k) + g_j(k)}$$
where $h_i$ and $g_j$ are the respective shape contexts.

### Global Matching
To match two shapes, one solves a bipartite matching problem (e.g., using the Hungarian algorithm) to minimize the total matching cost $\sum C_{i,\pi(i)}$.

## 4. Pseudo Code
```python
def compute_shape_context(points, num_r_bins=5, num_theta_bins=12):
    n = len(points)
    # 1. Compute pairwise distances and angles
    diffs = points[:, None, :] - points[None, :, :]
    dists = norm(diffs, axis=-1)
    angles = atan2(diffs[..., 1], diffs[..., 0])
    
    # 2. Log-normalize distances relative to mean distance
    mean_dist = mean(dists)
    log_dists = log(dists / mean_dist + 1e-6)
    
    # 3. Create histograms
    histograms = []
    for i in range(n):
        # Assign each point j to a log-polar bin relative to point i
        h = histogram2d(log_dists[i], angles[i], bins=[num_r_bins, num_theta_bins])
        histograms.append(h.flatten())
    return array(histograms)
```

## 5. Parameters Selections
- **Number of Sample Points:** Typically $N=100$ to $200$. Sampling is often done using a "farthest point" strategy for even distribution.
- **Binning:** $5 \times 12$ is standard. Increasing bin resolution adds detail but increases sensitivity to noise.
- **Rotation Invariance:** Achieved by normalizing the angles $\theta$ relative to the local tangent at each point.

## 6. Complexity
- **Descriptor Calculation:** $O(N^2)$ for $N$ points.
- **Matching Cost Matrix:** $O(N^2 \cdot K)$ where $K$ is the number of bins.
- **Shape Matching:** $O(N^3)$ for the Hungarian algorithm.

## 7. Usage
- **Handwritten Digit Recognition:** Original application by Belongie et al. on the MNIST dataset.
- **Logo Recognition:** Identifying brands and logos in images.
- **Medical Image Registration:** Aligning anatomical shapes across different patients.
- **3D Shape Analysis:** Generalizing the concept to 3D with spherical histograms.

## 9. References
1.  Belongie, S., et al. (2002). *Shape Matching and Object Recognition Using Shape Contexts*. IEEE Transactions on Pattern Analysis and Machine Intelligence.
2.  Mori, G., et al. (2005). *Efficient Shape Matching using Shape Contexts*. IEEE CVPR.
3.  Cormen, T. H., et al. (2009). *Introduction to Algorithms* (for Hungarian algorithm).
