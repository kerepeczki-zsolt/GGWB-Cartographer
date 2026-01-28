import os
import pandas as pd
from framework.config.ggwb_config import CONFIG

def fetch_local_data(detector):
    """LIGO-Grade adatbeolvasás a konfig alapján."""
    # A konfigból kiolvassuk, hol vannak az adatok
    data_path = CONFIG["paths"]["data"]
    # A konfigból kiolvassuk a fájl pontos nevét (GITHUB_STRESS_TEST_1000.csv)
    file_name = CONFIG["file_names"].get(detector)
    
    if not file_name:
        print(f"⚠️ Nincs fájlnév megadva a {detector} detektorhoz!")
        return None
        
    full_path = os.path.join(data_path, file_name)
    
    if os.path.exists(full_path):
        print(f"✅ ADATFOLYAM MEGNYITVA: {full_path}")
        df = pd.read_csv(full_path)
        return df
    else:
        print(f"❌ HIBA: Nem található a fájl: {full_path}")
        return None