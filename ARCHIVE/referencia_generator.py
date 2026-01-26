import os
import numpy as np
from PIL import Image
from scipy.stats import skew, kurtosis
import json

# ====================================================
# GGWB-CARTOGRAPHER: REFERENCIA GENERÁTOR (H1)
# ====================================================

# alapján a helyes útvonal:
BASE_PATH = r'data\O3'
DETECTOR = 'H1'

def extract_features(img_path):
    """Kiszámolja a kép komplex geometriai jellemzőit."""
    try:
        img = Image.open(img_path).convert('L')
        data = np.asarray(img)
        flat_data = data.flatten()
        
        # Geometriai jellemzők alapjai
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
    except Exception:
        return None

def futtatas():
    # A tiszta képek helye
    clean_dir = os.path.join(BASE_PATH, DETECTOR, 'processed', 'clean')
    
    print("====================================================")
    print("   GGWB-CARTOGRAPHER: REFERENCIA RÖGZÍTÉS            ")
    print("====================================================\n")
    
    if not os.path.exists(clean_dir):
        print(f"HIBA: A '{clean_dir}' mappa nem létezik!")
        return

    all_features = []
    files = [f for f in os.listdir(clean_dir) if f.endswith('.png')]
    
    print(f"[{DETECTOR}] {len(files)} tiszta kép elemzése...")

    for f in files:
        f_path = os.path.join(clean_dir, f)
        feat = extract_features(f_path)
        if feat:
            all_features.append(feat)
    
    if not all_features:
        print("HIBA: Nem sikerült adatot kinyerni a képekből!")
        return

    # Statisztikai profil készítése
    reference_profile = {}
    for key in all_features[0].keys():
        values = [img[key] for img in all_features]
        reference_profile[key] = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values))
        }

    # Mentés a GGWB-Clone mappába
    with open('no_glitch_reference.json', 'w') as f:
        json.dump(reference_profile, f, indent=4)
    
    print(f"\nSIKER! A 'no_glitch_reference.json' létrejött.")

if __name__ == "__main__":
    futtatas()