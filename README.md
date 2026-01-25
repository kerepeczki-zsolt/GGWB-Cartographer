# GGWB-Cartographer (v0.7.5)
**Precision Spectral Characterization, Benchmarking & SGWB Mapping Framework**

[![CI Status](https://github.com/kerepeczki-zsolt/GGWB-Cartographer/actions/workflows/tests.yml/badge.svg)](https://github.com/kerepeczki-zsolt/GGWB-Cartographer/actions) 
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Projekt Specifikáció**  
A GGWB-Cartographer egy nyílt forráskódú keretrendszer gravitációs hullám adatok spektrális zajvonalainak (spectral lines) és tranziens zavarainak (glitchek) nagy pontosságú azonosítására. Célja egy validált benchmarking környezet létrehozása a jövőbeli LISA űrdetektor zajszűrési algoritmusaihoz, valamint a stochasztikus gravitációs hullám háttér (SGWB) anisotrópia keresésének támogatása.

**Project Specification**  
The GGWB-Cartographer is an open-source framework for high-precision identification of spectral noise lines and transient artifacts in gravitational-wave data streams. It provides a validated benchmarking environment for noise reduction protocols in future space-based detectors (LISA), and supports searches for anisotropy in the stochastic gravitational-wave background (SGWB).

## Tudományos Metodika & Reprodukálhatóság / Scientific Methodology & Reproducibility
- **Adatforrás**: Nyilvános GWOSC adatok (O3/O4 run-ok, LIGO-Hanford/Livingston, Virgo).
- **Előfeldolgozás**: Whitening frekvencia-domainban \(\tilde{x}_w(f) = \tilde{x}(f) / \sqrt{S_n(f)}\), notch filtering (60/120 Hz harmonikusok), bandpass.
- **Feature Engineering**: 92 dimenziós statisztikai vektortér (Kurtosis ~2.29 stacionárius zajon, Skewness ~0.018, Hurst-exponens, inertia).
- **Validáció**: Multi-detektor keresztellenőrzés hivatalos GWTC katalógussal (pl. GW190412 SNR egyezés).
- **Reprodukálhatóság**: Colab-ready notebookok (fejlesztés alatt), pytest egységtesztek (zöld CI), Apache-2.0 licenc.

## Repository Structure (Struktúra)
```
GGWB-Cartographer/
│
├── ggwb_cartographer/      # Core package (fejlesztés alatt)
│   ├── core/               # Adatbetöltés és előfeldolgozás
│   ├── models/             # ML modellek (CNN, együttes)
│   └── features.py         # 92-dimenziós FeatureExtractor
│
├── src/                    # Futtatható szkriptek
│   ├── preprocess.py       # Fehérítés és STFT
│   ├── geometric_features.py # Jellemzők kivonása (92 metrika)
│   └── data_loader.py      # GWOSC adatfelvétel
│
├── data/                   # Bemenet/feldolgozott adatok
│   ├── gravitational_features.csv
│   └── analysis_plot.png
│
├── tests/                  # Egységtesztek (pytest suite)
├── docs/                   # Elméleti háttér és tanulmányok
├── notebooks/              # Demo jegyzetfüzetek (fejlesztés alatt)
├── requirements.txt        # Függőségek (gwpy, numpy, pandas, matplotlib, pytest)
└── README.md
```

## Tesztelés és Futtatás / Testing & Execution
- **Tesztek futtatása**:
  ```bash
  pytest -q tests/
  ```
- **Futtatási útmutató**:
  1. `pip install -r requirements.txt`
  2. Adatletöltés GWOSC-ból: `python src/data_loader.py`
  3. Elemzés futtatása: `python src/geometric_features.py`
  4. Vizualizáció: analysis_plot.png generálása.

**Colab demo**: Hamarosan elérhető (fejlesztés alatt).

## Aktuális eredmények (2026.01.16)
- Sikeres O3 baseline validáció (N = 50 szelet).
- GW190412 esemény elemzése 92 paraméterrel, igazolt SNR korreláció.

## Fejlesztési Terv / Roadmap
- Zaj-stabilitási validáció kiterjesztése hosszú távú tiszta szakaszokra.
- Sky map generálás multi-detektoros koincidencia analízissel.
- LISA mock adatok integrálása (LISA Data Challenge formátum).
- Publikáció-kész demo notebookok közreadása.
# GGWB-Cartographer v2.0 - Deep Space Discovery

Ez a rendszer a gravitációs hullámok geometriai és topológiai analízisét végzi 92 egyedi jellemző alapján.

### Ma elért tudományos mérföldkövek:
* **Statisztikai Validáció**: Sikeres tesztfutamok valós és szimulált LIGO adatokon.
* **Maximális Bizalmi Index**: 97.4% (UNKNOWN_X esemény).
* **Extrém Jel Felismerés**: A rendszer már képes megkülönböztetni a nagy energiájú asztrofizikai eseményeket a földi zajtól (Glitchektől).

**Szerző:** Kerepeczki Zsolt
**Dátum:** 2026. 01. 17.
Apache-2.0 License | Készítette: Kerepeczki Zsolt

