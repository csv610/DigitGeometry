import os

def to_filename(name):
    # Basic replacements
    filename = name.replace('\\', '').replace('*', 'Star').replace(' ', '_').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '').replace(':', '').replace('.', '').replace("'", "").replace('__', '_')
    
    # Map to existing files if different
    mapping = {
        "AStar_Search": "A_Star_Search",
        "Discrete_Gradient_Divergence_Laplacian": "Discrete_Calculus",
        "FAST_Harris_Shi_Tomasi_SUSAN_Corner_Detection": "Corner_Detection",
        "Laplacian_Gaussian_Sobel_Prewitt_Roberts_Filters": "Linear_Gradient_Filters",
        "Manhattan_Euclidean_Distance_Transforms": "Distance_Transforms",
        "Marching_Cubes_Squares_Tetrahedra": "Marching_Algorithms",
        "Mean_Gaussian_Principal_Curvature": "Surface_Curvatures",
        "Quadtree_Octree_Sparse_Voxel_Octree": "Quadtree_Octree_SVO",
        "Run_Length_Encoding_Decoding": "RLE",
        "Ray_Casting_Algorithm": "Ray_Casting_Polygon",
        "Box_Counting_Method": "Box_Counting",
        "Ring_Arithmetic_Method": "Ring_Arithmetic",
        "Mesh_Manifoldness_Verification": "Mesh_Manifoldness",
        "Douglas_Peucker_Simplification": "Douglas_Peucker",
        "Edge_Collapse_Mesh_Simplification": "Edge_Collapse",
        "Euler_Characteristic_Euler_Number": "Euler_Characteristic",
        "Hu_Zernike_Moments": "Hu_Zernike_Moments",
        "Earth_Movers_Distance": "Earth_Movers_Distance",
        "Persistent_Homology": "Persistent_Homology",
        "Fourier_Descriptors": "Fourier_Descriptors",
        "Fractal_Dimension": "Fractal_Dimension",
        "Freeman_Chain_Code": "Freeman_Chain_Code",
        "Geodesic_Distance_Dilation_Erosion": "Geodesic_Distance_Dilation_Erosion",
        "Graph_Cut_Segmentation": "Graph_Cut_Segmentation",
        "Hausdorff_Distance": "Hausdorff_Distance",
        "Hit_or_Miss_Transform": "Hit_or_Miss_Transform",
        "Iterative_Closest_Point": "Iterative_Closest_Point",
        "Jump_Flooding": "Jump_Flooding",
        "Medial_Axis_Transform": "Medial_Axis_Transform",
        "Menger_Curvature": "Menger_Curvature",
        "Minkowski_Content_Sum": "Minkowski_Content_Sum",
        "Moore_Neighbor_Boundary_Tracing": "Moore_Neighbor_Boundary_Tracing",
        "Neural_Implicit_SDF": "Neural_Implicit_SDF",
        "Scanline_Polygon_Fill": "Scanline_Polygon_Fill",
        "Shape_Context_Descriptor": "Shape_Context_Descriptor",
        "Skeletonization": "Skeletonization",
        "Surface_Nets": "Surface_Nets",
        "Suzuki_Contour_Tracing": "Suzuki_Contour_Tracing",
        "Voronoi_Diagram": "Voronoi_Diagram",
        "Voxelization": "Voxelization",
        "Watershed_Transform": "Watershed_Transform",
        "Wu_Line": "Wu_Line",
        "Raycasting_Raymarching": "Raycasting_Raymarching",
        "Voxel_IoU": "Voxel_IoU",
        "Spatial_Hashing": "Spatial_Hashing",
        "Instant_NGP_Hash_Encoding": "Instant_NGP_Hash_Encoding",
        "Voxel_Feature_Extraction": "Voxel_Feature_Extraction",
        "Approximate_Contour": "Approximate_Contour",
        "Area_Closing_Opening": "Area_Closing_Opening",
        "Bilinear_Bicubic_Resampling": "Bilinear_Bicubic_Resampling",
        "Black_White_Tophat": "Black_White_Tophat",
        "Bounding_Box": "Bounding_Box",
        "Bresenham_Line": "Bresenham_Line",
        "Canny_Edge_Detection": "Canny_Edge_Detection",
        "Chamfer_Distance_Transform": "Chamfer_Distance_Transform",
        "Connected_Components": "Connected_Components",
        "Convex_Hull": "Convex_Hull",
        "Crofton_Integral": "Crofton_Integral",
        "Curve_Shortening_Flow": "Curve_Shortening_Flow"
    }
    
    return mapping.get(filename, filename)

with open('algo_clean.txt', 'r') as f:
    algos = [line.strip() for line in f if line.strip()]

missing = []
for algo in algos:
    fname = to_filename(algo) + ".md"
    if not os.path.exists(f"algorithm_reports/{fname}"):
        missing.append((algo, fname))

if missing:
    print("Missing reports:")
    for algo, fname in missing:
        print(f"  {algo} -> {fname}")
else:
    print("All reports exist!")
