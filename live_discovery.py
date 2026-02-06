import numpy as np
import os
from master_processor import GGWB_Universal_Validator

def run_live_discovery():
    print("\n" + "!"*60)
    print("   GGWB V18.0 | ÉLES GRAVITÁCIÓS HULLÁM FIGYELŐ")
    print("!"*60)
    validator = GGWB_Universal_Validator()
    
    # Itt szimuláljuk az élő adatfolyamot a Hanford detektorból
    while True:
        # Generálunk egy kis zajt + néha egy véletlenszerű eseményt
        live_data = np.random.normal(0, 1, 4096)
        
        # 5% esély egy valódi jelre az univerzumból
        if np.random.rand() > 0.95:
             # Beoltunk egy GW-t, hogy lássuk a riasztást élesben
             t = np.linspace(0, 0.5, 2048)
             live_data[1000:3048] += 25 * np.sin(2 * np.pi * (40 + 160 * t**2))
        
        res, conf, freq = validator.deep_scan(live_data, 0)
        
        if res == "CANDIDATE_GW" and conf > 95:
            print(f"\a[RIASZTÁS] !!! {res} DETEKTÁLVA !!!")
            print(f"Biztonság: {conf}% | Frekvencia: {freq:.2f} Hz")
            print("-" * 60)
        
        time.sleep(1) # 1 másodperces frissítés

if __name__ == "__main__":
    import time
    run_live_discovery()
