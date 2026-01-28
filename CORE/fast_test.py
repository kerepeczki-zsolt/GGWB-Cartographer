import os
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt

def quick_spectrogram():
    print("--- GYORS SPEKTROGRAM GENERÁLÁSA (Valódi O3 adat) ---")
    detector = 'H1'
    # Csak 30 másodperc, hogy tényleg gyors legyen
    start = 1238166018
    end = start + 30
    
    try:
        print("1. Adatok letöltése...")
        data = TimeSeries.fetch_open_data(detector, start, end)
        
        print("2. Spektrogram számítása (ez a színes térkép)...")
        # Spektrogram készítése
        specgram = data.spectrogram(2, fftlength=1, overlap=0.5) ** 0.5
        
        print("3. Kép mentése...")
        plot = specgram.plot(norm='log')
        ax = plot.gca()
        ax.set_yscale('log')
        ax.set_ylim(10, 2000)
        plt.title(f"LIGO {detector} Spektrogram - V12 Valós Adat")
        
        # Elmentjük a REPORTS mappába
        os.makedirs("REPORTS", exist_ok=True)
        output_file = "REPORTS/elso_valodi_spektrogram.png"
        plt.savefig(output_file)
        
        print(f"✅ KÉSZ! A képet itt találod: {output_file}")
        
    except Exception as e:
        print(f"Hiba: {e}")

if __name__ == "__main__":
    quick_spectrogram()