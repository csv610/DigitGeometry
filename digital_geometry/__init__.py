"""Digital Geometry Library - Modular version."""

# Rasterization
from digital_geometry.raster import (
    bresenham_line,
    midpoint_circle,
    wu_line,
    supercover_line_2d,
    supercover_line_3d,
    scanline_polygon_fill,
    SE_SQUARE_3X3,
    SE_CROSS_3X3,
)

# Distance transforms
from digital_geometry.distance import (
    manhattan_distance,
    euclidean_distance,
    manhattan_distance_transform,
    euclidean_distance_transform,
    chamfer_distance_transform,
    geodesic_distance_transform,
    voronoi_diagram,
    hausdorff_distance,
    earth_movers_distance,
)

# Morphology
from digital_geometry.morphology import (
    dilate,
    erode,
    morph_opening,
    morph_closing,
    morph_boundary,
    morphological_skeleton,
    geodesic_dilation,
    geodesic_erosion,
    create_square_se,
    morph_erode,
    white_tophat,
    black_tophat,
)

# Additional utils
from digital_geometry.utils import (
    discrete_gradient,
    discrete_divergence,
    discrete_laplacian_grid,
    detect_skeleton_endpoints,
    detect_skeleton_junctions,
    prune_skeleton,
    skeleton_to_graph,
)

# Additional utils
from digital_geometry.utils import (
    discrete_gradient,
    discrete_divergence,
    discrete_laplacian_grid,
    detect_skeleton_endpoints,
    detect_skeleton_junctions,
    prune_skeleton,
    skeleton_to_graph,
)

# Edge detection
from digital_geometry.edge import (
    canny,
    sobel,
    prewitt,
    roberts,
    laplacian_4,
    laplacian_8,
    gaussian_smooth,
)

# Feature detection
from digital_geometry.features import (
    harris_corner,
    shi_tomasi_corner,
    susan_corner,
    fast_corner,
    structure_tensor,
    compute_corner_response,
)

# Shape analysis
from digital_geometry.shape import (
    polygon_area,
    polygon_centroid,
    polygon_perimeter,
    point_to_polygon_distance,
    bounding_box,
    shape_circularity,
    shape_solidity,
    shape_aspect_ratio,
    shape_eccentricity,
    shape_extent,
    shape_compactness,
)

# 3D geometry
from digital_geometry.geometry3d import (
    estimate_surface_normals,
    compute_normals_cross_product,
    fit_plane_least_squares,
    estimate_curvature_2d,
)

# Voxel geometry - core utilities
from digital_geometry.voxel_core import (
    get_neighbors_6,
    get_neighbors_18,
    get_neighbors_26,
    voxel_euler_number,
    voxel_connectivity_count,
    voxel_coloring,
    voxel_separated,
)

# Voxel geometry - topology
from digital_geometry.voxel_topology import (
    classify_voxel_grid,
    find_voxel_borders,
    find_voxel_edges,
    find_voxel_vertices,
    is_voxel_surface_manifold,
    voxel_junction_count,
    voxel_endpoint_count,
    extract_boundary_faces,
    voxel_contour_3d,
)

# Voxel geometry - transforms
from digital_geometry.voxel_transforms import (
    voxelize_triangle_mesh,
    voxelize_surface_mesh,
    merge_voxels,
    minkowski_sum_voxel,
    voxel_dilate_3d,
    voxel_erode_3d,
    fill_voxel_holes,
    voxel_pyramid,
)

# Voxel geometry - rendering
from digital_geometry.voxel_render import (
    surface_nets,
    voxel_carving,
    ray_voxel_intersection,
    ray_cast_volume,
    volume_raymarch,
    volume_raymarch_with_normal,
    dual_contouring,
    voxel_gradient_normals,
    smooth_isosurface,
)

# Voxel geometry - remaining (kept in voxel.py for now)
from digital_geometry.voxel import (
    voxel_sdf_3d,
    skeleton_3d_medial,
    compute_voxel_moments,
    extract_3d_contours,
    voxel_to_octree,
    octree_to_voxel,
    SparseVoxelOctree,
    build_sparse_voxel_octree,
    VoxelNeighborLookup,
    cut_mesh_by_plane,
    cut_voxel_by_plane,
    VoxelEpitome,
    build_voxel_epitomes,
    EulerOperators,
    detect_3d_corners,
    detect_3d_junctions,
    morphological_skeleton,
)

