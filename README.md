# Digital Geometry Library

A comprehensive Python library for digital geometry algorithms, including rasterization, distance transforms, morphological operations, voxel processing, topology analysis, and more.

## Quick Start

```bash
# Install
pip install -e .

# Run tests
pytest tests/

# Import functions
from digital_geometry import bresenham_line, canny, harris_corner, voxel_sdf_3d
```

## Features

- **170+ algorithms** across 45 modules
- **240+ tests** - all passing
- **Comprehensive documentation** with textbook

## Modules Overview

| Category | Modules |
|----------|---------|
| Core Operations | `raster`, `distance`, `morphology`, `edge`, `features` |
| Analysis | `contours`, `curves`, `shape`, `descriptors`, `geometry3d` |
| Topology | `topology`, `topology_basic`, `topology_persistent`, `volume3d` |
| Spatial | `spatial`, `pathfinding`, `pyramids`, `segmentation` |
| 3D/Volume | `voxel`, `voxel_analysis`, `voxel_sdf`, `voxel_render`, `voxel_topology`, `volume_isosurface` |
| Advanced | `voxel_octree`, `voxel_hashing`, `voxel_semantic`, `voxel_neural`, `registration` |

## Testing

All **243 tests** pass:

```bash
pytest tests/ -v
```

### Test Modules

| Test File | Coverage |
|-----------|----------|
| `test_raster.py` | Bresenham, Wu, midpoint circle |
| `test_distance.py` | Manhattan, Euclidean, Chamfer, geodesic |
| `test_morphology.py` | Dilation, erosion, opening, closing, skeleton |
| `test_topology.py` | Connected components, 3D topology |
| `test_edge.py` | Sobel, Canny, Laplacian, Gaussian |
| `test_features.py` | Harris, SUSAN, FAST, Shi-Tomasi |
| `test_transforms.py` | Affine, rotate, scale, resampling |
| `test_contours.py` | Flood fill, boundary tracing, RLE |
| `test_pathfinding.py` | A*, fast marching |
| `test_curves.py` | Convex hull, curvature, Douglas-Peucker |
| `test_shape.py` | Area, perimeter, circularity |
| `test_descriptors.py` | Hu moments, Zernike, Fourier |
| `test_segmentation.py` | Graph cuts, watershed |
| `test_spatial.py` | Quadtree, octree, SDF |
| `test_pyramids.py` | Gaussian, Laplacian pyramids |
| `test_geometry3d.py` | Normals, plane fitting |
| `test_volume3d.py` | Marching cubes, thinning |
| `test_voxel.py` | Voxelization, SDF, ray tracing |
| `test_registration.py` | ICP algorithm |
| `test_voxel_semantic.py` | Semantic voxel grids |
| `test_voxel_neural.py` | Feature volumes, neural SDF |
| `test_voxel_hashing.py` | Hash-based indexing |
| `test_voxel_octree.py` | Adaptive octrees |

## Documentation

### Python API Documentation

Each module includes comprehensive docstrings:

```python
from digital_geometry import canny

help(canny)  # Shows parameters, returns, examples
```

### Textbook

A comprehensive undergraduate textbook is available:

**File**: `digital_geometry_comprehensive.md`

**Chapters**:
1. The Digital World
2. Topology of Digital Images
3. Digitization and Grid Representations
4. Distance and Metrics
5. Mathematical Morphology
6. Edge Detection

**Features**:
- Written for independent study
- Mathematical proofs
- Python implementations
- Exercise sets (theory + programming + projects)
- Application-focused

## Usage Examples

### Basic Operations

```python
from digital_geometry import bresenham_line, erode, morph_opening

# Draw a line
line = bresenham_line((0, 0), (10, 10))

# Morphological operations
grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
eroded = erode(grid)
opened = morph_opening(grid)
```

### Edge Detection

```python
from digital_geometry import canny, sobel

image = load_image("photo.png")
edges = canny(image, low=50, high=150)
gradient, direction = sobel(image)
```

### 3D Processing

```python
from digital_geometry import voxelize_triangle_mesh, voxel_sdf_3d, merge_voxels

# Voxelize mesh
volume = voxelize_triangle_mesh(vertices, triangles, resolution=32)

# Compute SDF
sdf = voxel_sdf_3d(volume)

# Merge voxels
merged = merge_voxels(volume, level=2)
```

## License

MIT