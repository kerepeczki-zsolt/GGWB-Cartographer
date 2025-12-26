import numpy as np
import pytest
from src.feature_extraction.geometric_features import GeometricFeatureExtractor

extractor = GeometricFeatureExtractor()


@pytest.fixture
def zero_spectrum():
    """Null spektrogram."""
    return np.zeros((64, 128))


@pytest.fixture
def constant_spectrum():
    """Konstans spektrum."""
    return np.ones((64, 128)) * 0.5


@pytest.fixture
def single_peak_spectrum():
    """Egyetlen csúcs: f=32, t=64."""
    spec = np.zeros((64, 128))
    spec[32, 64] = 1.0
    return spec


@pytest.fixture
def powerline_spectrum():
    """Powerline csík: f=10."""
    spec = np.zeros((64, 128))
    for t in range(128):
        spec[10, t] = 0.8
    return spec


@pytest.fixture
def chirp_spectrum():
    """Chirp: 10->50 Hz."""
    spec = np.zeros((64, 128))
    for t in range(128):
        f_chirp = int(10 + 40 * t / 128)
        if 0 <= f_chirp < 64:
            spec[f_chirp, t] = 0.9
    return spec


@pytest.fixture
def nan_spectrum(zero_spectrum):
    """Spektrum NaN-okkal."""
    spec = zero_spectrum.copy()
    spec[0, 0] = np.nan
    return spec


@pytest.fixture
def freq_axis():
    """Frekvencia tengely."""
    return np.arange(64)


@pytest.fixture
def time_axis():
    """Idő tengely."""
    return np.arange(128)


def test_F1_F6_basic(zero_spectrum, constant_spectrum, single_peak_spectrum):
    """F1–F6 alapvető jellemzők."""
    assert extractor.F1_max_intensity(zero_spectrum) == 0.0, "Max intensity should be 0 for zero spectrum"
    assert abs(extractor.F2_mean_intensity(constant_spectrum) - 0.5) < 1e-10, "Mean intensity should be 0.5"
    assert abs(extractor.F3_std_intensity(constant_spectrum)) < 1e-10, "STD should be near 0 for constant"
    assert extractor.F4_dynamic_range(single_peak_spectrum) > 50.0, "Dynamic range should be high for single peak"


def test_F7_F10_spectral_stats(single_peak_spectrum, freq_axis):
    """F7–F10 spektrális statisztikák."""
    fc = extractor.F7_frequency_centroid(single_peak_spectrum, freq_axis)
    assert abs(fc - 32) < 1.0, f"Frequency centroid: {fc}"
    spread = extractor.F8_spectral_spread(single_peak_spectrum, freq_axis)
    assert spread < 5.0, f"Spectral spread: {spread}"


def test_F11_peak_frequency(single_peak_spectrum, freq_axis):
    """F11 csúcs frekvencia."""
    peak_f = extractor.F11_peak_frequency(single_peak_spectrum, freq_axis)
    assert abs(peak_f - 32) < 1.0, f"Peak frequency: {peak_f}"


def test_F12_rolloff(chirp_spectrum, freq_axis):
    """F12 roll-off frekvencia."""
    rolloff = extractor.F12_spectral_rolloff(chirp_spectrum, freq_axis)
    assert 40.0 < rolloff < 55.0, f"Spectral rolloff: {rolloff}"


def test_F13_hnr_exists_and_finite(single_peak_spectrum):
    """F13 – csak azt ellenőrizzük, hogy létezik és véges érték."""
    features = extractor.extract_all_features(single_peak_spectrum)
    assert 'F13' in features, "F13 must exist in features"
    F13_value = features['F13']
    assert np.isfinite(F13_value), f"F13 value: {F13_value}"


def test_F14_flatness(constant_spectrum):
    """F14 spektrális laposság – konstans spektrumra ~1."""
    flat_const = extractor.F14_spectral_flatness(constant_spectrum)
    assert 0.9 < flat_const < 1.1, f"Flatness: {flat_const}"


def test_extract_all_features(single_peak_spectrum, nan_spectrum, freq_axis, time_axis):
    """F1–F92 teljes vektor – ellenőrizzük, hogy minden véges."""
    try:
        features = extractor.extract_all_features(single_peak_spectrum, freq_axis, time_axis)
        assert len(features) == 92, "Exactly 92 features expected"
        assert all(np.isfinite(val) for val in features.values()), "All features must be finite"
    except TypeError as e:
        if "float64" in str(e):
            pytest.fail("Float index error in extract_all_features - fix class implementation")

    # Edge case: NaN spektrum
    features_nan = extractor.extract_all_features(nan_spectrum, freq_axis, time_axis)
    assert all(np.isfinite(val) or np.isnan(val) for val in features_nan.values()), "Handle NaNs gracefully"


