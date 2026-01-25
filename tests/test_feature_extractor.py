import pytest
import numpy as np
import sys
import os

# src mappa elérhetővé tétele
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from feature_extraction.geometric_features import GeometricFeatureExtractor

def test_initialization():
    extractor = GeometricFeatureExtractor()
    assert extractor.feature_count == 92

def test_extraction_values():
    extractor = GeometricFeatureExtractor()
    dummy_spec = np.zeros((100, 100))
    features = extractor.extract_all_features(dummy_spec)
    assert all(isinstance(f, float) for f in features)
