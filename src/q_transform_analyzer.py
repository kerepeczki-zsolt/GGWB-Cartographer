import matplotlib.pyplot as plt
import os
from gwpy.timeseries import TimeSeries

def generate_q_transform(gps_time, detector="L1"):
    """
    Kiszámítja és kirajzolja a Q-transzformációt (spectrogram).
    Ez a modul mutatja meg a 'chirp' jelet a zajban.
    """
    print(f"[Q-SCAN] Q-transzformáció generálása ({detector})...")
    
    try:
        # Adat letöltése a Q-scanhez (szűkített ablak a jobb láthatóságért)
        data = TimeSeries.fetch_open_data(detector, gps_time - 2, gps_time + 2)
        
        # Q-transzformáció számítása 20Hz és 512Hz között
        q_gram = data.q_transform(frange=(20, 512))
        
        # Grafika elkészítése
        plot = q_gram.plot()
        ax = plot.gca()
        ax.set_title(f"LIGO {detector} Q-scan - GPS: {gps_time}")
        ax.set_yscale('log')
        ax.set_ylabel('Frekvencia [Hz]')
        ax.set_xlabel('Idő [s]')
        plot.add_colorbar(label='Energia')
        
        output_file = "q_transform_output.png"
        plot.savefig(output_file)
        plt.close(plot)
        
        print(f"[Q-SCAN] Spektrogram sikeresen elmentve: {output_file}")
        return output_file
    except Exception as e:
        print(f"[Q-SCAN] HIBA a generálás során: {e}")
        return None