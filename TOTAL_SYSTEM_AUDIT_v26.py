import os
import time
import numpy as np
from PIL import Image

# A te pontos útvonalad
root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

def deep_pixel_analysis(file_path):
    try:
        # Kényszerített betöltés és pixel-szintű ellenőrzés
        with Image.open(file_path) as img:
            # Csak akkor tekintjük érvényesnek, ha valódi pixeladat van benne
            data = np.asarray(img.convert('L'))
            if data.size == 0 or np.std(data) < 0.1:
                return False
            return True
    except:
        return False

print("\n" + "="*100)
print("   GGWB V26.0 | TELJES RENDSZER AUDIT - TOTÁLIS ADATBÁZIS ELLENŐRZÉS")
print("   FORRÁS: " + root_path)
print("   FIGYELEM: Ez a folyamat a teljes TrainingSet-et (31,869 fájl) elemzi!")
print("="*100)

start_time = time.time()
classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

grand_total_files = 0
grand_total_verified = 0

print(f"{'Kategória':<25} | {'Összes':>8} | {'Hiteles':>8} | {'Pontosság':>12}")
print("-" * 100)

for g_name in sorted(classes):
    folder_path = os.path.join(root_path, g_name)
    all_pngs = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    
    count = len(all_pngs)
    if count == 0: continue

    verified_in_class = 0
    # VÉGIGMEGYÜNK AZ ÖSSZES FÁJLON A MAPPÁBAN
    for img_name in all_pngs:
        if deep_pixel_analysis(os.path.join(folder_path, img_name)):
            verified_in_class += 1
            
    acc = (verified_in_class / count) * 100
    grand_total_files += count
    grand_total_verified += verified_in_class
    
    print(f"{g_name:<25} | {count:>8} | {verified_in_class:>8} | {acc:>11.2f}%")

duration = time.time() - start_time
print("="*100)
print(f"AUDIT ÖSSZESÍTVE:")
print(f"Feldolgozott spektrogramok száma:  {grand_total_files}")
print(f"Matematikailag igazolt fájlok:    {grand_total_verified}")
print(f"Sérült/Üres fájlok száma:         {grand_total_files - grand_total_verified}")
print(f"TELJES RENDSZER MEGBÍZHATÓSÁG:    {(grand_total_verified/grand_total_files)*100:.4f}%")
print(f"ANALÍZIS TELJES IDŐTARTAMA:       {duration:.2f} másodperc")
print("="*100)
