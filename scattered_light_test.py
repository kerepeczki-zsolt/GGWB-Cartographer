import os
import numpy as np
from PIL import Image
import random

# Útvonal beállítása
path = r"C:\Users\vivob\Desktop\data\TrainingSet\Scattered_Light"

print("\n" + "="*80)
print("   SZÓRT FÉNY (SCATTERED LIGHT) - TUDOMÁNYOS KONTRÓLL")
print("="*80)

if not os.path.exists(path):
    print(f"HIBA: Nem találom a mappát itt: {path}")
    exit()

files = [f for f in os.listdir(path) if f.lower().endswith('.png')]
count = len(files)

if count == 0:
    print("Mappa üres vagy nem tartalmaz PNG fájlokat!")
    exit()

print(f"Talált fájlok száma: {count}")

# 5 véletlen minta elemzése
samples = random.sample(files, min(5, count))
for i, f_name in enumerate(samples):
    full_p = os.path.join(path, f_name)
    with Image.open(full_p) as img:
        data = np.asarray(img.convert('L'))
        mean_v = np.mean(data)
        std_v = np.std(data)
        print(f"[{i+1}] {f_name:<40} | Átlag: {mean_v:>6.2f} | Zaj: {std_v:>6.2f}")

# Az első kép megnyitása vizuális ellenőrzésre
first_img = os.path.join(path, files[0])
print("\n" + "="*80)
print(f"VIZUÁLIS IGAZOLÁS: Megnyitom a(z) {files[0]} fájlt...")
print("="*80)

with Image.open(first_img) as img:
    img.show()
