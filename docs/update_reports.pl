#!/usr/bin/perl
use strict;
use warnings;

my @files = (
    "A_Star_Search.md", "Active_Contour_Snake.md", "Adaptive_Octree.md", "Affine_Transform.md",
    "Anisotropic_Diffusion.md", "Approximate_Contour.md", "Area_Closing_Opening.md",
    "Bilinear_Bicubic_Resampling.md", "Black_White_Tophat.md", "Bounding_Box.md",
    "Box_Counting.md", "Bresenham_Line.md", "Canny_Edge_Detection.md", "Chamfer_Distance_Transform.md",
    "Connected_Components.md", "Convex_Hull.md", "Corner_Detection.md", "Crofton_Integral.md",
    "Curve_Shortening_Flow.md", "Discrete_Calculus.md", "Distance_Transforms.md",
    "Douglas_Peucker.md", "Dual_Contouring.md", "Earth_Movers_Distance.md", "Edge_Collapse.md",
    "Euler_Characteristic.md", "Fast_Marching_Method.md", "Flood_Fill.md", "Fourier_Descriptors.md",
    "Fractal_Dimension.md", "Freeman_Chain_Code.md", "Geodesic_Distance_Dilation_Erosion.md",
    "Graham_Scan.md", "Graph_Cut_Segmentation.md", "Hausdorff_Distance.md", "Hit_or_Miss_Transform.md",
    "Hu_Zernike_Moments.md", "Instant_NGP_Hash_Encoding.md", "Iterative_Closest_Point.md",
    "Jump_Flooding.md", "Linear_Gradient_Filters.md", "Marching_Algorithms.md",
    "Medial_Axis_Transform.md", "Menger_Curvature.md", "Mesh_Manifoldness.md",
    "Minkowski_Content_Sum.md", "Moore_Neighbor_Boundary_Tracing.md", "Neural_Implicit_SDF.md",
    "Persistent_Homology.md", "Quadtree_Octree_SVO.md", "Ray_Casting_Polygon.md",
    "Raycasting_Raymarching.md", "Ricci_Flow.md", "Ring_Arithmetic.md", "RLE.md",
    "Scanline_Polygon_Fill.md", "Shape_Context_Descriptor.md", "Skeletonization.md",
    "Spatial_Hashing.md", "Surface_Curvatures.md", "Surface_Nets.md", "Suzuki_Contour_Tracing.md",
    "Voronoi_Diagram.md", "Voxel_Feature_Extraction.md", "Voxel_IoU.md", "Voxelization.md",
    "Watershed_Transform.md", "Wu_Line.md"
);

foreach my $file (@files) {
    my $path = "algorithm_reports/$file";
    if (-e $path) {
        open(my $fh, "<", $path) or die "Cannot open $path for reading: $!";
        my @lines = <$fh>;
        close($fh);

        open(my $out, ">", $path) or die "Cannot open $path for writing: $!";
        foreach my $line (@lines) {
            $line =~ s/^## (?:[0-9]+\. )?Overview/## 1. Overview/;
            $line =~ s/^## (?:[0-9]+\. )?Definitions/## 2. Definitions/;
            $line =~ s/^## (?:[0-9]+\. )?Theory/## 3. Theory/;
            $line =~ s/^## (?:[0-9]+\. )?Pseudo Code/## 4. Pseudo Code/;
            $line =~ s/^## (?:[0-9]+\. )?Parameters Selections/## 5. Parameters Selections/;
            $line =~ s/^## (?:[0-9]+\. )?Complexity/## 6. Complexity/;
            $line =~ s/^## (?:[0-9]+\. )?Usage/## 7. Usage/;
            $line =~ s/^## (?:[0-9]+\. )?(?:8\. )?References/## 9. References/;
            print $out $line;
        }
        close($out);
    } else {
        warn "$path not found\n";
    }
}
