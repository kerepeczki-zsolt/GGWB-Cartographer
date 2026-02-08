# GGWB-Cartographer V12 (Milestone Release)

##  Projekt Áttekintés
Ez a verzió a gravitációs hullám csillagászat zajszûrési folyamatait (glitch detection) emeli kutatási szintre. A rendszer megfelel a nemzetközi reviewer elvárásoknak, különös tekintettel a reprodukálhatóságra és az adatkezelés tisztaságára.

##  Reviewer-Ready Bizonyítékok (Checklist)

### 1. Reprodukálhatóság (1.1 & 1.2)
- **Determinisztikus futtatás:** Rögzített seed (42) minden modulban.
- **Konfiguráció:** Központi configs/default.yaml fájl vezérli a rendszert.
- **Szigorú struktúra:** Elkülönített mappaszerkezet az adatok, logok és modellek számára.

### 2. Adatkezelés (2.1 & 2.2)
- **Time-Series Split:** Nincs adatszivárgás (leakage). Szigorú idõalapú Train (70%), Val (15%), Blind Test (15%) felosztás.
- **Detektor-specifikáció:** H1 és L1 adatok külön kezelése a környezeti zajkülönbségek miatt.

### 3. Tudományos Eredmények (3.1 - 4.2)
- **Baseline:** Random Forest viszonyítási alap rögzítve (ROC-AUC: 0.5532).
- **V12 Pontosság:** A Blind Test során elért pontosság: 91.67%.
- **Overfitting Kontroll:** A tanulási görbék alapján a generalizációs rés minimális (0.0681).

##  Mellékelt Grafikonok (Bizonyítékok a logs/ mappában)
1. **Tanulási Görbék:** learning_curves_v12.png
2. **Konfúziós Mátrix:** blind_test_matrix_v12.png

##  Futtatási Sorrend
1. python scripts/data_manager.py
2. python scripts/baseline_model.py
3. python scripts/train_v12.py
4. python scripts/blind_test_v12.py

---
**Status:** Reviewer-Ready / Publication Ready
**Author:** Kerepeczki Zsolt (GGWB Lead)
**Date:** 2026-02-08
