# Euler Characteristic and Euler Number

## 1. Overview
The Euler characteristic ($\chi$) is a topological invariant, a number that describes a topological space's shape or structure regardless of the way it is bent. In digital geometry and image processing, it is often called the Euler number and is used to characterize the connectivity and topology of digital shapes, particularly the relationship between the number of objects, holes, and cavities.

## 2. Definitions
*   **Vertex ($V$), Edge ($E$), Face ($F$):** The basic components of a polyhedral or cellular decomposition.
*   **Connected Component ($C$):** A set of connected elements.
*   **Hole ($H$):** A tunnel through an object (e.g., in a torus).
*   **Cavity ($Cav$):** A void fully enclosed within an object.
*   **Genus ($g$):** The number of "handles" on a surface (e.g., $g=1$ for a torus).

## 3. Theory
For a convex polyhedron or any surface topologically equivalent to a sphere, the Euler characteristic is:
$$\chi = V - E + F = 2$$
For more general surfaces, it is related to the genus $g$ by:
$$\chi = 2 - 2g$$
In 2D digital images, the Euler number $E$ is defined as the number of objects minus the number of holes:
$$E = C - H$$
In 3D, it is defined as:
$$E = C - H + Cav$$
In a digital grid, the Euler number can be computed locally by counting specific pixel patterns (configurations) called "Euler contribution" or using the "Marching Cubes" approach. For example, in a 2D binary image using 4-connectivity for objects and 8-connectivity for holes, the Euler number can be computed by counting 2x2 bit patterns.

## 4. Pseudo Code (Local Configuration Count - 2D)
```text
function EulerNumber2D(image)
    // Counts specific 2x2 patterns in a binary image
    // C1: Number of patterns with 1 foreground pixel
    // C2: Number of patterns with 2 diagonally adjacent foreground pixels
    // C3: Number of patterns with 3 foreground pixels
    
    // For 8-connectivity:
    euler_8 = (N(patterns_with_1) - N(patterns_with_3) - 2 * N(diagonal_2)) / 4
    
    // For 4-connectivity:
    euler_4 = (N(patterns_with_1) - N(patterns_with_3) + 2 * N(diagonal_2)) / 4
    
    return euler
```

## 5. Parameters Selections
*   **Connectivity (4 vs 8 in 2D, 6 vs 26 in 3D):** The choice of connectivity significantly affects the resulting Euler number. A common requirement is to use complementary connectivity for the background to maintain topological consistency (e.g., 8-connectivity for foreground and 4-connectivity for background).

## 6. Complexity
*   **Time Complexity:** $O(N)$, where $N$ is the number of pixels. The algorithm scans the image once.
*   **Space Complexity:** $O(1)$ additional space beyond the input image.

## 7. Usage
*   Shape analysis and feature extraction in medical imaging (e.g., characterizing bone porosity).
*   Quality control in manufacturing.
*   Topological consistency checks in surface reconstruction.
*   Symmetry and structural analysis of complex materials.

## 9. References
1.  Gray, S. B. (1971). Local Properties of Binary Images in Two Dimensions. IEEE Transactions on Computers.
2.  Kong, T. Y., & Rosenfeld, A. (1989). Digital Topology: Introduction and Survey. Computer Vision, Graphics, and Image Processing.
3.  Lachaud, J. O. (2007). Euler Characteristic of Discrete Surfaces. Digital Geometry.
