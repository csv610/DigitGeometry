"""Voxel editing operators."""

import numpy as np
from digital_geometry.voxel_transforms import point_in_triangle


def cut_mesh_by_plane(vertices, triangles, plane_normal, plane_d):
    """Cut mesh by plane."""
    intersection_points = []
    intersection_lines = []
    for tri in triangles:
        if len(tri) < 3:
            continue
        v0 = vertices[tri[0]]
        v1 = vertices[tri[1]]
        v2 = vertices[tri[2]]
        d0 = (
            plane_normal[0] * v0[0]
            + plane_normal[1] * v0[1]
            + plane_normal[2] * v0[2]
            - plane_d
        )
        d1 = (
            plane_normal[0] * v1[0]
            + plane_normal[1] * v1[1]
            + plane_normal[2] * v1[2]
            - plane_d
        )
        d2 = (
            plane_normal[0] * v2[0]
            + plane_normal[1] * v2[1]
            + plane_normal[2] * v2[2]
            - plane_d
        )
        if d0 == 0:
            intersection_points.append(v0)
        if d1 == 0:
            intersection_points.append(v1)
        if d2 == 0:
            intersection_points.append(v2)
    return intersection_points, intersection_lines


def cut_voxel_by_plane(volume, plane_normal, plane_d):
    """Cut voxel volume by plane."""
    volume = np.asarray(volume)
    depth, height, width = volume.shape
    result = np.zeros_like(volume)
    nx, ny, nz = plane_normal
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if volume[z, y, x] == 1:
                    dist = nx * x + ny * y + nz * z - plane_d
                    if dist <= 0:
                        result[z, y, x] = 1
    return result


class EulerOperators:
    """Euler operators for topological voxel editing."""

    @staticmethod
    def make_voxel(volume, x, y, z):
        result = np.asarray(volume).copy()
        result[z, y, x] = 1
        return result

    @staticmethod
    def remove_voxel(volume, x, y, z):
        result = np.asarray(volume).copy()
        result[z, y, x] = 0
        return result

    @staticmethod
    def toggle_voxel(volume, x, y, z):
        result = np.asarray(volume).copy()
        result[z, y, x] = 1 - result[z, y, x]
        return result
