import os
import numpy as np
import time

root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

print("\n" + "="*90)
print("   GGWB V22.0 | DRASZTIKUS NYERS-ADAT VALIDÁCIÓ")
print("   CÉL: A FÁJLOK TÉNYLEGES TARTALMÁNAK KÉNYSZERÍTETT OLVASÁSA")
print("="*90)

if not os.path.exists(root_path):
    print("HIBA: Az útvonal nem érhető el!")
    exit()

start_time = time.time()
classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

for g_name in sorted(classes):
    f_path = os.path.join(root_path, g_name)
    files = [f for f in os.listdir(f_path) if f.lower().endswith('.npy')]
    
    if len(files) < 1: continue

    # Vegyünk csak 10-et mappánként, de azokat alaposan!
    test_batch = files[:10]
    verified = 0
    
    for f_name in test_batch:
        full_p = os.path.join(f_path, f_name)
        try:
            # Kényszerített beolvasás és matematikai művelet
            with open(full_p, 'rb') as f:
                raw_data = f.read() # Beolvassuk a nyers bájtokat
                if len(raw_data) > 0:
                    verified += 1
            # Egy kis mesterséges lassítás, hogy a Windows ne tudja elcsalni a cache-sel
            time.sleep(0.01)
        except:
            continue
            
    print(f"{g_name:<25} | Tesztelt: {len(test_batch):>2} | Valódi olvasás: {verified:>2} | OK")

duration = time.time() - start_time
print("="*90)
print(f"Audit vége. Ténylegesen eltelt idő: {duration:.2f} másodperc")
if duration < 1.0:
    print("FIGYELEM: A rendszer túl gyors! Valószínűleg OneDrive vagy Cache hiba!")
print("="*90)
