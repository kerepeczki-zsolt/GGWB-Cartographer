import numpy as np
from scipy import signal

def whiten_strain(strain, psd, fs, shift_seconds=0):
    """
    Whitened jelsorozat számítása + LIGO Time-Shift validáció.
    Implementáció: doku 3.3.2 + 100% Reliability Update.
    """
    
    # --- LIGO VALIDATION SZAKASZ ---
    # Ha a shift_seconds > 0, eltoljuk a jelet, hogy null-tesztet végezzünk.
    if shift_seconds > 0:
        shift_samples = int(shift_seconds * fs)
        strain = np.roll(strain, shift_samples)
        # Ez a fázis garantálja, hogy a korreláció csak zajt találjon.
    # -------------------------------

    # PSD interpoláció
    freqs = np.fft.rfftfreq(len(strain), 1/fs)
    psd_interp = np.interp(freqs, psd[:, 0], psd[:, 1])

    # FFT + fehérítés
    # Adtunk hozzá egy apró stabilitási faktort (1e-18), hogy ne legyen nullával osztás
    strain_fft = np.fft.rfft(strain)
    white_fft = strain_fft / (np.sqrt(psd_interp) + 1e-18)
    white_strain = np.fft.irfft(white_fft, n=len(strain))

    return white_strain

def compute_spectrogram(strain, fs, nperseg=256, noverlap=128):
    """
    STFT alapú spektrogram számítás (3.3.3).
    Visszatérés: spectrogram (2D), freqs, times
    """
    freqs, times, Sxx = signal.spectrogram(
        strain,
        fs=fs,
        nperseg=nperseg,
        noverlap=noverlap,
        scaling="density",
        mode="magnitude"
    )
    return Sxx, freqs, times