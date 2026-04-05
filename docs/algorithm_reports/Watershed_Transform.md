# Watershed Transform

## 1. Overview
The **Watershed Transform** is a powerful morphological segmentation algorithm that views a grayscale image as a topographic surface. Bright pixels are peaks (high altitude) and dark pixels are valleys (low altitude). The image is partitioned into regions (catchment basins) based on where water would accumulate if the surface were flooded from its local minima.

## 2. Definitions
- **Catchment Basin:** A region where all points drain into the same local minimum.
- **Watershed Lines:** The boundaries that separate different catchment basins (ridges of the terrain).
- **Markers:** Specific points or areas that define the seeds for the flooding process.

## 3. Theory
### Flooding Analogy
Imagine the image as a 3D landscape. Small holes are drilled at each local minimum. As water rises, it fills the catchment basins. When water from two different basins is about to merge, a dam (watershed line) is built to keep them separate. The process continues until the entire image is covered.

### Marker-Controlled Watershed
A common problem is "over-segmentation," where every local minimum (even tiny ones from noise) creates its own basin. To solve this, **Markers** are used to specify exactly which regions should be grown. Only these markers serve as flooding sources.

## 4. Pseudo Code (Meyer's Watershed)
The algorithm uses a priority queue to manage the flooding process.

```python
def watershed_segmentation(gradient_image, markers):
    # markers: labeled image with seed regions
    pq = PriorityQueue()
    # 1. Initialize priority queue with neighbors of marker pixels
    for p in all_pixels:
        if is_neighbor_of_marker(p):
            priority = gradient_image[p]
            pq.push(p, priority)
            
    while not pq.empty():
        p, d = pq.pop_min()
        # 2. Assign label from neighbor marker if possible
        if p has labeled neighbor and not yet labeled:
            assign_label(p, neighbor_label)
            # 3. Add p's unlabeled neighbors to the queue
            for q in neighbors(p):
                if q not labeled and q not in pq:
                    pq.push(q, gradient_image[q])
                    
    return labeled_image
```

## 5. Parameters Selections
- **Gradient Image:** Usually, the watershed is applied to the image's gradient (e.g., Sobel, Canny) rather than the original grayscale. This ensures boundaries are located at the highest intensity changes.
- **Connectivity:** 4-connected vs. 8-connected. 4-connectivity often results in thicker watershed lines.
- **Marker Selection:** Automatic markers (from distance transforms or regional minima) vs. manual markers.

## 6. Complexity
- **Time Complexity:** $O(N \log N)$ where $N$ is the number of pixels. The $\log N$ comes from the priority queue operations.
- **Space Complexity:** $O(N)$ to store labels, the priority queue, and the image itself.

## 7. Usage
- **Medical Imaging:** Segmenting nuclei in cells or organs in MRI scans.
- **Object Tracking:** Separating touching or overlapping objects (e.g., coins, cells).
- **Image Editing:** Implementing "Intelligent Scissors" or semi-automatic cutout tools.

## 9. References
1.  Beucher, S., & Lantuéjoul, C. (1979). *Use of Watersheds in Contour Detection*. International Workshop on Image Processing.
2.  Meyer, F. (1994). *Topographic Distance and Watershed Lines*. Signal Processing.
3.  Vincent, L., & Soille, P. (1991). *Watersheds in Digital Spaces: An Efficient Algorithm Based on Immersion Simulations*. IEEE Transactions on Pattern Analysis and Machine Intelligence.
