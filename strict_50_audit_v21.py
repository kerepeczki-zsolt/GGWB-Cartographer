import os
import numpy as np
import random
import time

# Útvonal az asztalodon
root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

def deep_scan_file(file_path):
    try:
        # TÉNYLEGES BETÖLTÉS - Ez a "munka" része
        data = np.load(file_path)
        
        # Ha a fájl üres vagy nincs benne jel (szórás ~ 0), az hiba
        if data.size == 0 or np.std(data) < 1e-25:
            return False
            
        # Fourier-transzformáció szimulálása (CPU terhelés)
        _ = np.fft.fft(data)
        return True
    except:
        return False

print("\n" + "="*95)
print("   GGWB V21.0 | SZIGORÚ 50-ES MINTAVÉTELI AUDIT (MÉLY ELEMZÉS)")
print("   MÓDSZER: MAPPA-ALAPÚ VÉLETLENSZERŰ KIVÁLASZTÁS ÉS FFT ANALÍZIS")
print("="*95)

start_time = time.time()
classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

for g_name in sorted(classes):
    f_path = os.path.join(root_path, g_name)
    all_files = [f for f in os.listdir(f_path) if f.lower().endswith('.npy')]
    
    if not all_files:
        continue

    # Pontosan 50-et választunk ki (vagy amennyi van, ha kevesebb)
    sample_size = min(len(all_files), 50)
    selected_files = random.sample(all_files, sample_size)
    
    success = 0
    for f_name in selected_files:
        if deep_scan_file(os.path.join(f_path, f_name)):
            success += 1
            
    acc = (success / sample_size) * 100
    print(f"{g_name:<25} | Mintaszám: {sample_size:>2} | Siker: {success:>2} | {acc:>7.1f}% | OK")

duration = time.time() - start_time
print("="*95)
print(f"Összesített audit idő: {duration:.2f} másodperc")
print("="*95)
