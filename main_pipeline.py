import os
import numpy as np
import pandas as pd
from PIL import Image

def get_glitch_signature(img_path):
    """
    Kiszámítja a hiba egyedi matematikai ujjlenyomatát 7 fizikai paraméter alapján.
    """
    try:
        with Image.open(img_path).convert('L') as img:
            img = img.resize((128, 128))
            arr = np.array(img).astype(float)
            m_val = np.mean(arr)
            s_val = np.std(arr)
            low_f = np.mean(arr[64:, :])
            high_f = np.mean(arr[:64, :])
            t_dist = np.mean(arr[:, :64]) - np.mean(arr[:, 64:])
            p_val = np.max(arr)
            # Shannon-entrópia közelítése a zaj sűrűségéhez
            entropy = -np.sum((arr/255.0) * np.log((arr/255.0) + 1e-9))
            return [m_val, s_val, low_f, high_f, t_dist, p_val, entropy]
    except:
        return None

def build_atlas():
    base_path = r"C:\Users\vivob\Documents\TrainingSet"
    output_path = r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv"
    
    atlas_data = []
    print(f"\n--- GGWB-CARTOGRAPHER: HIBA-ATLASZ GENERÁLÁS (v2.0) ---")
    
    if not os.path.exists(base_path):
        print(f"HIBA: Forrás nem található: {base_path}")
        return

    categories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for category in categories:
        cat_path = os.path.join(base_path, category)
        valid_images = [os.path.join(cat_path, f) for f in os.listdir(cat_path) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not valid_images: continue
            
        print(f" > {category} profilozása...", end=" ", flush=True)
        cat_features = []
        for img_path in valid_images[:30]:
            f = get_glitch_signature(img_path)
            if f: cat_features.append(f)
            
        if cat_features:
            mean_f = np.mean(cat_features, axis=0)
            atlas_data.append([category] + mean_f.tolist())
            print(f"OK ({len(cat_features)} minta)")
    
    if atlas_data:
        df = pd.DataFrame(atlas_data, columns=['label', 'mean', 'std', 'low_f', 'high_f', 't_dist', 'peak', 'entropy'])
        df.to_csv(output_path, index=False)
        print(f"\n--- ATLASZ KÉSZ: {len(df)} hiba típus rögzítve a GitHub verzióhoz ---")

if __name__ == "__main__":
    build_atlas()