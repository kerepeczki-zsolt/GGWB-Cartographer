from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
from PIL import Image
import torch
from torchvision import transforms


# Alap torchvision pipeline Gravity Spy spektrogramokhoz
# - crop: levágja a tengelyeket / feliratokat (Gravity Spy PNG-khez igazítva)
# - resize: 224x224 (ImageNet-kompatibilis)
# - tensor + normalizálás: [0,1] tartomány, majd standard normálás
_GRAVITY_SPY_TRANSFORM = transforms.Compose(
    [
        transforms.Lambda(lambda img: img.crop((100, 60, 775, 640))),  # left, top, right, bottom [web:267]
        transforms.Resize((224, 224)),  # tipikus bemenet VGG/ResNet-hez [web:261]
        transforms.ToTensor(),  # -> [C, H, W] float32 [0,1] [web:262]
        transforms.Normalize(
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5],
        ),
    ]
)


def load_spectrogram_image(path: str | Path) -> Tuple[torch.Tensor, Dict[str, Any]]:
    """
    Gravity Spy jellegű spektrogram kép betöltése és előfeldolgozása.

    Visszatérés:
        tensor: torch.Tensor alakú kép [3, 224, 224]
        meta:   szótár néhány egyszerű háttér-geometriai jellemzővel
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    # Kép betöltése RGB-ben
    img = Image.open(path).convert("RGB")  # Pillow + torchvision együtt [web:262]

    # Nyers numpy másolat a geometriai feature-ökhöz
    np_img = np.array(img).astype(np.float32)  # shape: [H, W, 3]

    # Alap háttér‑geometria jellemzők (intenzitás fluktuációk)
    # 1) Globális átlag és szórás
    mean_intensity = float(np_img.mean())
    std_intensity = float(np_img.std())

    # 2) Vízszintes és függőleges intenzitás-gradiens átlagos nagysága
    gy, gx = np.gradient(np_img.mean(axis=2))  # szürkeárnyalatos átlagcsatorna
    grad_mag = np.sqrt(gx ** 2 + gy ** 2)
    mean_grad = float(grad_mag.mean())
    std_grad = float(grad_mag.std())

    # 3) Egyszerű "patch-variancia": felosztás 4x4 rácsra, ott variancia átlagolva
    H, W, _ = np_img.shape
    h_step = H // 4
    w_step = W // 4
    patch_vars = []
    for i in range(4):
        for j in range(4):
            patch = np_img[i * h_step : (i + 1) * h_step, j * w_step : (j + 1) * w_step]
            patch_vars.append(float(patch.mean(axis=2).var()))
    mean_patch_var = float(np.mean(patch_vars))
    std_patch_var = float(np.std(patch_vars))

    meta: Dict[str, Any] = {
        "mean_intensity": mean_intensity,
        "std_intensity": std_intensity,
        "mean_gradient": mean_grad,
        "std_gradient": std_grad,
        "mean_patch_var": mean_patch_var,
        "std_patch_var": std_patch_var,
        "original_height": int(H),
        "original_width": int(W),
        "path": str(path),
    }

    # Torchvision transform alkalmazása
    tensor = _GRAVITY_SPY_TRANSFORM(img)  # [3, 224, 224]

    return tensor, meta


def describe_meta(meta: Dict[str, Any]) -> str:
    """
    Embernek olvasható szöveges összefoglaló a geometriai jellemzőkről.
    Ez hasznos lehet notebookban / logban.
    """
    lines = [
        f"File: {meta.get('path', 'N/A')}",
        f"Original size: {meta.get('original_width')} x {meta.get('original_height')}",
        f"Mean intensity: {meta.get('mean_intensity'):.2f}",
        f"Std intensity: {meta.get('std_intensity'):.2f}",
        f"Mean gradient magnitude: {meta.get('mean_gradient'):.4f}",
        f"Std gradient magnitude: {meta.get('std_gradient'):.4f}",
        f"Mean patch variance (4x4 grid): {meta.get('mean_patch_var'):.4f}",
        f"Std patch variance (4x4 grid): {meta.get('std_patch_var'):.4f}",
    ]
    return "
".join(lines)


__all__ = [
    "load_spectrogram_image",
    "describe_meta",
  ]
