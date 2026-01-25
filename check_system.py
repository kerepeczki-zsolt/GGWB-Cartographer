import numpy as np
import os
import pandas as pd
from PIL import Image
from scipy.stats import kurtosis, entropy
from scipy.ndimage import gaussian_filter

class GGWB_Cartographer_Core:
    def __init__(self, atlas_path):
        self.atlas = pd.read_csv(atlas_path, sep=None, engine='python')
        print(f"--- RENDSZER ÉLESÍTVE: {len(self.atlas)} kategória betöltve ---")
        
    def get_features(self, img_path):
        try:
            with Image.open(img_path).convert('L') as img:
                arr = np.array(img).astype(float)
                arr = gaussian_filter(arr, sigma=0.8)
                arr = (arr - np.mean(arr)) / (np.std(arr) + 1e-6)
                mask = arr > 2.2 # Finomabb érzékelés a GW jelekhez
                if np.sum(mask) < 2: return None
                y, x = np.where(mask)
                h, w = arr.shape
                coords = np.vstack([x, y])
                cov = np.cov(coords)
                evals, _ = np.linalg.eig(cov)
                orientation = np.abs(evals[0] / (evals[1] + 1e-6))
                hist, _ = np.histogram(arr.flatten(), bins=30, density=True)
                ent_val = entropy(hist + 1e-9)
                mid_x = np.mean(x)
                symm = abs(np.sum(mask[:, :int(mid_x)]) - np.sum(mask[:, int(mid_x):])) / (np.sum(mask) + 1e-6)
                return np.array([ent_val, kurtosis(arr.flatten()), np.mean(y)/h,
                                (np.max(x)-np.min(x)+1)/(np.max(y)-np.min(y)+1),
                                np.sum(mask)/((np.max(y)-np.min(y)+1)*(np.max(x)-np.min(x)+1)),
                                symm, orientation])
        except: return None

    def auto_classify(self, img_path):
        f = self.get_features(img_path)
        if f is None: return "ZAJ / ÜRES", 0.0
        
        diffs = []
        for _, r in self.atlas.iterrows():
            a_v = r.values[1:8].astype(float)
            diffs.append((r.values[0], np.linalg.norm(f - a_v)))
        
        diffs.sort(key=lambda x: x[1])
        best_cat, dist = diffs[0]
        
        # LOGIKA: Ha nem hasonlít semmire (nagy a távolság), de van jele -> POTENCIÁLIS GW
        if dist > 4.5:
            return "!! POTENCIÁLIS GW JEL !!", 65.0
            
        conf = max(10.0, 100 - (dist * 18))
        return best_cat, conf

if __name__ == "__main__":
    ATLAS = r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv"
    # A te pontos útvonalad az asztalon:
    TEST_DIR = r"C:\Users\vivob\Desktop\GGWB-Clone\IDEGEN_TESZT"

    seeker = GGWB_Cartographer_Core(ATLAS)
    print(f"\nAUTOMATIKUS ANALÍZIS INDUL: {TEST_DIR}\n" + "="*60)
    
    if os.path.exists(TEST_DIR):
        files = [f for f in os.listdir(TEST_DIR) if f.lower().endswith(('.png', '.jpg'))]
        for fn in files:
            res, conf = seeker.auto_classify(os.path.join(TEST_DIR, fn))
            # Kiemelés, ha valami gyanús
            marker = ">>>" if "GW" in res else "   "
            print(f"{marker} Fájl: {fn:20} | EREDMÉNY: {res:22} | Bizalom: {conf:.1f}%")
    else:
        print(f"Hiba: Nem találom a mappát: {TEST_DIR}")