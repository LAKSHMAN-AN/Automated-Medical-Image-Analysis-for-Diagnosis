"""
GradCAM Visualizer & Affected Region Bounding Box Detector
Computes activation heatmaps and extracts bounding box region coordinates for disease localization.
"""

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, Any, Tuple

class GradCAMVisualizer:
    """Generates visual heatmaps and detects anatomical bounding boxes of pathology regions."""

    @staticmethod
    def generate_heatmap(model: torch.nn.Module, target_layer: torch.nn.Module, input_tensor: torch.Tensor, target_class: int = None) -> np.ndarray:
        """Calculates Grad-CAM activation map."""
        model.eval()
        gradients = []
        activations = []

        def backward_hook(module, grad_in, grad_out):
            gradients.append(grad_out[0])

        def forward_hook(module, input, output):
            activations.append(output)

        h1 = target_layer.register_forward_hook(forward_hook)
        h2 = target_layer.register_full_backward_hook(backward_hook)

        output = model(input_tensor)
        if target_class is None:
            target_class = torch.argmax(output, dim=1).item()

        model.zero_grad()
        score = output[0, target_class]
        score.backward()

        h1.remove()
        h2.remove()

        grads = gradients[0][0].cpu().data.numpy()       # (C, H, W)
        acts = activations[0][0].cpu().data.numpy()       # (C, H, W)
        weights = np.mean(grads, axis=(1, 2))            # (C,)

        cam = np.zeros(acts.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * acts[i, :, :]

        cam = np.maximum(cam, 0)
        if np.max(cam) > 0:
            cam = cam / np.max(cam)

        return cam

    @staticmethod
    def extract_bounding_box(heatmap: np.ndarray, threshold: float = 0.5) -> Dict[str, int]:
        """Detects bounding box coordinates (x, y, w, h) of primary activation region."""
        binary_mask = np.uint8(heatmap > threshold) * 255
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            return {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}

        return {"x": 0, "y": 0, "width": 0, "height": 0}

    @classmethod
    def process_and_overlay(cls, image_path: str, heatmap: np.ndarray) -> Tuple[np.ndarray, Dict[str, int]]:
        """Overlays heatmap on BGR image and extracts lesion bounding box."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read image {image_path}")

        h, w = img.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        colormap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        overlay = cv2.addWeighted(img, 0.6, colormap, 0.4, 0)
        bbox = cls.extract_bounding_box(heatmap_resized)

        # Draw rectangle on overlay
        if bbox["width"] > 0 and bbox["height"] > 0:
            cv2.rectangle(overlay, (bbox["x"], bbox["y"]), (bbox["x"] + bbox["width"], bbox["y"] + bbox["height"]), (0, 255, 0), 2)

        return overlay, bbox
