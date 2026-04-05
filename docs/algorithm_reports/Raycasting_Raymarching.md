# Raycasting and Raymarching

## 1. Overview
**Raycasting** and **Raymarching** are techniques for rendering 3D scenes by tracing the path of "rays" from the viewer's eye into the scene. While Raycasting typically solves for a direct intersection with geometry (like triangles), Raymarching iteratively steps along the ray until it hits a surface, making it ideal for implicit surfaces (SDFs) and volumetric data.

## 2. Definitions
- **Ray:** A mathematical line segment represented as $R(t) = \mathbf{O} + t\mathbf{D}$, where $\mathbf{O}$ is the origin, $\mathbf{D}$ is the direction vector, and $t \geq 0$.
- **Raycasting:** Finding the closest intersection of a ray with scene geometry (e.g., triangle meshes, spheres).
- **Raymarching:** An iterative technique to find the intersection of a ray with a surface defined implicitly (SDF) or to sample volumetric effects (fog, smoke).
- **Sphere Tracing:** A specific form of raymarching that uses SDF values to determine the maximum safe step size at each iteration.

## 3. Theory
### Raycasting
For each pixel in the image:
1.  Generate a ray from the eye through the pixel.
2.  Find the closest intersection of the ray with any object in the scene.
3.  Calculate the pixel color based on the object's material and lighting.

### Raymarching (Sphere Tracing)
Instead of an analytic intersection, the algorithm steps along the ray. At each step:
1.  Calculate the distance $d$ to the nearest object in the scene using the scene's SDF.
2.  Advance the ray by distance $d$. Since $d$ is the minimum distance to any surface, the ray is guaranteed not to "overstep" any geometry.
3.  Repeat until $d < \epsilon$ (hit) or the ray exceeds the maximum distance (miss).

## 4. Pseudo Code (Sphere Tracing)
```python
def sphere_trace(origin, direction):
    t = 0
    for i in range(MAX_STEPS):
        p = origin + t * direction
        dist = scene_sdf(p)
        if dist < EPSILON:
            return p, dist # Hit
        t += dist
        if t > MAX_DIST:
            break
    return None # Miss

def scene_sdf(p):
    # Example: SDF of a sphere at origin with radius R
    dist_sphere = p.norm() - R
    # Combine other objects with min (union)
    return min(dist_sphere, other_objects_sdf(p))
```

## 5. Parameters Selections
- **MAX_STEPS:** Number of iterations to perform before giving up (e.g., 64-256).
- **EPSILON:** The distance threshold for a "hit" (e.g., $10^{-3}$ to $10^{-6}$).
- **MAX_DIST:** Maximum distance the ray can travel (e.g., 100.0).
- **Step Size (Volumetric):** For non-SDF raymarching, a constant step size is used, which must be small enough to capture fine details but large enough for performance.

## 6. Complexity
- **Time Complexity:** $O(P \cdot S)$ where $P$ is the number of pixels and $S$ is the average number of steps per ray. The complexity also depends on the complexity of the `scene_sdf` evaluation.
- **Space Complexity:** $O(1)$ per ray, or $O(P)$ to store the final image.

## 7. Usage
- **Wolfenstein 3D Style Games:** Early uses of raycasting for 2D floor plans.
- **GPU Fragment Shaders:** Used to render complex mathematical shapes and procedural textures.
- **Volumetric Rendering:** Rendering fog, smoke, clouds, and medical CT/MRI data.
- **Demoscene:** Efficiently rendering intricate fractals (like the Mandelbulb) in real-time.

## 9. References
1.  Appel, A. (1968). *Some techniques for shading machine renderings of solids*. AFIPS.
2.  Hart, J. C. (1996). *Sphere tracing: a geometric method for the antialiased ray tracing of implicit surfaces*. The Visual Computer.
3.  Pharr, M., et al. (2016). *Physically Based Rendering: From Theory To Implementation*. Morgan Kaufmann.
