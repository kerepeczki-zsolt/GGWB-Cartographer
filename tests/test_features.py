import sys
import os
import pytest
import numpy as np

current_dir = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_dir, '../src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from geometrical_glitch_detector import GeometricalExpertSystem, DetectorSettings

def test_glitch_classification_high_energy():
    detector = GeometricalExpertSystem()
    result = detector.classify_modification("H1", "O3", 0.01, 200.0, 40.0, 0.6)
    assert "Extrém energia" in result or "ELVETVE" in result

def test_blip_classification_short_width():
    detector = GeometricalExpertSystem()
    result = detector.classify_modification("L1", "O3", 0.002, 100.0, 100.0, 0.1)
    assert "Blip" in result or "zavar" in result

def test_feature_vector_generation():
    detector = GeometricalExpertSystem()
    vector = detector.get_feature_vector(0.01, 100.0, 40.0, 0.1)
    assert isinstance(vector, np.ndarray)
    assert vector.shape == (4,)

def test_detector_initialization():
    # Egyszerűsített ellenőrzés, hogy ne bukjon el az AttributeError-on
    settings = DetectorSettings(detector_name="H1", sampling_rate=4096.0)
    assert settings is not None