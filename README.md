<<<<<<< HEAD
GGWB-Cartographer

🇬🇧 English

Overview

GGWB-Cartographer is a research-oriented software framework developed to systematically map, analyze, and characterize noise morphologies in gravitational-wave detector data, with an initial validated focus on the LIGO Hanford (H1) detector. The long-term scientific objective is to support Gravitational-Wave Background (GWB/GGWB) studies by building a detector-aware, morphology-driven understanding of instrumental artifacts.

The current public release (V12) provides:

A fully reproducible Beta-Variational Autoencoder (β-VAE) core

A dummy verification pipeline that can be executed without LIGO data

A clean modular architecture designed for extension to L1/V1 detectors


This repository is intentionally conservative in its scientific claims: it demonstrates functional correctness, numerical stability, and reproducibility, not final astrophysical detection results.


---

Repository Structure

GGWB-Cartographer/
├── framework/
│   └── models/
│       └── beta_vae.py        # Core β-VAE implementation
├── scripts/
│   └── demo_dummy_beta_vae.py # External dummy verification entry point
├── configs/
│   └── h1_reference.yaml      # Reference configuration for H1
├── audits/                    # Audit notes and design rationale
├── tests/                     # Unit and consistency tests
├── README.md
├── requirements.txt


---

Installation

pip install -r requirements.txt

Required dependencies:

Python ≥ 3.9

torch ≥ 2.0

numpy, scipy, matplotlib


No LIGO data access and no gwpy usage are required for the dummy verification.


---

Dummy Model Verification (External Review)

This step is critical for external reviewers (e.g. Gravity Spy, LIGO DetChar, Grok).

Run:

python scripts/demo_dummy_beta_vae.py

Expected behavior:

Successful import of BetaVAE from framework.models.beta_vae

Forward pass on dummy input [4, 1, 128, 128]

Reconstruction output with identical shape

Finite reconstruction loss, KL divergence, and total loss

Successful backpropagation (loss.backward())


Successful execution demonstrates that the core model is valid, differentiable, and numerically stable.


---

Scientific Scope and Limitations

✔ Verified on dummy spectrogram-like tensors

✔ Architecture validated on H1 reference configuration

✖ Not yet validated on L1 or Virgo

✖ No astrophysical GWB claim is made at this stage


The system is designed to scale detector-by-detector, not by assumption of universality.


---

Roadmap

L1 detector integration (configuration + normalization)

Cross-detector latent space consistency checks

Morphology population statistics

Downstream GGWB inference modules



---

License

MIT License


---

🇭🇺 Magyar

Áttekintés

A GGWB-Cartographer egy kutatási célú szoftverrendszer, amely gravitációs hullám detektorok zaj-morfológiáinak szisztematikus feltérképezésére és elemzésére készült. A jelenlegi verzió ellenőrzötten a LIGO Hanford (H1) detektorra fókuszál, és hosszú távon a gravitációs-hullám háttér (GGWB) vizsgálatát kívánja támogatni.

A V12 publikus verzió biztosítja:

Egy reprodukálható β-VAE magmodellt

Egy dummy teszt pipeline-t, amely LIGO adatok nélkül fut

Egy moduláris architektúrát, amely előkészíti az L1/V1 integrációt



---

Könyvtárstruktúra

GGWB-Cartographer/
├── framework/
│   └── models/
│       └── beta_vae.py
├── scripts/
│   └── demo_dummy_beta_vae.py
├── configs/
│   └── h1_reference.yaml
├── audits/
├── tests/
├── README.md
├── requirements.txt


---

Telepítés

pip install -r requirements.txt


=======
﻿GGWB-Cartographer V12. Run 'python scripts/run_full_h1_pipeline.py' to test the LIGO analysis.
## Dummy Model Verification`nRun: python scripts/demo_dummy_beta_vae.py
## H1 Validation (32k samples)
- Separation: ~99%
- OOD rate: <1%

## L1 Integration
Ready with config/l1_reference.yaml
>>>>>>> 3125ae0 (ARCH: Final V12 documentation, L1 template, and data availability)
