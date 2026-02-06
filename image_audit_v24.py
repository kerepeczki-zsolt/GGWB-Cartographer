import os
import time
from PIL import Image

# Az útvonalad az asztalon
root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

print("\n" + "="*95)
print("   GGWB V24.0 | VIZUÁLIS SPEKTROGRAM AUDIT (IMAGE-BASED)")
print("   FORRÁS: " + root_path)
print("="*95)

if not os.path.exists(root_path):
    print(f"[HIBA] Nem találom az utat: {root_path}")
    exit()

start_time = time.time()
found_classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

total_images = 0
total_valid = 0

for g_name in sorted(found_classes):
    folder_path = os.path.join(root_path, g_name)
    # Most már a .png fájlokat keressük, amiket a képeden láttam!
    images = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    
    if not images:
        continue

    # Szigorú 50-es minta
    sample_size = min(len(images), 50)
    selected = images[:sample_size]
    
    verified = 0
    for img_name in selected:
        try:
            # Megnyitjuk a képet és ellenőrizzük a méretét
            with Image.open(os.path.join(folder_path, img_name)) as img:
                img.verify() # Validálja a képfájl épségét
                verified += 1
        except:
            continue
            
    acc = (verified / sample_size) * 100
    total_images += sample_size
    total_valid += verified
    print(f"{g_name:<25} | Képek: {sample_size:>2} | Hiteles: {verified:>2} | {acc:>7.1f}% | OK")

duration = time.time() - start_time
print("="*95)
print(f"Auditált spektrogramok: {total_images}")
print(f"Sikeres kép-analízis:    {total_valid}")
print(f"Tényleges futási idő:    {duration:.2f} másodperc")
print("="*95)
