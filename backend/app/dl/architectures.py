"""
Multi-Modality Vision Models (PyTorch)
Architectures for Chest X-Ray Disease, Brain MRI Tumor, and Lung CT Cancer Detection.
"""

import torch
import torch.nn as nn
from torchvision import models
from typing import Dict, Any, List

class ChestDiseaseModel(nn.Module):
    """ResNet50 architecture fine-tuned for Chest X-Ray classification (4 Classes)."""
    def __init__(self, num_classes: int = 4):
        super(ChestDiseaseModel, self).__init__()
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)

class BrainTumorModel(nn.Module):
    """EfficientNet-B0 fine-tuned for Brain MRI tumor detection (4 Classes: Glioma, Meningioma, Pituitary, No Tumor)."""
    def __init__(self, num_classes: int = 4):
        super(BrainTumorModel, self).__init__()
        self.backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier[1] = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)

class LungCancerModel(nn.Module):
    """Custom ResNet-based Transfer Learning model for Lung CT Cancer (3 Classes: Benign, Malignant, Normal)."""
    def __init__(self, num_classes: int = 3):
        super(LungCancerModel, self).__init__()
        self.backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)

# Modality Model Factory
def get_model_for_modality(modality: str = "CHEST_XRAY") -> nn.Module:
    mod = modality.upper()
    if mod == "BRAIN_MRI":
        return BrainTumorModel(num_classes=4)
    elif mod == "LUNG_CT":
        return LungCancerModel(num_classes=3)
    else:
        return ChestDiseaseModel(num_classes=4)
