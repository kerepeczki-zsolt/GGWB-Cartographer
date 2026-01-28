import os
import shutil

# Projekt gyökér könyvtárának meghatározása
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Szigorú besorolási szabályok
RULES = {
    "framework/ingestion": [
        "gw_data_fetcher.py",
        "mission_control.py",
        "data_fetcher.py",
        "get_data.py"
    ],
    "framework/preprocessing": [
        "preprocessing.py",
        "whitening_engine.py",
        "psd_analyzer.py",
        "q_transform_analyzer.py"
    ],
    "framework/morphology": [
        "geometrical_glitch_detector.py",
        "gravity_spy_brain.py",
        "fingerprint_engine.py"
    ],
    "framework/cross_detector": [
        "cross_correlator.py",
        "skymap_generator.py",
        "sky_locator.py"
    ],
    "framework/statistics": [
        "far_calculator.py",
        "event_classifier.py",
        "signal_classifier.py"
    ],
    "framework/reporting": [
        "result_visualizer.py",
        "visualizer_engine.py",
        "generate_final_report.py"
    ],
    "framework/config": [
        "config_interferometers.py",
        "ggwb_config.py"
    ]
}

# Kulcsszavak az archiváláshoz
ARCHIVE_KEYWORDS = ["másolata", "backup", "old", "final", "v12", "v13"]

def ensure_dirs():
    """Létrehozza a célkönyvtárakat, ha nem léteznének."""
    for path in RULES:
        os.makedirs(os.path.join(ROOT, path), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "archive"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)

def move_file(fname, target):
    """Fájl mozgatása a célhelyre."""
    src = os.path.join(ROOT, fname)
    dst = os.path.join(ROOT, target, fname)
    if os.path.exists(src):
        print(f"MOVE: {fname} → {target}")
        shutil.move(src, dst)

def main():
    ensure_dirs()
    # Csak a gyökérben lévő .py fájlokat vizsgáljuk
    files = [f for f in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, f)) and f.endswith(".py")]

    for f in files:
        # A script saját magát ne mozgassa el futás közben
        if f == "auto_migrate_project.py":
            continue

        lower = f.lower()

        # 1. Szabály: Archiválás kulcsszavak alapján
        if any(k in lower for k in ARCHIVE_KEYWORDS):
            print(f"ARCHIVE: {f}")
            shutil.move(os.path.join(ROOT, f), os.path.join(ROOT, "archive", f))
            continue

        # 2. Szabály: Besorolás a RULES szótár alapján
        placed = False
        for target, names in RULES.items():
            if f in names:
                move_file(f, target)
                placed = True
                break

        # 3. Szabály: Ha nem tudjuk hova tenni, biztonsági okból archive/
        if not placed:
            print(f"UNCLASSIFIED → ARCHIVE: {f}")
            shutil.move(os.path.join(ROOT, f), os.path.join(ROOT, "archive", f))

    print("\n✅ MIGRÁCIÓ LEFUTOTT. A RENDSZER MODULÁRIS.")

if __name__ == "__main__":
    main()