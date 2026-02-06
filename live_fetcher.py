from gwpy.timeseries import TimeSeries
import os
import time

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

def fetch_safe_data():
    print("--- GGWB V13.7 | BIZTONSÁGOS ADATLEKÉRÉS ---")
    
    # Nem a legutolsó másodpercet kérjük, hanem visszaugrunk 3 órát
    # Így biztosan benne leszünk a már publikált Open Data tartományban
    try:
        # Keressük meg az utolsó elérhető adatot (H1 detektor)
        print("[SZERVER] Kapcsolódás a GWOSC-hez...")
        
        # Ez a GPS idő garantáltan tartalmaz adatot tesztelésre (O3 run vége felé)
        # Később ezt automatizáljuk a legfrissebb elérhetőre
        start_time = 1251651618 
        end_time = start_time + 10
        
        data = TimeSeries.fetch_open_data('H1', start_time, end_time)
        
        save_path = os.path.join(project_root, "data", "live_stream.npy")
        import numpy as np
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
            
        np.save(save_path, data.value)
        print(f"[SIKER] 10 másodpercnyi éles adat lementve: {save_path}")

    except Exception as e:
        print(f"[HIBA] Adatlekérési hiba: {e}")

if __name__ == "__main__":
    fetch_safe_data()
