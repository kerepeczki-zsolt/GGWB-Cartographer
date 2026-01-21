import os
import numpy as np
import pandas as pd
from PIL import Image

def get_glitch_signature(img_path):
    try:
        with Image.open(img_path).convert('L') as img:
            img = img.resize((128, 128))
            arr = np.array(img).astype(float)
            return [np.mean(arr), np.std(arr), np.mean(arr[64:, :]), np.mean(arr[:64, :]), 
                    np.mean(arr[:, :64]) - np.mean(arr[:, 64:]), np.max(arr),
                    -np.sum((arr/255.0) * np.log((arr/255.0) + 1e-9))]
    except: return None

if __name__ == "__main__":
    atlas_path = r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv"
    test_dir = r"C:\Users\vivob\Desktop\GGWB-Clone\IDEGEN_TESZT"
    
    if not os.path.exists(atlas_path):
        print("HIBA: Előbb generáld le az Atlaszt!")
    else:
        atlas = pd.read_csv(atlas_path)
        print(f"--- GGWB DETEKTOR AKTÍV (Precise Seeker Mode) ---\n")
        
        files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.png', '.jpg'))]
        for fn in files:
            f = get_glitch_signature(os.path.join(test_dir, fn))
            if f:
                dists = []
                for _, row in atlas.iterrows():
                    d = np.linalg.norm(np.array(f) - row.values[1:].astype(float))
                    dists.append((row['label'], d))
                
                dists.sort(key=lambda x: x[1])
                best_match = dists[0][0]
                dist_val = dists[0][1]
                
                # Tudományos küszöb: ha 3.0-nál messzebb van a zajtól, az GW!
                if dist_val > 3.0:
                    print(f"!!! TALÁLAT !!! -> Fájl: {fn:20} | EREDMÉNY: GRAVITÁCIÓS HULLÁM (GW) | Eltérés: {dist_val:.2f}")
                else:
                    print(f"Fájl: {fn:25} | EREDMÉNY: {best_match:15} | Bizalom: {(100/(1+dist_val/10)):.1f}%")