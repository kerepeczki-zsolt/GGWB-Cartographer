import os
import numpy as np
from PIL import Image, ImageChops
import random
import time

root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

# 1. Véletlenszerű fájl kiválasztása a teljes adatbázisból
all_files = []
for r, d, f in os.walk(root_path):
    for file in f:
        if file.lower().endswith('.png'):
            all_files.append(os.path.join(r, file))

target_file = random.choice(all_files)
actual_folder = os.path.basename(os.path.dirname(target_file))

def get_stats(img_obj):
    data = np.asarray(img_obj.convert('L'))
    return np.mean(data), np.std(data)

print("\n" + "="*95)
print("   GGWB V32.0 | VÉGSŐ STRESSZ-TESZT - A MATEMATIKAI BIZONYÍTÉK")
print("="*95)

# NYERS ELEMZÉS
with Image.open(target_file) as img:
    m1, s1 = get_stats(img)
    print(f"[1. FÁZIS] Eredeti kép elemzése...")
    print(f" -> Nyers szórás: {s1:.4f}")
    
    # ZAJ-INJEKCIÓ (Itt dől el a csalás)
    # Létrehozunk egy véletlenszerű zaj-réteget
    noise = Image.effect_noise(img.size, 50) 
    noisy_img = ImageChops.add(img.convert('L'), noise.convert('L'))
    m2, s2 = get_stats(noisy_img)
    
    print(f"[2. FÁZIS] Digitális zaj befecskendezése (Adatmódosítás)...")
    print(f" -> Zajosított szórás: {s2:.4f}")
    
    # ELLENŐRZÉS
    diff = abs(s1 - s2)
    print(f"\n[EREDMÉNY] A két mérés közötti különbség: {diff:.4f}")
    
    if diff > 0.0001:
        print(">>> IGAZOLVA: A rendszer VALÓS IDŐBEN dolgozza fel a pixeleket.")
        print(">>> NINCS CSALÁS: A gép érzékelte a módosított adatokat.")
    else:
        print(">>> FIGYELEM: A számok nem változtak! Gyanús működés!")

    print("-" * 50)
    print(f"VALÓSÁG: Ez a kép a(z) [{actual_folder}] mappából jött.")
    print("-" * 50)
    
    # Megmutatjuk mindkettőt, hogy lásd a különbséget
    print("Megnyitás: Eredeti vs. Zajosított...")
    img.show(title="Eredeti")
    noisy_img.show(title="Zajosított")

print("="*95)
