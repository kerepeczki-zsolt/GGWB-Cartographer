import os
import numpy as np
from PIL import Image
from scipy.stats import skew, kurtosis
import json
import shutil

# ====================================================
# GGWB-CARTOGRAPHER: ANOMÁLIA DETEKTOR (H1)
# 92 JELLEMZŐ ALAPJÁN TÖRTÉNŐ ÖSSZEHASONLÍTÁS
# ====================================================

# Konfiguráció a te mappaszerkezetedhez
BASE_PATH = r'data\O3'
DETECTOR = 'H1'

def extract_features(img_path):
    """
    Kiszámolja a kép egyedi geometriai ujjlenyomatát.
    Ezek a pillérei a 92 geometriai jellemzőnek.
    """
    try:
        img = Image.open(img_path).convert('L')
        data = np.asarray(img)
        flat_data = data.flatten()
        
        # Geometriai és statisztikai mérőszámok
        features = {
            'atlag': float(np.mean(data)),
            'szoras': float(np.std(data)),
            'ferdeseg': float(skew(flat_data)),
            'csucsossag': float(kurtosis(flat_data)),
            'energia': float(np.sum(data**2) / data.size),
            'max_intenzitas': int(np.max(data)),
            'el_suruseg': float(np.sum(np.diff(data) > 35) / data.size),
            'viz_szimmetria': float(np.mean(np.abs(data - np.flipud(data)))),
            'fugg_szimmetria': float(np.mean(np.abs(data - np.fliplr(data))))
        }
        return features
    except Exception as e:
        print(f"Hiba a fájl feldolgozásakor: {img_path} -> {e}")
        return None

def inditas():
    # 1. Betöltjük a 364 kép alapján készült "No Glitch" átlagokat (referenciát)
    try:
        with open('no_glitch_reference.json', 'r') as f:
            ref = json.load(f)
    except FileNotFoundError:
        print("HIBA: Nem találom a 'no_glitch_reference.json' fájlt!")
        print("Futtasd előbb a 'referencia_generator.py' kódot!")
        return

    raw_dir = os.path.join(BASE_PATH, DETECTOR, 'raw')
    suspicious_dir = os.path.join(BASE_PATH, DETECTOR, 'processed', 'suspicious')
    
    # Mappa ürítése és létrehozása az új eredményeknek
    if os.path.exists(suspicious_dir):
        shutil.rmtree(suspicious_dir)
    os.makedirs(suspicious_dir, exist_ok=True)

    print("====================================================")
    print("   GGWB-CARTOGRAPHER: SZIGORÚ ANOMÁLIA KERESÉS       ")
    print("   (Referencia: 364 No-Glitch kép átlaga)           ")
    print("====================================================\n")

    files = [f for f in os.listdir(raw_dir) if f.endswith('.png')]
    found_count = 0

    for f in files:
        img_path = os.path.join(raw_dir, f)
        feat = extract_features(img_path)
        
        if feat is None: continue

        # ÖSSZEHASONLÍTÁS A REFERENCIÁVAL
        # Megnézzük, hány jellemző tér el jelentősen az átlagtól
        eltérés_pontszam = 0
        for key in ref.keys():
            if key.endswith('_std'): continue # A szórást nem hasonlítjuk, csak használjuk
            
            # Kiszámoljuk a különbséget az átlagtól
            tavolsag = abs(feat[key] - ref[key]['mean'])
            
            # SZIGORÍTÁS: 3 helyett 1.5-ös szorzót használunk
            if tavolsag > (ref[key]['std'] * 1.5):
                eltérés_pontszam += 1
        
        # SZIGORÍTÁS: Már 1 eltérésnél (ponthnál) is gyanúsnak bélyegezzük
        if eltérés_pontszam >= 1:
            print(f"[!] ANOMÁLIA: {f} -> {eltérés_pontszam} geometriai eltérés észlelve.")
            shutil.copy(img_path, os.path.join(suspicious_dir, f))
            found_count += 1

    print(f"\n----------------------------------------------------")
    print(f"Eredmény: {len(files)} képből {found_count} darab lett gyanús.")
    print(f"A fájlok a 'suspicious' mappába kerültek.")
    print("====================================================")

if __name__ == "__main__":
    inditas()