import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries

def generate_visual_proof_fixed():
    print("--- [V12] VÉGSŐ VIZUÁLIS IGAZOLÁS (Javított) ---")
    detector = 'L1'
    # A te pontos találatod!
    glitch_gps = 1126259462.418 
    
    try:
        # Kicsit hosszabb mintát veszünk (4 másodperc), hogy az algoritmus ne hibázzon
        data = TimeSeries.fetch_open_data(detector, glitch_gps-2, glitch_gps+2)
        white = data.whiten()
        
        # Sima spektrogram, ami mindig működik
        specgram = white.spectrogram2(fftlength=0.1, overlap=0.05)
        plot = specgram.plot(norm='log')
        ax = plot.gca()
        ax.set_yscale('log')
        ax.set_ylim(20, 500)
        ax.colorbar(label='Energia')
        plt.title(f"A RENDSZERED ÁLTAL TALÁLT HIBA: GPS {glitch_gps}")
        
        plt.savefig("REPORTS/IGAZOLT_HIBA_SPEKTROGRAM.png")
        print("\n✅ SIKER! A kép elmentve: REPORTS/IGAZOLT_HIBA_SPEKTROGRAM.png")
        print("Ha látsz egy sárga/fényes foltot a közepén, az a te trófeád!")

    except Exception as e:
        print(f"Hiba: {e}")

if __name__ == "__main__":
    generate_visual_proof_fixed()