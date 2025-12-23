"""
GGWB-Térképész – Alap feature-készítő modul.

Feladat:
- A metaadat DataFrame-ből modellezésre alkalmas numerikus feature-ök előállítása.
- Hiányzó értékek alap kezelése.
- Egyszerű, könnyen bővíthető pipeline létrehozása.

Használat (példa):
from src.data_loader import load_metadata
from src.features import build_basic_features

df_meta = load_metadata("adat/trainingset_v1d1_metadata-1.csv")
X = build_basic_features(df_meta)
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd


def _safe_numeric(
    df: pd.DataFrame,
    columns: List[str],
    fill_value: float = 0.0,
) -> pd.DataFrame:
    """
    Kiválaszt néhány numerikus oszlopot és gondoskodik arról,
    hogy:
    - minden érték float legyen,
    - a hiányzó értékeket egy alapértékkel (pl. 0) töltse ki.

    Ez segít abban, hogy a neurális háló modellek ne bukjanak el
    NaN vagy típus-problémák miatt.
    """
    existing = [c for c in columns if c in df.columns]
    if not existing:
        raise ValueError("Egyik kért feature-oszlop sem található a DataFrame-ben.")

    out = df[existing].astype("float32").copy()
    out = out.fillna(fill_value)

    return out


def build_basic_features(
    df_meta: pd.DataFrame,
    extra_numeric_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Alap feature-képzés GGWB-metaadatokra.

    A függvény példaként feltételez néhány tipikus LIGO-szerű mezőt,
    de úgy van megírva, hogy könnyen testre szabható legyen.

    Paraméterek
    ----------
    df_meta : pd.DataFrame
        Eredeti metaadat tábla (pl. trainingset_v1d1_metadata-1.csv beolvasva).
    extra_numeric_cols : list[str], opcionális
        További, a DataFrame-ben meglévő numerikus oszlopok nevei,
        amelyeket be szeretnél vonni a feature-készítésbe.

    Visszatérés
    -----------
    pd.DataFrame
        Modellezésre előkészített, tisztított numerikus feature-mátrix.
    """

    # Példa: tipikus mezőnevek, amelyeket érdemes lehet használni.
    # Ezeket majd a konkrét CSV oszlopneveihez igazíthatod.
    default_cols = [
        "ifo1_snr",        # detektor 1 jel-zaj arány
        "ifo2_snr",        # detektor 2 jel-zaj arány
        "delta_time",      # időeltérés a detektorok eseményei között
        "central_freq",    # központi frekvencia
        "bandwidth",       # sávszélesség
    ]

    if extra_numeric_cols is not None:
        candidate_cols = list(dict.fromkeys(default_cols + extra_numeric_cols))
    else:
        candidate_cols = default_cols

    X = _safe_numeric(df_meta, candidate_cols, fill_value=0.0)

    # Egyszerű példaként hozzáadunk néhány kombinált feature-t is.
    if {"ifo1_snr", "ifo2_snr"}.issubset(X.columns):
        X["snr_sum"] = X["ifo1_snr"] + X["ifo2_snr"]
        X["snr_diff"] = X["ifo1_snr"] - X["ifo2_snr"]

    if {"central_freq", "bandwidth"}.issubset(X.columns):
        # Normalizált sávszélesség (dimenzió nélküli mennyiség)
        with np.errstate(divide="ignore", invalid="ignore"):
            X["rel_bandwidth"] = X["bandwidth"] / X["central_freq"].replace(0, np.nan)
            X["rel_bandwidth"] = X["rel_bandwidth"].fillna(0.0)

    return X
