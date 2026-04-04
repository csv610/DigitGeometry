# Digital Geometry Library

A comprehensive modular Python library for digital geometry algorithms, including rasterization, distance transforms, morphological operations, voxel processing, topology analysis, and more.

## Installation

```bash
pip install -e .
```

## Modules (21 modules, 170+ functions)

| Module | Description |
|--------|-------------|
| `raster` | Line and circle drawing (Bresenham, Wu, supercover, scanline) |
| `distance` | Distance transforms (Manhattan, Euclidean, Chamfer, Geodesic, Hausdorff) |
| `morphology` | Morphological operations (dilate, erode, opening, closing, skeleton, top-hat) |
| `topology` | Connected components, homology persistence, surface curvature, 3D |
| `pathfinding` | A* pathfinding, fast marching method |
| `curves` | Curvature, smoothing, polygon ops, DSLS certification |
| `contours` | Flood fill, boundary tracing, Suzuki contours, RLE, Freeman chain |
| `edge` | Edge detection (Canny, Sobel, Prewitt, Roberts, Laplacian) |
| `features` | Feature detection (Harris, SUSAN, FAST, Shi-Tomasi corners) |
| `transforms` | Affine transforms, rotation, scaling, resampling (bilinear, bicubic) |
| `descriptors` | Hu moments, Zernike moments, Fourier descriptors, shape context, Hough |
| `pyramids` | Gaussian and Laplacian pyramids |
| `segmentation` | Graph cuts, watershed transform |
| `spatial` | Quadtree, Octree, REEB graph, SDF, jump flooding |
| `shape` | Polygon operations (area, centroid, perimeter), shape metrics |
| `geometry3d` | 3D normals, curvature, plane fitting |
| `volume3d` | Marching cubes/squares, thinning, medial axis, 3D operations |
| `voxel` | Comprehensive voxel processing (80+ functions) |
| `curves` | Additional curve operations |
| `utils` | Gradient, divergence, Laplacian, skeleton tools |

## Voxel Module (Highlights)

The `voxel` module provides extensive voxel-based geometry algorithms:

- **Neighbor utilities**: 6/18/26-connectivity
- **Topology**: Border/edge/vertex classification, manifold detection
- **Voxelization**: Surface/converts mesh to voxels
- **Surface extraction**: Marching cubes, Surface Nets, Dual Contouring
- **Operations**: Dilate, erode, hole filling, morphological
- **SDF**: 3D signed distance fields
- **Skeleton**: Medial axis, endpoint/junction detection
- **Octree**: Sparse and dense conversions
- **Ray tracing**: Voxel intersection, volume raymarching
- **Compression**: Epitomes, multi-resolution pyramids
- **Editing**: Euler operators for topological editing
- **Analysis**: Moments, Euler number, connectivity count

## Usage

```python
from digital_geometry import bresenham_line, erode, morph_opening, canny, harris_corner

# Draw a line
line = bresenham_line((0, 0), (10, 10))

# Morphological operations
grid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
eroded = erode(grid)
opened = morph_opening(grid)

# Edge detection
edges = canny(grid)

# Corner detection
corners = harris_corner(grid)

# Voxel operations
from digital_geometry import voxelize_triangle_mesh, voxel_sdf_3d, merge_voxels
volume = voxelize_triangle_mesh(vertices, triangles, resolution=32)
sdf = voxel_sdf_3d(volume)
merged = merge_voxels(volume, level=2)
```

## Testing

```bash
pytest tests/
```

## License

MIT
