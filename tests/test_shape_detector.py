import pytest
import cv2
import numpy as np
from digital_geometry.shape_detector import ShapeDetector


def test_preprocess():
    detector = ShapeDetector()
    # Create a 100x100 white image with a black circle
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.circle(image, (50, 50), 20, (0, 0, 0), -1)

    processed = detector.preprocess(image)
    # THRESH_BINARY_INV should make the circle white (255) and background black (0)
    assert processed[50, 50] == 255
    assert processed[0, 0] == 0


def test_detect_circle():
    detector = ShapeDetector()
    image = np.ones((200, 200, 3), dtype=np.uint8) * 255
    # Use a size that is likely to be detected by HoughCircles (param1=50, param2=30)
    # The default params in detect_circles are optimized for larger nodes
    cv2.circle(image, (100, 100), 50, (0, 0, 0), -1)

    shapes = detector.detect(image)
    assert any(s.name == "Circle" for s in shapes)


def test_detect_polygons():
    detector = ShapeDetector()
    # Use a larger image and shapes to ensure they are above min_area
    image = np.ones((400, 400, 3), dtype=np.uint8) * 255

    # Triangle
    pts = np.array([[100, 100], [150, 200], [50, 200]], np.int32)
    cv2.drawContours(image, [pts], -1, (0, 0, 0), -1)

    # Square
    cv2.rectangle(image, (250, 50), (350, 150), (0, 0, 0), -1)

    # Rectangle
    cv2.rectangle(image, (250, 250), (380, 300), (0, 0, 0), -1)

    shapes = detector.detect(image)
    shape_names = [s.name for s in shapes]

    assert "Triangle" in shape_names
    assert "Square" in shape_names
    assert "Rectangle" in shape_names


def test_detect_line():
    detector = ShapeDetector()
    image = np.ones((400, 400, 3), dtype=np.uint8) * 255

    # Draw a thin long line (represented as a long thin rectangle)
    cv2.rectangle(image, (50, 50), (350, 60), (0, 0, 0), -1)

    shapes = detector.detect(image)
    assert any(s.name == "Line" for s in shapes)


def test_visualize():
    detector = ShapeDetector()
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.circle(image, (50, 50), 20, (0, 0, 0), -1)

    shapes = detector.detect(image)
    result = detector.visualize(image, shapes)

    assert result.shape == image.shape
    # Check if we actually drew something (result should not be all white)
    assert not np.array_equal(result, image)
