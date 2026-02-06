import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. JEGYZŐKÖNYV MEGYNYITÁSA ÉS ÉRTÉKELÉSE
csv_path = "C:/Users/vivob/GGWB_FINAL_V12/hiteles_jegyzokonyv_22.csv"
data_dir = "C:/Users/vivob/GGWB_FINAL_V12/LIGO_VALIDATED_DATA"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print("\n--- GGWB V12 AUDIT ÖSSZESÍTŐ ---")
    print(df.to_string(index=False))
    
    # 2. EGY VALÓDI ADATFÁJL VIZUÁLIS MEGJELENÍTÉSE
    # Kiválasztunk egy 'Koi_Fish' mintát, mert ott volt bizonytalanság
    sample_file = os.path.join(data_dir, "Koi_Fish_0.npy")
    
    if os.path.exists(sample_file):
        data = np.load(sample_file)
        plt.figure(figsize=(12, 6))
        plt.plot(data, color='#00ffcc', alpha=0.7)
        plt.title("GGWB-Cartographer: Validált 'Koi_Fish' Jel-minta (Időtartomány)")
        plt.xlabel("Mintavétel (4096 Hz)")
        plt.ylabel("Relatív Amplitúdó")
        plt.grid(True, linestyle='--', alpha=0.5)
        
        print("\n[INFO] Grafikon generálása folyamatban...")
        plt.show()
    else:
        print(f"\n[HIBA] Nem található a minta fájl: {sample_file}")
else:
    print(f"\n[HIBA] A jegyzőkönyv nem található itt: {csv_path}")
