# main.py - GGWB-Cartographer V12 Milestone (Nagy fájlok nélkül)
import cartographer_v12_expert_final as v12

def start_mapping():
    print("--- GGWB-Cartographer V12 ---")
    print("Státusz: Stabil (Nagy adathalmazok leválasztva)")
    try:
        # Csak a matematikai modellt futtatjuk
        v12.run_analysis()
        print("Sikeres analízis.")
    except Exception as e:
        print(f"Hiba: {e}")

if __name__ == "__main__":
    start_mapping()