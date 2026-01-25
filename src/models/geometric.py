import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def build_geometric_classifier(input_dim=92, num_classes=27):
    """
    Geometriai / 92-feature alapú osztályozó.
    Implementáció: doku 5.x (geometrikus modell) alapján.
    """
    model = Sequential()
    model.add(Dense(256, activation="relu", input_shape=(input_dim,)))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))
    return model
