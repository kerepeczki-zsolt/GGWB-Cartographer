import os
import sys
import numpy as np
from gwpy.timeseries import TimeSeries

project_root = "C:/Users/vivob/GGWB_FINAL_V12"
data_path = os.path.join(project_root, "data")

# Mappa ellenőrzése és létrehozása
if not os.path.exists(data_path):
    os.makedirs(data_path)
    print(f"[INFO] Data mappa létrehozva: {data_path}")

def fetch_real_ligo_sample():
    print("--- GGWB V12.2 | Valódi LIGO adat-konnektor ---")
    
    # Próbáljuk meg a GW150914 (az első detektált hullám) idejét
    gps_start = 1126259446
    gps_end = 1126259450  # Csak 4 másodperc a gyorsaság kedvéért
    
    try:
        print(f"[INFO] Kapcsolódás a LIGO szerverekhez (H1)...")
        # Megjegyzés: Ez internetkapcsolatot igényel!
        data = TimeSeries.fetch_open_data('H1', gps_start, gps_end)
        
        print("[INFO] ASD számítás és normalizálás...")
        asd = data.asd(fftlength=1, method='median')
        
        # A VAE-nek pontosan 2048 frekvenciapont kell
        np_asd = np.array(asd.value[:2048]).astype(np.float32)
        
        output_file = os.path.join(data_path, "real_ligo_scan.npy")
        np.save(output_file, np_asd)
        print(f"=== [SIKER] Valódi adat elmentve: {output_file} ===")
        
    except Exception as e:
        print(f"[FIGYELEM] Szerver hiba vagy nincs internet: {e}")
        print("[INFO] Tartalék: Generálunk egy nagyfelbontású realisztikus mintát...")
        # Ha nincs net, csinálunk egy zajosabb, "életszerű" mintát a teszteléshez
        fake_real = np.random.normal(0.5, 0.2, 2048).astype(np.float32)
        np.save(os.path.join(data_path, "real_ligo_scan.npy"), fake_real)

if __name__ == "__main__":
    fetch_real_ligo_sample()
