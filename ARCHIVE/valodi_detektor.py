import os
import numpy as np
import json
from PIL import Image
import shutil

# ====================================================
# GGWB-CARTOGRAPHER: NYERS ADAT ELEMZŐ (H1)
# ====================================================

# Útvonalak beállítása
BASE_PATH = r'data\O3'
DETECTOR = 'H1'

def futtatas():
    # 1. Betöltjük a 364 kép alapján készült referenciát
    try:
        with open('no_glitch_reference.json', 'r') as f:
            ref = json.load(f)
    except FileNotFoundError:
        print("HIBA: 'no_glitch_reference.json' nem található! Futtasd a generátort.")
        return

    # 2. Mappák kijelölése (Most a RAW mappát vizsgáljuk!)
    raw_dir = os.path.join(BASE_PATH, DETECTOR, 'raw')
    result_dir = os.path.join(BASE_PATH, DETECTOR, 'processed', 'valodi_talalatok')
    
    # Eredmény mappa előkészítése
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.makedirs(result_dir, exist_ok=True)

    print(f"--- ANALÍZIS INDUL A NYERS ADATOKON ({raw_dir}) ---")
    print(f"Referencia alapja: 364 tiszta kép.\n")

    files = [f for f in os.listdir(raw_dir) if f.endswith('.png')]
    talalat_szam = 0

    # A 364 kép átlagos maximum fényereje
    ref_max_atlag = ref['max_intenzitas']['mean']
    ref_max_szoras = ref['max_intenzitas']['std']

    for f in files:
        img_path = os.path.join(raw_dir, f)
        img = Image.open(img_path).convert('L')
        data = np.asarray(img)
        
        current_max = np.max(data)
        
        # LOGIKA: Ha a kép legfényesebb pontja több mint 5 szórással 
        # tér el a tiszta átlagtól, az statisztikailag biztosan Glitch.
        szigma_elteres = (current_max - ref_max_atlag) / ref_max_szoras

        if szigma_elteres > 5:
            print(f"[!] TALÁLAT: {f} | Eltérés: {szigma_elteres:.2f} szigma")
            shutil.copy(img_path, os.path.join(result_dir, f))
            talalat_szam += 1

    print(f"\nElemzés kész! {len(files)} nyers képből {talalat_szam} valódi anomáliát találtam.")
    print(f"Helyszín: {result_dir}")

if __name__ == "__main__":
    futtatas()