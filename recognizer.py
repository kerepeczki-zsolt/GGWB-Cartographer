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
            thresh = np.mean(arr) + np.std(arr) * 1.2
            mask = arr > thresh
            if np.any(mask):
                cy, cx = center_of_mass(mask)
                dy, dx = int(80 - cy), int(80 - cx)
                arr = np.roll(arr, (dy, dx), axis=(0, 1))
            img_f = Image.fromarray(arr.astype('uint8')).resize((160, 160))
            arr = np.array(img_f).astype(float)
            f = [np.mean(arr), np.std(arr)]
            for r in range(4):
                for c in range(4):
                    z = arr[r*40:(r+1)*40, c*40:(c+1)*40]
                    f.extend([np.mean(z), np.std(z), np.max(z), np.count_nonzero(z)])
            for p in [10, 25, 50, 75, 90, 95, 98, 99]:
                f.append(np.percentile(arr, p))
            laplacian = cv2.Laplacian(arr.astype('uint8'), cv2.CV_64F)
            f.extend([np.mean(np.abs(laplacian)), np.std(np.abs(laplacian))])
            f.append(np.std(np.diff(arr, axis=1)) - np.std(np.diff(arr, axis=0)))
            return f
    except: return None

if __name__ == "__main__":
    db = pd.read_csv(r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv")
    test_dir = r"C:\Users\vivob\Desktop\GGWB-Clone\IDEGEN_TESZT"
    truth = {}
    with open(r"C:\Users\vivob\Desktop\GGWB-Clone\truth_log.txt", "r", encoding="utf-8") as f:
        for l in f:
            if ":" in l: k, v = l.strip().split(": "); truth[k] = v.lower().replace("_","").strip()
    
    db_feats = db.iloc[:, 1:].values
    stds = np.std(db_feats, axis=0); stds[stds == 0] = 1
    correct, total = 0, 0
    for fn in sorted(os.listdir(test_dir)):
        if not fn.lower().endswith(('.png', '.jpg')): continue
        sig = get_hybrid_features(os.path.join(test_dir, fn))
        if sig:
            total += 1
            dists = np.sqrt(np.sum(((db_feats - np.array(sig)) / stds)**2, axis=1))
            top_idx = np.argsort(dists)[:3] # Top-3 a zaj ellen
            tipp = db.iloc[top_idx].iloc[:, 0].value_counts().index[0]
            val = truth.get(fn, "").lower().replace("_","")
            is_ok = tipp.lower().replace("_","") == val
            if is_ok: correct += 1
            print(f"{'[ JÓ ]' if is_ok else '[ !! ]'} {fn:20} | Tipp: {tipp}")
    print(f"\nEREDMÉNY: {(correct/total)*100:.1f}%")