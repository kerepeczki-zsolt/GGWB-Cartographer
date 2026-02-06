import os
import numpy as np
from PIL import Image
import random

path = r"C:\Users\vivob\Desktop\data\TrainingSet\Koi_Fish"
files = [f for f in os.listdir(path) if f.endswith('.png')]

print("\n" + "="*70)
print("   KOI FISH - MÉLY-ELLENŐRZÉS (PIXEL STATISZTIKA)")
print("="*70)

if len(files) < 5:
    print("Nincs elég fájl!")
    exit()

test_samples = random.sample(files, 5)

for i, f_name in enumerate(test_samples):
    full_p = os.path.join(path, f_name)
    with Image.open(full_p) as img:
        data = np.asarray(img.convert('L'))
        mean_val = np.mean(data)
        std_val = np.std(data)
        print(f"[{i+1}] Fájl: {f_name}")
        print(f"    Átlagos fényerő: {mean_val:.2f}")
        print(f"    Pixel szórás (Zaj): {std_val:.2f}")
        print(f"    Dimenzió: {img.size}")
        print("-" * 50)

print("="*70)
print("VÉLEMÉNY: Ha az összes fájl értéke hajszálpontosan ugyanaz, akkor")
print("a fájlok duplikátumok! Ha eltérnek, akkor valódi adatok.")
print("="*70)
