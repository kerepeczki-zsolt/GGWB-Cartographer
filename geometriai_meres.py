import os
import numpy as np
import json
from PIL import Image
from scipy.stats import skew, kurtosis

# ====================================================
# GGWB-CARTOGRAPHER: PONTOS GEOMETRIAI ÖSSZEHASONLÍTÓ
# ====================================================

# Konfiguráció
BASE_PATH = r'data\O3'
DETECTOR = 'H1'

def meres():
    # 1. A 364 képből gyúrt átlagértékek betöltése
    try:
        with open('no_glitch_reference.json', 'r') as f:
            ref = json.load(f)
    except FileNotFoundError:
        print("HIBA: Nincs meg a referencia! Futtasd a generátort.")
        return

    susp_dir = os.path.join(BASE_PATH, DETECTOR, 'processed', 'suspicious')
    files = [f for f in os.listdir(susp_dir) if f.endswith('.png')]

    print(f"--- RÉSZLETES GEOMETRIAI ELEMZÉS: {len(files)} ANOMÁLIA ---")
    print(f"{'Fájlnév':<25} | {'Átlag Eltérés':<15} | {'Státusz'}")
    print("-" * 60)

    for f in files:
        img_path = os.path.join(susp_dir, f)
        img = Image.open(img_path).convert('L')
        data = np.asarray(img)
        
        # Aktuális kép átlaga
        current_mean = np.mean(data)
        
        # Eltérés számítása a 364 kép átlagától (százalékban)
        ref_mean = ref['atlag']['mean']
        elteres_szazalek = abs((current_mean - ref_mean) / ref_mean) * 100
        
        statusz = "BLIP GYANÚ" if elteres_szazalek > 50 else "EGYÉB GLITCH"
        
        print(f"{f:<25} | {elteres_szazalek:>13.2f}% | {statusz}")

if __name__ == "__main__":
    meres()