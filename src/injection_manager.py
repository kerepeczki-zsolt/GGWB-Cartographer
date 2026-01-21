import numpy as np
import pandas as pd
import os

def create_synthetic_chirp(output_path="data/injected_signal.csv"):
    print("--- 1. Lépés: Szintetikus gravitációs jel generálása (Offline mód) ---")
    
    # Paraméterek beállítása
    fs = 4096  # Mintavételi frekvencia (LIGO standard)
    duration = 2.0  # Időtartam (másodperc)
    t = np.linspace(0, duration, int(fs * duration))

    # Egy 'chirp' jel generálása (emelkedő frekvencia, mint a fekete lyukaknál)
    f_start = 30   # Kezdő frekvencia (Hz)
    f_end = 250    # Vég frekvencia (Hz)
    
    # Frekvencia-modulált szinusz hullám
    signal = np.sin(2 * np.pi * (f_start * t + (f_end - f_start) * t**2 / (2 * duration)))
    
    # Ablakfüggvény alkalmazása (Hanning), hogy a jel finoman induljon és érjen véget
    window = np.hanning(len(t))
    signal = signal * window * 1e-21  # Reális amplitúdó skálázás

    # Ellenőrizzük, hogy létezik-e a data mappa
    if not os.path.exists('data'):
        os.makedirs('data')

    # Adatok mentése DataFrame-be
    df = pd.DataFrame({'time': t, 'strain': signal})
    df.to_csv(output_path, index=False)
    
    print(f"--- 2. Lépés: Sikeres mentés ide: {output_path} ---")
    print(f"Generált adatpontok száma: {len(df)}")

if __name__ == "__main__":
    create_synthetic_chirp()