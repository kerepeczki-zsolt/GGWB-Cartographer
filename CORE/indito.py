import os
import shutil

BASE_PATH = r'data\O3'
SOURCE_DIR = os.path.join(BASE_PATH, 'TrainingSet', 'No_Glitch')

def ggwb_cartographer_intelligent_sorter():
    if not os.path.exists(SOURCE_DIR):
        print(f"HIBA: Forrás nem található: {SOURCE_DIR}")
        return
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.png')]
    for f in files:
        if f.startswith('H1'): det = 'H1'
        elif f.startswith('L1'): det = 'L1'
        elif f.startswith('V1'): det = 'V1'
        else: continue
        target_raw_dir = os.path.join(BASE_PATH, det, 'raw')
        os.makedirs(target_raw_dir, exist_ok=True)
        shutil.copy(os.path.join(SOURCE_DIR, f), os.path.join(target_raw_dir, f))
    print("Sikeres szétválogatás!")

if __name__ == "__main__":
    ggwb_cartographer_intelligent_sorter()