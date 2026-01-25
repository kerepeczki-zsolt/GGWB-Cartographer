from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import os

def download_discovery_event():
    print("--- KAPCSOLÓDÁS A LIGO SZERVERÉHEZ ---")
    
    # GW150914 ideje: 1126259462
    t0 = 1126259462
    detector = 'H1'
    
    try:
        print(f"Adatok lekérése a {detector} detektorból...")
        # Csak 2 másodpercet kérünk le a teszthez
        data = TimeSeries.fetch_open_data(detector, t0 - 1, t0 + 1)
        
        print("Adatfeldolgozás: Q-transzformáció...")
        # Ez csinálja meg a 'Gravity Spy' stílusú képet a nyers rezgésből
        q_transform = data.q_transform(frange=(20, 500))
        
        # Grafikon készítése
        plot = q_transform.plot()
        ax = plot.gca()
        ax.set_yscale('log')
        ax.colorbar(label="Normalizált energia")
        
        if not os.path.exists('research_gallery'): os.makedirs('research_gallery')
        save_path = "research_gallery/REAL_GRAVITY_WAVE_H1.png"
        plot.save(save_path)
        print(f"SIKER! A valódi jel lementve ide: {save_path}")
        
    except Exception as e:
        print(f"Hiba történt az adatletöltés közben: {e}")

if __name__ == "__main__":
    download_discovery_event()