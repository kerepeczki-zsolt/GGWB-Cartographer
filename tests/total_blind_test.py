import os
import numpy as np
from PIL import Image
import random
import time

root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

# 1. Összes fájl begyűjtése 'vak' módon
all_file_paths = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.lower().endswith('.png'):
            all_file_paths.append(os.path.join(root, file))

if not all_file_paths:
    print("Nem található kép!")
    exit()

# 2. Véletlen választás
random_file = random.choice(all_file_paths)

print("\n" + "="*90)
print("   GGWB V31.0 | TOTÁLIS VAK-ANALÍZIS - A GÉP NEM TUD SEMMIT")
print("="*90)
print("[INFO] Egy véletlenszerű fájl kiválasztva a 31 869-ből...")

# 3. Nyers pixel-elemzés
with Image.open(random_file) as img:
    data = np.asarray(img.convert('L'))
    mean_v = np.mean(data)
    std_v = np.std(data)
    
    print(f"\n[NYERS MÉRÉSI ADATOK]")
    print(f"Átlagos intenzitás: {mean_v:.2f}")
    print(f"Jel-zaj szórás: {std_v:.2f}")
    
    # 4. A gép 'tippje' a korábbi tapasztalatok alapján (Matematikai profil)
    prediction = "ISMERETLEN"
    if std_v > 100: prediction = "KOI FISH vagy BLIP (Erős, koncentrált jel)"
    elif 40 < std_v <= 100: prediction = "SCATTERED LIGHT vagy WHISTLE (Kiterjedt mintázat)"
    else: prediction = "NO GLITCH vagy LOW FREQUENCY (Alacsony energia)"

    print(f"\n[GÉPI JÓSLAT]: {prediction}")
    print("-" * 50)
    input("NYOMJ ENTER-T A VALÓSÁG FELFEDÉSÉHEZ ÉS A KÉP MEGNYITÁSÁHOZ...")
    
    # 5. Felfedés
    actual_class = os.path.basename(os.path.dirname(random_file))
    print(f"\n[VALÓSÁG]: Ez a fájl a(z) >> {actual_class} << mappából való.")
    print(f"Fájlnév: {os.path.basename(random_file)}")
    
    img.show()

print("="*90)
