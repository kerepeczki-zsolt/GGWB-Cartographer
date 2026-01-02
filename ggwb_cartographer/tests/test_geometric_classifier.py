import numpy as np
from ggwb_cartographer.models.geometric import GeometricClassifier

def test_geometric_classifier_basic_fit_and_predict():
    clf = GeometricClassifier()

    # Dummy tanító adat (10 minta, 92 jellemző)
    X_train = np.random.rand(10, 92)
    y_train = np.random.randint(0, 2, size=10)

    clf.fit(X_train, y_train)

    # Dummy teszt adat (5 minta)
    X_test = np.random.rand(5, 92)
    y_pred = clf.predict(X_test)

    # Ellenőrzés
    assert isinstance(y_pred, np.ndarray)
    assert len(y_pred) == 5
