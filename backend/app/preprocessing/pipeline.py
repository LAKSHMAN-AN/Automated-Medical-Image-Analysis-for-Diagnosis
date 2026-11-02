"""
Multi-Modality Medical Image Preprocessing Pipeline Suite
Pipelines for Chest X-Ray (CLAHE), Brain MRI (Skull Stripping & Bias Correction), and Lung CT (Windowing).
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any

class ModalityImagePreprocessor:
    """Modality-specific medical image preprocessing engine."""

    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size

    # --- 1. CHEST X-RAY PREPROCESSING PIPELINE ---
    def preprocess_chest_xray(self, image: np.ndarray) -> np.ndarray:
        """Chest X-Ray: CLAHE, Histogram Equalization, Noise Removal, Standardization."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # CLAHE Contrast Enhancement
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # OpenCV Non-Local Means Denoising
        denoised = cv2.fastNlMeansDenoising(enhanced, None, h=10, templateWindowSize=7, searchWindowSize=21)

        # Resize & Convert to 3-Channel RGB
        resized = cv2.resize(denoised, self.target_size, interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        
        # ImageNet Normalization [0, 1]
        normalized = rgb.astype(np.float32) / 255.0
        return normalized

    # --- 2. BRAIN MRI PREPROCESSING PIPELINE ---
    def preprocess_brain_mri(self, image: np.ndarray) -> np.ndarray:
        """Brain MRI: Skull Stripping (Otsu contour mask), Bias Field Correction, Resize, Normalization."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Skull Stripping via Otsu Thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            c = max(contours, key=cv2.contourArea)
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [c], -1, 255, -1)
            stripped = cv2.bitwise_and(gray, mask)
        else:
            stripped = gray

        # Bias Field Correction (Gaussian ratio smoothing)
        blur = cv2.GaussianBlur(stripped, (21, 21), 0).astype(np.float32) + 1e-5
        corrected = np.clip((stripped.astype(np.float32) / blur) * 128.0, 0, 255).astype(np.uint8)

        # Resize & Convert to 3-Channel RGB
        resized = cv2.resize(corrected, self.target_size, interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        return rgb.astype(np.float32) / 255.0

    # --- 3. LUNG CT SCAN PREPROCESSING PIPELINE ---
    def preprocess_lung_ct(self, image: np.ndarray, window_center: int = -600, window_width: int = 1500) -> np.ndarray:
        """Lung CT: Hounsfield Windowing, Contrast Enhancement, Normalization."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # CT Windowing (Intensity clipping)
        min_val = window_center - (window_width / 2.0)
        max_val = window_center + (window_width / 2.0)
        windowed = np.clip(gray, min_val, max_val)
        
        # Scale to [0, 255]
        scaled = ((windowed - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)

        # Contrast Enhancement
        equalized = cv2.equalizeHist(scaled)

        # Resize & Convert to 3-Channel RGB
        resized = cv2.resize(equalized, self.target_size, interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        return rgb.astype(np.float32) / 255.0

    # --- AUTOMATIC PIPELINE ROUTER ---
    def process_by_modality(self, image_path: str, modality: str = "CHEST_XRAY") -> np.ndarray:
        """Routes image to modality-specific preprocessing pipeline."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read image at path {image_path}")

        mod = modality.upper()
        if mod == "BRAIN_MRI":
            return self.preprocess_brain_mri(img)
        elif mod == "LUNG_CT":
            return self.preprocess_lung_ct(img)
        else:
            return self.preprocess_chest_xray(img)
