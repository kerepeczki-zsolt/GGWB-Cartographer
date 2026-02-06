import numpy as np
import os
import time

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"
from master_processor import GGWB_Final_Validator

def run_mass_test(count=50):
    print(f"=== GGWB V16.0 | TÖMEGES STRESSZ-TESZT ({count} jel/típus) ===")
    validator = GGWB_Final_Validator()
    results = {"Violin_Mode": 0, "CANDIDATE_GW": 0}
    
    fs = 4096
    
    # TESZT 1: 50 darab Violin Mode generálása és tesztelése
    print(f"Tesztelés: Violin_Mode...")
    for _ in range(count):
        # Kicsit variáljuk a frekvenciát 490 és 510 Hz között, hogy ne legyen egyforma
        freq = np.random.uniform(490, 510)
        t = np.linspace(0, 1, fs)
        signal = 20 * np.sin(2 * np.pi * freq * t)
        
        res, conf, f = validator.deep_scan(signal, 0)
        if res == "Violin_Mode":
            results["Violin_Mode"] += 1

    # TESZT 2: 50 darab Gravitációs Hullám (Chirp)
    print(f"Tesztelés: CANDIDATE_GW...")
    for _ in range(count):
        t = np.linspace(0, 0.5, 2048)
        # Variáljuk a kezdőfrekvenciát
        start_f = np.random.uniform(30, 50)
        chirp = 15 * np.sin(2 * np.pi * (start_f + 100 * t**2))
        full_signal = np.zeros(fs)
        full_signal[:2048] = chirp
        
        res, conf, f = validator.deep_scan(full_signal, 0)
        if res == "CANDIDATE_GW":
            results["CANDIDATE_GW"] += 1

    print("\n--- ÖSSZESÍTETT EREDMÉNYEK ---")
    for key, val in results.items():
        accuracy = (val / count) * 100
        print(f"{key:<15} | Találat: {val}/{count} | Pontosság: {accuracy}%")

if __name__ == "__main__":
    run_mass_test(50)
