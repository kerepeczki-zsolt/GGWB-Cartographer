import numpy as np
from scipy.signal import welch, resample

# --- GGWB-CARTOGRAPHER ADAPTIVE WHITENING ENGINE (v8.0.0 PRO) ---
# Dinamikus zajfehérítés valódi PSD becsléssel a LIGO standardok alapján.
# Készítette: Kerepeczki Zsolt

def apply_whitening(data, fs):
    """
    Ablakozott PSD becslésen alapuló fehérítés a spektrális szivárgás ellen.
    """
    n = len(data)
    
    # 1. PSD becslése Welch-módszerrel (profi LIGO eljárás)
    # Ez megmutatja a detektor pillanatnyi zajszintjét minden frekvencián
    f_psd, psd_values = welch(data, fs, nperseg=fs//2)
    
    # 2. Interpolláció a teljes FFT hosszakhoz
    # Biztosítjuk, hogy a PSD görbe pontosan illeszkedjen a jel FFT-jéhez
    psd_interp = np.interp(np.fft.rfftfreq(n, 1/fs), f_psd, psd_values)
    
    # 3. FFT végrehajtása
    data_fft = np.fft.rfft(data)
    
    # 4. Fehérítés: A jelet elosztjuk a zaj szórásával (gyök-PSD)
    # Hozzáadunk egy kis epsilon értéket a nullával való osztás ellen
    whitened_fft = data_fft / np.sqrt(psd_interp + 1e-20)
    
    # 5. Visszaalakítás idő-tartományba
    return np.fft.irfft(whitened_fft, n=n)

if __name__ == "__main__":
    print("[LOG] Whitening Engine v8.0.0 PRO tesztüzem...")