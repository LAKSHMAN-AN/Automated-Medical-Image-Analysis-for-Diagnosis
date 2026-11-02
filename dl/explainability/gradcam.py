"""
Grad-CAM (Gradient-weighted Class Activation Mapping) Visualizer
Computes class activation heatmaps to highlight visual anomalies in radiological scans.
"""

import cv2
import numpy as np
import torch
import torch.nn.functional as F

class GradCAMEngine:
    """Computes Grad-CAM heatmap overlay for PyTorch vision models."""

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Register forward and backward hooks
        self.target_layer.register_forward_hook(self._forward_hook)
        self.target_layer.register_full_backward_hook(self._backward_hook)

    def _forward_hook(self, module, input, output):
        self.activations = output.detach()

    def _backward_hook(self, module, grad_in, grad_out):
        self.gradients = grad_out[0].detach()

    def generate_heatmap(self, input_tensor: torch.Tensor, target_class: int = None) -> np.ndarray:
        """Computes Grad-CAM activation heatmap normalized to [0, 1]."""
        self.model.eval()
        output = self.model(input_tensor)

        if target_class is None:
            target_class = torch.argmax(output, dim=1).item()

        self.model.zero_grad()
        score = output[0, target_class]
        score.backward()

        # Compute weights via Global Average Pooling of gradients
        gradients = self.gradients[0]          # (C, H, W)
        activations = self.activations[0]      # (C, H, W)
        weights = torch.mean(gradients, dim=(1, 2), keepdim=True)  # (C, 1, 1)

        # Weighted combination of activation maps
        cam = torch.sum(weights * activations, dim=0)  # (H, W)
        cam = F.relu(cam)                              # Apply ReLU to keep positive activations

        # Normalize heatmap to [0, 1]
        cam = cam.cpu().numpy()
        if np.max(cam) > 0:
            cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam) + 1e-8)
        else:
            cam = np.zeros_like(cam)

        return cam

    def overlay_heatmap(self, original_image_bgr: np.ndarray, heatmap: np.ndarray, alpha: float = 0.4) -> np.ndarray:
        """Overlays heatmap on original BGR image using Jet colormap."""
        h, w = original_image_bgr.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        
        # Colorize heatmap
        colormap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        # Blend colormap with original image
        overlay = cv2.addWeighted(original_image_bgr, 1 - alpha, colormap, alpha, 0)
        return overlay
