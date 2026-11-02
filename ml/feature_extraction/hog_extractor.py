"""
HOG (Histogram of Oriented Gradients) Shape & Edge Feature Extractor
Extracts contour and anatomical boundary descriptors.
"""

import cv2
import numpy as np
from skimage.feature import hog

class HOGFeatureExtractor:
    """Extracts HOG feature vectors from medical images."""

    def __init__(self, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(2, 2)):
        self.orientations = orientations
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block

    def extract(self, image_path: str, target_size=(128, 128)) -> np.ndarray:
        """Reads image, resizes to target_size, computes HOG descriptor vector."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Unable to read image at {image_path}")

        resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

        features = hog(
            resized,
            orientations=self.orientations,
            pixels_per_cell=self.pixels_per_cell,
            cells_per_block=self.cells_per_block,
            block_norm='L2-Hys',
            visualize=False
        )

        return features.astype(np.float32)
