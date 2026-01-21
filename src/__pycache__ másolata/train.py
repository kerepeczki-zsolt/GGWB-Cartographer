<<<<<<< HEAD
"""
GGWB-Térképész – Egyszerű tanító szkript.

Feladat:
- Metaadat-fájl beolvasása.
- Feature-képzés.
- MLP osztályozó modell felépítése és tanítása.
- Modell és tanítási görbe elmentése fájlba.

Megjegyzés:
- A konkrét label/osztály oszlop nevét a CSV-ben neked kell beállítani
  a LABEL_COLUMN változóban.
- A szkriptet elsősorban Google Colab / Jupyter környezetben célszerű futtatni.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.data_loader import load_metadata
from src.features import build_basic_features
from src.models import build_mlp_classifier


# ---- Konfigurálható paraméterek -------------------------------------------------

DATA_PATH = "adat/trainingset_v1d1_metadata-1.csv"  # metaadat-fájl útvonala
LABEL_COLUMN = "label"  # TODO: írd át a tényleges oszlopnévre a CSV-ben

TEST_SIZE = 0.2
RANDOM_STATE = 42
EPOCHS = 20
BATCH_SIZE = 256

HIDDEN_UNITS = [128, 64]
DROPOUT_RATE = 0.2
LEARNING_RATE = 1e-3

OUTPUT_DIR = "eredmenyek"  # ide mentjük a modellt és a history-t


# ---- Segédfüggvények ------------------------------------------------------------


def prepare_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Adatok betöltése, feature-képzés, train/val felosztás.

    Visszatérés
    -----------
    X_train, X_val, y_train, y_val : np.ndarray
    """
    df = load_metadata(DATA_PATH)

    if LABEL_COLUMN not in df.columns:
        raise ValueError(
            f"A LABEL_COLUMN ({LABEL_COLUMN}) oszlop nem található a metaadat-fájlban."
        )

    y = df[LABEL_COLUMN].values
    df_features = df.drop(columns=[LABEL_COLUMN])

    X = build_basic_features(df_features)

    X_train, X_val, y_train, y_val = train_test_split(
        X.values,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    return X_train, X_val, y_train, y_val


def ensure_output_dir(path: str | Path) -> Path:
    """
    Gondoskodik arról, hogy a kimeneti könyvtár létezzen.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---- Fő tanítási logika ---------------------------------------------------------


def main() -> None:
    """
    Teljes tanítási pipeline futtatása.
    """
    X_train, X_val, y_train, y_val = prepare_data()

    input_dim = X_train.shape[1]

    model = build_mlp_classifier(
        input_dim=input_dim,
        hidden_units=HIDDEN_UNITS,
        dropout_rate=DROPOUT_RATE,
        learning_rate=LEARNING_RATE,
        output_activation="sigmoid",
        n_outputs=1,
    )

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
    )

    out_dir = ensure_output_dir(OUTPUT_DIR)

    # Modell mentése
    model_path = out_dir / "ggwb_mlp_classifier.keras"
    model.save(model_path)

    # Tanítási history mentése JSON-be
    hist_dict = history.history
    history_path = out_dir / "training_history.json"
    with history_path.open("w", encoding="utf-8") as f:
        json.dump(hist_dict, f, ensure_ascii=False, indent=2)

    print(f"Modell elmentve ide: {model_path}")
    print(f"Tanítási history elmentve ide: {history_path}")


if __name__ == "__main__":
    main()
=======
"""
GGWB-Térképész – Egyszerű tanító szkript.

Feladat:
- Metaadat-fájl beolvasása.
- Feature-képzés.
- MLP osztályozó modell felépítése és tanítása.
- Modell és tanítási görbe elmentése fájlba.

Megjegyzés:
- A konkrét label/osztály oszlop nevét a CSV-ben neked kell beállítani
  a LABEL_COLUMN változóban.
- A szkriptet elsősorban Google Colab / Jupyter környezetben célszerű futtatni.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.data_loader import load_metadata
from src.features import build_basic_features
from src.models import build_mlp_classifier


# ---- Konfigurálható paraméterek -------------------------------------------------

DATA_PATH = "adat/trainingset_v1d1_metadata-1.csv"  # metaadat-fájl útvonala
LABEL_COLUMN = "label"  # TODO: írd át a tényleges oszlopnévre a CSV-ben

TEST_SIZE = 0.2
RANDOM_STATE = 42
EPOCHS = 20
BATCH_SIZE = 256

HIDDEN_UNITS = [128, 64]
DROPOUT_RATE = 0.2
LEARNING_RATE = 1e-3

OUTPUT_DIR = "eredmenyek"  # ide mentjük a modellt és a history-t


# ---- Segédfüggvények ------------------------------------------------------------


def prepare_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Adatok betöltése, feature-képzés, train/val felosztás.

    Visszatérés
    -----------
    X_train, X_val, y_train, y_val : np.ndarray
    """
    df = load_metadata(DATA_PATH)

    if LABEL_COLUMN not in df.columns:
        raise ValueError(
            f"A LABEL_COLUMN ({LABEL_COLUMN}) oszlop nem található a metaadat-fájlban."
        )

    y = df[LABEL_COLUMN].values
    df_features = df.drop(columns=[LABEL_COLUMN])

    X = build_basic_features(df_features)

    X_train, X_val, y_train, y_val = train_test_split(
        X.values,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    return X_train, X_val, y_train, y_val


def ensure_output_dir(path: str | Path) -> Path:
    """
    Gondoskodik arról, hogy a kimeneti könyvtár létezzen.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---- Fő tanítási logika ---------------------------------------------------------


def main() -> None:
    """
    Teljes tanítási pipeline futtatása.
    """
    X_train, X_val, y_train, y_val = prepare_data()

    input_dim = X_train.shape[1]

    model = build_mlp_classifier(
        input_dim=input_dim,
        hidden_units=HIDDEN_UNITS,
        dropout_rate=DROPOUT_RATE,
        learning_rate=LEARNING_RATE,
        output_activation="sigmoid",
        n_outputs=1,
    )

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
    )

    out_dir = ensure_output_dir(OUTPUT_DIR)

    # Modell mentése
    model_path = out_dir / "ggwb_mlp_classifier.keras"
    model.save(model_path)

    # Tanítási history mentése JSON-be
    hist_dict = history.history
    history_path = out_dir / "training_history.json"
    with history_path.open("w", encoding="utf-8") as f:
        json.dump(hist_dict, f, ensure_ascii=False, indent=2)

    print(f"Modell elmentve ide: {model_path}")
    print(f"Tanítási history elmentve ide: {history_path}")


if __name__ == "__main__":
    main()
>>>>>>> e93f1bf2 (Fix CI and update features)
