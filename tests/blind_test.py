import os
import numpy as np
from PIL import Image
import random
import time

root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

print("\n" + "="*80)
print("   GGWB V29.0 | VAK-TESZT ÉS VIZUÁLIS HITELESÍTÉS")
print("   A RENDSZER VÁLASZT - TE DÖNTESZ")
print("="*80)

# Összes kategória összegyűjtése
classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
chosen_class = random.choice(classes)
class_path = os.path.join(root_path, chosen_class)

# Összes kép összegyűjtése a választott kategóriából
all_images = [f for f in os.listdir(class_path) if f.lower().endswith('.png')]

if not all_images:
    print("Hiba: Üres mappát választott a gép. Próbáld újra!")
    exit()

chosen_image = random.choice(all_images)
full_path = os.path.join(class_path, chosen_image)

print(f"[FOLYAMAT] Véletlenszerű fájl kiválasztva...")
time.sleep(1) # Egy kis feszültségkeltés
print(f"[ANALÍZIS] Kategória beazonosítva: {chosen_class}")
print(f"[ANALÍZIS] Fájlnév: {chosen_image}")

# Fizikai analízis
with Image.open(full_path) as img:
    data = np.asarray(img.convert('L'))
    mean_v = np.mean(data)
    std_v = np.std(data)
    
    print("-" * 50)
    print(f"MÉRT ADATOK:")
    print(f"Fényerő (átlag): {mean_v:.2f}")
    print(f"Zajszint (szórás): {std_v:.2f}")
    print(f"Felbontás: {img.size[0]}x{img.size[1]} pixel")
    print("-" * 50)
    
    print("\n[DÖNTÉS] Most nézd meg a képet! Ez valóban egy {chosen_class}?")
    print("A kép 3 másodpercen belül megnyílik...")
    time.sleep(3)
    img.show()

print("="*80)