# Topology
from digital_geometry.topology import (
    count_connected_components,
    calculate_topology,
    compute_h0_persistence,
    compute_h1_persistence,
    compute_surface_curvatures,
    connected_components_3d,
    UnionFindPersistence,
)

# Pathfinding
from digital_geometry.pathfinding import a_star, fast_marching_method

# Curves
from digital_geometry.curves import (
    point_in_polygon,
    convex_hull,
    menger_curvature,
    compute_curvature,
    smooth_points,
    douglas_peucker,
    perpendicular_distance,
    curve_shortening_flow,
    is_digitally_straight,
    estimate_tangents,
    certify_dsls,
    dsls_Arithmetical_Distance,
    naive_dsls_recognition,
)

# Contours
from digital_geometry.contours import (
    flood_fill,
    moore_neighbor_boundary_trace,
    suzuki_contour_trace,
    run_length_encode,
    run_length_decode,
    freeman_chain_code,
)

# Transforms
from digital_geometry.transforms import (
    invert_affine_matrix,
    transform_points,
    translate_points,
    rotate_points,
    scale_points,
    affine_transform_grid,
    translate_grid,
    rotate_grid,
    scale_grid,
    bilinear_resample,
    bicubic_resample,
    upscale_grid,
    downscale_grid,
)

# Descriptors
from digital_geometry.descriptors import (
    calculate_hu_moments,
    calculate_zernike_moments,
    fourier_descriptors,
    shape_context_descriptor,
    generalized_hough_transform,
    detect_critical_points,
)

# Pyramids
from digital_geometry.pyramids import build_gaussian_pyramid, build_laplacian_pyramid

# Segmentation
from digital_geometry.segmentation import (
    min_cut_max_flow,
    graph_cut_segmentation,
    watershed_transform,
)

# Spatial data structures
from digital_geometry.spatial import (
    Quadtree,
    Octree,
    compute_reeb_graph,
    jump_flooding_dt,
    compute_sdf,
)

# 3D volume processing - thinning
from digital_geometry.volume_thinning import (
    zhang_suen_thinning,
    thinning_3d,
    morphological_skeleton,
    skeleton_3d_medial,
    medial_axis_transform,
    medial_axis_transform_3d,
)

# 3D volume processing - isosurface
from digital_geometry.volume_isosurface import (
    marching_squares,
    marching_tetrahedra,
    marching_cubes,
    surface_nets,
    dual_contouring,
)

# 3D volume processing - mesh
from digital_geometry.volume_mesh import (
    fractal_dimension,
    is_simple_point_2d,
    is_simple_point_3d,
    dominant_laplacian_eigenvalues,
    laplacian_mesh_smoothing,
    mesh_simplification_edge_collapse,
    mean_curvature_flow_grid,
    active_contour_snake,
    iterative_closest_point,
)

from digital_geometry.volume_thinning import medial_axis_transform_3d

