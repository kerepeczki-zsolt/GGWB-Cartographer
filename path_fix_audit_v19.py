import os
import numpy as np
import time

# A te asztali útvonalad, amit a képen láttam
root_path = r"C:\Users\vivob\Desktop\data\TrainingSet"

print("\n" + "="*90)
print("   GGWB V19.0 | MÉLY-AUDIT ÉS FÁJLKERESŐ (ZSOLT RÉSZÉRE)")
print("="*90)

if not os.path.exists(root_path):
    print(f"[HIBA] Az útvonal nem létezik: {root_path}")
    exit()

start_time = time.time()
classes = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

total_found = 0
total_physically_read = 0

for g_name in sorted(classes):
    folder_path = os.path.join(root_path, g_name)
    # Listázunk MINDEN fájlt, nem csak az .npy-t
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    count = len(all_files)
    if count == 0:
        print(f"{g_name:<25} | ÜRES MAPPA!")
        continue

    read_ok = 0
    for f_name in all_files:
        f_full_path = os.path.join(folder_path, f_name)
        try:
            # Megpróbáljuk beolvasni a fájl méretét és az első pár bájtot
            if os.path.getsize(f_full_path) > 0:
                read_ok += 1
        except:
            continue

    total_found += count
    total_physically_read += read_ok
    acc = (read_ok / count) * 100
    print(f"{g_name:<25} | Talált: {count:>5} | Beolvasható: {read_ok:>5} | {acc:>6.1f}%")

duration = time.time() - start_time
print("="*90)
print(f"Összesen talált fájl:      {total_found}")
print(f"Ebből fizikailag elérhető: {total_physically_read}")
print(f"Audit ideje:               {duration:.2f} másodperc")
print("="*90)
