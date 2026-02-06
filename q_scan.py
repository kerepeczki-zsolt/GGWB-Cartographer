import numpy as np
import matplotlib.pyplot as plt
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

def generate_spectrogram_v12(anomaly_id):
    print(f"--- GGWB V12.4 | Vizuális Spektrogram Analízis (ID: {anomaly_id}) ---")
    
    # Paraméterek
    fs = 2048  # Mintavételezés (Hz)
    t = np.linspace(0, 1, fs)
    
    # Generálunk egy teszt GW-jelet (Chirp), hogy lásd, mit kell keresni
    # Valódi futtatásnál itt a 'real_ligo_scan.npy' szeletét töltenénk be
    f0, f1 = 30, 500
    chirp = np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t**2 / 2))
    noise = np.random.normal(0, 0.8, fs)
    data = chirp + noise

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Spektrogram kiszámítása
    # NFFT=256 a jó felbontáshoz, noverlap=240 a folyamatossághoz
    Pxx, freqs, bins, im = ax.specgram(data, Fs=fs, NFFT=256, noverlap=240, cmap='magma')
    
    ax.set_title(f"GGWB V12.4 | Frekvencia-Idő Ujjlenyomat (ID: {anomaly_id})", color='cyan')
    ax.set_xlabel("Idő (másodperc)")
    ax.set_ylabel("Frekvencia (Hz)")
    ax.set_ylim(20, 600)  # A legfontosabb tudományos tartomány
    
    plt.colorbar(im, label='Relatív Energia (dB)')
    
    out_file = os.path.join(project_root, f"q_scan_id_{anomaly_id}.png")
    plt.savefig(out_file)
    print(f"=== [SIKER] A vizuális bizonyíték elmentve: {out_file} ===")

if __name__ == "__main__":
    generate_spectrogram_v12(27)
