import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt

def run_real_data_audit():
    print("\n" + "="*70)
    print("   GGWB V40.0 | HIVATALOS LIGO (GWOSC) ADATOK AUDITJA")
    print("="*70)

    # 1. VALÓDI ADATOK LETÖLTÉSE (GW150914 esemény környéke)
    # Ez nem generált, ez a valós mérési adat!
    t0 = 1126259462.4  # A GW150914 időpontja
    print(f"[INFO] Valódi adatok lekérése a LIGO-Hanford detektorból (GPS: {t0})...")
    
    try:
        data = TimeSeries.fetch_open_data('H1', t0 - 2, t0 + 2)
        print("[SIKER] Adatok letöltve.")
    except Exception as e:
        print(f"[HIBA] Nem sikerült az adatletöltés: {e}")
        return

    # 2. AUDIT LOGIKA (A te rendszerednek fel kell ismernie a jelet a valóságban is)
    # Fehérítés (Whitening) és sávszűrő alkalmazása, ahogy a profik csinálják
    white_data = data.whiten()
    filtered_data = white_data.bandpass(30, 400)
    
    # Keressük a jelet (GW150914 egy Chirp jel)
    max_amp = np.max(np.abs(filtered_data.value))
    
    print("\n--- ANALÍZIS EREDMÉNYE ---")
    if max_amp > 5:  # Standard küszöbérték a fehérített adatoknál
        prediction = "CANDIDATE_GW (Validált)"
        status = "SIKER"
    else:
        prediction = "Background Noise"
        status = "Hiba / Zaj"

    print(f"Detektált típus: {prediction}")
    print(f"Státusz:         {status}")
    print(f"Max Amplitúdó:   {max_amp:.2f}")

    # 3. VIZUALIZÁCIÓ (Spektrogram a VALÓDI adatokból)
    specgram = filtered_data.spectrogram2(fftlength=0.02, overlap=0.01) ** (1/2.)
    
    plot = specgram.plot(norm='log', vmin=1e-23, vmax=1e-19)
    ax = plot.gca()
    ax.set_ylim(20, 500)
    ax.set_yscale('log')
    plt.title("VALÓDI LIGO ADAT: GW150914 Spektrogram")
    plt.show()

if __name__ == '__main__':
    run_real_data_audit()
