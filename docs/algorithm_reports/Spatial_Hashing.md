# Spatial Hashing (Nießner et al.)

## 1. Overview
Spatial Hashing, particularly the version popularized by Nießner et al. (2013), is an efficient data structure for real-time 3D reconstruction and surface representation. Unlike traditional dense grids (which are memory-heavy) or Octrees (which have high traversal costs), Spatial Hashing uses a hash table to store only those 3D regions (blocks) that actually contain surface information. This allows for representing large-scale environments with high resolution while maintaining a low memory footprint and enabling fast GPU-based operations.

## 2. Definitions
*   **Voxel Block:** A small, fixed-size cube of voxels (e.g., $8 \times 8 \times 8$). This is the fundamental unit of storage.
*   **Hash Table:** A data structure that maps 3D coordinates $(x, y, z)$ to a pointer (or index) in a "bucket" of voxel blocks.
*   **SDF (Signed Distance Function):** A function representing a surface by storing the distance to the nearest point on the surface, where the sign indicates whether a voxel is inside or outside the object.
*   **Hash Function:** A mathematical function that converts a 3D coordinate into a 1D index for the hash table.

## 3. Theory
Spatial Hashing combines the benefits of sparse storage with the speed of constant-time access. Instead of allocating memory for empty space, it only allocates "voxel blocks" as needed.

1.  **Coordinate Mapping:** The world space is divided into a grid of blocks. For any given 3D point $(x, y, z)$, its block coordinates are $B = (\lfloor x/L \rfloor, \lfloor y/L \rfloor, \lfloor z/L \rfloor)$, where $L$ is the block size.
2.  **Hashing:** The block coordinates are converted into a hash index $H(B)$:
    $$H(x, y, z) = (x \cdot p_1 \oplus y \cdot p_2 \oplus z \cdot p_3) \pmod{N}$$
    where $p_i$ are large prime numbers and $N$ is the size of the hash table.
3.  **Bucket Management:** Since multiple coordinates can hash to the same index (collision), each entry in the hash table points to a bucket. Buckets store pointers to actual voxel blocks in a pre-allocated "block pool."
4.  **Integration:** As new sensor data (e.g., from a depth camera) arrives, the algorithm:
    *   Finds the blocks along the camera rays.
    *   Allocates new blocks if they don't exist.
    *   Updates the SDF values within existing blocks.

## 4. Pseudo Code
```text
function getBlock(worldPos)
    blockPos := floor(worldPos / BLOCK_SIZE)
    hashIndex := computeHash(blockPos)
    
    // Check hash table for block index
    bucket := hashTable[hashIndex]
    for entry in bucket:
        if entry.pos == blockPos:
            return entry.blockIndex
            
    // If not found, allocate from pool
    newIndex := allocateFromPool()
    hashTable[hashIndex].insert(blockPos, newIndex)
    return newIndex

function integrateDepthFrame(depthImg, cameraPose)
    for pixel in depthImg:
        ray := backProject(pixel, cameraPose)
        for blockPos along ray:
            block := getBlock(blockPos)
            updateSDF(block, ray, depthImg[pixel])
```

## 5. Parameters Selections
*   **Voxel Size:** Typically 1cm to 5cm, depending on the required reconstruction detail.
*   **Block Size:** Usually $8 \times 8 \times 8$ voxels. This size is optimized for GPU threading (512 threads per block).
*   **Hash Table Size:** Must be large enough to minimize collisions (e.g., $2^{20}$ entries).
*   **Prime Numbers:** Common choices are large primes like $73856093, 19349663, 83492791$.

## 6. Complexity
*   **Time Complexity:** $O(1)$ on average for block retrieval (hashing). The integration step is $O(M)$ where $M$ is the number of voxels affected by the camera's field of view.
*   **Space Complexity:** $O(B \cdot V^3)$, where $B$ is the number of non-empty blocks and $V$ is the block resolution. This is much smaller than $O(N^3)$ for a dense grid.

## 7. Usage
*   **Real-time 3D Scanning:** Systems like Microsoft's KinectFusion (enhanced with hashing).
*   **Robotics:** SLAM (Simultaneous Localization and Mapping) for large-scale environments.
*   **AR/VR:** Creating interactive meshes of physical rooms in real-time.
*   **GPU Path Tracing:** Using the hashed SDF to efficiently trace rays in complex scenes.

## 9. References
1.  Nießner, M., et al. (2013). *Real-time 3D Reconstruction at Scale using Voxel Hashing*. ACM Transactions on Graphics (TOG).
2.  Teschner, M., et al. (2003). *Optimized Spatial Hashing for Collision Detection of Deformable Objects*. VMV.
3.  Newcombe, R. A., et al. (2011). *KinectFusion: Real-time dense surface reconstruction and tracking*. ISMAR.
