import os
import sys

# Beállítjuk, hogy a Python lássa az src mappát
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from geometrical_glitch_detector import GeometricalExpertSystem
import final_report 

if __name__ == "__main__":
    print("\n" + "="*50)
    print("--- GGWB-CARTOGRAPHER: RUN MANAGER V11.0 ---")
    print("="*50)

    expert = GeometricalExpertSystem()
    
    # 1. ELEMZÉS
    print(">>> LIGO adatok feldolgozása a 92 geometria alapján...")
    res_1 = expert.classify_modification("LLO", "O2", 2.5, 20.0, 45.0, 0.1)
    print(f"EREDMÉNY 1 (45Hz): {res_1}")
    
    # 2. JELENTÉS GENERÁLÁSA
    print("\n>>> HIVATALOS JELENTÉS KÉSZÍTÉSE...")
    try:
        # Most már a pontos nevet hívjuk meg: generate_final_report
        path = final_report.generate_final_report()
        print(f">>> SIKER! A jelentés elkészült: {path}")
        print(f">>> A FÁJL DÁTUMA FRISSÜLT: {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f">>> HIBA a jelentésnél: {e}")

    print("="*50)