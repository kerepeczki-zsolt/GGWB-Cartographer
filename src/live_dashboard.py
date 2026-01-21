import time
import os
import sys
import numpy as np

# Útvonal hozzáadása, hogy a src mappából lássuk a főkönyvtárat
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from detektor import run_cartographer_analysis
except ImportError as e:
    print(f"HIBA: Nem sikerült betölteni a detektor modult! {e}")
    sys.exit(1)

def start_live_monitoring(iterations=3):
    """
    Folyamatosan futtatja az elemzést.
    Zsolt, ez a javított verzió már látja a szülőmappa fájljait is.
    """
    print("="*60)
    print("      GGWB-CARTOGRAPHER ÉLŐ MONITOR (v0.9.3)")
    print("="*60)
    
    current_gps = 1126259462 
    
    for i in range(iterations):
        print(f"\n>>> {i+1}. MÉRÉSI CIKLUS")
        
        # Szimulált élő adatok
        live_strain = np.random.normal(0, 1, 4096)
        
        # Analízis futtatása
        status = run_cartographer_analysis(current_gps, live_strain)
        
        print(f"CIKLUS KÉSZ. Aktuális státusz: {status}")
        
        if i < iterations - 1:
            print("Várakozás a következő adatszeletre (5 mp)...")
            time.sleep(5)
        
        current_gps += 4 

    print("\n" + "="*60)
    print("      MONITOROZÁSI SZAKASZ VÉGE")
    print("="*60)

if __name__ == "__main__":
    start_live_monitoring()