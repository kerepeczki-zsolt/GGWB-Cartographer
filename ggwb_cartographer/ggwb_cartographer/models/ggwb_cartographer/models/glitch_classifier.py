from typing import List

import torch
from torch import nn
from torchvision import models


class GlitchClassifier(nn.Module):
    """
    Egyszerű ResNet18 alapú osztályozó Gravity Spy spektrogramokra.
    A bemenet alakja: [B, 3, 224, 224].
    """

    def __init__(self, num_classes: int, pretrained: bool = True):
        super().__init__()

        # ResNet18 backbone ImageNet súlyokkal [web:269]
        self.backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None)

        in_features = self.backbone.fc.in_features
        # Eredeti teljesen kapcsolt réteg cseréje saját kimenetre
        self.backbone.fc = nn.Linear(in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)


def build_glitch_classifier(class_names: List[str], pretrained: bool = True) -> GlitchClassifier:
    """
    Segédfüggvény: modell létrehozása osztálynevek listájából.
    """
    model = GlitchClassifier(num_classes=len(class_names), pretrained=pretrained)
    return model


__all__ = [
    "GlitchClassifier",
    "build_glitch_classifier",
]
