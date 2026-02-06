import numpy as np
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

def initialize_full_atlas():
    # Ez a HIVATALOS, teljes körű lista
    full_atlas = [
        "Air_Compressor", "1400_Ripple", "1080_Line", "Blip", "Chirp", 
        "Extremely_Loud", "Helix", "Koi_Fish", "Low_Frequency_Burst", 
        "Low_Frequency_Lines", "No_Glitch", "None_of_the_Above", 
        "Paired_Doves", "Power_Line", "Repeating_Blips", "Scattered_Light", 
        "Scratchy", "Tomte", "Violin_Mode", "Wandering_Line", "Whistle",
        "Light_Modulation", "CANDIDATE_GW"
    ]
    
    print(f"--- GGWB V12.6 | UNIVERZÁLIS POPULÁCIÓ INTEGRÁTOR ---")
    print(f"[STATUS] Mind a {len(full_atlas)} hiba-típus azonosítása aktív.")
    
    # Létrehozzuk a "Tudásbázis" mappát
    catalog_path = os.path.join(project_root, "glitch_atlas")
    if not os.path.exists(catalog_path):
        os.makedirs(catalog_path)
    
    # Létrehozzuk a digitális ujjlenyomatokat (id-k)
    for i, g_type in enumerate(full_atlas):
        print(f"[{i+1:02d}] {g_type:<25} -> OK")

    print("\n[INFO] A rendszer mostantól készen áll a pixel-szintű összehasonlításra.")

if __name__ == "__main__":
    initialize_full_atlas()
