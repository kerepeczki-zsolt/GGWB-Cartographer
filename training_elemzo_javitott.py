import os
import numpy as np
import json
from PIL import Image

# ====================================================
# GGWB-CARTOGRAPHER: TRAINING SET MERES - ZSOLT GEPERE
# ====================================================

# A TE GEPED PONTOS UTVONALAI
BASE_DIR = r'C:\Users\vivob\Desktop\GGWB-Clone'
DATA_DIR = r'C:\Users\vivob\Desktop\TrainingSet'
REF_FILE = os.path.join(BASE_DIR, 'no_glitch_reference.json')

def inditas():
    print(f"--- ELLENORZES ---")
    if not os.path.exists(DATA_DIR):
        print(f"HIBA: Nem lelom a TrainingSet-et itt: {DATA_DIR}")
        return
    if not os.path.exists(REF_FILE):
        print(f"HIBA: Nincs meg a referencia itt: {REF_FILE}")
        return

    print(f"{'GLITCH TIPUS':<20} | {'ELTERES %'}")
    print("-" * 45)

    # Vegigmegyunk a mappakon (Blip, Chirp, stb.)
    for kategoria in os.listdir(DATA_DIR):
        kat_path = os.path.join(DATA_DIR, kategoria)
        if os.path.isdir(kat_path):
            kepek = [f for f in os.listdir(kat_path) if f.endswith('.png')]
            if kepek:
                img = Image.open(os.path.join(kat_path, kepek[0])).convert('L')
                data = np.asarray(img)
                
                with open(REF_FILE, 'r') as f:
                    ref = json.load(f)
                
                diff = abs((np.mean(data) - ref['atlag']['mean']) / ref['atlag']['mean']) * 100
                print(f"{kategoria:<20} | {diff:>15.2f} %")

if __name__ == "__main__":
    inditas()