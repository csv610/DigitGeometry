# Anisotropic Diffusion

## 1. Overview
Anisotropic diffusion, also called Perona-Malik diffusion, is a technique aiming at reducing image noise without removing significant parts of the image content, typically edges, lines, or other details that are important for the interpretation of the image. Unlike isotropic diffusion (standard Gaussian blurring), anisotropic diffusion is a non-linear and space-variant transformation.

## 2. Definitions
*   **Isotropic Diffusion:** Uniform blurring across the image (e.g., Gaussian blur).
*   **Anisotropic Diffusion:** A process where the diffusion is adapted to the local image features, typically the gradient.
*   **Edge:** A location in an image where the intensity changes rapidly.
*   **Diffusion Coefficient ($c$):** A function that controls the rate of diffusion at a given point based on the local image gradient.

## 3. Theory
The diffusion process is described by the partial differential equation (PDE):
$$ \frac{\partial I}{\partial t} = \text{div}(c(x, y, t) \nabla I) = \nabla c \cdot \nabla I + c(x, y, t) \Delta I $$
where $I$ is the image, $t$ is the time (iteration step), and $\text{div}$ is the divergence operator.

Perona and Malik proposed two diffusion coefficients:
1.  $c(|\nabla I|) = \exp(-(|\nabla I|/K)^2)$
2.  $c(|\nabla I|) = \frac{1}{1 + (|\nabla I|/K)^2}$

where $K$ is a constant that controls the sensitivity to edges. When $|\nabla I| \gg K$, the coefficient $c$ approaches 0, stopping diffusion and preserving the edge. When $|\nabla I| \ll K$, $c$ approaches 1, allowing smoothing.

## 4. Pseudo Code
```text
function Anisotropic_Diffusion(image, iterations, kappa, delta_t)
    I := copy(image)
    for i from 1 to iterations
        // Calculate gradients in 4 directions (N, S, E, W)
        gradN := roll(I, -1, axis=0) - I
        gradS := roll(I, 1, axis=0) - I
        gradE := roll(I, -1, axis=1) - I
        gradW := roll(I, 1, axis=1) - I
        
        // Calculate diffusion coefficients
        cN := exp(-(gradN/kappa)^2)
        cS := exp(-(gradS/kappa)^2)
        cE := exp(-(gradE/kappa)^2)
        cW := exp(-(gradW/kappa)^2)
        
        // Update image
        I := I + delta_t * (cN*gradN + cS*gradS + cE*gradE + cW*gradW)
    return I
```

## 5. Parameters Selections
*   **$K$ (Kappa):** The gradient threshold. Small values of $K$ preserve even weak edges but leave more noise. Large values of $K$ smooth more but may blur important edges.
*   **$\Delta t$ (Delta T):** The time step. For 2D images, $\Delta t$ must be $\leq 0.25$ to ensure numerical stability.
*   **Iterations:** The number of times the diffusion is applied. More iterations lead to smoother images.

## 6. Complexity
*   **Time Complexity:** $O(W \cdot H \cdot N)$, where $W, H$ are image dimensions and $N$ is the number of iterations.
*   **Space Complexity:** $O(W \cdot H)$ to store the image and temporary gradient maps.

## 7. Usage
*   Image denoising (preserving sharp edges).
*   Preprocessing for edge detection and image segmentation.
*   Scale-space analysis.
*   Enhancement of low-contrast images.

## 9. References
1.  Perona, P., & Malik, J. (1990). Scale-space and edge detection using anisotropic diffusion. IEEE Transactions on Pattern Analysis and Machine Intelligence.
2.  Gerig, G., et al. (1992). Nonlinear anisotropic filtering of MRI data. IEEE Transactions on Medical Imaging.
3.  Weickert, J. (1998). Anisotropic Diffusion in Image Processing. Teubner.
