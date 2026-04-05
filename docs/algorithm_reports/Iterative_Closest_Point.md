# Iterative Closest Point (ICP)

## 1. Overview
The Iterative Closest Point (ICP) is an algorithm used to minimize the difference between two clouds of points. ICP is often used to reconstruct 2D or 3D surfaces from different scans, to localize robots and achieve optimal path planning, and to register medical images. The goal is to find the optimal rigid transformation (translation and rotation) that aligns a source point cloud with a target point cloud.

## 2. Definitions
*   **Source Cloud ($P$):** The point cloud to be moved.
*   **Target Cloud ($Q$):** The reference point cloud.
*   **Transformation ($T$):** A combination of a rotation matrix $R$ and a translation vector $t$ that maps points from $P$ to $Q$.
*   **Correspondence:** A mapping that assigns each point in $P$ to its nearest neighbor in $Q$.

## 3. Theory
The ICP algorithm iteratively refines the transformation to minimize a cost function, typically the sum of squared distances:
$$E(R, t) = \sum_{i=1}^{n} \| (R p_i + t) - q_i \|^2$$
where $p_i \in P$ and $q_i \in Q$ are corresponding points.
Each iteration of the algorithm consists of two main steps:
1.  **Correspondence Search:** For each point in the transformed source cloud, find its nearest neighbor in the target cloud.
2.  **Transformation Update:** Use Singular Value Decomposition (SVD) or a similar method to find the optimal $R$ and $t$ that align the corresponding points.

### ICP Variants
*   **Point-to-Point:** Minimizes the distance between points.
*   **Point-to-Plane:** Minimizes the distance between a point in $P$ and the tangent plane at the corresponding point in $Q$. This variant is more robust and converges faster.

## 4. Pseudo Code
```text
function ICP(source, target)
    transformation := Identity
    while not converged
        // 1. Find correspondences
        correspondences := []
        for each p in source
            q := findNearestNeighbor(transform(p, transformation), target)
            correspondences.append(p, q)
            
        // 2. Estimate transformation
        R, t := estimateBestTransform(correspondences)
        
        // 3. Update the global transformation
        transformation := compose(transformation, R, t)
        
        if change(transformation) < threshold
            break
            
    return transformation
```

## 5. Parameters Selections
*   **Initial Guess:** ICP is a local optimizer. It requires a reasonably good initial alignment to avoid falling into local minima.
*   **Correspondence Metric:** Euclidean distance is standard. Rejecting correspondences beyond a certain distance threshold can improve robustness to outliers.
*   **Stopping Criterion:** Typically based on the change in error or the change in transformation parameters between iterations.

## 6. Complexity
*   **Time Complexity:** $O(I \cdot N \log M)$, where $I$ is the number of iterations, $N$ is the number of points in the source cloud, and $M$ is the number of points in the target cloud (assuming a KD-Tree is used for nearest-neighbor search).
*   **Space Complexity:** $O(N + M)$ for storing point clouds and KD-Trees.

## 7. Usage
*   3D reconstruction from LiDAR or structured light scans.
*   SLAM (Simultaneous Localization and Mapping) for autonomous vehicles and drones.
*   Medical imaging for aligning 3D bone or organ models from CT scans.
*   CAD/CAM for quality inspection of manufactured parts.

## 9. References
1.  Besl, P. J., & McKay, N. D. (1992). A method for registration of 3-D shapes. *IEEE Transactions on Pattern Analysis and Machine Intelligence*.
2.  Chen, Y., & Medioni, G. (1991). Object modeling by registration of multiple range images. *IEEE Conference on Robotics and Automation*.
3.  Rusinkiewicz, S., & Levoy, M. (2001). Efficient variants of the ICP algorithm. *International Conference on 3-D Digital Imaging and Modeling*.
