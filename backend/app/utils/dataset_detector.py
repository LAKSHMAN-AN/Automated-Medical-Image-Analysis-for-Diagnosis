"""
Automatic Dataset Detection & Quality Validation Utility
Supports Chest X-Ray, Brain MRI, and Lung CT datasets.
"""

import os
import cv2
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any

SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.dcm'}

class DatasetDetector:
    """Detects dataset modality, verifies directory splits, and flags corrupted or duplicate scans."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def detect_modality(self) -> str:
        """Determines dataset type based on directory path or filename conventions."""
        dir_str = str(self.root_dir).lower()
        if "brain" in dir_str or "mri" in dir_str:
            return "BRAIN_MRI"
        elif "ct" in dir_str or "lung" in dir_str:
            return "LUNG_CT"
        return "CHEST_XRAY"

    def audit_dataset((self)) -> Dict[str, Any]:
        """Scans dataset directory for total counts, duplicate hashes, and corrupted files."""
        total_files = 0
        corrupted_files = []
        file_hashes = {}
        duplicates = []
        class_counts = {}

        if not self.root_dir.exists():
            return {"error": f"Path {self.root_dir} does not exist"}

        for split in ['train', 'validation', 'test']:
            split_dir = self.root_dir / split
            if not split_dir.exists():
                continue
            for cls_dir in split_dir.iterdir():
                if cls_dir.is_dir():
                    cls_name = cls_dir.name
                    class_counts[cls_name] = class_counts.get(cls_name, 0)
                    for file_path in cls_dir.iterdir():
                        if file_path.suffix.lower() in SUPPORTED_FORMATS:
                            total_files += 1
                            class_counts[cls_name] += 1

                            # Check corrupt
                            img = cv2.imread(str(file_path))
                            if img is None:
                                corrupted_files.append(str(file_path))
                                continue

                            # Check duplicate via SHA256
                            with open(file_path, 'rb') as f:
                                f_hash = hashlib.sha256(f.read()).hexdigest()
                                if f_hash in file_hashes:
                                    duplicates.append((str(file_path), file_hashes[f_hash]))
                                else:
                                    file_hashes[f_hash] = str(file_path)

        return {
            "modality": self.detect_modality(),
            "total_images": total_files,
            "class_counts": class_counts,
            "corrupted_images_count": len(corrupted_files),
            "duplicate_images_count": len(duplicates),
            "corrupted_files": corrupted_files,
            "duplicate_pairs": duplicates
        }
