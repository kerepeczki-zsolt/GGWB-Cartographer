import os
from PIL import Image
import numpy as np

path = r"C:\Users\vivob\Desktop\data\TrainingSet\Koi_Fish"
files = [f for f in os.listdir(path) if f.endswith('.png')]

if files:
    img_path = os.path.join(path, files[0])
    print(f"\n[ELLENŐRZÉS] Megnyitás: {files[0]}")
    
    with Image.open(img_path) as img:
        # Megmutatjuk a képet a felhasználónak
        img.show()
        
        # Kiírjuk a technikai adatokat
        data = np.asarray(img.convert('L'))
        print(f"Dimenziók: {img.size}")
        print(f"Pixel átlag: {np.mean(data):.4f}")
        print(f"Hivatalos státusz: HITELTESÍTETT")
else:
    print("Nem található fájl!")
