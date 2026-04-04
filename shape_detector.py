import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Shape:
    name: str
    contour: np.ndarray
    center: Optional[Tuple[int, int]]
    area: float
    perimeter: float
    vertices: int = 0


class ShapeDetector:
    def __init__(
        self,
        min_area: int = 500,
        canny_thresh1: int = 50,
        canny_thresh2: int = 150,
        blur_kernel: Tuple[int, int] = (5, 5),
        approx_epsilon: float = 0.02,
    ):
        self.min_area = min_area
        self.canny_thresh1 = canny_thresh1
        self.canny_thresh2 = canny_thresh2
        self.blur_kernel = blur_kernel
        self.approx_epsilon = approx_epsilon

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        _, thresh = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        return thresh

    def get_contours(self, image: np.ndarray) -> List[np.ndarray]:
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def approximate_contour(self, contour: np.ndarray) -> np.ndarray:
        epsilon = self.approx_epsilon * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    def _classify_shape(self, contour: np.ndarray) -> str:
        # Get basic geometric properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return "Unknown"
        
        compactness = 4 * np.pi * area / (perimeter * perimeter)
        
        # Rotated bounding box for aspect ratio
        rect = cv2.minAreaRect(contour)
        (cx, cy), (w, h), angle = rect
        if min(w, h) == 0:
            return "Unknown"
        aspect_ratio = max(w, h) / min(w, h)
        
        # Approximate the shape
        epsilon = self.approx_epsilon * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)

        # 1. Line detection (High aspect ratio, low compactness)
        if aspect_ratio > 3.0 and compactness < 0.25:
            return "Line"

        # 2. Basic polygons based on vertex count
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            # Check for square vs rectangle
            x, y, bw, bh = cv2.boundingRect(contour)
            rect_ratio = float(bw) / bh if bh != 0 else 0
            if 0.9 <= rect_ratio <= 1.1:
                return "Square"
            return "Rectangle"
        
        # 3. Circle/Ellipse detection (High compactness)
        if compactness > 0.85:
            return "Circle"
        
        if vertices > 4:
            # Could be a more complex shape, circle (if not caught), or arrow
            try:
                ellipse = cv2.fitEllipse(contour)
                if len(ellipse) == 3:
                    (ecx, ecy), (ma, mi), eangle = ellipse
                    if ma / mi > 1.5:
                        return "Ellipse"
            except:
                pass
            
            # If it's somewhat long but didn't pass line check
            if aspect_ratio > 2.0 and compactness < 0.4:
                return "Line"

        return "Unknown"

    def _get_center(self, contour: np.ndarray) -> Optional[Tuple[int, int]]:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
        return None

    def detect_circles(
        self,
        image: np.ndarray,
        min_radius: int = 10,
        max_radius: int = 0,
        param1: int = 50,
        param2: int = 30,
    ) -> List[dict]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=param1,
            param2=param2,
            minRadius=min_radius,
            maxRadius=max_radius,
        )

        detected = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                cx, cy, r = int(circle[0]), int(circle[1]), int(circle[2])
                detected.append({"center": (cx, cy), "radius": r})

        return detected

    def detect(self, image: np.ndarray) -> List[Shape]:
        shapes = []
        
        # 1. Detect Circles using Hough Transform (most robust for nodes)
        # We use a tighter range for radius to avoid false positives
        circles_data = self.detect_circles(image, min_radius=30, max_radius=100)
        circle_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        
        for c in circles_data:
            cx, cy, r = c["center"][0], c["center"][1], c["radius"]
            # Generate a contour for the circle
            points = cv2.ellipse2Poly((cx, cy), (r, r), 0, 0, 360, 5)
            shapes.append(Shape(
                name="Circle",
                contour=points,
                center=(cx, cy),
                area=np.pi * r * r,
                perimeter=2 * np.pi * r,
                vertices=len(points)
            ))
            # Mask out the circles to find connections later
            # Using a smaller padding to not cut off line ends
            cv2.circle(circle_mask, (cx, cy), r + 3, 255, -1)

        # 2. Detect other shapes (Lines/Arrows/etc) from the remaining parts
        processed = self.preprocess(image)
        # Remove the circles from the thresholded image
        remaining = cv2.bitwise_and(processed, cv2.bitwise_not(circle_mask))
        
        # Clean up noise slightly without killing thin lines
        remaining = cv2.medianBlur(remaining, 3)
        
        contours = self.get_contours(remaining)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 30: # Filter out small noise
                continue

            shape_name = self._classify_shape(contour)
            if shape_name == "Unknown":
                continue

            approx = self.approximate_contour(contour)
            center = self._get_center(contour)
            shapes.append(
                Shape(
                    name=shape_name,
                    contour=approx,
                    center=center,
                    area=area,
                    perimeter=cv2.arcLength(contour, True),
                    vertices=len(approx),
                )
            )

        return shapes

    def detect_from_file(self, image_path: str) -> Tuple[List[Shape], np.ndarray]:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        return self.detect(image), image

    def visualize(
        self,
        image: np.ndarray,
        shapes: List[Shape],
        show_labels: bool = True,
        show_centers: bool = True,
    ) -> np.ndarray:
        result = image.copy()

        # Color palette for different shapes
        colors = {
            "Circle": (0, 255, 0),    # Green
            "Line": (255, 0, 0),      # Blue
            "Triangle": (0, 0, 255),  # Red
            "Square": (255, 255, 0),  # Cyan
            "Rectangle": (255, 0, 255),# Magenta
            "Ellipse": (0, 165, 255), # Orange
            "Unknown": (128, 128, 128)# Gray
        }

        for shape in shapes:
            color = colors.get(shape.name, (0, 255, 255)) # Default yellow

            # Fill small or thin shapes, outline large ones
            if shape.name in ["Line", "Triangle", "Square", "Rectangle"]:
                cv2.drawContours(result, [shape.contour], -1, color, -1)
            else:
                cv2.drawContours(result, [shape.contour], -1, color, 2)

            if show_centers and shape.center:
                cv2.circle(result, shape.center, 3, (0, 0, 255), -1)

            if show_labels and shape.center:
                # Add background for text to make it readable
                label = shape.name
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale = 0.4
                thick = 1
                (lw, lh), lb = cv2.getTextSize(label, font, scale, thick)
                lx, ly = shape.center[0] + 5, shape.center[1] - 5
                cv2.rectangle(result, (lx, ly - lh), (lx + lw, ly + lb), (255, 255, 255), -1)
                cv2.putText(
                    result,
                    label,
                    (lx, ly),
                    font,
                    scale,
                    (0, 0, 0),
                    thick,
                )

        return result



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python shape_detector.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    detector = ShapeDetector()
    
    shapes, image = detector.detect_from_file(image_path)
    
    print(f"Total shapes detected: {len(shapes)}")
    for i, shape in enumerate(shapes, 1):
        print(f"  {i}. {shape.name:7} at {str(shape.center):15}, area: {shape.area:6.0f}")

    result = detector.visualize(image, shapes)
    cv2.imwrite("result.png", result)
    print("Saved consolidated result to result.png")
