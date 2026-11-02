"""
Inference Manager & Multi-Modality Model Router
Handles model loading, inference routing, and ONNX export.
"""

import os
import torch
import numpy as np
from typing import Dict, Any, List
from backend.app.core.logging_config import logger
from backend.app.dl.architectures import get_model_for_modality

class InferenceManager:
    """Manages AI model loading and multi-modality prediction routing."""

    MODALITY_CLASSES = {
        "CHEST_XRAY": ["NORMAL", "COVID", "PNEUMONIA", "TUBERCULOSIS"],
        "BRAIN_MRI": ["GLIOMA", "MENINGIOMA", "PITUITARY", "NO_TUMOR"],
        "LUNG_CT": ["BENIGN", "MALIGNANT", "NORMAL"]
    }

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.loaded_models: Dict[str, torch.nn.Module] = {}

    def get_model(self, modality: str) -> torch.nn.Module:
        mod = modality.upper()
        if mod not in self.loaded_models:
            logger.info(f"Loading Model for modality '{mod}' on device '{self.device}'...")
            model = get_model_for_modality(mod).to(self.device)
            model.eval()
            self.loaded_models[mod] = model
        return self.loaded_models[mod]

    def predict(self, image_tensor: np.ndarray, modality: str = "CHEST_XRAY") -> Dict[str, Any]:
        """Performs forward pass for preprocessed image tensor."""
        mod = modality.upper()
        classes = self.MODALITY_CLASSES.get(mod, self.MODALITY_CLASSES["CHEST_XRAY"])

        # Convert numpy (H, W, C) to torch tensor (1, C, H, W)
        tensor = torch.from_numpy(image_tensor).permute(2, 0, 1).unsqueeze(0).float().to(self.device)

        model = self.get_model(mod)
        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()

        pred_idx = int(np.argmax(probs))
        pred_class = classes[pred_idx]
        confidence = float(probs[pred_idx])

        prob_dict = {cls_name: float(probs[i]) for i, cls_name in enumerate(classes)}

        return {
            "modality": mod,
            "predicted_class": pred_class,
            "confidence_score": round(confidence, 4),
            "class_probabilities": prob_dict,
            "supported_classes": classes
        }

inference_manager = InferenceManager()
