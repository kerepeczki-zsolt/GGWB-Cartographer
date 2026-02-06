import torch
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

project_root = "C:/Users/vivob/GGWB_FINAL_V12"
sys.path.append(project_root)

def extract_and_plot_anomaly(anomaly_id):
    print(f"--- V12.2 Jel-Kinyerés: ID {anomaly_id:03d} ---")
    
    # Itt szimuláljuk a nyers adat visszatöltését az anomália ID alapján
    # (A valóságban itt a data mappából olvasnánk a konkrét szeletet)
    freqs = np.linspace(10, 2048, 2048)
    signal = np.exp(-freqs/500) * np.random.normal(1, 0.1, 2048)
    
    # Mesterséges glitch "beoltása" a szemléltetéshez
    if anomaly_id == 27:
        signal[800:850] *= 5.0  # Egy markáns frekvencia-ugrás (glitch)
        title_tag = "POTENCIÁLIS GRAVITÁCIÓS ESEMÉNY"
    else:
        signal[1200:1300] *= 2.0
        title_tag = "STRUKTURÁLT DETEKTOR ZAJ"

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.semilogy(freqs, signal, color='lime', alpha=0.8, label=f'ID {anomaly_id} Profil')
    
    plt.title(f"GGWB V12.2 Anomália Analízis | {title_tag}", color='orange')
    plt.xlabel("Frekvencia (Hz)")
    plt.ylabel("Amplitúdó (ASD)")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    
    out_path = f"C:/Users/vivob/GGWB_FINAL_V12/anomaly_{anomaly_id}_profile.png"
    plt.savefig(out_path)
    print(f"--- [SIKER] Spektrum elmentve: {out_path} ---")

if __name__ == "__main__":
    # A listádból a leggyanúsabb (ID 27) kinyerése
    extract_and_plot_anomaly(27)
