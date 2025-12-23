"""
GGWB-Térképész – Alap adatbetöltő modul.

Feladat:
- CSV vagy hasonló táblázatos metaadat-fájlok beolvasása (pl. LIGO training set).
- Alap szűrések és oszlop-választás.
- Az adatok előkészítése további feature-képzéshez és modellezéshez.

A modul úgy van megírva, hogy Google Colab-ban is egyszerűen importálható legyen:
from src.data_loader import load_metadata
"""

from __future__ import annotations

import os
from typing import List, Optional

import pandas as pd


def load_metadata(
    path: str,
    use_columns: Optional[List[str]] = None,
    n_rows: Optional[int] = None,
) -> pd.DataFrame:
    """
    Metaadat-fájl beolvasása (pl. LIGO trainingset CSV).

    Paraméterek
    ----------
    path : str
        A bemeneti fájl elérési útja (relatív vagy abszolút).
    use_columns : list[str], opcionális
        Ha meg van adva, csak ezeket az oszlopokat tartja meg.
    n_rows : int, opcionális
        Ha meg van adva, csak az első n sor kerül beolvasásra
        (gyors próba-futtatásokhoz hasznos).

    Visszatérés
    -----------
    pd.DataFrame
        A beolvasott (és opcionálisan szűrt) adatok.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"A megadott fájl nem létezik: {path}")

    df = pd.read_csv(path, nrows=n_rows)

    if use_columns is not None:
        missing = set(use_columns) - set(df.columns)
        if missing:
            raise ValueError(
                f"A következő kért oszlopok nem találhatók a fájlban: {missing}"
            )
        df = df[use_columns]

    return df


def basic_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Egyszerű statisztikai összefoglaló egy DataFrame-ről.

    Számolja az oszlopok:
    - elemszámát,
    - hiányzó értékek számát,
    - átlagát (numerikus oszlopoknál).

    Visszatérés
    -----------
    pd.DataFrame
        Összefoglaló táblázat.
    """
    summary = pd.DataFrame(
        {
            "count": df.count(),
            "missing": df.isna().sum(),
        }
    )

    numeric_cols = df.select_dtypes(include="number").columns
    summary.loc[numeric_cols, "mean"] = df[numeric_cols].mean()

    return summary
