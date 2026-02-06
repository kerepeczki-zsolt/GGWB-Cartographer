import numpy as np
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

def sync_all_populations():
    # Ez a lista tartalmazza az ÖSSZES hivatalos LIGO hiba-osztályt
    full_atlas = [
        "Air_Compressor", "1400_Ripple", "1080_Line", "Blip", "Chirp", 
        "Extremely_Loud", "Helix", "Koi_Fish", "Low_Frequency_Burst", 
        "Low_Frequency_Lines", "No_Glitch", "None_of_the_Above", 
        "Paired_Doves", "Power_Line", "Repeating_Blips", "Scattered_Light", 
        "Scratchy", "Tomte", "Violin_Mode", "Wandering_Line", "Whistle",
        "Light_Modulation", "CANDIDATE_GW"
    ]
    
    print(f"--- GGWB V12.5 | Adat-Szinkronizáció indítása ---")
    print(f"[INFO] Cél: Mind a {len(full_atlas)} populáció integrálása.")
    
    # Itt készítjük elő a mappastruktúrát az egyes típusok mintáinak
    for glitch_type in full_atlas:
        path = os.path.join(project_root, "catalog", glitch_type)
        if not os.path.exists(path):
            os.makedirs(path)
            
    print(f"[SIKER] A rendszered felkészült mind a {len(full_atlas)} típus fogadására.")
    print(">>> Következő lépés: Valódi minták letöltése a LIGO szervereiről.")

if __name__ == "__main__":
    sync_all_populations()
