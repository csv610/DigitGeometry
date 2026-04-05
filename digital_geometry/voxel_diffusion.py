"""Voxel diffusion for understanding 3D geometry and generation."""

import math
import random
from typing import Optional, Tuple, List, Dict

from digital_geometry.voxel_core import NEIGHBOR_6, NEIGHBOR_26


def voxel_heat_diffusion(volume, iterations=10, dt=0.25):
    """Apply heat diffusion on binary voxel volume."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    u = [[list(row) for row in layer] for layer in volume]
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                u[z][y][x] = float(volume[z][y][x])

    for _ in range(iterations):
        u_new = [[[0.0] * width for _ in range(height)] for _ in range(depth)]

        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    laplacian = 0.0
                    count = 0
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            laplacian += u[nz][ny][nx] - u[z][y][x]
                            count += 1
                    if count > 0:
                        u_new[z][y][x] = u[z][y][x] + dt * laplacian

        u = u_new

    return u


def voxel_anisotropic_diffusion(volume, iterations=5, k=1.0):
    """Apply anisotropic diffusion (Perona-Malik) on voxel volume."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    u = [[list(row) for row in layer] for layer in volume]

    for _ in range(iterations):
        u_new = [
            [[u[z][y][x] for x in range(width)] for y in range(height)]
            for z in range(depth)
        ]

        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    grad = 0.0
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            diff = u[nz][ny][nx] - u[z][y][x]
                            cond = math.exp(-(diff**2) / (k**2))
                            grad += cond * diff

                    u_new[z][y][x] = u[z][y][x] + 0.25 * grad

        u = u_new

    return u


