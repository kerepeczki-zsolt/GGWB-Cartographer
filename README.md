GGWB-Cartographer

Gravitational-Wave Glitch & Background Cartography Framework


---

English version 🇬🇧

Overview

GGWB-Cartographer is a research-oriented framework for unsupervised gravitational-wave noise morphology analysis.
Its primary goal is not gravitational-wave detection, but systematic characterization and cartography of detector noise, with a particular focus on:

glitch morphology,

latent-space structure of detector noise,

identification of unknown or rare noise populations,

data quality support for GGWB / SGWB searches.


The framework is currently validated on LIGO Hanford (H1) data only.

> ⚠️ This project does not replace official LIGO/Virgo pipelines and does not claim 100% classification accuracy.




---

Scientific Motivation

Searches for stochastic or gravitational-wave backgrounds (GGWB/SGWB) are extremely sensitive to subtle, persistent noise structures.
Traditional glitch catalogs and supervised classifiers are limited by predefined labels.

GGWB-Cartographer addresses this by:

learning a latent morphology map of detector noise using a β-VAE,

constructing an unsupervised noise atlas,

flagging out-of-distribution or unknown patterns,

enabling systematic audits and blind tests.



---

Current Scope (Important)

✅ Detector: LIGO Hanford (H1) only

❌ Not a GW detection pipeline

❌ Not a real-time system

❌ No astrophysical claims


Multi-detector support (L1, V1) is planned after independent per-detector validation.


---

Repository Structure

GGWB-Cartographer/
├── framework/
│   ├── models/
│   │   └── beta_vae.py          # Core β-VAE architecture
│   └── core/
│       └── training_engine.py   # Training and embedding logic
│
├── pipeline/
│   └── __init__.py              # Pipeline hooks (future expansion)
│
├── configs/
│   └── h1_reference.yaml        # H1-specific configuration
│
├── audits/
│   ├── stress_test.py           # Stress and robustness tests
│   └── real_data_audit.py       # Real H1 data audit
│
├── tests/
│   └── total_blind_test.py      # Fully blind validation
│
├── requirements.txt
├── .gitignore
└── README.md


---

Installation

Python ≥ 3.9 recommended.

git clone https://github.com/kerepeczki-zsolt/GGWB-Cartographer.git
cd GGWB-Cartographer
pip install -r requirements.txt


---

Configuration

All detector-specific parameters are defined via YAML files.

Example (H1):

configs/h1_reference.yaml

This includes:

sample rate assumptions,

segment lengths,

latent dimension,

training hyperparameters,

safety thresholds.



---

Training the β-VAE (H1)

python framework/core/training_engine.py \
    --config configs/h1_reference.yaml

This step learns the latent morphology space from H1 noise data.


---

Running Audits

Stress test:

python audits/stress_test.py \
    --config configs/h1_reference.yaml

Real data audit:

python audits/real_data_audit.py \
    --config configs/h1_reference.yaml


---

Blind Validation

python tests/total_blind_test.py \
    --config configs/h1_reference.yaml

This test evaluates the system on previously unseen data segments.


---

Output & Interpretation

The framework produces:

latent embeddings,

anomaly / unknown flags,

internal diagnostic metrics.


Interpretation is statistical and morphological, not astrophysical.


---

Limitations

Single-detector only (H1)

No calibrated strain inference

No detection claims

Research-stage code



---

License

MIT License


---

Acknowledgments

Inspired by the Gravity Spy project and LIGO detector characterization efforts.


---


---

Magyar verzió 🇭🇺

Áttekintés

A GGWB-Cartographer egy kutatási célú rendszer, amely gravitációs hullám detektorok zajának morfológiai feltérképezésére szolgál.

A rendszer célja nem gravitációs hullámok detektálása, hanem:

zajtípusok struktúrájának feltárása,

látens térben megjelenő mintázatok elemzése,

ismeretlen zajformák azonosítása,

adatminőség javítása GGWB / SGWB keresések előtt.


A jelenlegi verzió kizárólag a LIGO Hanford (H1) detektorra van validálva.


---

Tudományos háttér

A háttérgravitációs hullám keresések rendkívül érzékenyek a finom, nem-triviális zajmintázatokra.
A felügyelt osztályozás gyakran nem képes új vagy ritka zajformák kezelésére.

A GGWB-Cartographer:

β-VAE segítségével tanul látens zajtérképet,

zajatlaszt épít,

ismeretlen mintákat jelöl,

vaktesztekkel ellenőrzi a stabilitást.



---

Jelenlegi hatókör

✅ Detektor: H1

❌ Nem detekciós pipeline

❌ Nem real-time

❌ Nem asztrofizikai állítás



---

Telepítés

git clone https://github.com/kerepeczki-zsolt/GGWB-Cartographer.git
cd GGWB-Cartographer
pip install -r requirements.txt


---

Tréning (H1)

python framework/core/training_engine.py \
    --config configs/h1_reference.yaml


---

Audit és vakteszt

python audits/stress_test.py --config configs/h1_reference.yaml
python tests/total_blind_test.py --config configs/h1_reference.yaml


---

Korlátok

Egyetlen detektor

Kutatási fázis

Nem helyettesít hivatalos LIGO pipeline-okat



