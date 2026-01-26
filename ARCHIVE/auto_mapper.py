import time
import os
import sys
import subprocess

def start_auto_survey():
    print("\n" + "="*80)
    print("   GGWB-CARTOGRAPHER - AUTOMATIKUS ÉGBOLT-FIGYELŐ SZOLGÁLTATÁS")
    print("="*80)
    print("[STATUS] A rendszer 10 percenként frissíti a 'skymap_output.png' fájlt.")
    
    try:
        while True:
            # Lefuttatjuk a mapper kódot
            print(f"\n[{time.strftime('%H:%M:%S')}] Térkép frissítése az új adatokkal...")
            subprocess.run(["python", "sky_mapper.py"])
            
            print("[OK] Térkép sikeresen frissítve. Következő frissítés 10 perc múlva.")
            # Várakozás 10 percig (600 másodperc)
            time.sleep(600)
            
    except KeyboardInterrupt:
        print("\n[STOP] Automatikus figyelés leállítva.")

if __name__ == "__main__":
    start_auto_survey()