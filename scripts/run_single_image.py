from pathlib import Path

import torch

from ggwb_cartographer.core.pipeline import load_spectrogram_image, describe_meta
from ggwb_cartographer.models.glitch_classifier import build_glitch_classifier


def main():
    # IDE írd be egy Gravity Spy PNG vagy JPG relatív útvonalát a repo-ból
    example_path = Path("data/example_glitch.png")

    tensor, meta = load_spectrogram_image(example_path)
    print(describe_meta(meta))

    # Példa osztálylista – később lecserélheted a sajátodra
    class_names = [
        "Blip",
        "KoiFish",
        "Helix",
        "PowerLine",
        "ExtremelyLoud",
    ]

    model = build_glitch_classifier(class_names, pretrained=False)
    model.eval()

    with torch.no_grad():
        tensor_batched = tensor.unsqueeze(0)  # [1, 3, 224, 224]
        logits = model(tensor_batched)
        probs = torch.softmax(logits, dim=1)[0]

    top_prob, top_idx = torch.max(probs, dim=0)
    print(f"
Predicted class: {class_names[int(top_idx)]}  (p = {float(top_prob):.3f})")


if __name__ == "__main__":
    main()
