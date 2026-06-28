# -*- coding: utf-8 -*-
"""
GGWB-Cartographer - V12 Milestone
Fájl név: core_functions.py
Leírás: LIGO-szintű matematikai jelfeldolgozó mag a gyökérkönyvtárhoz.
        Tartalmazza a fáziseltolódás-mentes Butterworth szűrést,
        a dinamikus spektrális fehérítést (Whitening) és a kereszt-korrelációt.
"""

import numpy as np
from scipy.signal import butter, filtffilt, welch

def butter_bandpass(lowcut, highcut, fs, order=4):
    """
    Legenerálja a Butterworth sáváteresztő szűrő együtthatóit (b, a).
    A Nyquist-frekvenciához normalizálja a megadott vágási határokat.
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Fáziseltolódás-mentes Butterworth sáváteresztő szűrés alkalmazása.
    A filtffilt függvény kétszer futtatja le a szűrőt (előre és hátra),
    így a jel fázisa matematikailag teljesen érintetlen marad.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = filtffilt(b, a, data)
    return filtered_data

def whiten_signal(data, fs, dt=1.0):
    """
    Professzionális Spektrális Fehérítés (Whitening).
    Kiszámítja az interferométer aktuális zajteljesítmény-sűrűségét (PSD) Welch-módszerrel,
    majd a frekvenciatartományban normalizálja a jelet, hogy eltüntesse a fix földi zajcsúcsokat.
    """
    # 1. Zajteljesítmény-sűrűség (PSD) becslése Welch-módszerrel
    nperseg = int(fs * dt)
    frequencies, psd = welch(data, fs=fs, nperseg=nperseg, noverlap=nperseg//2)
    
    # 2. A jel átvitele a frekvenciatartományba Fourier-transzformációval (RFFT)
    data_fft = np.fft.rfft(data)
    fft_freqs = np.fft.rfftfreq(len(data), d=1/fs)
    
    # 3. A Welch-féle PSD interpolálása, hogy pontosan illeszkedjen az FFT pontjaihoz
    psd_interp = np.interp(fft_freqs, frequencies, psd)
    
    # 4. Fehérítés: a Fourier-komponenseket elosztjuk a zaj szórásával (gyök PSD)
    # Egy apró 1e-20 tagot adunk hozzá, hogy a nullával való osztás matematikailag kizárt legyen
    whitened_fft = data_fft / np.sqrt(psd_interp + 1e-20)
    
    # 5. Inverz Fourier-transzformáció (IRFFT) a tiszta időtartományba való visszatéréshez
    whitened_data = np.fft.irfft(whitened_fft, n=len(data))
    return whitened_data

def calculate_cross_correlation(signal_h1, signal_l1):
    """
    Kereszt-korreláció számítása a Hanford (H1) és Livingston (L1) adatok között.
    A bemeneti idősorokat normalizálja, majd kiszámítja a fázis-koherenciát.
    Az asztrofizikai koincidencia-ablak ellenőrzésének alapja.
    """
    # Ha a két időszelet hossza eltérne, a rövidebbhez igazítjuk a méretet
    if len(signal_h1) != len(signal_l1):
        min_len = min(len(signal_h1), len(signal_l1))
        signal_h1 = signal_h1[:min_len]
        signal_l1 = signal_l1[:min_len]
        
    # Normalizálás a stabil kereszt-korrelációhoz (Z-score normalizálás)
    norm_h1 = (signal_h1 - np.mean(signal_h1)) / (np.std(signal_h1) + 1e-12)
    norm_l1 = (signal_l1 - np.mean(signal_l1)) / (np.std(signal_l1) + 1e-12)
    
    # Kereszt-korreláció kiszámítása, a kimenet hossza megegyezik a bemenetével
    correlation = np.correlate(norm_h1, norm_l1, mode='same') / len(norm_h1)
    return correlation
