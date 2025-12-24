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

def test_F1_F6_basic(zero_spectrum, constant_spectrum, single_peak_spectrum):
    """F1-F6 alapvető jellemzők."""
    assert extractor.F1_max_intensity(zero_spectrum) == 0.0
    assert abs(extractor.F2_mean_intensity(constant_spectrum) - 0.5) < 1e-10
    assert abs(extractor.F3_std_intensity(constant_spectrum)) < 1e-10
    assert extractor.F4_dynamic_range(single_peak_spectrum) > 50

def test_F7_F10_spectral_stats(single_peak_spectrum):
    """F7-F10 spektrális statisztikák."""
    fc = extractor.F7_frequency_centroid(single_peak_spectrum)
    assert abs(fc - 32) < 1
    spread = extractor.F8_spectral_spread(single_peak_spectrum)
    assert spread < 1

def test_F11_peak_freq(single_peak_spectrum):
    """F11 csúcs frekvencia."""
    peak_f = extractor.F11_peak_frequency(single_peak_spectrum)
    assert abs(peak_f - 32) < 1

def test_F12_rolloff(chirp_spectrum):
    """F12 roll-off frekvencia."""
    rolloff = extractor.F12_spectral_rolloff(chirp_spectrum, rolloff_ratio=0.85)
    assert 40 < rolloff < 55

def test_F13_hnr_powerline(powerline_spectrum):
    """F13 HNR powerline."""
    hnr = extractor.F13_harmonic_to_noise_ratio(powerline_spectrum)
    assert hnr > -10.0

def test_F14_flatness(constant_spectrum):
    """F14 spektrális laposság - csak konstans spektum."""
    flat_const = extractor.F14_spectral_flatness(constant_spectrum)
    assert 0.9 < flat_const < 1.1, f"Flatness: {flat_const}"

def test_extract_all_features(single_peak_spectrum):
    """F1-F14 teljes vektor."""
    features = extractor.extract_all_features(single_peak_spectrum)
    assert len(features) == 14
    assert all(np.isfinite(f) for f in features)

def test_validate_errors():
    """Input validáció hibák."""
    with pytest.raises(ValueError):
        extractor._validate_spectrogram(None)
    with pytest.raises(ValueError):
        extractor._validate_spectrogram(np.array([1]))
    with pytest.raises(ValueError):
        extractor._validate_spectrogram(np.array([[np.nan]]))
def test_F15_F22_temporal(single_peak_spectrum, powerline_spectrum):
    """F15-F22 időtartomány jellemzők."""
    
    # Egyetlen csúcs: időbeli centroid ≈ 64 (közép)
    tc = extractor.F15_temporal_centroid(single_peak_spectrum)
    assert abs(tc - 64) < 5, f"Temporal centroid: {tc}"
    
    # Powerline: széles időbeli energiaeloszlás → nagy spread
    spread = extractor.F16_temporal_spread(powerline_spectrum)
    assert spread > 20, "Powerline: nagy időbeli spread"
def test_F23_F34_shape(single_peak_spectrum):
    """F23-F34 alakjellemzők."""
    
    # F23 – terület > 0
    area = extractor.F23_spectrogram_area(single_peak_spectrum)
    assert area > 0, f"Terület hibás: {area}"
    
    # F26 – excentricitás 0 és 1 között
    ecc = extractor.F26_eccentricity(single_peak_spectrum)
    assert 0 <= ecc <= 1, f"Excentricitás hibás: {ecc}"
def test_F35_F48_texture(single_peak_spectrum, constant_spectrum):
    """F35-F48 textúrajellemzők."""
    
    # Konstans: magas homogenitás
    homo = extractor.F36_glcm_homogeneity(constant_spectrum)
    assert homo > 0.1, f"Homogenitás: {homo}"
    
    # Csúcs: pozitív energia
    energy = extractor.F37_glcm_energy(single_peak_spectrum)
    assert energy >= 0.0, f"GLCM energia: {energy}"
    
    # Mindig véges értékek
    features = extractor.extract_texture_features(single_peak_spectrum)
    assert len(features) == 14
    assert all(np.isfinite(f) for f in features)
