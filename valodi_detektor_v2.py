import os
import numpy as np
import json
from PIL import Image
import shutil

# ====================================================
# GGWB-CARTOGRAPHER: NYERS ADAT ELEMZŐ (JAVÍTOTT)
# ====================================================

BASE_PATH = r'data\O3'
DETECTOR = 'H1'

def futtatas():
    # 1. Betöltjük a 364 kép alapján készült referenciát
    try:
        with open('no_gl_reference.json', 'r') as f: # Ellenőrizd a pontos nevet!
            ref = json.load(f)
    except:
        # Próbáljuk a másik néven is, ha az előző nem sikerült
        try:
            with open('no_glitch_reference.json', 'r') as f:
                ref = json.load(f)
        except:
            print("HIBA: Nem találom a referencia JSON fájlt!")
            return

    raw_dir = os.path.join(BASE_PATH, DETECTOR, 'raw')
    result_dir = os.path.join(BASE_PATH, DETECTOR, 'processed', 'valodi_talalatok')
    
    if os.path.exists(result_dir): shutil.rmtree(result_dir)
    os.makedirs(result_dir, exist_ok=True)

    print(f"--- ANALÍZIS INDUL (Hiba elleni védelemmel) ---")

    files = [f for f in os.listdir(raw_dir) if f.endswith('.png')]
    talalat_szam = 0

    # Referencia értékek
    ref_max_atlag = ref['max_intenzitas']['mean']
    # Védelem: Ha a szórás 0, adunk neki egy minimális értéket (0.0001)
    ref_max_szoras = max(ref['max_intenzitas']['std'], 0.0001)

    for f in files:
        img_path = os.path.join(raw_dir, f)
        img = Image.open(img_path).convert('L')
        data = np.asarray(img)
        current_max = np.max(data)
        
        # Kiszámoljuk az eltérést
        szigma_elteres = (current_max - ref_max_atlag) / ref_max_szoras

        # LOGIKA: Ha a fényerő 2-szerese a tiszta átlagnak, az biztosan anomália
        if current_max > (ref_max_atlag * 2) or szigma_elteres > 5:
            print(f"[!] TALÁLAT: {f} | Intenzitás: {current_max}")
            shutil.copy(img_path, os.path.join(result_dir, f))
            talalat_szam += 1

    print(f"\nElemzés kész! {len(files)} képből {talalat_szam} találat.")

if __name__ == "__main__":
    futtatas()