__all__ = [
    # Raster
    "bresenham_line",
    "midpoint_circle",
    "wu_line",
    "supercover_line_2d",
    "supercover_line_3d",
    "scanline_polygon_fill",
    "SE_SQUARE_3X3",
    "SE_CROSS_3X3",
    # Distance
    "manhattan_distance",
    "euclidean_distance",
    "manhattan_distance_transform",
    "euclidean_distance_transform",
    "chamfer_distance_transform",
    "geodesic_distance_transform",
    "voronoi_diagram",
    "hausdorff_distance",
    "earth_movers_distance",
    # Morphology
    "dilate",
    "erode",
    "morph_opening",
    "morph_closing",
    "morph_boundary",
    "morphological_skeleton",
    "geodesic_dilation",
    "geodesic_erosion",
    "white_tophat",
    "black_tophat",
    # Edge detection
    "canny",
    "sobel",
    "prewitt",
    "roberts",
    "laplacian_4",
    "laplacian_8",
    "gaussian_smooth",
    # Feature detection
    "harris_corner",
    "shi_tomasi_corner",
    "susan_corner",
    "fast_corner",
    "structure_tensor",
    "compute_corner_response",
    # Shape analysis
    "polygon_area",
    "polygon_centroid",
    "polygon_perimeter",
    "point_to_polygon_distance",
    "bounding_box",
    "shape_circularity",
    "shape_solidity",
    "shape_aspect_ratio",
    "shape_eccentricity",
    "shape_extent",
    "shape_compactness",
    # 3D geometry
    "estimate_surface_normals",
    "compute_normals_cross_product",
    "fit_plane_least_squares",
    "estimate_curvature_2d",
    # Voxel geometry
    "get_neighbors_6",
    "get_neighbors_18",
    "get_neighbors_26",
    "classify_voxel_grid",
    "find_voxel_borders",
    "find_voxel_edges",
    "find_voxel_vertices",
    "voxelize_triangle_mesh",
    "voxelize_surface_mesh",
    "surface_nets",
    "voxel_carving",
    "ray_voxel_intersection",
    "ray_cast_volume",
    "minkowski_sum_voxel",
    "merge_voxels",
    "voxel_euler_number",
    "voxel_connectivity_count",
    "voxel_sdf_3d",
    "skeleton_3d_medial",
    "extract_boundary_faces",
    "voxel_dilate_3d",
    "voxel_erode_3d",
    "fill_voxel_holes",
    "compute_voxel_moments",
    "extract_3d_contours",
    "voxel_to_octree",
    "octree_to_voxel",
    "voxel_contour_3d",
    "SparseVoxelOctree",
    "build_sparse_voxel_octree",
    "VoxelNeighborLookup",
    "voxel_coloring",
    "voxel_separated",
    "cut_mesh_by_plane",
    "cut_voxel_by_plane",
    "volume_raymarch",
    "volume_raymarch_with_normal",
    "smooth_isosurface",
    "voxel_gradient_normals",
    "dual_contouring",
    "VoxelEpitome",
    "build_voxel_epitomes",
    "voxel_pyramid",
    "is_voxel_surface_manifold",
    "voxel_junction_count",
    "voxel_endpoint_count",
    "EulerOperators",
    "detect_3d_corners",
    "detect_3d_junctions",
    # Topology
    "count_connected_components",
    "calculate_topology",
    "compute_h0_persistence",
    "compute_h1_persistence",
    "compute_surface_curvatures",
    "connected_components_3d",
    "UnionFindPersistence",
    # Pathfinding
    "a_star",
    "fast_marching_method",
    # Curves
    "menger_curvature",
    "compute_curvature",
    "smooth_points",
    "douglas_peucker",
    "perpendicular_distance",
    "curve_shortening_flow",
    "is_digitally_straight",
    "estimate_tangents",
    "certify_dsls",
    "dsls_Arithmetical_Distance",
    "naive_dsls_recognition",
    # Contours
    "flood_fill",
    "moore_neighbor_boundary_trace",
    "suzuki_contour_trace",
    "run_length_encode",
    "run_length_decode",
    "freeman_chain_code",
    # Transforms
    "invert_affine_matrix",
    "transform_points",
    "translate_points",
    "rotate_points",
    "scale_points",
    "affine_transform_grid",
    "translate_grid",
    "rotate_grid",
    "scale_grid",
    "bilinear_resample",
    "bicubic_resample",
    "upscale_grid",
    "downscale_grid",
    # Descriptors
    "calculate_hu_moments",
    "calculate_zernike_moments",
    "fourier_descriptors",
    "shape_context_descriptor",
    "generalized_hough_transform",
    "detect_critical_points",
    # Pyramids
    "build_gaussian_pyramid",
    "build_laplacian_pyramid",
    # Segmentation
    "min_cut_max_flow",
    "graph_cut_segmentation",
    "watershed_transform",
    # Spatial
    "Quadtree",
    "Octree",
    "compute_reeb_graph",
    "jump_flooding_dt",
    "compute_sdf",
    # 3D
    "zhang_suen_thinning",
    "thinning_3d",
    "marching_squares",
    "marching_tetrahedra",
    "marching_cubes",
    "medial_axis_transform",
    "medial_axis_transform_3d",
    "fractal_dimension",
    "is_simple_point_2d",
    "is_simple_point_3d",
    "dominant_laplacian_eigenvalues",
    "laplacian_mesh_smoothing",
    "mesh_simplification_edge_collapse",
    "active_contour_snake",
    "iterative_closest_point",
]
