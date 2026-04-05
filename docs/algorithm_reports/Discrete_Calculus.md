# Discrete Gradient, Divergence, and Laplacian

## 1. Overview
The discrete versions of vector calculus operators—Gradient, Divergence, and Laplacian—are fundamental building blocks in digital geometry and image processing. They allow for the extension of continuous field theory to discrete grids (e.g., pixel grids or meshes) and are used for edge detection, image smoothing, fluid simulation, and geometric modeling.

## 2. Definitions
*   **Scalar Field ($f$):** A mapping that assigns a scalar value (e.g., intensity) to each pixel or vertex.
*   **Vector Field ($\mathbf{v}$):** A mapping that assigns a vector (e.g., gradient) to each pixel or edge.
*   **Gradient ($\nabla f$):** A vector field representing the direction and magnitude of the steepest increase of a scalar field.
*   **Divergence ($\nabla \cdot \mathbf{v}$):** A scalar field representing the net "flow" out of a point in a vector field.
*   **Laplacian ($\nabla^2 f$):** A scalar field representing the average local change in a scalar field, often used for smoothing and diffusion.

## 3. Theory
On a standard 2D digital grid with unit spacing:
*   **Discrete Gradient ($\nabla f$):** Typically computed using finite differences.
    $\nabla f(x, y) = [f(x+1, y) - f(x, y), f(x, y+1) - f(x, y)]^T$
*   **Discrete Divergence ($\nabla \cdot \mathbf{v}$):** For a vector field $\mathbf{v} = (v_x, v_y)$.
    $\nabla \cdot \mathbf{v}(x, y) = [v_x(x, y) - v_x(x-1, y)] + [v_y(x, y) - v_y(x, y-1)]$
*   **Discrete Laplacian ($\nabla^2 f$):** The divergence of the gradient, often approximated by the 5-point stencil:
    $\nabla^2 f(x, y) = f(x+1, y) + f(x-1, y) + f(x, y+1) + f(x, y-1) - 4f(x, y)$
These operators are linear and can be represented as sparse matrices. In image processing, they are often implemented as convolution kernels (e.g., Sobel for gradient, discrete Laplacian kernel).

## 4. Pseudo Code (Laplacian Smoothing)
```text
function LaplacianSmoothing(image, iterations, lambda)
    for iter from 1 to iterations
        new_image := copy(image)
        for y from 1 to height-2
            for x from 1 to width-2
                laplacian := image[x+1, y] + image[x-1, y] + 
                             image[x, y+1] + image[x, y-1] - 4 * image[x, y]
                new_image[x, y] := image[x, y] + lambda * laplacian
        image := new_image
    return image
```

## 5. Parameters Selections
*   **Finite Difference Scheme:** Forward, backward, or central differences depending on the application (e.g., central differences are better for symmetric operations).
*   **Boundary Conditions:** Neumann (zero gradient), Dirichlet (fixed value), or Periodic conditions are necessary for boundary pixels.
*   **Stencil Size:** Larger stencils (e.g., 9-point Laplacian) can provide better rotational invariance.

## 6. Complexity
*   **Time Complexity:** $O(N)$, where $N$ is the number of pixels or vertices.
*   **Space Complexity:** $O(N)$ to store the field and its derivatives.

## 7. Usage
*   Image segmentation (edge detection).
*   Heat diffusion and image smoothing.
*   Poisson image editing (seamless blending).
*   Mesh fairing and surface analysis.

## 9. References
1.  Strang, G. (2007). Computational Science and Engineering. Wellesley-Cambridge Press.
2.  Botsch, M., Kobbelt, L., Pauly, M., Alliez, P., & Levy, B. (2010). Polygon Mesh Processing. CRC Press.
3.  Grady, L. J., & Polimeni, J. R. (2010). Discrete Calculus: Applied Analysis on Graphs for Computational Science. Springer.
