import numpy as np
import pytest
from src.feature_extraction.geometric_features import GeometricFeatureExtractor

extractor = GeometricFeatureExtractor()


@pytest.fixture
def zero_spectrum():
    return np.zeros((64, 128))


@pytest.fixture
def constant_spectrum():
    return np.ones((64, 128)) * 0.5


@pytest.fixture
def single_peak_spectrum():
    spec = np.zeros((64, 128))
    spec[32, 64] = 1.0
    return spec


@pytest.fixture
def chirp_spectrum():
    spec = np.zeros((64, 128))
    for t in range(128):
        f = int(10 + 40 * t / 128)
        if 0 <= f < 64:
            spec[f, t] = 0.9
    return spec


def test_extract_all_features_shape(single_peak_spectrum):
    """Check that extract_all_features returns exactly 92 features."""
    features = extractor.extract_all_features(single_peak_spectrum)
    assert isinstance(features, np.ndarray)
    assert features.shape == (92,)


def test_basic_features_finite(single_peak_spectrum):
    """F1–F6 should be finite."""
    f = extractor.basic_features(single_peak_spectrum)
    assert len(f) == 6
    assert all(np.isfinite(v) for v in f)


def test_frequency_features_finite(single_peak_spectrum):
    """F7–F22 should be finite."""
    f = extractor.frequency_features(single_peak_spectrum)
    assert len(f) == 16
    assert all(np.isfinite(v) for v in f)


def test_temporal_features_finite(single_peak_spectrum):
    """F23–F44 should be finite."""
    f = extractor.temporal_features(single_peak_spectrum)
    assert len(f) == 22
    assert all(np.isfinite(v) for v in f)


def test_geometric_features_finite(single_peak_spectrum):
    """F45–F56 should be finite."""
    f = extractor.geometric_features(single_peak_spectrum)
    assert len(f) == 12
    assert all(np.isfinite(v) for v in f)


def test_wavelet_features_finite(single_peak_spectrum):
    """F57–F81 should be finite."""
    f = extractor.wavelet_features(single_peak_spectrum)
    assert len(f) == 25
    assert all(np.isfinite(v) for v in f)


def test_texture_features_finite(single_peak_spectrum):
    """F82–F92 should be finite."""
    f = extractor.texture_features(single_peak_spectrum)
    assert len(f) == 11
    assert all(np.isfinite(v) for v in f)


def test_zero_spectrum(zero_spectrum):
    """Zero spectrum should not break anything."""
    f = extractor.extract_all_features(zero_spectrum)
    assert f.shape == (92,)
    assert all(np.isfinite(v) or v == 0 for v in f)
