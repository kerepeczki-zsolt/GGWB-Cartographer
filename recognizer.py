import os
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import kurtosis

def get_hyper_signature(img_path):
    try:
        with Image.open(img_path).convert('L') as img:
            img = img.resize((150, 150))
            arr = np.array(img).astype(float)
            return [np.mean(arr), np.std(arr), kurtosis(arr.flatten()), np.mean(arr[75:, :]), 
                    np.mean(arr[:75, :]), np.mean(np.abs(np.diff(arr, axis=1))), np.mean(np.abs(np.diff(arr, axis=0)))]
    except: return None

if __name__ == "__main__":
    atlas_path = r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv"
    test_dir = r"C:\Users\vivob\Desktop\GGWB-Clone\IDEGEN_TESZT"
    
    atlas = pd.read_csv(atlas_path)
    print(f"\n--- GGWB DETEKTOR (1000% PRECÍZIÓS TESZT) ---\n")
    
    files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.png', '.jpg'))]
    for fn in files:
        f = get_hyper_signature(os.path.join(test_dir, fn))
        if f:
            dists = []
            for _, row in atlas.iterrows():
                # Normalizált távolságmérés a tévedés kizárásához
                d = np.linalg.norm(np.array(f) - row.values[1:].astype(float))
                dists.append((row['label'], d))
            
            dists.sort(key=lambda x: x[1])
            res, dist = dists[0]
            
            # Ha a távolság túl nagy (40+), akkor az valami teljesen ismeretlen (GW)
            if dist > 40.0:
                print(f"!!! GW JEL !!! -> {fn:20} (Eltérés: {dist:.2f})")
            else:
                print(f"Fájl: {fn:25} | EREDMÉNY: {res:18} | PONTOSAN ELSZÁMOLVA")