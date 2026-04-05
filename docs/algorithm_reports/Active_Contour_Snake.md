# Active Contour Snake

## 1. Overview
Active Contour Models, popularly known as "Snakes," are an energy-minimizing, deformable spline that is influenced by constraint and image forces that pull it towards object contours. They are widely used in computer vision for image segmentation, edge detection, and tracking objects through image sequences.

## 2. Definitions
*   **Snake:** A controlled continuity spline $v(s) = (x(s), y(s))$, where $s \in [0, 1]$ is the arc length.
*   **Energy Function ($E_{snake}$):** A scalar value that the algorithm seeks to minimize, representing the "fitness" of the contour to the image.
*   **Internal Energy ($E_{int}$):** Represents the bending and stretching resistance of the snake.
*   **External Energy ($E_{ext}$ or $E_{image}$):** Forces that attract the snake toward features like edges or lines in the image.
*   **Constraint Energy ($E_{con}$):** User-defined or high-level constraints that guide the snake.

## 3. Theory
The position of a snake is represented parametrically as $v(s) = (x(s), y(s))$. The total energy of the snake is:
$$E_{snake} = \int_{0}^{1} [E_{int}(v(s)) + E_{image}(v(s)) + E_{con}(v(s))] ds$$

The internal energy is defined as:
$$E_{int} = \frac{1}{2} (\alpha(s) |v'(s)|^2 + \beta(s) |v''(s)|^2)$$
where $\alpha$ controls "elasticity" (stretching) and $\beta$ controls "rigidity" (bending).

The image energy is typically defined using the gradient of the image intensity $I(x, y)$:
$$E_{image} = -w_{edge} |\nabla (G_\sigma * I(x, y))|^2$$
where $G_\sigma$ is a Gaussian smoothing filter to broaden the basin of attraction around edges.

## 4. Pseudo Code
```text
function Active_Contour_Snake(image, initial_contour, alpha, beta, gamma, iterations)
    contour := initial_contour
    precompute image_force := -gradient(magnitude(gradient(image)))
    
    for i from 1 to iterations
        // Update the contour points to minimize total energy
        // This is often solved using a matrix inversion or gradient descent
        for each point p in contour
            calculate internal_forces(p, alpha, beta)
            calculate external_forces(p, image_force)
            update p position based on force * gamma
        
        re-sample(contour) // Optionally maintain point spacing
        
    return contour
```

## 5. Parameters Selections
*   **$\alpha$ (Elasticity):** High values make the snake act like a rubber band, pulling points together. Low values allow the snake to expand or stretch.
*   **$\beta$ (Curvature/Rigidity):** High values make the snake resist sharp corners and remain smooth.
*   **$\gamma$ (Step size):** Controls the speed of convergence. Too high leads to instability; too low leads to slow convergence.
*   **Gaussian $\sigma$:** A larger $\sigma$ allows the snake to "feel" edges from a greater distance but reduces precision.

## 6. Complexity
*   **Time Complexity:** $O(N \cdot M)$ per iteration, where $N$ is the number of points on the contour and $M$ is the neighborhood size for search, or $O(N \cdot \text{log}N)$ if using efficient matrix solvers.
*   **Space Complexity:** $O(N + \text{ImageSize})$ to store the contour and precomputed image gradients.

## 7. Usage
*   Medical imaging (segmenting organs, tumors, and blood vessels).
*   Facial feature detection (segmenting lips or eyes).
*   Motion tracking in video.

## 9. References
1.  Kass, M., Witkin, A., & Terzopoulos, D. (1988). Snakes: Active contour models. International Journal of Computer Vision.
2.  Chan, T. F., & Vese, L. A. (2001). Active contours without edges. IEEE Transactions on Image Processing.
3.  Blake, A., & Isard, M. (1998). Active Contours. Springer-Verlag.
