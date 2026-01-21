import numpy as np
from src.models.geometric import build_geometric_classifier
from src.models.resnet50 import build_resnet50_classifier

def test_geometric_model_builds():
    model = build_geometric_classifier()
    assert model is not None
    assert len(model.layers) > 0

def test_resnet50_model_builds():
    model = build_resnet50_classifier()
    assert model is not None
    assert len(model.layers) > 0

def test_geometric_model_predicts():
    model = build_geometric_classifier()
    X = np.random.rand(2, 92)
    y = model.predict(X)
    assert y.shape == (2, 27)

def test_resnet50_model_predicts():
    model = build_resnet50_classifier()
    X = np.random.rand(2, 224, 224, 3)
    y = model.predict(X)
    assert y.shape == (2, 27)
