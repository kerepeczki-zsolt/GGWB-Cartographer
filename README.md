# 🌌 GGWB-Cartographer (v0.12.0)
**High-Precision Gravitational-Wave Transient Artifact Classification and Stochastic Background Mapping Framework**

[![Python Tests](https://github.com/kerepeczki-zsolt/GGWB-Cartographer/actions/workflows/tests.yml/badge.svg)](https://github.com/kerepeczki-zsolt/GGWB-Cartographer/actions/workflows/tests.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Project Specification (English)
The GGWB-Cartographer is an open-source Python framework for the high-precision identification, classification, and characterization of transient instrumental artifacts (glitches) in gravitational-wave strain data from ground-based detectors. The primary focus is on LIGO Hanford (H1) observations across O1, O2, O3, and O3b runs, with extensions to multi-detector coherence analysis (H1, L1, Virgo).

The framework provides reproducible tools for glitch mitigation and supports stochastic gravitational-wave background (SGWB) anisotropy studies. It is designed as a benchmarking platform for future space-based missions such as LISA.

## Projekt Specifikáció (Magyar)
A GGWB-Cartographer egy nyílt forráskódú Python keretrendszer a gravitációs hullám detektorok strain adataiban előforduló tranziens műszeres zavarok (glitchek) nagy pontosságú azonosítására, osztályozására és karakterizálására. A fő fókusz a LIGO Hanford (H1) megfigyelésein van az O1, O2, O3 és O3b futamokban, multi-detektor koherencia analízissel (H1, L1, Virgo).

A keretrendszer reprodukálható eszközöket biztosít glitch-csökkentéshez, és támogatja a stochasztikus gravitációs hullám háttér (SGWB) anisotrópia vizsgálatát. Benchmarking platformként szolgál a jövőbeli LISA űrmisszióhoz.

## Scientific Methodology
- **Data Sources**: Public GW Open Science Center (GWOSC) strain data from O1, O2, O3, and O3b observing runs (primarily H1, with multi-detector extensions).
- **Preprocessing**: Frequency-domain whitening using PSD estimation, notch filtering of known instrumental lines (60/120 Hz harmonics), and bandpass filtering.
- **Feature Extraction**: 92-dimensional statistical and geometric vector per segment (including kurtosis, skewness, Hurst exponent, spectral entropy, and inertial metrics).
- **Classification**: Hybrid statistical and machine-learning approach for transient artifact categorization.
- **Validation**: Blind testing on withheld segments; preliminary results on selected O3/O3b samples show high accuracy, with ongoing extension to injection recovery and false alarm rate estimation.

## Current Validation Results (2026.01.26)
- Successful processing and validation on H1 data from O1, O2, O3, and O3b runs.
- Preliminary blind test results: High identification accuracy on tested categories (Blip, Scattered Light, Whistle, No Glitch).
- Note: Results are preliminary; full injection recovery, false alarm rate quantification, and multi-detector benchmarking are in progress.

## Reproducibility and Execution
**Requirements**:
```bash
pip install -r requirements.txt
```
Key dependencies: gwpy, numpy, pandas, matplotlib, scipy, scikit-learn.

**Quick Start**:
```bash
python h1_super_test_v18.py
```
The script retrieves sample data from GWOSC, performs preprocessing, feature extraction, classification, and generates diagnostic outputs (CSV summaries and plots).

**Colab Demonstration**: Under development.

## Repository Structure
```
GGWB-Cartographer/
│
├── src/
│   ├── h1_super_test_v18.py      # Main analysis and validation script
│   ├── diagnostic_engine.py      # Automated pipeline engine
│   └── geometric_features.py     # 92-dimensional feature extraction
│
├── data/
│   ├── H1_O3b_mini.csv           # Sample dataset (O3b)
│   └── Super_Test_Images/        # Validation spectrograms
│
├── tests/                        # Unit tests (pytest suite)
├── requirements.txt
├── README.md
└── LICENSE (Apache-2.0)
```

## Development Roadmap
- Full injection recovery tests and false alarm rate (FAR) estimation.
- Multi-detector cross-correlation and sky localization with Healpy.
- Extension to complete O1–O4 datasets and LISA mock data integration.
- Publication-ready benchmarking against official LVK results.

This framework is under active development and intended for research purposes. Results are preliminary and subject to further validation.

Apache-2.0 License | Author: Kerepeczki Zsolt

---

**Magyar Összefoglaló**

A GGWB-Cartographer egy nyílt forráskódú Python keretrendszer a gravitációs hullám strain adatok tranziens műszeres zavarainak (glitchek) nagy pontosságú azonosítására és osztályozására. A rendszer H1 adatokat dolgoz fel az O1, O2, O3 és O3b futamokból, multi-detektor kiterjesztéssel.

**Előzetes Validáció**: Sikeres feldolgozás O1–O3b adatakon, magas azonosítási pontosság előzetes vakteszteken.

**Korlátozások**: Kis mintaméret, FAR/injection hiánya, multi-detektor teljes integráció fejlesztés alatt.

**További Fejlesztés**: Injekciós tesztek, sky map, teljes run-ok elemzése, LISA mock adatok.

Apache-2.0 Licenc | Szerző: Kerepeczki Zsolt