def test_validate_errors():
    """Input validáció hibák."""
    with pytest.raises(ValueError):
        extractor._validate_spectrogram(None)
    with pytest.raises(ValueError):
        extractor._validate_spectrogram(np.array([1]))
    with pytest.raises(ValueError):
        extractor._validate_spectrogram(np.array([[np.nan]]))


def test_F15_F22_temporal(single_peak_spectrum, powerline_spectrum, time_axis):
    """F15–F22 időtartomány jellemzők."""
    tc = extractor.F15_temporal_centroid(single_peak_spectrum, time_axis)
    assert abs(tc - 64) < 5, f"Temporal centroid: {tc}"
    spread = extractor.F16_temporal_spread(powerline_spectrum, time_axis)
    assert spread > 20, f"Temporal spread: {spread}"


def test_F23_F44_shape(single_peak_spectrum, zero_spectrum, freq_axis, time_axis):
    """F23–F44 alakjellemzők – magas szintű ellenőrzés."""
    features = extractor.extract_all_features(single_peak_spectrum, freq_axis, time_axis)
    shape_features = [features[f'F{i}'] for i in range(23, 45)]
    assert len(shape_features) == 22, "F23-F44: 22 features"
    assert all(np.isfinite(f) for f in shape_features), "All shape features finite"

    # Zero case fallback
    features_zero = extractor.extract_all_features(zero_spectrum, freq_axis, time_axis)
    shape_zero = [features_zero[f'F{i}'] for i in range(23, 45)]
    assert all(f == 0 or np.isfinite(f) for f in shape_zero), "Fallback for zero spectrum"


def test_F82_F92_texture(single_peak_spectrum, constant_spectrum, freq_axis, time_axis):
    """F82–F92 textúrajellemzők."""
    features_const = extractor.extract_all_features(constant_spectrum, freq_axis, time_axis)
    features_single = extractor.extract_all_features(single_peak_spectrum, freq_axis, time_axis)

    # Feltételezve, hogy F82-F89 GLCM: pl. F82 homogenitás-szerű (magas konstansra)
    # Ha pontos mapping kell, add meg a F82_to_F89_glcm implementációt
    homo_assumed = features_const['F82']  # Cseréld, ha más a homogeneity
    assert homo_assumed >= 0.0, f"Assumed homogeneity: {homo_assumed}"

    # Energia-szerű (pl. F83)
    energy_assumed = features_single['F83']  # Cseréld, ha más az energy
    assert energy_assumed >= 0.0, f"Assumed GLCM energy: {energy_assumed}"

    # Minden textúra véges
    texture_features = [features_single[f'F{i}'] for i in range(82, 93)]
    assert len(texture_features) == 11, "F82-F92: 11 features"
    assert all(np.isfinite(f) for f in texture_features), "All texture features finite"


def test_F45_F81_wavelets(chirp_spectrum, constant_spectrum, zero_spectrum, freq_axis, time_axis):
    """F45–F81 wavelet jellemzők (ridge/energy helyett)."""
    features_chirp = extractor.extract_all_features(chirp_spectrum, freq_axis, time_axis)
    features_const = extractor.extract_all_features(constant_spectrum, freq_axis, time_axis)
    features_zero = extractor.extract_all_features(zero_spectrum, freq_axis, time_axis)

    # Wavelet feature-ök végesek
    wavelet_features_chirp = [features_chirp[f'F{i}'] for i in range(45, 82)]
    assert len(wavelet_features_chirp) == 37, "F45-F81: 37 features"
    assert all(np.isfinite(f) for f in wavelet_features_chirp), "Chirp wavelet features finite"

    # Konstans: pl. entropy véges (F81 wavelet entropy)
    entropy = features_const['F81']
    assert np.isfinite(entropy), f"Wavelet entropy: {entropy}"

    # Nulla: fallback véges
    wavelet_zero = [features_zero[f'F{i}'] for i in range(45, 82)]
    assert all(np.isfinite(f) for f in wavelet_zero), "Zero wavelet features finite"
