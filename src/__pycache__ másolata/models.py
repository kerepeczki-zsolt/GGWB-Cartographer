<<<<<<< HEAD
"""
GGWB-Térképész – Neurális háló modellek TensorFlow/Keras-szal.

Feladat:
- Általános, GGWB-metaadatokra alkalmas MLP (multi-layer perceptron) háló definiálása.
- Könnyen bővíthető architektúra létrehozása osztályozási vagy regressziós feladatokra.

Használat (példa):
from src.models import build_mlp_classifier

model = build_mlp_classifier(
    input_dim=X.shape[1],
    hidden_units=[128, 64],
    dropout_rate=0.2,
)
"""

from __future__ import annotations

from typing import List, Literal, Optional

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def build_mlp_classifier(
    input_dim: int,
    hidden_units: List[int] = [128, 64],
    dropout_rate: float = 0.2,
    output_activation: Literal["sigmoid", "softmax"] = "sigmoid",
    learning_rate: float = 1e-3,
    n_outputs: int = 1,
) -> keras.Model:
    """
    Többrétegű perceptron (MLP) bináris vagy többosztályos osztályozáshoz.

    Paraméterek
    ----------
    input_dim : int
        Bemeneti feature-ök száma (X oszlopainak száma).
    hidden_units : list[int]
        Rejtett rétegek neuronjainak száma rétegenként.
    dropout_rate : float
        Dropout arány a rejtett rétegek után (0–1 között).
    output_activation : {"sigmoid", "softmax"}
        Kimeneti aktiváció:
        - "sigmoid": bináris osztályozás (n_outputs=1).
        - "softmax": többosztályos osztályozás (n_outputs>=2).
    learning_rate : float
        Adam optimizátor tanulási rátája.
    n_outputs : int
        Kimeneti neuronok száma.

    Visszatérés
    -----------
    keras.Model
        Létrehozott és lefordított Keras modell.
    """
    inputs = keras.Input(shape=(input_dim,), name="features")

    x = inputs
    for i, units in enumerate(hidden_units):
        x = layers.Dense(units, activation="relu", name=f"dense_{i+1}")(x)
        x = layers.Dropout(dropout_rate, name=f"dropout_{i+1}")(x)

    outputs = layers.Dense(n_outputs, activation=output_activation, name="output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="ggwb_mlp_classifier")

    if output_activation == "sigmoid" and n_outputs == 1:
        loss = "binary_crossentropy"
        metrics = ["accuracy"]
    else:
        loss = "sparse_categorical_crossentropy"
        metrics = ["accuracy"]

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    return model


def build_mlp_regressor(
    input_dim: int,
    hidden_units: List[int] = [128, 64],
    dropout_rate: float = 0.2,
    learning_rate: float = 1e-3,
    n_outputs: int = 1,
) -> keras.Model:
    """
    Többrétegű perceptron (MLP) regressziós feladathoz
    (pl. valamilyen GGWB-intenzitás vagy paraméter becslésére).

    Paraméterek
    ----------
    input_dim : int
        Bemeneti feature-ök száma.
    hidden_units : list[int]
        Rejtett rétegek neuronjainak száma rétegenként.
    dropout_rate : float
        Dropout arány a rejtett rétegek után.
    learning_rate : float
        Adam optimizátor tanulási rátája.
    n_outputs : int
        Kimeneti neuronok száma.

    Visszatérés
    -----------
    keras.Model
        Létrehozott és lefordított Keras regressziós modell.
    """
    inputs = keras.Input(shape=(input_dim,), name="features")

    x = inputs
    for i, units in enumerate(hidden_units):
        x = layers.Dense(units, activation="relu", name=f"dense_{i+1}")(x)
        x = layers.Dropout(dropout_rate, name=f"dropout_{i+1}")(x)

    outputs = layers.Dense(n_outputs, activation="linear", name="output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="ggwb_mlp_regressor")

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

    return model
if __name__ == "__main__":
    # Teszteljük, hogy felépül-e a GGWB hálózat
    print("\n" + "="*40)
    print("   GGWB-TÉRKÉPÉSZ MODELL TESZT")
    print("="*40)
    
    # Tegyünk úgy, mintha 3 adatunk lenne (pl. terület, szög, elnyúltság)
    test_model = build_mlp_classifier(input_dim=3, n_outputs=5, output_activation="softmax")
    
    print(f"Modell neve: {test_model.name}")
    print("Bemeneti réteg: 3 paraméter (Terület, Szög, Elnyúltság)")
    print("Kimeneti réteg: 5 hiba-kategória")
    print("-" * 40)
    test_model.summary() # Ez megmutatja a hálózat szerkezetét
=======
"""
GGWB-Térképész – Neurális háló modellek TensorFlow/Keras-szal.

Feladat:
- Általános, GGWB-metaadatokra alkalmas MLP (multi-layer perceptron) háló definiálása.
- Könnyen bővíthető architektúra létrehozása osztályozási vagy regressziós feladatokra.

Használat (példa):
from src.models import build_mlp_classifier

model = build_mlp_classifier(
    input_dim=X.shape[1],
    hidden_units=[128, 64],
    dropout_rate=0.2,
)
"""

from __future__ import annotations

from typing import List, Literal, Optional

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def build_mlp_classifier(
    input_dim: int,
    hidden_units: List[int] = [128, 64],
    dropout_rate: float = 0.2,
    output_activation: Literal["sigmoid", "softmax"] = "sigmoid",
    learning_rate: float = 1e-3,
    n_outputs: int = 1,
) -> keras.Model:
    """
    Többrétegű perceptron (MLP) bináris vagy többosztályos osztályozáshoz.

    Paraméterek
    ----------
    input_dim : int
        Bemeneti feature-ök száma (X oszlopainak száma).
    hidden_units : list[int]
        Rejtett rétegek neuronjainak száma rétegenként.
    dropout_rate : float
        Dropout arány a rejtett rétegek után (0–1 között).
    output_activation : {"sigmoid", "softmax"}
        Kimeneti aktiváció:
        - "sigmoid": bináris osztályozás (n_outputs=1).
        - "softmax": többosztályos osztályozás (n_outputs>=2).
    learning_rate : float
        Adam optimizátor tanulási rátája.
    n_outputs : int
        Kimeneti neuronok száma.

    Visszatérés
    -----------
    keras.Model
        Létrehozott és lefordított Keras modell.
    """
    inputs = keras.Input(shape=(input_dim,), name="features")

    x = inputs
    for i, units in enumerate(hidden_units):
        x = layers.Dense(units, activation="relu", name=f"dense_{i+1}")(x)
        x = layers.Dropout(dropout_rate, name=f"dropout_{i+1}")(x)

    outputs = layers.Dense(n_outputs, activation=output_activation, name="output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="ggwb_mlp_classifier")

    if output_activation == "sigmoid" and n_outputs == 1:
        loss = "binary_crossentropy"
        metrics = ["accuracy"]
    else:
        loss = "sparse_categorical_crossentropy"
        metrics = ["accuracy"]

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    return model


def build_mlp_regressor(
    input_dim: int,
    hidden_units: List[int] = [128, 64],
    dropout_rate: float = 0.2,
    learning_rate: float = 1e-3,
    n_outputs: int = 1,
) -> keras.Model:
    """
    Többrétegű perceptron (MLP) regressziós feladathoz
    (pl. valamilyen GGWB-intenzitás vagy paraméter becslésére).

    Paraméterek
    ----------
    input_dim : int
        Bemeneti feature-ök száma.
    hidden_units : list[int]
        Rejtett rétegek neuronjainak száma rétegenként.
    dropout_rate : float
        Dropout arány a rejtett rétegek után.
    learning_rate : float
        Adam optimizátor tanulási rátája.
    n_outputs : int
        Kimeneti neuronok száma.

    Visszatérés
    -----------
    keras.Model
        Létrehozott és lefordított Keras regressziós modell.
    """
    inputs = keras.Input(shape=(input_dim,), name="features")

    x = inputs
    for i, units in enumerate(hidden_units):
        x = layers.Dense(units, activation="relu", name=f"dense_{i+1}")(x)
        x = layers.Dropout(dropout_rate, name=f"dropout_{i+1}")(x)

    outputs = layers.Dense(n_outputs, activation="linear", name="output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="ggwb_mlp_regressor")

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

    return model
if __name__ == "__main__":
    # Teszteljük, hogy felépül-e a GGWB hálózat
    print("\n" + "="*40)
    print("   GGWB-TÉRKÉPÉSZ MODELL TESZT")
    print("="*40)
    
    # Tegyünk úgy, mintha 3 adatunk lenne (pl. terület, szög, elnyúltság)
    test_model = build_mlp_classifier(input_dim=3, n_outputs=5, output_activation="softmax")
    
    print(f"Modell neve: {test_model.name}")
    print("Bemeneti réteg: 3 paraméter (Terület, Szög, Elnyúltság)")
    print("Kimeneti réteg: 5 hiba-kategória")
    print("-" * 40)
    test_model.summary() # Ez megmutatja a hálózat szerkezetét
>>>>>>> e93f1bf2 (Fix CI and update features)
    print("="*40 + "\n")