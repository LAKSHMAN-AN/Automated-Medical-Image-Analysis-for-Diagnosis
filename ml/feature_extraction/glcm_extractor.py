"""
GLCM (Gray-Level Co-occurrence Matrix) Texture Feature Extractor
Extracts contrast, dissimilarity, homogeneity, energy, correlation, and ASM.
"""

import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

class GLCMFeatureExtractor:
    """Extracts GLCM texture feature vector from medical grayscale images."""
    
    def __init__(self, distances=[1, 3], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256):
        self.distances = distances
        self.angles = angles
        self.levels = levels
        self.properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']

    def extract(self, image_path: str) -> np.ndarray:
        """Reads image, computes GLCM matrix across angles & distances, returns 1D feature vector."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Unable to read image at {image_path}")

        # Compute GLCM
        glcm = graycomatrix(
            img, 
            distances=self.distances, 
            angles=self.angles, 
            levels=self.levels, 
            symmetric=True, 
            normed=True
        )

        features = []
        for prop in self.properties:
            prop_matrix = graycoprops(glcm, prop)
            features.extend(prop_matrix.ravel())

        return np.array(features, dtype=np.float32)
