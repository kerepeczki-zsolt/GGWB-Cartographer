import pandas as pd
import os
import glob
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# PONTOS NÉV: geometrical
from geometrical_glitch_detector import GeometricalExpertSystem

def generate_final_report():
    results_dir = "GGWB_Results"
    files = glob.glob(f"{results_dir}/*.csv")
    if not files:
        print("HIBA: Nincs CSV! Előbb futtasd az automated_research.py-t!")
        return

    latest_file = max(files, key=os.path.getctime)
    df = pd.read_csv(latest_file)
    
    print("\n" + "═"*40)
    print("   GGWB TUDOMÁNYOS ÖSSZEGZÉS")
    print("═"*40)
    print(f"Események: {len(df)}")
    print(f"Forrás:    {os.path.basename(latest_file)}")
    print("═"*40 + "\n")

if __name__ == "__main__":
    generate_final_report()