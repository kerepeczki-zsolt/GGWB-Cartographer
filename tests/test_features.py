       
        import numpy as np
import math

from ggwb_cartographer.features import FeatureExtractor


# -----------------------------
# Helper: check numeric validity
# -----------------------------
def _check_numeric_list(values, expected_len):
    assert isinstance(values, list)
    assert len(values) == expected_len
    for v in values:
        assert isinstance(v, float)
        assert not math.isnan(v)
        assert math.isfinite(v)


# -----------------------------
# Geometric features tests
# -----------------------------
def test_geometric_features_random():
    extractor = FeatureExtractor()
    spec = np.random.rand(64, 64)
    result = extractor.geometric_features(spec)
    _check_numeric_list(result, 12)


def test_geometric_features_constant():
    extractor = FeatureExtractor()
    spec = np.ones((64, 64))
    result = extractor.geometric_features(spec)
    _check_numeric_list(result, 12)


def test_geometric_features_nan_input():
    extractor = FeatureExtractor()
    spec = np.full((64, 64), np.nan)
    result = extractor.geometric_features(spec)
    _check_numeric_list(result, 12)


# -----------------------------
# Wavelet features tests
# -----------------------------
def test_wavelet_features_random():
    extractor = FeatureExtractor()
    spec = np.random.rand(64, 64)
    result = extractor.wavelet_features(spec)
    _check_numeric_list(result, 25)


def test_wavelet_features_constant():
    extractor = FeatureExtractor()
    spec = np.ones((64, 64))
    result = extractor.wavelet_features(spec)
    _check_numeric_list(result, 25)


def test_wavelet_features_nan_input():
    extractor = FeatureExtractor()
    spec = np.full((64, 64), np.nan)
    result = extractor.wavelet_features(spec)
    _check_numeric_list(result, 25)


# -----------------------------
# Texture features tests
# -----------------------------
def test_texture_features_random():
    extractor = FeatureExtractor()
    spec = np.random.rand(64, 64)
    result = extractor.texture_features(spec)
    _check_numeric_list(result, 11)


def test_texture_features_constant():
    extractor = FeatureExtractor()
    spec = np.ones((64, 64))
    result = extractor.texture_features(spec)
    _check_numeric_list(result, 11)


def test_texture_features_nan_input():
    extractor = FeatureExtractor()
    spec = np.full((64, 64), np.nan)
    result = extractor.texture_features(spec)
    _check_numeric_list(result, 11)


# -----------------------------
# Full feature vector test
# -----------------------------
def test_full_feature_vector():
    extractor = FeatureExtractor()
    spec = np.random.rand(64, 64)

    # Ha van extract_all_features metódusod:
    if hasattr(extractor, "extract_all_features"):
        result = extractor.extract_all_features(spec)
        assert isinstance(result, list)
        assert len(result) == 92
        for v in result:
            assert isinstance(v, float)
            assert not math.isnan(v)
            assert math.isfinite(v)
