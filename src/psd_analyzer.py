import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

def calculate_psd(strain_data, fs=4096):
    """
    Kiszámítja a jel teljesítménysűrűség-spektrumát (PSD).
    Ez mutatja meg, mely frekvenciákon 'zajos' a detektorunk.
    """
    print("[PSD] Frekvencia-analízis indítása...")
    
    # Welch-metódus használata a spektrum becsléséhez
    frequencies, psd_values = signal.welch(strain_data, fs, nperseg=fs//4)
    
    # Grafikon készítése
    plt.figure(figsize=(10, 5))
    plt.semilogy(frequencies, psd_values, color='darkgreen')
    plt.title("GGWB-Cartographer: Spektrális Érzékenység (PSD)")
    plt.xlabel("Frekvencia [Hz]")
    plt.ylabel("Teljesítmény [strain^2/Hz]")
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    output_file = "psd_analysis.png"
    plt.savefig(output_file)
    plt.close()
    
    print(f"[PSD] Spektrum elmentve: {os.path.abspath(output_file)}")
    return frequencies, psd_values

if __name__ == "__main__":
    # Teszt valósághűbb zajjal (szűrt zaj)
    sample_data = np.random.normal(0, 1, 16384)
    calculate_psd(sample_data)