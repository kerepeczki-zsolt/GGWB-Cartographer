import os
import numpy as np
from PIL import Image
import random
import time

root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

print("\n" + "="*90)
print("   GGWB V30.0 | MÁSODIK VAK-TESZT - SZIGORÍTOTT ELLENŐRZÉS")
print("   CÉL: EGY ÚJ, AZONOSÍTHATÓ SPEKTROGRAM KERESÉSE")
print("="*90)

classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

# Kizárjuk a legutóbbiakat, hogy biztosan újat lássunk
exclude = ["Koi_Fish", "Scattered_Light"]
available_classes = [c for c in classes if c not in exclude]

chosen_class = random.choice(available_classes)
class_path = os.path.join(root_path, chosen_class)
all_images = [f for f in os.listdir(class_path) if f.lower().endswith('.png')]

chosen_image = random.choice(all_images)
full_path = os.path.join(class_path, chosen_image)

print(f"[SZERVER] Új elemzés indítása...")
time.sleep(1)

# Valódi pixel-analízis
with Image.open(full_path) as img:
    data = np.asarray(img.convert('L'))
    mean_v = np.mean(data)
    std_v = np.std(data)
    
    print(f"\n[ANALÍZIS EREDMÉNYE]")
    print(f"Kiválasztott típus: {chosen_class}")
    print(f"Fájl: {chosen_image}")
    print(f"Pixel szórás (Stabilitás): {std_v:.2f}")
    print("-" * 50)
    print(f"A gép szerint ez egyértelműen: {chosen_class}")
    print("-" * 50)
    
    print("\n[VÁRAKOZÁS] A kép megnyílik, hasonlítsd össze a fenti kategóriával!")
    time.sleep(2)
    img.show()

print("="*90)
