import numpy as np
from src.feature_extractor import CompleteFeatureExtractor

def test_feature_extractor_output_shape():
    extractor = CompleteFeatureExtractor()
    spec = np.random.rand(64, 64)
    freqs = np.linspace(0, 1, 64)
    times = np.linspace(0, 1, 64)

    result = extractor.extract_all_features(spec, freqs, times)

    assert isinstance(result, np.ndarray)
    assert result.shape == (92,)
    assert np.all(np.isfinite(result))
