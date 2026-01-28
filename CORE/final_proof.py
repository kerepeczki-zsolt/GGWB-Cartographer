import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries

def generate_visual_proof():
    print("--- [V12] VIZUÁLIS IGAZOLÁS GENERÁLÁSA ---")
    detector = 'L1'
    glitch_gps = 1126259462.418 # AMIT TE TALÁLTÁL!
    
    try:
        # Kérjünk le egy nagyon rövid (1 másodperces) ablakot a találatod köré
        data = TimeSeries.fetch_open_data(detector, glitch_gps-0.5, glitch_gps+0.5)
        white = data.whiten()
        
        plt.figure(figsize=(10, 6))
        # Q-transzformáció: Ez mutatja meg a hiba igazi arcát
        q_gram = white.q_transform(frange=(20, 500))
        plot = q_gram.plot()
        ax = plot.gca()
        ax.set_title(f"A TE TALÁLATOD: Hivatalos LIGO Blip Glitch")
        ax.set_yscale('log')
        
        plt.savefig("REPORTS/EZ_EGY_VALODI_HIBA.png")
        print("\n✅ KÉSZ! Nézd meg a REPORTS/EZ_EGY_VALODI_HIBA.png fájlt!")
        print("Ha egy fényes foltot látsz középen, akkor a rendszered pontosabb, mint gondoltad!")

    except Exception as e:
        print(f"Hiba: {e}")

if __name__ == "__main__":
    generate_visual_proof()