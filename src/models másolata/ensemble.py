import numpy as np
from typing import List
from tensorflow.keras.models import load_model

class EnsembleClassifier:
    """
    Súlyozott 5-modelles ensemble:
    [resnet_std, resnet_aug, resnet_geo, densenet, geometric]
    Implementáció: doku 5.4.2 alapján.
    """

    def __init__(self, models: List, weights=None):
        if weights is None:
            weights = [0.25, 0.22, 0.28, 0.15, 0.10]
        self.models = models
        self.weights = np.array(weights, dtype=float)
        self.weights = self.weights / np.sum(self.weights)

    def predict(self, X_cnn, X_geo):
        """
        X_cnn: 4D tensor (N, 224, 224, 3)
        X_geo: 2D tensor (N, 92)
        """
        all_preds = []

        for model in self.models:
            name = getattr(model, "name", "").lower()

            if "geometric" in name:
                pred = model.predict(X_geo)
            else:
                pred = model.predict(X_cnn)

            all_preds.append(pred)

        all_preds = np.stack(all_preds, axis=0)
        return np.average(all_preds, axis=0, weights=self.weights)

    @classmethod
    def load(cls, base_path="deployment/models"):
        """
        Modellek betöltése doku 12. függelék szerinti elnevezéssel.
        A fájlneveket később pontosítjuk.
        """
        resnet_std = load_model(f"{base_path}/resnet_std.h5")
        resnet_aug = load_model(f"{base_path}/resnet_aug.h5")
        resnet_geo = load_model(f"{base_path}/resnet_geo.h5")
        densenet = load_model(f"{base_path}/densenet.h5")
        geometric = load_model(f"{base_path}/geometric.h5")

        models = [resnet_std, resnet_aug, resnet_geo, densenet, geometric]
        return cls(models=models)
