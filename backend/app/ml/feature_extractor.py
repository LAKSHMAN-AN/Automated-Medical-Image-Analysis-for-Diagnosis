"""
Medical Image Feature Extraction Engine
Extracts texture features (GLCM), shape boundaries (HOG/Canny), and intensity histogram statistics.
"""

import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops, hog
from typing import Tuple, Dict, Any

class AdvancedFeatureExtractor:
    """Extracts 256-dimensional feature vector for traditional machine learning algorithms."""

    def __init__(self, target_size: Tuple[int, int] = (128, 128)):
        self.target_size = target_size

    def extract_glcm_texture(self, img_gray: np.ndarray) -> np.ndarray:
        """Extracts GLCM contrast, dissimilarity, homogeneity, energy, and correlation."""
        glcm = graycomatrix(
            img_gray, 
            distances=[1, 3], 
            angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], 
            levels=256, 
            symmetric=True, 
            normed=True
        )
        props = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']
        features = []
        for prop in props:
            features.extend(graycoprops(glcm, prop).ravel())
        return np.array(features, dtype=np.float32)

    def extract_intensity_histogram(self, img_gray: np.ndarray, bins: int = 32) -> np.ndarray:
        """Extracts pixel intensity histogram distribution."""
        hist, _ = np.histogram(img_gray, bins=bins, range=(0, 256), density=True)
        return hist.astype(np.float32)

    def extract_canny_edges(self, img_gray: np.ndarray) -> np.ndarray:
        """Extracts edge density and contour statistics via Canny edge detection."""
        edges = cv2.Canny(img_gray, 50, 150)
        edge_density = np.sum(edges > 0) / float(edges.size)
        mean_edge_intensity = np.mean(edges)
        return np.array([edge_density, mean_edge_intensity], dtype=np.float32)

    def extract_full_features(self, image_path: str) -> np.ndarray:
        """Extracts combined 1D feature vector for image."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Unable to read image at {image_path}")

        resized = cv2.resize(img, self.target_size, interpolation=cv2.INTER_AREA)

        glcm_feat = self.extract_glcm_texture(resized)
        hist_feat = self.extract_intensity_histogram(resized)
        edge_feat = self.extract_canny_edges(resized)

        hog_feat = hog(
            resized,
            orientations=9,
            pixels_per_cell=(16, 16),
            cells_per_block=(2, 2),
            block_norm='L2-Hys'
        ).astype(np.float32)

        combined = np.hstack([glcm_feat, hist_feat, edge_feat, hog_feat])
        return combined
