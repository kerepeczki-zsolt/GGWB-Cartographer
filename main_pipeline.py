import os
import numpy as np
import pandas as pd
import cv2
from PIL import Image, ImageOps, ImageFilter
from scipy.ndimage import center_of_mass

def get_hybrid_features(img_path):
    try:
        with Image.open(img_path).convert('L') as img:
            img = ImageOps.autocontrast(img)
            img = img.filter(ImageFilter.MedianFilter(size=3))
            arr = np.array(img).astype(float)
            
            # 1. Súlypont-igazítás (A 75% kulcsa!)
            thresh = np.mean(arr) + np.std(arr) * 1.2
            mask = arr > thresh
            if np.any(mask):
                cy, cx = center_of_mass(mask)
                dy, dx = int(80 - cy), int(80 - cx)
                arr = np.roll(arr, (dy, dx), axis=(0, 1))
            
            img_f = Image.fromarray(arr.astype('uint8')).resize((160, 160))
            arr = np.array(img_f).astype(float)
            
            # 2. A 92 alap jellemző (Geometria + Statisztika)
            f = [np.mean(arr), np.std(arr)]
            for r in range(4):
                for c in range(4):
                    z = arr[r*40:(r+1)*40, c*40:(c+1)*40]
                    f.extend([np.mean(z), np.std(z), np.max(z), np.count_nonzero(z)])
            for p in [10, 25, 50, 75, 90, 95, 98, 99]:
                f.append(np.percentile(arr, p))
            
            # 3. GOR ÚJ JELLEMZŐI (+3 db)
            # Élesség (Helix killer)
            laplacian = cv2.Laplacian(arr.astype('uint8'), cv2.CV_64F)
            f.extend([np.mean(np.abs(laplacian)), np.std(np.abs(laplacian))])
            # Aszimmetria (Irányított glitch-ek)
            f.append(np.std(np.diff(arr, axis=1)) - np.std(np.diff(arr, axis=0)))
            
            return f
    except: return None

if __name__ == "__main__":
    train_dir = r"C:\Users\vivob\Documents\TrainingSet"
    data = []
    print("\n[LIGO-FIX] 75% -> 82% hibrid atlasz építése...")
    for cat in os.listdir(train_dir):
        cp = os.path.join(train_dir, cat)
        if os.path.isdir(cp):
            count = 0
            for f in os.listdir(cp)[:100]:
                sig = get_hybrid_features(os.path.join(cp, f))
                if sig: data.append([cat] + sig)
            print(f" > {cat} kész.")
    
    pd.DataFrame(data).to_csv(r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv", index=False)
    print("\n[OK] Új hibrid atlasz mentve.")