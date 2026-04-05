# Freeman Chain Code

## 1. Overview
The Freeman Chain Code is a compact representation of a 2D boundary or line as a sequence of unit-length steps in a specific direction. It is a fundamental technique in digital geometry and computer vision for shape representation and boundary encoding. By representing a boundary as a series of integers, it reduces the amount of data needed to describe the shape.

## 2. Definitions
*   **Grid Graph:** The digital image is treated as a collection of nodes at $(x, y)$ coordinates.
*   **Direction Code:** An integer representing the direction of a move from the current pixel to the next boundary pixel.
*   **4-Connectivity:** A set of 4 directions (0, 1, 2, 3) representing moves to the right, up, left, and down.
*   **8-Connectivity:** A set of 8 directions (0, 1, 2, 3, 4, 5, 6, 7) representing the 4 cardinal directions and the 4 diagonals.
*   **Normalization:** Modifying the chain code to make it invariant to the starting point and rotation.

## 3. Theory
The boundary is represented by a starting coordinate $(x_0, y_0)$ and a sequence $c_1, c_2, \dots, c_n$, where each $c_i$ is a direction code.
### 8-Connectivity Code (Standard Freeman):
*   0: $(+1, 0)$ (East)
*   1: $(+1, +1)$ (North-East)
*   2: $(0, +1)$ (North)
*   3: $(-1, +1)$ (North-West)
*   4: $(-1, 0)$ (West)
*   5: $(-1, -1)$ (South-West)
*   6: $(0, -1)$ (South)
*   7: $(+1, -1)$ (South-East)

### Invariances
1.  **Translation Invariance:** The chain code itself is translation-invariant. Only the starting point $(x_0, y_0)$ contains location information.
2.  **Rotation Invariance:** The **Chain Difference Code** is rotation-invariant. Each element is the number of units of counter-clockwise rotation needed to change from the current direction to the next.
3.  **Starting Point Invariance:** Normalization is achieved by treating the code as a circular sequence and finding the lexicographical minimum.

## 4. Pseudo Code
### Boundary to Chain Code
```text
function getChainCode(boundaryPoints)
    if length(boundaryPoints) < 2 then return []
    
    chainCode := []
    for i from 0 to length(boundaryPoints) - 2
        p1 := boundaryPoints[i]
        p2 := boundaryPoints[i + 1]
        dx := p2.x - p1.x
        dy := p2.y - p1.y
        direction := findDirection(dx, dy)
        chainCode.append(direction)
        
    return chainCode
```

## 5. Parameters Selections
*   **Connectivity (4 or 8):** 8-connectivity provides a more accurate representation of diagonal boundaries, whereas 4-connectivity is simpler.
*   **Sampling Density:** The distance between the points being coded determines the resolution. High density captures more detail but increases data size.

## 6. Complexity
*   **Time Complexity:** $O(L)$, where $L$ is the number of points in the boundary sequence.
*   **Space Complexity:** $O(L)$ to store the chain code. Typically, it uses only 2 bits for 4-connectivity and 3 bits for 8-connectivity per boundary point.

## 7. Usage
*   Image data compression.
*   Shape recognition and matching.
*   Medical imaging for object boundary analysis.
*   Optical Character Recognition (OCR).
*   Calculating shape properties like perimeter and area using the chain code.

## 9. References
1.  Freeman, H. (1961). On the encoding of arbitrary geometric configurations. *IRE Transactions on Electronic Computers*.
2.  Freeman, H. (1974). Computer processing of line-drawing images. *ACM Computing Surveys*.
3.  Rosenfeld, A., & Pfaltz, J. L. (1966). Sequential operations in digital picture processing. *Journal of the ACM*.
