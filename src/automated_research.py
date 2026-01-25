import pandas as pd
import os
import sys

# Hozzáadjuk a keresési útvonalat, hogy lássa az agyat
sys.path.append(os.path.abspath("src"))
from gravity_spy_brain import GravitySpyBrain

def run_smart_analysis():
    input_file = "data/extracted_measurements.csv"
    if not os.path.exists(input_file):
        print("Hiba: Nincs bemeneti adat!")
        return

    # Betöltés és az agy bekapcsolása
    df = pd.read_csv(input_file)
    brain = GravitySpyBrain()
    
    # Minden egyes mérésnél megkérdezzük: "Ez melyik Gravity Spy hiba?"
    df['classification'] = df.apply(lambda x: brain.identify_by_geometry(x['f'], x['t']), axis=1)
    
    # Mentés a jelentéshez
    if not os.path.exists("GGWB_Results"): os.makedirs("GGWB_Results")
    df.to_csv("GGWB_Results/smart_analysis_results.csv", index=False)
    print(f">>> Elemzés kész! Típusok: {df['classification'].unique()}")

if __name__ == "__main__":
    run_smart_analysis()