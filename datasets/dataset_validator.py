"""
Medical Image Dataset Validation & Preprocessing Pipeline
Automated Medical Image Analysis for Diagnosis
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Supported image extensions and magic byte signatures
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.dcm'}
MAGIC_BYTES = {
    'png': b'\x89PNG',
    'jpg': b'\xff\xd8\xff',
    'dicom': b'DICM'
}

class MedicalDatasetValidator:
    """Validates dataset structure, file integrity, and channel formats."""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.classes = ['NORMAL', 'COVID', 'PNEUMONIA', 'TUBERCULOSIS']
        self.splits = ['train', 'validation', 'test']

    def validate_folder_structure(self) -> Dict[str, bool]:
        """Verifies presence of required split and class directories."""
        results = {}
        for split in self.splits:
            for cls in self.classes:
                dir_path = self.base_dir / split / cls
                exists = dir_path.exists() and dir_path.is_dir()
                results[f"{split}/{cls}"] = exists
        return results

    def validate_image_file(self, file_path: str) -> Tuple[bool, str]:
        """Validates single image integrity, dimensions, and magic bytes."""
        path = Path(file_path)
        if not path.exists():
            return False, "File does not exist"
        
        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            return False, f"Unsupported extension: {ext}"

        # Read binary header for magic bytes verification
        try:
            with open(path, 'rb') as f:
                header = f.read(132)
                if ext in ['.png'] and not header.startswith(MAGIC_BYTES['png']):
                    return False, "Corrupted PNG header"
                elif ext in ['.jpg', '.jpeg'] and not header.startswith(MAGIC_BYTES['jpg']):
                    return False, "Corrupted JPEG header"
                elif ext == '.dcm' and header[128:132] != MAGIC_BYTES['dicom']:
                    return False, "Corrupted DICOM header"
        except Exception as e:
            return False, f"File read error: {str(e)}"

        # Verify image loadability and dimensions
        try:
            img = cv2.imread(str(path))
            if img is None:
                return False, "OpenCV failed to decode image"
            h, w, c = img.shape
            if h < 224 or w < 224:
                return False, f"Image resolution too low ({w}x{h}). Minimum required: 224x224"
        except Exception as e:
            return False, f"Image decode exception: {str(e)}"

        return True, "Valid"

    def get_class_distribution(self, split: str = 'train') -> Dict[str, int]:
        """Counts valid images per class directory in a split."""
        distribution = {}
        for cls in self.classes:
            cls_dir = self.base_dir / split / cls
            if cls_dir.exists():
                count = sum(1 for f in cls_dir.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS)
                distribution[cls] = count
            else:
                distribution[cls] = 0
        return distribution


class MedicalImagePreprocessor:
    """Preprocesses medical images: CLAHE contrast enhancement, resizing, normalization."""

    def __init__(self, target_size: Tuple[int, int] = (224, 224), apply_clahe: bool = True):
        self.target_size = target_size
        self.apply_clahe = apply_clahe
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.imagenet_mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.imagenet_std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def preprocess(self, image_path: str) -> np.ndarray:
        """Processes raw image into normalized 3-channel (C, H, W) numpy tensor."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read image at {image_path}")

        # Convert to Grayscale for CLAHE if color, then convert back to 3-channel
        if len(img.shape) == 3 and img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        # Apply CLAHE Contrast Enhancement
        if self.apply_clahe:
            gray = self.clahe.apply(gray)

        # Convert Grayscale to 3-channel RGB
        rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        # Resize to target dimensions
        resized = cv2.resize(rgb, self.target_size, interpolation=cv2.INTER_AREA)

        # Normalize pixel values [0, 1] then standardize to ImageNet mean/std
        normalized = resized.astype(np.float32) / 255.0
        standardized = (normalized - self.imagenet_mean) / self.imagenet_std

        # Transpose from (H, W, C) to (C, H, W) for PyTorch compatibility
        tensor = np.transpose(standardized, (2, 0, 1))
        return tensor


if __name__ == "__main__":
    validator = MedicalDatasetValidator("datasets/chest_xray")
    print("Folder Structure Validation:", validator.validate_folder_structure())
    print("Train Class Distribution:", validator.get_class_distribution('train'))
