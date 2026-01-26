import os
import numpy as np
import json
from PIL import Image

# ====================================================
# GGWB-CARTOGRAPHER: TRAINING SET ÖSSZEHASONLÍTÓ
# ====================================================

# 1. Itt vannak a kódjaid és a JSON fájlod
BASE_DIR = r'C:\Users\vivob\Desktop\GGWB-Clone'

# 2. Itt vannak a képeid a különböző mappákban (Blip, Chirp, stb.)
# A képed alapján ez az útvonal:
DATA_DIR = r'C:\Users\vivob\Desktop\TrainingSet'

def inditas():
    # Referencia betöltése a kód mellől
    ref_path = os.path.join(BASE_DIR, 'no_glitch_reference.json')
    try:
        with open(ref_path, 'r') as f:
            ref = json.load(f)
    except:
        print(f"HIBA: Nem találom a referenciát itt: {ref_path}")
        return

    print(f"{'GLITCH TÍPUS':<20} | {'ÁTLAGOS ELTÉRÉS A TISZTÁTÓL'}")
    print("-" * 50)

    # Végigmegyünk a TrainingSet mappáin (Blip, Chirp, Koi_Fish, stb.)
    for kategoria in os.listdir(DATA_DIR):
        kat_path = os.path.join(DATA_DIR, kategoria)
        
        if os.path.isdir(kat_path):
            kepek = [f for f in os.listdir(kat_path) if f.endswith('.png')]
            if not kepek: continue

            elteresek = []
            # Megnézzük az első 20 képet minden típusból
            for img_name in kepek[:20]:
                img = Image.open(os.path.join(kat_path, img_name)).convert('L')
                data = np.asarray(img)
                
                curr_mean = np.mean(data)
                ref_mean = ref['atlag']['mean']
                
                # Százalékos eltérés a 364 tiszta kép átlagától
                diff = abs((curr_mean - ref_mean) / ref_mean) * 100
                elteresek.append(diff)

            atlagos_eltérés = np.mean(elteresek)
            print(f"{kategoria:<20} | {atlagos_eltérés:>25.2f} %")

if __name__ == "__main__":
    inditas()