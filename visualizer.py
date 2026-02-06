import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

# Útvonalak beállítása
data_dir = "C:/Users/vivob/GGWB_FINAL_V12/LIGO_VALIDATED_DATA"
sample_file = os.path.join(data_dir, "Koi_Fish_0.npy")

if os.path.exists(sample_file):
    data = np.load(sample_file)
    fs = 4096  # Mintavételi frekvencia

    # Spektrogram készítése (STFT - Short-Time Fourier Transform)
    f, t, Sxx = signal.spectrogram(data, fs, nperseg=256, noverlap=128)

    plt.figure(figsize=(12, 7), facecolor='#121212')
    ax = plt.axes()
    ax.set_facecolor('#121212')

    # Logaritmikus skálázás a jobb láthatóságért (dB-szerű)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='magma')
    
    plt.title("GGWB V12 | Spektrogram Analízis: 'Koi_Fish' Detektálva", color='white', fontsize=14)
    plt.ylabel("Frekvencia [Hz]", color='white')
    plt.xlabel("Idő [s]", color='white')
    plt.colorbar(label='Intenzitás (log)')
    plt.ylim(10, 1000)  # A lényegi tartományra fókuszálunk
    
    plt.tick_params(colors='white')
    print("\n[ANALÍZIS] Spektrogram ablak megnyitása...")
    plt.show()
else:
    print(f"\n[HIBA] Nem található a fájl: {sample_file}")
