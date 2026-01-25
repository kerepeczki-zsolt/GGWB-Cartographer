import os
import shutil
import numpy as np
from PIL import Image

# GGWB-Cartographer: VÉGLEGES TISZTÍTÓ RENDSZER (H1, L1, V1)
BASE_PATH = r'data\O3'
DETECTORS = ['H1', 'L1', 'V1']
# A Blip-ek rejtekhelye (Ezt találtuk meg ma együtt)
MIN_VAR = 9000
MAX_VAR = 12500

def ggwb_cartographer_final_clean():
    print("====================================================")
    print("   GGWB-CARTOGRAPHER: TELJES HÁLÓZAT TISZTÍTÁSA      ")
    print("====================================================\n")
    
    for det in DETECTORS:
        raw_dir = os.path.join(BASE_PATH, det, 'raw')
        clean_dir = os.path.join(BASE_PATH, det, 'processed', 'clean')
        suspicious_dir = os.path.join(BASE_PATH, det, 'processed', 'suspicious')

        # Mappák előkészítése
        if not os.path.exists(raw_dir): 
            print(f"[{det}] Nincs raw mappa, ugrom...")
            continue
            
        if os.path.exists(clean_dir): shutil.rmtree(clean_dir)
        if os.path.exists(suspicious_dir): shutil.rmtree(suspicious_dir)
        os.makedirs(clean_dir, exist_ok=True)
        os.makedirs(suspicious_dir, exist_ok=True)

        files = [f for f in os.listdir(raw_dir) if f.endswith('.png')]
        print(f"[{det}] {len(files)} kép elemzése folyamatban...")

        count_clean = 0
        count_susp = 0

        for f in files:
            img_path = os.path.join(raw_dir, f)
            with Image.open(img_path) as img:
                variance = np.var(np.asarray(img.convert('L')))
                
                # Szűrés a megtalált tartomány alapján
                if MIN_VAR <= variance <= MAX_VAR:
                    shutil.copy(img_path, os.path.join(suspicious_dir, f))
                    count_susp += 1
                else:
                    shutil.copy(img_path, os.path.join(clean_dir, f))
                    count_clean += 1

        print(f" -> {count_clean} Tiszta, {count_susp} Gyanús (Blip)")

    print("\n====================================================")
    print("   MINDEN DETEKTOR KÉSZ! TÖRÖLD A BLIP-EKET!        ")
    print("====================================================")

if __name__ == "__main__":
    ggwb_cartographer_final_clean()