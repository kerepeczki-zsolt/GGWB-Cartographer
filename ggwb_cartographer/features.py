import numpy as np
import cv2
from scipy import stats
from skimage.feature import greycomatrix, greycoprops


class GeometricFeatureExtractor:
    def __init__(self):
        # A teljes feature-vektor hossza (F1–F92)
        self.feature_count = 92

    def extract_all_features(self, spectrogram: np.ndarray) -> np.ndarray:
        """
        Az összes (F1–F92) feature kinyerése egy spektrumból / spektrogramból.

        - Bemenet: 2D numpy tömb (frekvencia x idő)
        - Kimenet: 1D numpy vektor, hossz: self.feature_count
        """
        # Biztonságos konverzió float típusra
        spec = np.asarray(spectrogram, dtype=float)

        # NaN / ±inf eltávolítása
        spec = np.nan_to_num(spec, nan=0.0, posinf=0.0, neginf=0.0)

        features = []

        # Kategória I: Alapvető jellemzők
        features.extend(self.basic_features(spec))

        # Kategória II: Frekvencia domain
        features.extend(self.frequency_features(spec))

        # Kategória III: Időbeli domain
        features.extend(self.temporal_features(spec))

        # Kategória IV: Geometriai forma
        features.extend(self.geometric_features(spec))

        # Kategória V: Wavelet
        features.extend(self.wavelet_features(spec))

        # Kategória VI: Textúra
        features.extend(self.texture_features(spec))

        return np.asarray(features, dtype=float)

    def basic_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória I – Alapvető intenzitás-jellemzők.

        F1: max intensity
        F2: mean intensity
        F3: std intensity
        F4: dynamic range (dB, stabilizált)
        F5: entropy (stabilizált)
        F6: contrast (stabilizált)
        """
        eps = 1e-8  # numerikus stabilitási konstans

        # Alap statisztikák
        max_val = float(np.max(spec))
        mean_val = float(np.mean(spec))
        std_val = float(np.std(spec))
        min_val = float(np.min(spec))

        # F4: dynamic range [dB] – elkerüljük a log(0)-t
        dynamic_range = 20.0 * np.log10((max_val + eps) / (min_val + eps))

        # F5: entropy – normalizált, pozitív eloszlásból
        flat = spec.flatten().astype(float)
        flat = flat + eps          # mindenhol > 0
        flat = flat / np.sum(flat) # normált eloszlás
        entropy = float(stats.entropy(flat))

        # F6: contrast – elkerüljük az osztást 0-val
        contrast = (max_val - mean_val) / (max_val + mean_val + eps)

        return [
            max_val,       # F1
            mean_val,      # F2
            std_val,       # F3
            dynamic_range, # F4
            entropy,       # F5
            contrast       # F6
        ]
