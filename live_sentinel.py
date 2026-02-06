import subprocess
import time
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"
fetcher = os.path.join(project_root, "live_fetcher.py")
processor = os.path.join(project_root, "master_processor.py")

print("\n" + "="*60)
print("   GGWB V13.8 | AUTOMATA ÉLŐ VADÁSZAT INDÍTÁSA")
print("="*60)

while True:
    # 1. Friss adatok letöltése
    print(f"\n[{time.strftime('%H:%M:%S')}] Adatgyűjtés a LIGO-tól...")
    subprocess.run(["python", fetcher])
    
    # 2. Azonnali elemzés
    print(f"[{time.strftime('%H:%M:%S')}] Mély-diagnosztika futtatása...")
    subprocess.run(["python", processor])
    
    print("\n[INFO] Következő megfigyelési ciklus 15 perc múlva.")
    time.sleep(900) 
