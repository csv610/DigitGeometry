# Neural Implicit SDF (Signed Distance Fields)

## 1. Overview
**Neural Implicit SDFs** represent a 3D surface as the zero level-set of a signed distance function, where the function itself is approximated by a neural network. Unlike traditional explicit representations (meshes, point clouds) or discrete implicit ones (voxels), neural implicit SDFs provide a continuous, high-resolution representation of geometry.

## 2. Definitions
- **Signed Distance Function (SDF):** A function $f: \mathbb{R}^3 \to \mathbb{R}$ where $|f(\mathbf{x})|$ is the distance to the nearest surface, and the sign indicates if $\mathbf{x}$ is inside (negative) or outside (positive) the surface.
- **Neural Implicit Representation:** A neural network $\Phi$ with parameters $\theta$ such that $\Phi_\theta(\mathbf{x}) \approx f(\mathbf{x})$.
- **Iso-surface:** The surface $\mathcal{S}$ is defined as $\{\mathbf{x} \in \mathbb{R}^3 \mid \Phi_\theta(\mathbf{x}) = 0\}$.

## 3. Theory
### Multi-Layer Perceptrons (MLP)
A common choice for $\Phi_\theta$ is an MLP with ReLU or SIREN activations. The network takes a coordinate $\mathbf{x} = (x, y, z)$ as input and outputs a single scalar value.

### Eikonal Constraint
For $\Phi_\theta$ to represent a valid SDF, its gradient should have unit norm almost everywhere:
$$\|\nabla \Phi_\theta(\mathbf{x})\| = 1$$
This is often enforced as a regularization term in the loss function during training.

### DeepSDF
One of the pioneering methods (Park et al., 2019), which uses a latent code $\mathbf{z}$ to represent different shapes in a single network: $\Phi_\theta(\mathbf{z}, \mathbf{x})$.

## 4. Pseudo Code (Training Loop)
```python
def train_neural_sdf(model, points, distances):
    # points: (N, 3), distances: (N,) ground truth SDF values
    optimizer = Adam(model.parameters(), lr=1e-4)
    for epoch in range(num_epochs):
        predicted_sdf = model(points)
        
        # 1. Main SDF loss (e.g., L1 or L2)
        loss_sdf = mean((predicted_sdf - distances)**2)
        
        # 2. Eikonal loss (regularization)
        gradients = compute_gradient(model, points)
        loss_eikonal = mean((gradients.norm(dim=-1) - 1)**2)
        
        # 3. Combined loss
        loss = loss_sdf + lambda_eik * loss_eikonal
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## 5. Parameters Selections
- **Activation Function:** **SIREN** (Sinusoidal) is often preferred over ReLU for better capturing high-frequency details and gradients.
- **Positional Encoding:** Using sinusoidal features (like in NeRF) helps the network learn high-frequency details.
- **$\lambda_{\text{eik}}$:** The weight for the Eikonal loss, typically $10^{-1}$ to $10^{-2}$.
- **Latent Code Size:** Usually 128-512 for complex shape spaces.

## 6. Complexity
- **Inference:** $O(L \cdot W^2)$ per point, where $L$ is number of layers and $W$ is layer width. Since points are independent, this is highly parallelizable on GPUs.
- **Surface Extraction:** $O(V \cdot \text{Inference})$ where $V$ is number of grid cells for Marching Cubes.
- **Training:** $O(\text{epochs} \cdot \text{points} \cdot \text{Inference})$.

## 7. Usage
- **3D Shape Compression:** Representing complex geometry with a small number of network weights.
- **Shape Completion:** Inferring missing parts of a scan from a learned shape prior.
- **Neural Rendering:** Integrated with volumetric rendering (e.g., NeuS, VolSDF) for 3D reconstruction from images.

## 9. References
1.  Park, J. J., et al. (2019). *DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation*. CVPR.
2.  Sitzmann, V., et al. (2020). *Implicit Neural Representations with Periodic Activation Functions*. NeurIPS.
3.  Gropp, A., et al. (2020). *Implicit Geometric Regularization for Learning Shapes*. ICML.
