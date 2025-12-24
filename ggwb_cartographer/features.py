A.1 Geometric Feature Extractor

```python
import numpy as np
import cv2
from scipy import stats
from skimage.feature import greycomatrix, greycoprops

class GeometricFeatureExtractor:
    def __init__(self):
        self.feature_count = 92

    def extract_all_features(self, spectrogram):
        features = []

        # Kategória I: Alapvető jellemzők
        features.extend(self.basic_features(spectrogram))

        # Kategória II: Frekvencia domain  
        features.extend(self.frequency_features(spectrogram))

        # Kategória III: Időbeli domain
        features.extend(self.temporal_features(spectrogram))

        # Kategória IV: Geometriai forma
        features.extend(self.geometric_features(spectrogram))

        # Kategória V: Wavelet
        features.extend(self.wavelet_features(spectrogram))

        # Kategória VI: Textúra
        features.extend(self.texture_features(spectrogram))

        return np.array(features)

    def basic_features(self, spec):
        return [
            np.max(spec),           # F1: max intensity
            np.mean(spec),          # F2: mean intensity  
            np.std(spec),           # F3: std intensity
            20*np.log10(np.max(spec)/np.min(spec)), # F4: dynamic range
            stats.entropy(spec.flatten()), # F5: entropy
            (np.max(spec)-np.mean(spec))/(np.max(spec)+np.mean(spec)) # F6: contrast
        ]
```

