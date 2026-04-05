# Medial Axis Transform (MAT)

## 1. Overview
The Medial Axis Transform (MAT) is a powerful tool for representing the shape and structure of a 2D or 3D object. The medial axis (or "skeleton") is the set of all points that have more than one closest point on the object's boundary. The transform itself consists of this skeleton along with the distance from each point on the skeleton to the nearest point on the boundary (the "radius"). It is fundamental in digital geometry for shape analysis, compression, and recognition.

## 2. Definitions
*   **Boundary ($\partial S$):** The set of points that define the edge of the object $S$.
*   **Distance Transform ($DT$):** The function mapping each point inside $S$ to its distance to $\partial S$.
*   **Medial Axis ($MA$):** The locus of centers of maximal inscribed balls within the object.
*   **Maximal Inscribed Ball ($B$):** A ball contained in $S$ that is not a subset of any other ball contained in $S$.
*   **Skeleton:** The geometric representation of the medial axis.

## 3. Theory
The medial axis can be thought of as the "burn-out" points where fire fronts originating from the object's boundary meet, assuming the fire spreads inward at a constant speed. This is known as the **Grassfire Analogy**.
For a point $p$ to be on the medial axis, there must exist at least two distinct points $b_1, b_2 \in \partial S$ such that $d(p, b_1) = d(p, b_2) = DT(p)$.
The medial axis transform is an **invertible** representation. The original shape can be reconstructed by taking the union of all maximal inscribed balls defined by the MAT.

## 4. Pseudo Code
### Extracting MAT from a Distance Transform
```text
function extractMedialAxis(distanceTransform)
    skeleton := emptySet()
    for each pixel (x, y)
        // A pixel is on the medial axis if it is a local maximum
        // of the distance transform in at least one direction.
        if isLocalMaximum(distanceTransform, x, y)
            skeleton.add(x, y, radius := distanceTransform[x, y])
            
    // Post-processing: thinning or pruning to ensure 
    // the skeleton is one-pixel thick and connected.
    skeleton := pruneBranches(skeleton)
    return skeleton
```

## 5. Parameters Selections
*   **Pruning Threshold:** The medial axis is highly sensitive to noise on the boundary. Small boundary perturbations can result in large, spurious "branches" in the skeleton. Pruning removes these branches based on their length or the "importance" of the region they represent.
*   **Connectivity:** Define whether 4-way or 8-way connectivity is used to ensure the skeleton is topologically consistent with the original shape.

## 6. Complexity
*   **Time Complexity:** $O(N)$ for both the initial distance transform and the extraction of the skeleton (where $N$ is the number of pixels).
*   **Space Complexity:** $O(N)$ for storing the distance field and the skeleton.

## 7. Usage
*   Shape recognition and matching.
*   Computer animation for character rigging (skeleton extraction).
*   Handwriting recognition and optical character recognition (OCR).
*   Medical imaging for analyzing the structure of blood vessels or bones.
*   Image compression by storing only the MAT instead of the full shape.

## 9. References
1.  Blum, H. (1967). A transformation for extracting new descriptors of shape. *Models for the Perception of Speech and Visual Form*.
2.  Siddiqi, K., & Pizer, S. M. (2008). *Medial Representations: Mathematics, Algorithms and Applications*.
3.  Telea, A., & Van Wijk, J. J. (1999). An augmented fast marching method for computing skeletons and centerlines. *Joint Eurographics-IEEE TCVG Symposium on Visualization*.
