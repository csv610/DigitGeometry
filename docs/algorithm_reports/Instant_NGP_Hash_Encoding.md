# Instant NGP Hash Encoding (Multiresolution Hashing)

## 1. Overview
Instant NGP (Neural Graphics Primitives), introduced by Müller et al. (2022), is a groundbreaking technique for training neural representations (like NeRF - Neural Radiance Fields) in seconds rather than hours. The core of this speedup is **Multiresolution Hash Encoding**. Instead of relying purely on large neural networks to learn coordinate-based functions, it uses a hybrid approach: a small, trainable hash-based feature grid combined with a tiny MLP. This allows for representing high-frequency spatial details with minimal computational overhead.

## 2. Definitions
*   **Hash Encoding:** A method where 3D coordinates are hashed to retrieve trainable feature vectors from a fixed-size table.
*   **Multiresolution:** The use of multiple independent grids at different scales (from coarse to fine).
*   **MLP (Multi-Layer Perceptron):** A small neural network that processes the retrieved hash features into the final output (e.g., color, density).
*   **Trilinear Interpolation:** A process of calculating feature values at a point based on its eight surrounding grid vertices.

## 3. Theory
The Multiresolution Hash Encoding maps a continuous 3D coordinate $\mathbf{x} \in \mathbb{R}^3$ into a high-dimensional feature vector.

1.  **Multiple Levels ($L$):** The space is partitioned into $L$ independent grids with resolutions $N_l$ (coarse to fine).
2.  **Grid Traversal:** For each level $l$, the coordinate $\mathbf{x}$ is scaled by the resolution $N_l$. The eight corners of the surrounding voxel are identified.
3.  **Hashing:** The integer coordinates of these corners are hashed into a table of size $T$. If the resolution is low enough ($N_l^3 \leq T$), the mapping is a direct 1-to-1 grid. At higher resolutions, collisions occur, which the neural network learns to resolve.
4.  **Lookup and Interpolation:** Feature vectors are retrieved from the hash table for each of the eight corners. Trilinear interpolation is performed based on the relative position of $\mathbf{x}$ within the voxel.
5.  **Concatenation:** The interpolated features from all $L$ levels are concatenated (and potentially augmented with auxiliary inputs like viewing direction) to form the input to a small MLP.

### Hashing Formula:
$$h(\mathbf{p}) = \left( \bigoplus_{i=1}^d p_i \cdot \pi_i \right) \pmod{T}$$
where $\pi_i$ are large, unique prime numbers.

## 4. Pseudo Code
```text
function getEncodedFeatures(x, resolutions, hashTables)
    allFeatures := []
    for l in range(L):
        res := resolutions[l]
        table := hashTables[l]
        
        // Find corners of the voxel containing x
        p_float := x * res
        p_floor := floor(p_float)
        p_ceil := p_floor + 1
        
        corners := getEightCorners(p_floor, p_ceil)
        cornerFeatures := []
        for c in corners:
            h := computeHash(c, table.size)
            cornerFeatures.append(table[h])
            
        // Interpolate within the voxel
        weights := p_float - p_floor
        interpolated := trilinearInterpolate(cornerFeatures, weights)
        allFeatures.append(interpolated)
        
    return concatenate(allFeatures)
```

## 5. Parameters Selections
*   **Number of Levels ($L$):** Typically 16.
*   **Hash Table Size ($T$):** Usually $2^{14}$ to $2^{24}$, balancing memory and collision rate.
*   **Feature Dimension ($F$):** Usually 2 features per level.
*   **Resolution Range:** Coarse resolution (e.g., 16) to fine resolution (e.g., $2^{19}$). The resolutions usually follow a geometric progression.
*   **MLP Size:** Typically 2 layers with 64 neurons, significantly smaller than traditional NeRF models.

## 6. Complexity
*   **Time Complexity:** $O(L \cdot F)$ for feature retrieval and interpolation. This is independent of the spatial resolution, making it extremely fast.
*   **Space Complexity:** $O(L \cdot T \cdot F)$ to store the trainable hash tables.
*   **Training Speed:** Up to 100x-1000x faster than traditional coordinate-based neural networks.

## 7. Usage
*   **Neural Radiance Fields (NeRF):** High-speed reconstruction of 3D scenes from 2D images.
*   **Signed Distance Functions (SDFs):** Rapidly learning implicit surfaces from point clouds or meshes.
*   **Neural Volumes:** Representing volumetric data like smoke or fire.
*   **Real-time Rendering:** Enabling neural-based effects in interactive applications.

## 9. References
1.  Müller, T., et al. (2022). *Instant Neural Graphics Primitives with a Multiresolution Hash Encoding*. ACM Transactions on Graphics (TOG).
2.  Mildenhall, B., et al. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV.
3.  Sun, C., et al. (2022). *Direct Voxel Grid Optimization: Super-fast Convergence for Radiance Fields Reconstruction*. CVPR.
