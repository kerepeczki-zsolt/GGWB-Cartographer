import os
import pandas as pd

def load_local_data(detector, data_path="data/"):
    """
    Betölti a helyi CSV adatokat a megadott detektorhoz.
    """
    file_name = f"{detector}_O3b_mini.csv"
    full_path = os.path.join(data_path, file_name)
    
    print(f"🔍 Keresem az adatokat: {full_path}")
    
    if os.path.exists(full_path):
        data = pd.read_csv(full_path)
        print(f"✅ {detector} adatok betöltve: {len(data)} sor.")
        return data
    else:
        print(f"⚠️ FIGYELEM: Nem találom a fájlt: {full_path}")
        return None