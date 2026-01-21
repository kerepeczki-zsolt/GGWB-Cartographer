<<<<<<< HEAD
import os
import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Interferométerek: H1 (Hanford), L1 (Livingston)
INTERFEROMETERS = ['H1', 'L1']

# Útvonalak beállítása
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'data'))

def generate_spectrograms(max_images=5):
    """Garantált adatokat keres a LIGO aranykorából."""
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    found_count = 0
    
    # 2019. augusztus 14. - GW190814 esemény napja.
    # Ekkor a detektorok stabilan mértek (Science Mode).
    current_date = datetime(2019, 8, 14, 21, 0) 
    end_date = current_date + timedelta(hours=5)

    print(f"\n>>> LIGO ADATBÁNYÁSZAT INDÍTÁSA (Célpont: 2019-08-14)")
    print(f">>> Mentési hely: {DATA_DIR}\n")
    
    while current_date < end_date and found_count < max_images:
        for ifo in INTERFEROMETERS:
            start_gps = current_date.timestamp()
            # 500 másodperces darabokat töltünk le (kb. 8 perc)
            end_gps = start_gps + 500 
            
            try:
                print(f"Lekérés: {ifo} | Idő: {current_date.strftime('%H:%M:%S')}")
                
                # Adat letöltése
                strain = TimeSeries.fetch_open_data(ifo, start_gps, end_gps, cache=True)
                
                # Jel feldolgozása (glitch-ek kiemelése)
                white = strain.whiten()
                bp = white.bandpass(10, 300)
                spec = bp.spectrogram(fftlength=4, overlap=2) ** 0.5
                
                # Spektrogram kirajzolása
                plot = spec.plot(norm='log', vmin=1e-24, vmax=1e-20)
                ax = plot.gca()
                ax.set_axis_off() 
                
                # Fájlnév generálása és mentés
                filename = os.path.join(DATA_DIR, f"spec_{ifo}_{int(start_gps)}.png")
                plot.savefig(filename, bbox_inches='tight', pad_inches=0)
                plt.close()
                
                print(f"--- SIKER! Kép mentve: {os.path.basename(filename)}")
                found_count += 1
                
            except Exception as e:
                # Ha ezen a rövid szakaszon nincs adat, megyünk tovább
                continue

        # Ha végeztünk az interferométerekkel, ugrunk 10 percet előre
        current_date += timedelta(minutes=10)

    if found_count > 0:
        print(f"\nKÉSZ! {found_count} kép vár a 'data' mappában az elemzésre.")
    else:
        print("\nMég mindig nem találtunk adatot. Ellenőrizd az internetkapcsolatot!")

if __name__ == "__main__":
=======
import os
import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Interferométerek: H1 (Hanford), L1 (Livingston)
INTERFEROMETERS = ['H1', 'L1']

# Útvonalak beállítása
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'data'))

def generate_spectrograms(max_images=5):
    """Garantált adatokat keres a LIGO aranykorából."""
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    found_count = 0
    
    # 2019. augusztus 14. - GW190814 esemény napja.
    # Ekkor a detektorok stabilan mértek (Science Mode).
    current_date = datetime(2019, 8, 14, 21, 0) 
    end_date = current_date + timedelta(hours=5)

    print(f"\n>>> LIGO ADATBÁNYÁSZAT INDÍTÁSA (Célpont: 2019-08-14)")
    print(f">>> Mentési hely: {DATA_DIR}\n")
    
    while current_date < end_date and found_count < max_images:
        for ifo in INTERFEROMETERS:
            start_gps = current_date.timestamp()
            # 500 másodperces darabokat töltünk le (kb. 8 perc)
            end_gps = start_gps + 500 
            
            try:
                print(f"Lekérés: {ifo} | Idő: {current_date.strftime('%H:%M:%S')}")
                
                # Adat letöltése
                strain = TimeSeries.fetch_open_data(ifo, start_gps, end_gps, cache=True)
                
                # Jel feldolgozása (glitch-ek kiemelése)
                white = strain.whiten()
                bp = white.bandpass(10, 300)
                spec = bp.spectrogram(fftlength=4, overlap=2) ** 0.5
                
                # Spektrogram kirajzolása
                plot = spec.plot(norm='log', vmin=1e-24, vmax=1e-20)
                ax = plot.gca()
                ax.set_axis_off() 
                
                # Fájlnév generálása és mentés
                filename = os.path.join(DATA_DIR, f"spec_{ifo}_{int(start_gps)}.png")
                plot.savefig(filename, bbox_inches='tight', pad_inches=0)
                plt.close()
                
                print(f"--- SIKER! Kép mentve: {os.path.basename(filename)}")
                found_count += 1
                
            except Exception as e:
                # Ha ezen a rövid szakaszon nincs adat, megyünk tovább
                continue

        # Ha végeztünk az interferométerekkel, ugrunk 10 percet előre
        current_date += timedelta(minutes=10)

    if found_count > 0:
        print(f"\nKÉSZ! {found_count} kép vár a 'data' mappában az elemzésre.")
    else:
        print("\nMég mindig nem találtunk adatot. Ellenőrizd az internetkapcsolatot!")

if __name__ == "__main__":
>>>>>>> e93f1bf2 (Fix CI and update features)
    generate_spectrograms()