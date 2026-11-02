"""
Image Preprocessing Service
Resize, Normalization, CLAHE, Histogram Equalization, Noise Removal using OpenCV & Albumentations logic.
"""

import cv2
import numpy as np
from typing import Tuple

class PreprocessingService:
    """Service providing medical image enhancement operations."""

    @staticmethod
    def resize_image(img: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        return cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

    @staticmethod
    def apply_clahe(img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        enhanced = clahe.apply(gray)
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def remove_noise(img: np.ndarray) -> np.ndarray:
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    @staticmethod
    def normalize_image(img: np.ndarray) -> np.ndarray:
        return (img.astype(np.float32) / 255.0).clip(0, 1)

    @classmethod
    def full_pipeline(cls, image_path: str, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read image at path {image_path}")
        
        resized = cls.resize_image(img, target_size)
        enhanced = cls.apply_clahe(resized)
        denoised = cls.remove_noise(enhanced)
        normalized = cls.normalize_image(denoised)
        return normalized
