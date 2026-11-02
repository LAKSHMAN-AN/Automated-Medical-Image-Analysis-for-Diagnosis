"""
ResNet50 Medical Image Classifier Architecture
Pre-trained ImageNet backbone with custom classifier head for 4-class medical image diagnosis.
"""
import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
class MedicalResNet50(nn.Module):
    """ResNet50 Convolutional Neural Network for Medical Image Classification."""

    def __init__(self, num_classes: int = 4, freeze_backbone: bool = False, dropout_rate: float = 0.4):
        super(MedicalResNet50, self).__init__()
        weights = ResNet50_Weights.DEFAULT
        self.backbone = resnet50(weights=weights)

        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False

        # Replace final fc layer
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(p=dropout_rate),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate / 2),
            nn.Linear(512, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through ResNet50 backbone and classifier head."""
        return self.backbone(x)

    def get_final_conv_layer(self) -> nn.Module:
        """Returns layer4[2] for Grad-CAM activation extraction."""
        return self.backbone.layer4[2]
