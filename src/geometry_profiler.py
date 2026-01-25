import pandas as pd
import glob
import os
import json

class GeometryProfiler:
    def __init__(self, input_dir="knowledge_base/structured_training"):
        self.input_dir = input_dir
        self.output_profile = "knowledge_base/master_geometry_profile.json"

    def calculate_profiles(self):
        print(">>> Geometriai profilok számítása a teljes adatbázisból...")
        all_profiles = {}
        
        # Megkeressük az összes CSV-t, amit az előbb legeneráltunk
        csv_files = glob.glob(f"{self.input_dir}/*.csv")
        
        for file in csv_files:
            df = pd.read_csv(file)
            if df.empty: continue
            
            # Meghatározzuk a kategóriát a fájlnévből
            file_name = os.path.basename(file)
            if "GW_Candidates" in file_name:
                label = f"CLEAN_{file_name.split('_')[0]}_{file_name.split('_')[1]}" # Pl: CLEAN_H1_O4
            else:
                label = file_name.replace(".csv", "")

            # Kiszámoljuk az átlagos geometriai jellemzőket (Frekvencia, SNR mint energia)
            profile = {
                "avg_freq": float(df['peak_frequency'].mean()),
                "std_freq": float(df['peak_frequency'].std()),
                "avg_snr": float(df['snr'].mean()),
                "count": int(len(df))
            }
            all_profiles[label] = profile
            print(f" - Profil elkészült: {label} ({len(df)} minta alapján)")

        # Mentjük a Mester Profilt, amit a detektorunk használni fog
        with open(self.output_profile, 'w') as f:
            json.dump(all_profiles, f, indent=4)
        
        print(f"\n>>> SIKER! A Mester Geometriai Profil mentve: {self.output_profile}")

if __name__ == "__main__":
    profiler = GeometryProfiler()
    profiler.calculate_profiles()