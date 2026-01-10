import numpy as np
from feature_extraction.geometric_features import GeometricFeatureExtractor

def test_feature_extractor_output_shape():
    extractor = GeometricFeatureExtractor()
    spec = np.random.rand(64, 64)

    result = extractor.extract_all_features(spec)

    assert isinstance(result, np.ndarray)
    assert result.shape == (92,)
    assert np.all(np.isfinite(result))
