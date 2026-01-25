import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

def generate_pro_spectrogram():
    print("\n" + "="*60)
    print("   GGWB-CARTOGRAPHER: ADVANCED SPECTROGRAM ANALYSIS")
    print("="*60)

    # Paraméterek: 4096 Hz-es mintavételezés (LIGO standard)
    fs = 4096
    duration = 0.55
    t = np.linspace(-0.5, 0.05, int(fs * duration))
    
    # 1. Valódi LIGO jel modell (Chirp)
    # A frekvencia az idővel nem-lineárisan nő (ez a híres összefutó fekete lyuk hang)
    f_start = 30
    gw_signal = np.sin(2 * np.pi * (f_start * (1.0 - t)**(-0.25))) * 1e-21
    gw_signal[t > 0] = 0 # Az ütközés pillanata után elcsendesedik
    
    # 2. Háttérzaj generálása
    noise = np.random.normal(0, 1.2e-22, len(t))
    data = noise + gw_signal

    # 3. Spektrogram számítása (Idő-Frekvencia térkép)
    # A 'nperseg' határozza meg a felbontást - most finomra állítjuk
    f, times, Sxx = signal.spectrogram(data, fs, nperseg=128, noverlap=120)

    # 4. VIZUALIZÁCIÓ - A "Nobel-díjas" grafikon elkészítése
    plt.figure(figsize=(12, 10))
    
    # Felső ábra: A nyers hullámforma (Idő tartomány)
    plt.subplot(2, 1, 1)
    plt.plot(t, data, color='gray', alpha=0.4, label='Zaj + Gravitációs Hullám')
    plt.plot(t, gw_signal, color='#00FF00', linewidth=1.5, label='Ideális Chirp Modell')
    plt.title("GW150914 Esemény - Időbeli Hullámforma", fontsize=14)
    plt.xlabel("Idő az ütközéshez képest [s]")
    plt.ylabel("Strain (Téridő megnyúlás)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Alsó ábra: A Spektrogram (Idő-Frekvencia tartomány)
    plt.subplot(2, 1, 2)
    # A 'magma' színskála a leglátványosabb a csillagászati adatokhoz
    plt.pcolormesh(times - 0.5, f, 10 * np.log10(Sxx), shading='gouraud', cmap='magma')
    plt.title("Spektrogram - A Fekete Lyukak 'Éneke'", fontsize=14)
    plt.ylabel("Frekvencia [Hz]")
    plt.xlabel("Idő [s]")
    plt.ylim(20, 512) # A LIGO érzékenységi tartománya
    plt.colorbar(label='Energia Intenzitás [dB]')

    plt.tight_layout()
    
    # Automatikus mentés az eredmények közé
    if not os.path.exists("GGWB_Results"):
        os.makedirs("GGWB_Results")
    
    output_path = "GGWB_Results/GW150914_Ultimate_Analysis.png"
    plt.savefig(output_path, dpi=300) # Nagy felbontásban mentjük
    print(f"\nSiker! A grafikon elmentve: {output_path}")
    
    # Megjelenítés a képernyőn
    plt.show()

if __name__ == "__main__":
    generate_pro_spectrogram()