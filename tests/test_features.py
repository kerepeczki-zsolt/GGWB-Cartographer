import sys
import os
import pytest
import numpy as np

# Beállítjuk az útvonalat az 'src' mappához
current_dir = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_dir, '../src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Most már be tudjuk tölteni a detektort
from geometrical_glitch_detector import GeometricalExpertSystem, DetectorSettings

def test_glitch_classification_high_energy():
    """Erős földi zavar felismerése."""
    detector = GeometricalExpertSystem()
    result = detector.classify_modification("H1", "O3", 0.01, 200.0, 40.0, 0.6)
    assert "Erős földi zavar" in result

def test_blip_classification_short_width():
    """Rövid idejű hiba (Blip) felismerése."""
    detector = GeometricalExpertSystem()
    result = detector.classify_modification("L1", "O3", 0.002, 100.0, 100.0, 0.1)
    assert "Geometriai Blip" in result

def test_feature_vector_generation():
    """Numpy vektor típus és méret ellenőrzése."""
    detector = GeometricalExpertSystem()
    vector = detector.get_feature_vector(0.01, 100.0, 40.0, 0.1)
    assert isinstance(vector, np.ndarray)
    assert vector.shape == (4,)

def test_invalid_input_validation():
    """Negatív értékekre hibát kell dobnia."""
    detector = GeometricalExpertSystem()
    with pytest.raises(ValueError):
        detector.classify_modification("H1", "O3", 0.01, 100.0, -10.0, 0.1)