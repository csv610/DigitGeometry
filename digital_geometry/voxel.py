"""Voxel utilities - compatibility module.

This module imports from the split voxel submodules for backward compatibility.
"""

from digital_geometry.voxel_core import (
    get_neighbors_6,
    get_neighbors_18,
    get_neighbors_26,
    voxel_euler_number,
    voxel_connectivity_count,
    voxel_coloring,
    voxel_separated,
)

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

from digital_geometry.volume_thinning import morphological_skeleton, skeleton_3d_medial
from digital_geometry.volume_isosurface import surface_nets
from digital_geometry.voxel_render import (
    ray_voxel_intersection,
    ray_cast_volume,
    volume_raymarch,
    volume_raymarch_with_normal,
    dual_contouring,
    voxel_gradient_normals,
    smooth_isosurface,
    voxel_carving,
)

from digital_geometry.voxel_sdf import (
    voxel_sdf_3d,
    voxel_to_octree,
    octree_to_voxel,
    SparseVoxelOctree,
    build_sparse_voxel_octree,
    VoxelEpitome,
    build_voxel_epitomes,
)

from digital_geometry.voxel_analysis import (
    compute_voxel_moments,
    detect_3d_corners,
    detect_3d_junctions,
    extract_3d_contours,
    VoxelNeighborLookup,
)

from digital_geometry.voxel_diffusion import (
    voxel_heat_diffusion,
    voxel_anisotropic_diffusion,
    compute_diffusion_distance,
    compute_heat_kernel_signature,
    voxel_curvature_diffusion,
    diffusion_boundary_detection,
    voxel_geodesic_diffusion,
    SimpleVoxelDiffusion,
    VoxelDiffusionConfig,
    VoxelDiffusionModel,
    create_sphere_voxel,
    create_box_voxel,
    create_torus_voxel,
    augment_voxel_with_noise,
    compute_voxel_iou,
    voxel_to_point_cloud,
    LatentVoxelDiffusion,
    augment_voxel_with_noise,
    cosine_beta_schedule,
    linear_beta_schedule,
    extract_voxel_slices,
    save_slice_as_png,
    extract_and_save_slices,
    visualize_voxel_slice,
    create_colored_voxel_volume,
    save_voxel_volume_image,
    extract_slices_along_direction,
    extract_orthogonal_slices,
    rotate_voxels_by_direction,
)

from digital_geometry.voxel_operators import (
    cut_mesh_by_plane,
    cut_voxel_by_plane,
    EulerOperators,
)

from digital_geometry.geometric_measure_theory import (
    compute_voxel_perimeter,
    compute_voxel_surface_area,
    compute_isoperimetric_quotient,
    compute_minkowski_content,
    compute_mean_curvature_voxel,
    compute_gaussian_curvature_voxel,
    compute_principal_curvatures,
    compute_crofton_integral,
    compute_support_function,
    compute_mean_width,
    compute_mean_curvature_flow_voxel,
    compute_inverse_mean_curvature_flow,
    compute_geodesic_on_voxel_surface,
    compute_minimal_surface_voxel,
    compute_normal_current,
    compute_euler_characteristic,
    compute_filling_volume,
    compute_distance_to_measure,
    compute_medial_axis_voxel,
)

from digital_geometry.voxel_diffusion import (
    ricci_flow_voxel,
    RicciFlowConfig,
    build_voxel_graph,
    compute_discrete_curvature_vertex,
    ricci_flow_boundary_extraction,
    voxel_shape_signature_ricci,
    simplify_voxel_shape_by_ricci,
    ricci_flow_smoothing_iterations,
)
