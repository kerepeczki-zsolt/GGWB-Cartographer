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
            
            # 7 Brutálisan pontos mutató
            m_val = np.mean(arr)
            s_val = np.std(arr)
            # Kurtosis (megmutatja, mennyire "tüskés" a hiba - ez választja el a Blipet a többitől)
            kurt = kurtosis(arr.flatten())
            # Frekvencia arányok
            low_f = np.mean(arr[75:, :])
            high_f = np.mean(arr[:75, :])
            # Mintázat iránya (vízszintes vs függőleges - ez kell a Whistle/Ripples különbséghez)
            h_pattern = np.mean(np.abs(np.diff(arr, axis=1)))
            v_pattern = np.mean(np.abs(np.diff(arr, axis=0)))
            
            return [m_val, s_val, kurt, low_f, high_f, h_pattern, v_pattern]
    except:
        return None

def build_hyper_atlas():
    base_path = r"C:\Users\vivob\Documents\TrainingSet"
    output_path = r"C:\Users\vivob\Desktop\GGWB-Clone\omega_atlas_v35.csv"
    
    atlas_data = []
    print("\n--- GGWB: HYPER-ATLASZ GENERÁLÁS (100%-OS CÉL) ---")
    
    categories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    for category in categories:
        cat_path = os.path.join(base_path, category)
        imgs = [os.path.join(cat_path, f) for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg'))]
        
        features = []
        for img_path in imgs[:100]: # 100 minta a tökéletes átlaghoz
            f = get_hyper_signature(img_path)
            if f: features.append(f)
            
        if features:
            atlas_data.append([category] + np.mean(features, axis=0).tolist())
            print(f" > {category}: OK")
            
    df = pd.DataFrame(atlas_data, columns=['label', 'm', 's', 'k', 'lf', 'hf', 'hp', 'vp'])
    df.to_csv(output_path, index=False)
    print("\n--- HYPER-ATLASZ KÉSZ ---")

if __name__ == "__main__":
    build_hyper_atlas()