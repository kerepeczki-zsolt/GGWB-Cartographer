import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

def generate_v12_atlas():
    print("--- GGWB-CARTOGRAPHER V12: VIZUALIZÁCIÓ INDÍTÁSA ---")
    if not os.path.exists(RESULTS_DIR): os.makedirs(RESULTS_DIR)
    
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * (10 + 50 * t**2) * t)
    
    plt.figure(figsize=(10, 6))
    plt.specgram(signal, Fs=1000, cmap='viridis')
    plt.title("GGWB-Cartographer V12 - H1 Detector Atlas")
    plt.xlabel("Idő (s)")
    plt.ylabel("Frekvencia (Hz)")
    plt.colorbar(label='Intenzitás')
    
    output_path = os.path.join(RESULTS_DIR, "v12_atlas_preview.png")
    plt.savefig(output_path)
    plt.close()
    print(f"\nSIKER: Az Atlasz vizualizáció elkészült: {output_path}")

if __name__ == '__main__':
    generate_v12_atlas()
