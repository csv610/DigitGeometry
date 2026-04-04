"""Image pyramids."""

from digital_geometry.transforms import downscale_grid


def build_gaussian_pyramid(grid, levels=3):
    """Build Gaussian pyramid."""
    pyramid = [grid]

    current = grid
    for _ in range(levels - 1):
        height = len(current)
        width = len(current[0])

        if height < 2 or width < 2:
            break

        new_height = height // 2
        new_width = width // 2

        level = [[0.0] * new_width for _ in range(new_height)]

        for y in range(new_height):
            for x in range(new_width):
                total = 0
                count = 0

                for dy in range(2):
                    for dx in range(2):
                        sy = y * 2 + dy
                        sx = x * 2 + dx

                        if sy < height and sx < width:
                            total += current[sy][sx]
                            count += 1

                level[y][x] = total / count if count > 0 else 0

        pyramid.append(level)
        current = level

    return pyramid


def build_laplacian_pyramid(gaussian_pyramid):
    """Build Laplacian pyramid from Gaussian pyramid."""
    pyramid = []

    for i in range(len(gaussian_pyramid) - 1):
        current = gaussian_pyramid[i]
        next_level = gaussian_pyramid[i + 1]

        height = len(current)
        width = len(current[0])
        new_height = len(next_level)
        new_width = len(next_level[0])

        upsampled = [[0.0] * width for _ in range(height)]

        for y in range(new_height):
            for x in range(new_width):
                val = next_level[y][x]

                upsampled[2 * y][2 * x] = val
                if 2 * x + 1 < width:
                    upsampled[2 * y][2 * x + 1] = val
                if 2 * y + 1 < height:
                    upsampled[2 * y + 1][2 * x] = val
                    if 2 * x + 1 < width:
                        upsampled[2 * y + 1][2 * x + 1] = val

        laplacian = [
            [current[y][x] - upsampled[y][x] for x in range(width)]
            for y in range(height)
        ]
        pyramid.append(laplacian)

    pyramid.append(gaussian_pyramid[-1])

    return pyramid