def compute_diffusion_distance(volume, source, radius=10):
    """Compute diffusion distance from a source voxel."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    dist = [[[float("inf")] * width for _ in range(height)] for _ in range(depth)]
    dist[source[2]][source[1]][source[0]] = 0.0

    queue = [source]

    while queue:
        x, y, z = queue.pop(0)
        d = dist[z][y][x]

        if d >= radius:
            continue

        for dx, dy, dz in NEIGHBOR_6:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                if volume[nz][ny][nx] == 1 and dist[nz][ny][nx] == float("inf"):
                    dist[nz][ny][nx] = d + 1
                    queue.append((nx, ny, nz))

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if dist[z][y][x] == float("inf"):
                    dist[z][y][x] = radius

    return dist


def compute_heat_kernel_signature(volume, sources, t_values=[1, 2, 4, 8]):
    """Compute heat kernel signature at multiple time scales."""
    signatures = {}

    for source in sources:
        diffusion = voxel_heat_diffusion(volume, iterations=max(t_values) * 2)
        signature = [diffusion[source[2]][source[1]][source[0]] for _ in t_values]
        signatures[source] = signature

    return signatures


def voxel_curvature_diffusion(volume, iterations=20):
    """Estimate mean curvature through diffusion."""
    smoothed = voxel_heat_diffusion(volume, iterations=iterations)

    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    curvature = [[[0.0] * width for _ in range(height)] for _ in range(depth)]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue

                laplacian = 0.0
                count = 0
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        laplacian += smoothed[nz][ny][nx] - smoothed[z][y][x]
                        count += 1

                if count > 0:
                    curvature[z][y][x] = laplacian / count

    return curvature


def diffusion_boundary_detection(volume, threshold=0.1):
    """Detect boundaries using diffusion."""
    smoothed = voxel_heat_diffusion(volume, iterations=5)

    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    boundary = [[[0] * width for _ in range(height)] for _ in range(depth)]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    continue

                max_grad = 0.0
                for dx, dy, dz in NEIGHBOR_6:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                        grad = abs(smoothed[nz][ny][nx] - smoothed[z][y][x])
                        max_grad = max(max_grad, grad)

                if max_grad > threshold:
                    boundary[z][y][x] = 1

    return boundary


def voxel_geodesic_diffusion(volume, seeds, iterations=50):
    """Compute geodesic distance using heat method."""
    depth = len(volume)
    height = len(volume[0])
    width = len(volume[0][0])

    u = [[[0.0] * width for _ in range(height)] for _ in range(depth)]
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z][y][x] == 0:
                    u[z][y][x] = 0.0
                else:
                    u[z][y][x] = 1.0

    for seed in seeds:
        u[seed[2]][seed[1]][seed[0]] = 0.0

    for _ in range(iterations):
        u_new = [[[0.0] * width for _ in range(height)] for _ in range(depth)]

        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if volume[z][y][x] == 0:
                        continue

                    avg = 0.0
                    count = 0
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            if volume[nz][ny][nx] == 1:
                                avg += u[nz][ny][nx]
                                count += 1

                    if count > 0:
                        u_new[z][y][x] = avg / count

        u = u_new

    return u


class VoxelDiffusionConfig:
    """Configuration for voxel diffusion model."""

    def __init__(
        self,
        voxel_size: int = 32,
        latent_channels: int = 64,
        num_classes: int = 2,
        num_timesteps: int = 1000,
        beta_start: float = 0.0001,
        beta_end: float = 0.02,
        hidden_dims: List[int] = None,
    ):
        self.voxel_size = voxel_size
        self.latent_channels = latent_channels
        self.num_classes = num_classes
        self.num_timesteps = num_timesteps
        self.beta_start = beta_start
        self.beta_end = beta_end
        self.hidden_dims = hidden_dims or [64, 128, 256, 512]


def cosine_beta_schedule(timesteps: int, s: float = 0.008) -> List[float]:
    """Cosine schedule for diffusion beta values."""
    steps = timesteps + 1
    x = [i / timesteps for i in range(steps)]
    alphas_cumprod = [
        math.cos(((x[i] + s) / (1 + s) * math.pi * 0.5)) ** 2 for i in range(steps)
    ]
    alphas_cumprod = [a / alphas_cumprod[0] for a in alphas_cumprod]
    betas = [1 - (alphas_cumprod[i + 1] / alphas_cumprod[i]) for i in range(timesteps)]
    return [max(0, min(0.999, b)) for b in betas]


def linear_beta_schedule(
    timesteps: int, beta_start: float = 0.0001, beta_end: float = 0.02
) -> List[float]:
    """Linear schedule for diffusion beta values."""
    return [
        beta_start + (beta_end - beta_start) * i / timesteps for i in range(timesteps)
    ]


class SimpleVoxelDiffusion:
    """Simplified voxel diffusion model for 3D shape generation.

    Uses discrete diffusion for binary voxel grids (occupied/empty).
    """

    def __init__(self, config: Optional[VoxelDiffusionConfig] = None):
        self.config = config or VoxelDiffusionConfig()
        self.beta_schedule = linear_beta_schedule(
            self.config.num_timesteps, self.config.beta_start, self.config.beta_end
        )
        self.alphas = [1.0 - b for b in self.beta_schedule]
        self.alphas_cumprod = []
        prod = 1.0
        for a in self.alphas:
            prod *= a
            self.alphas_cumprod.append(prod)

    def add_noise(
        self, voxels: List[List[List[int]]], t: int
    ) -> Tuple[List[List[List[int]]], int]:
        """Add noise to voxel grid at timestep t (forward process)."""
        if t == 0:
            return voxels, 0

        depth = len(voxels)
        height = len(voxels[0])
        width = len(voxels[0][0])

        noise_prob = 1.0 - self.alphas_cumprod[t - 1]

        noisy = []
        for z in range(depth):
            layer = []
            for y in range(height):
                row = []
                for x in range(width):
                    if random.random() < noise_prob:
                        row.append(1 - voxels[z][y][x])
                    else:
                        row.append(voxels[z][y][x])
                layer.append(row)
            noisy.append(layer)

        return noisy, t

    def denoise_step(
        self, noisy_voxels: List[List[List[int]]], t: int
    ) -> List[List[List[int]]]:
        """Single denoising step (simplified reverse process)."""
        if t == 0:
            return noisy_voxels

        depth = len(noisy_voxels)
        height = len(noisy_voxels[0])
        width = len(noisy_voxels[0][0])

        denoised = []
        noise_level = t / self.config.num_timesteps

        for z in range(depth):
            layer = []
            for y in range(height):
                row = []
                for x in range(width):
                    prob = noisy_voxels[z][y][x]

                    local_density = self._compute_local_density(noisy_voxels, x, y, z)

                    pred = prob * (1 - noise_level) + local_density * noise_level

                    if pred > 0.5:
                        row.append(1)
                    else:
                        row.append(0)
                layer.append(row)
            denoised.append(layer)

        return denoised

    def _compute_local_density(self, voxels, x, y, z) -> float:
        """Compute local density around a voxel."""
        depth = len(voxels)
        height = len(voxels[0])
        width = len(voxels[0][0])

        count = 0
        total = 0

        for dx, dy, dz in NEIGHBOR_6:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                count += voxels[nz][ny][nx]
                total += 1

        return count / max(total, 1)

    def generate(
        self, num_steps: int = None, initial_noise=None
    ) -> List[List[List[int]]]:
        """Generate a voxel shape from random noise."""
        num_steps = num_steps or self.config.num_timesteps // 10

        if initial_noise is None:
            depth = self.config.voxel_size
            height = self.config.voxel_size
            width = self.config.voxel_size

            voxels = [
                [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
                for _ in range(depth)
            ]
        else:
            voxels = initial_noise

        for t in range(num_steps, 0, -1):
            voxels = self.denoise_step(voxels, t)

        return voxels

    def interpolate(
        self,
        voxels1: List[List[List[int]]],
        voxels2: List[List[List[int]]],
        alpha: float = 0.5,
    ) -> List[List[List[int]]]:
        """Interpolate between two voxel grids."""
        depth = len(voxels1)
        height = len(voxels1[0])
        width = len(voxels1[0][0])

        result = []
        for z in range(depth):
            layer = []
            for y in range(height):
                row = []
                for x in range(width):
                    val = voxels1[z][y][x] * (1 - alpha) + voxels2[z][y][x] * alpha
                    row.append(1 if val > 0.5 else 0)
                layer.append(row)
            result.append(layer)

        return result


class VoxelDiffusionModel:
    """Neural network-based voxel diffusion model placeholder."""

    def __init__(self, config: Optional[VoxelDiffusionConfig] = None):
        self.config = config or VoxelDiffusionConfig()
        self.noise_schedule = cosine_beta_schedule(self.config.num_timesteps)


def create_sphere_voxel(
    center: Tuple[int, int, int], radius: int, size: int
) -> List[List[List[int]]]:
    """Create a spherical voxel shape."""
    cx, cy, cz = center
    voxels = [[[0] * size for _ in range(size)] for _ in range(size)]

    for z in range(size):
        for y in range(size):
            for x in range(size):
                if (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2 <= radius**2:
                    voxels[z][y][x] = 1

    return voxels


def create_box_voxel(
    min_bound: Tuple[int, int, int], max_bound: Tuple[int, int, int], size: int
) -> List[List[List[int]]]:
    """Create a box-shaped voxel volume."""
    x1, y1, z1 = min_bound
    x2, y2, z2 = max_bound

    voxels = [[[0] * size for _ in range(size)] for _ in range(size)]

    for z in range(size):
        for y in range(size):
            for x in range(size):
                if x1 <= x < x2 and y1 <= y < y2 and z1 <= z < z2:
                    voxels[z][y][x] = 1

    return voxels


def create_torus_voxel(
    major_radius: int, minor_radius: int, center: Tuple[int, int, int], size: int
) -> List[List[List[int]]]:
    """Create a torus-shaped voxel volume."""
    cx, cy, cz = center
    voxels = [[[0] * size for _ in range(size)] for _ in range(size)]

    for z in range(size):
        for y in range(size):
            for x in range(size):
                dx, dy, dz = x - cx, y - cy, z - cz
                dist_xy = math.sqrt(dx**2 + dy**2)
                if (
                    abs(dist_xy - major_radius) <= minor_radius
                    and dz**2 <= minor_radius**2
                ):
                    voxels[z][y][x] = 1

    return voxels


def augment_voxel_with_noise(
    voxels: List[List[List[int]]], noise_level: float = 0.1
) -> List[List[List[int]]]:
    """Add random noise to voxel grid."""
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    result = []
    for z in range(depth):
        layer = []
        for y in range(height):
            row = []
            for x in range(width):
                if random.random() < noise_level:
                    row.append(1 - voxels[z][y][x])
                else:
                    row.append(voxels[z][y][x])
            layer.append(row)
        result.append(layer)

    return result


def compute_voxel_iou(
    voxels1: List[List[List[int]]], voxels2: List[List[List[int]]]
) -> float:
    """Compute Intersection over Union between two voxel grids."""
    depth = len(voxels1)
    height = len(voxels1[0])
    width = len(voxels1[0][0])

    intersection = 0
    union = 0

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                v1 = voxels1[z][y][x]
                v2 = voxels2[z][y][x]

                if v1 == 1 or v2 == 1:
                    union += 1
                if v1 == 1 and v2 == 1:
                    intersection += 1

    return intersection / max(union, 1)


def voxel_to_point_cloud(
    voxels: List[List[List[int]]], resolution: int = 1024
) -> List[Tuple[float, float, float]]:
    """Convert voxel grid to point cloud."""
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    points = []

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if voxels[z][y][x] == 1:
                    px = (x + 0.5) / width - 0.5
                    py = (y + 0.5) / height - 0.5
                    pz = (z + 0.5) / depth - 0.5
                    points.append((px, py, pz))

    if len(points) > resolution:
        return random.sample(points, resolution)

    return points


class LatentVoxelDiffusion:
    """Latent diffusion model for voxel generation."""

    def __init__(self, config: Optional[VoxelDiffusionConfig] = None):
        self.config = config or VoxelDiffusionConfig()
        self.diffusion = SimpleVoxelDiffusion(config)

    def encode(self, voxels: List[List[List[int]]]) -> List[float]:
        """Encode voxel grid to latent representation."""
        depth = len(voxels)
        height = len(voxels[0])
        width = len(voxels[0][0])

        density = sum(sum(row) for layer in voxels for row in layer) / (
            depth * height * width
        )

        centroid = self._compute_centroid(voxels)

        latent = [density]
        latent.extend(centroid)

        return (
            latent[: self.config.latent_channels]
            if len(latent) < self.config.latent_channels
            else latent
        )

    def decode(self, latent: List[float]) -> List[List[List[int]]]:
        """Decode latent representation to voxel grid."""
        size = self.config.voxel_size
        center = (size // 2, size // 2, size // 2)

        if len(latent) >= 4:
            density = latent[0]
            radius = int(size * density * 0.3)
            radius = max(2, min(radius, size // 2 - 1))

            return create_sphere_voxel(center, radius, size)

        return create_sphere_voxel(center, size // 4, size)

    def _compute_centroid(
        self, voxels: List[List[List[int]]]
    ) -> Tuple[float, float, float]:
        """Compute centroid of voxel mass."""
        depth = len(voxels)
        height = len(voxels[0])
        width = len(voxels[0][0])

        cx = cy = cz = 0
        count = 0

        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if voxels[z][y][x] == 1:
                        cx += x
                        cy += y
                        cz += z
                        count += 1

        if count == 0:
            return (0.0, 0.0, 0.0)

        return (
            cx / count / width - 0.5,
            cy / count / height - 0.5,
            cz / count / depth - 0.5,
        )

    def generate_variations(
        self, voxels: List[List[List[int]]], num_variations: int = 4
    ) -> List[List[List[List[int]]]]:
        """Generate variations of an input voxel shape."""
        latent = self.encode(voxels)

        variations = []
        for i in range(num_variations):
            noisy_latent = [l + random.gauss(0, 0.1) for l in latent]
            variation = self.decode(noisy_latent)

            variation = self.diffusion.denoise_step(variation, t=5)

            variations.append(variation)

        return variations


def extract_voxel_slices(
    voxels: List[List[List[int]]],
    axis: str = "z",
    output_dir: str = None,
    prefix: str = "slice",
):
    """Extract 2D slices from 3D voxel grid.

    Args:
        voxels: 3D binary voxel grid
        axis: 'x', 'y', or 'z' for slice direction
        output_dir: Directory to save PNG files (None = don't save)
        prefix: Filename prefix for saved slices

    Returns:
        List of slice images (2D arrays) or filenames if output_dir provided
    """
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    slices = []
    filenames = []

    if axis == "z":
        for z in range(depth):
            slice_2d = voxels[z]
            slices.append(slice_2d)
            if output_dir:
                import os

                filepath = os.path.join(output_dir, f"{prefix}_z_{z:03d}.png")
                filenames.append(filepath)
    elif axis == "y":
        for y in range(height):
            slice_2d = [voxels[z][y] for z in range(depth)]
            slices.append(slice_2d)
            if output_dir:
                filepath = os.path.join(output_dir, f"{prefix}_y_{y:03d}.png")
                filenames.append(filepath)
    elif axis == "x":
        for x in range(width):
            slice_2d = [[voxels[z][y][x] for y in range(height)] for z in range(depth)]
            slices.append(slice_2d)
            if output_dir:
                filepath = os.path.join(output_dir, f"{prefix}_x_{x:03d}.png")
                filenames.append(filepath)

    return slices if not output_dir else filenames


def save_slice_as_png(slice_2d: List[List[int]], filepath: str, scale: int = 1) -> None:
    """Save a 2D slice as PNG image.

    Args:
        slice_2d: 2D array of voxel values (0 or 1)
        filepath: Output file path
        scale: Upscale factor for higher resolution
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("PIL (Pillow) required. Install: pip install Pillow")

    height = len(slice_2d)
    width = len(slice_2d[0]) if height > 0 else 0

    if scale > 1:
        width *= scale
        height *= scale

    img = Image.new("L", (width, height), color=0)

    for y in range(height):
        for x in range(width):
            sx = x // scale if scale > 1 else x
            sy = y // scale if scale > 1 else y
            pixel = slice_2d[sy][sx] * 255
            img.putpixel((x, y), pixel)

    img.save(filepath)


def extract_and_save_slices(
    voxels,
    output_dir,
    axis="z",
    prefix="slice",
    scale=4,
    num_slices=None,
):
    """Extract and save all slices as PNG images.

    Args:
        voxels: 3D binary voxel grid
        output_dir: Directory to save PNG files
        axis: 'x', 'y', or 'z' for slice direction
        prefix: Filename prefix
        scale: Upscale factor

    Returns:
        List of saved file paths
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    saved_files = []

    if axis == "z":
        for z in range(depth):
            filepath = os.path.join(output_dir, f"{prefix}_z_{z:03d}.png")
            save_slice_as_png(voxels[z], filepath, scale)
            saved_files.append(filepath)
    elif axis == "y":
        for y in range(height):
            slice_2d = [voxels[z][y] for z in range(depth)]
            filepath = os.path.join(output_dir, f"{prefix}_y_{y:03d}.png")
            save_slice_as_png(slice_2d, filepath, scale)
            saved_files.append(filepath)
    elif axis == "x":
        for x in range(width):
            slice_2d = [[voxels[z][y][x] for y in range(height)] for z in range(depth)]
            filepath = os.path.join(output_dir, f"{prefix}_x_{x:03d}.png")
            save_slice_as_png(slice_2d, filepath, scale)
            saved_files.append(filepath)

    return saved_files


def visualize_voxel_slice(slice_2d: List[List[int]]) -> str:
    """Create ASCII visualization of a 2D slice.

    Args:
        slice_2d: 2D array of voxel values

    Returns:
        ASCII art string
    """
    lines = []
    for row in slice_2d:
        line = "".join("█" if pixel else " " for pixel in row)
        lines.append(line)
    return "\n".join(lines)


def create_colored_voxel_volume(voxels: List[List[List[int]]]):
    """Create RGB voxel volume for visualization.

    Args:
        voxels: Binary voxel grid

    Returns:
        RGB voxel grid
    """
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    rgb = []
    for z in range(depth):
        layer = []
        for y in range(height):
            row = []
            for x in range(width):
                if voxels[z][y][x] == 1:
                    ratio_z = z / depth
                    r = int(255 * ratio_z)
                    g = int(255 * (1 - abs(ratio_z - 0.5) * 2))
                    b = int(255 * (1 - ratio_z))
                    row.append((r, g, b))
                else:
                    row.append((0, 0, 0))
            layer.append(row)
        rgb.append(layer)

    return rgb


def extract_slices_along_direction(
    voxels: List[List[List[int]]],
    direction: Tuple[float, float, float] = (0, 0, 1),
    num_slices: int = None,
    output_dir: str = None,
    prefix: str = "slice",
) -> List[List[List[int]]]:
    """Extract 2D slices along arbitrary direction vector.

    Args:
        voxels: 3D binary voxel grid
        direction: Direction vector (dx, dy, dz) - will be normalized
        num_slices: Number of slices to extract (default: volume size)
        output_dir: Directory to save PNG files (None = don't save)
        prefix: Filename prefix for saved slices

    Returns:
        List of 2D slices (each is 2D array)
    """
    import os

    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    dx, dy, dz = direction
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length == 0:
        raise ValueError("Direction vector cannot be zero")
    dx, dy, dz = dx / length, dy / length, dz / length

    if num_slices is None:
        num_slices = max(depth, height, width)

    step = 1.0

    slices = []
    filenames = []

    for i in range(num_slices):
        proj_value = i * step

        slice_array = [[0] * width for _ in range(height)]

        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if voxels[z][y][x] == 1:
                        proj = x * dx + y * dy + z * dz
                        if abs(proj - proj_value) < step / 2:
                            if 0 <= y < height and 0 <= x < width:
                                slice_array[y][x] = 1

        slices.append(slice_array)

        if output_dir:
            filepath = os.path.join(output_dir, f"{prefix}_{i:03d}.png")
            try:
                save_slice_as_png(slice_array, filepath, scale=4)
                filenames.append(filepath)
            except Exception:
                pass

    return slices if not output_dir else filenames


def extract_orthogonal_slices(
    voxels: List[List[List[int]]],
    normal: Tuple[float, float, float] = (0, 0, 1),
    output_dir: str = None,
    prefix: str = "slice",
) -> List[List[List[int]]]:
    """Extract slices perpendicular to given normal direction.

    This is similar to extract_slices_along_direction but uses a normal
    vector to define the viewing direction.

    Args:
        voxels: 3D binary voxel grid
        normal: Normal vector defining slice plane direction
        output_dir: Directory to save PNG files
        prefix: Filename prefix

    Returns:
        List of 2D slices
    """
    return extract_slices_along_direction(
        voxels, normal, output_dir=output_dir, prefix=prefix
    )


def rotate_voxels_by_direction(
    voxels: List[List[List[int]]],
    direction: Tuple[float, float, float],
) -> List[List[List[int]]]:
    """Rotate voxel grid so given direction aligns with Z-axis.

    Args:
        voxels: Binary voxel grid
        direction: Target direction vector

    Returns:
        Rotated voxel grid
    """
    import numpy as np

    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    dx, dy, dz = direction
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length == 0:
        return voxels
    dx, dy, dz = dx / length, dy / length, dz / length

    if abs(dz - 1) < 0.01:
        return voxels

    pitch = math.acos(dz)
    yaw = math.atan2(dy, dx)

    cx, cy, cz = width // 2, height // 2, depth // 2

    rotated = [[[0] * width for _ in range(height)] for _ in range(depth)]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if voxels[z][y][x] == 1:
                    nx = x - cx
                    ny = y - cy
                    nz = z - cz

                    cos_yaw, sin_yaw = math.cos(-yaw), math.sin(-yaw)
                    nx1 = nx * cos_yaw - ny * sin_yaw
                    ny1 = nx * sin_yaw + ny * cos_yaw
                    nz1 = nz

                    cos_pitch, sin_pitch = math.cos(-pitch), math.sin(-pitch)
                    nx2 = nx1
                    ny2 = ny1 * cos_pitch - nz1 * sin_pitch
                    nz2 = ny1 * sin_pitch + nz1 * cos_pitch

                    rx = int(nx2 + cx)
                    ry = int(ny2 + cy)
                    rz = int(nz2 + cz)

                    if 0 <= rx < width and 0 <= ry < height and 0 <= rz < depth:
                        rotated[rz][ry][rx] = 1

    return rotated


def save_voxel_volume_image(
    voxels: List[List[List[int]]],
    filepath: str,
    view: str = "orthographic",
    axis: str = "z",
):
    """Save voxel volume as a single image (projection).

    Args:
        voxels: Binary voxel grid
        filepath: Output file path
        view: 'orthographic' or 'max_projection'
        axis: Projection axis ('x', 'y', or 'z')
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("PIL (Pillow) required. Install: pip install Pillow")

    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    if axis == "z":
        proj_h, proj_w = height, width
    elif axis == "y":
        proj_h, proj_w = depth, width
    else:
        proj_h, proj_w = depth, height

    img = Image.new("RGB", (proj_w, proj_h), color=(0, 0, 0))

    pixels = img.load()

    for y in range(proj_h):
        for x in range(proj_w):
            if axis == "z":
                val = voxels[min(y, height - 1)][min(x, width - 1)]
            elif axis == "y":
                val = voxels[min(y, depth - 1)][min(x, width - 1)]
            else:
                val = voxels[min(y, depth - 1)][min(x, height - 1)]

            if val == 1:
                pixels[x, y] = (255, 255, 255)

    img.save(filepath)


def build_voxel_graph(
    voxels: List[List[List[int]]],
) -> Dict[Tuple[int, int, int], List[Tuple[int, int, int]]]:
    """Build adjacency graph from voxel grid.

    Args:
        voxels: Binary voxel grid

    Returns:
        Dictionary mapping voxel coords to neighbor coords
    """
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    graph = {}
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if voxels[z][y][x] == 1:
                    neighbors = []
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            if voxels[nz][ny][nx] == 1:
                                neighbors.append((nx, ny, nz))
                    graph[(x, y, z)] = neighbors

    return graph


def compute_discrete_curvature_vertex(
    voxels: List[List[List[int]]], vertex: Tuple[int, int, int]
) -> float:
    """Compute discrete curvature at a voxel vertex.

    Uses angle deficit method for 3D grid.

    Args:
        voxels: Binary voxel grid
        vertex: (x, y, z) coordinates

    Returns:
        Curvature value
    """
    x, y, z = vertex
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    if not (0 <= x < width and 0 <= y < height and 0 <= z < depth):
        return 0.0

    neighbors_6 = []
    for dx, dy, dz in NEIGHBOR_6:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
            if voxels[nz][ny][nx] == 1:
                neighbors_6.append((nx, ny, nz))

    k = len(neighbors_6)

    if k == 0:
        return 0.0

    curvature = 2.0 * math.pi * (1.0 - k / 6.0)

    return curvature


def compute_edge_curvature(
    voxels: List[List[List[int]]],
    edge: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
) -> float:
    """Compute discrete curvature on edge (combinatorial Ricci flow).

    Args:
        voxels: Binary voxel grid
        edge: Tuple of two voxel coordinates

    Returns:
        Edge curvature value
    """
    v1, v2 = edge
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    if not (0 <= x1 < width and 0 <= y1 < height and 0 <= z1 < depth):
        return 0.0
    if not (0 <= x2 < width and 0 <= y2 < height and 0 <= z2 < depth):
        return 0.0

    if voxels[z1][y1][x1] != 1 or voxels[z2][y2][x2] != 1:
        return 0.0

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    cz = (z1 + z2) // 2

    n1 = compute_discrete_curvature_vertex(voxels, v1)
    n2 = compute_discrete_curvature_vertex(voxels, v2)

    mid_curvature = 0.0
    if 0 <= cx < width and 0 <= cy < height and 0 <= cz < depth:
        if voxels[cz][cy][cx] == 1:
            mid_curvature = compute_discrete_curvature_vertex(voxels, (cx, cy, cz))

    edge_curvature = (n1 + n2 + mid_curvature) / 3.0

    return edge_curvature


class RicciFlowConfig:
    """Configuration for discrete Ricci flow."""

    def __init__(
        self,
        num_iterations: int = 100,
        step_size: float = 0.01,
        convergence_threshold: float = 1e-6,
    ):
        self.num_iterations = num_iterations
        self.step_size = step_size
        self.convergence_threshold = convergence_threshold


def ricci_flow_voxel(
    voxels: List[List[List[int]]],
    config: Optional[RicciFlowConfig] = None,
    return_history: bool = False,
):
    """Apply discrete Ricci flow on voxel model.

    Evolves edge weights to equalize curvature across the voxel graph.

    Args:
        voxels: Binary voxel grid
        config: Ricci flow configuration
        return_history: Whether to return iteration history

    Returns:
        Smoothed voxel grid
    """
    config = config or RicciFlowConfig()

    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    graph = build_voxel_graph(voxels)

    edges = []
    edge_weights = {}
    edge_curvatures = {}

    for v1, neighbors in graph.items():
        for v2 in neighbors:
            edge = (v1, v2) if v1 < v2 else (v2, v1)
            if edge not in edge_weights:
                edges.append(edge)
                edge_weights[edge] = 1.0

    history = []

    for iteration in range(config.num_iterations):
        for edge in edges:
            edge_curvatures[edge] = compute_edge_curvature(voxels, edge)

        total_curvature = sum(abs(edge_curvatures[e]) for e in edges)

        if total_curvature < config.convergence_threshold:
            break

        avg_curvature = total_curvature / len(edges) if edges else 0

        for edge in edges:
            delta = config.step_size * (edge_curvatures[edge] - avg_curvature)
            edge_weights[edge] = max(0.01, edge_weights[edge] - delta)

        history.append(
            {
                "iteration": iteration,
                "total_curvature": total_curvature,
                "avg_curvature": avg_curvature,
            }
        )

    smoothed = []
    for z in range(depth):
        layer = []
        for y in range(height):
            row = []
            for x in range(width):
                if voxels[z][y][x] == 1:
                    local_weight = 0.0
                    count = 0
                    for dx, dy, dz in NEIGHBOR_6:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
                            if voxels[nz][ny][nx] == 1:
                                edge = ((x, y, z), (nx, ny, nz))
                                edge = edge if edge[0] < edge[1] else (edge[1], edge[0])
                                if edge in edge_weights:
                                    local_weight += edge_weights[edge]
                                    count += 1

                    threshold = 0.5 * count if count > 0 else 0
                    row.append(1 if local_weight >= threshold else 0)
                else:
                    row.append(0)
            layer.append(row)
        smoothed.append(layer)

    if return_history:
        return smoothed, history

    return smoothed


def ricci_flow_boundary_extraction(
    voxels: List[List[List[int]]],
) -> List[Tuple[int, int, int]]:
    """Extract high-curvature boundary points using Ricci flow.

    Args:
        voxels: Binary voxel grid

    Returns:
        List of boundary voxel coordinates with high curvature
    """
    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    boundary_voxels = []

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if voxels[z][y][x] != 1:
                    continue

                curvature = compute_discrete_curvature_vertex(voxels, (x, y, z))

                if abs(curvature) > 0.5:
                    boundary_voxels.append((x, y, z))

    return boundary_voxels


def voxel_shape_signature_ricci(voxels: List[List[List[int]]]) -> Dict[str, float]:
    """Compute geometric signature using Ricci flow metrics.

    Args:
        voxels: Binary voxel grid

    Returns:
        Dictionary of geometric features
    """
    graph = build_voxel_graph(voxels)

    curvatures = []
    for vertex in graph:
        c = compute_discrete_curvature_vertex(voxels, vertex)
        curvatures.append(c)

    if not curvatures:
        return {"mean_curvature": 0.0, "var_curvature": 0.0, "total_curvature": 0.0}

    mean_c = sum(curvatures) / len(curvatures)
    var_c = sum((c - mean_c) ** 2 for c in curvatures) / len(curvatures)
    total_c = sum(abs(c) for c in curvatures)

    num_voxels = len(graph)
    num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    euler = num_voxels - num_edges

    return {
        "mean_curvature": mean_c,
        "var_curvature": var_c,
        "total_curvature": total_c,
        "euler_characteristic": euler,
        "num_voxels": num_voxels,
        "num_edges": num_edges,
    }


def simplify_voxel_shape_by_ricci(
    voxels: List[List[List[int]]],
    target_voxel_count: int,
):
    """Simplify voxel shape by collapsing low-curvature regions.

    Args:
        voxels: Binary voxel grid
        target_voxel_count: Target number of voxels in simplified shape

    Returns:
        Simplified voxel grid
    """
    graph = build_voxel_graph(voxels)

    curvatures = {}
    for vertex in graph:
        curvatures[vertex] = compute_discrete_curvature_vertex(voxels, vertex)

    depth = len(voxels)
    height = len(voxels[0])
    width = len(voxels[0][0])

    simplified = [[[0] * width for _ in range(height)] for _ in range(depth)]

    sorted_vertices = sorted(graph.keys(), key=lambda v: abs(curvatures[v]))

    for vertex in sorted_vertices[:target_voxel_count]:
        x, y, z = vertex
        simplified[z][y][x] = 1

    return simplified


def ricci_flow_smoothing_iterations(
    voxels: List[List[List[int]]],
    iterations: int = 10,
):
    """Apply multiple iterations of Ricci flow smoothing.

    Args:
        voxels: Binary voxel grid
        iterations: Number of smoothing iterations

    Returns:
        Smoothed voxel grid
    """
    current = voxels

    for i in range(iterations):
        config = RicciFlowConfig(num_iterations=20, step_size=0.05)
        current = ricci_flow_voxel(current, config)

    return current
