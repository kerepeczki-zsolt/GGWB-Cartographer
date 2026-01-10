import numpy as np
import cv2
from scipy import stats
from skimage.feature import greycomatrix, greycoprops


class GeometricFeatureExtractor:
    def __init__(self):
        # A teljes feature-vektor hossza (F1–F92)
        self.feature_count = 92

    def extract_all_features(self, spectrogram: np.ndarray) -> np.ndarray:
        """
        Az összes (F1–F92) feature kinyerése egy spektrumból / spektrogramból.

        - Bemenet: 2D numpy tömb (frekvencia x idő)
        - Kimenet: 1D numpy vektor, hossz: self.feature_count
        """
        # Biztonságos konverzió float típusra
        spec = np.asarray(spectrogram, dtype=float)

        # NaN / ±inf eltávolítása
        spec = np.nan_to_num(spec, nan=0.0, posinf=0.0, neginf=0.0)

        features = []

        # Kategória I: Alapvető jellemzők
        features.extend(self.basic_features(spec))

        # Kategória II: Frekvencia domain
        features.extend(self.frequency_features(spec))

        # Kategória III: Időbeli domain
        features.extend(self.temporal_features(spec))

        # Kategória IV: Geometriai forma
        features.extend(self.geometric_features(spec))

        # Kategória V: Wavelet
        features.extend(self.wavelet_features(spec))

        # Kategória VI: Textúra
        features.extend(self.texture_features(spec))

        return np.asarray(features, dtype=float)

    def basic_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória I – Alapvető intenzitás-jellemzők.

        F1: max intensity
        F2: mean intensity
        F3: std intensity
        F4: dynamic range (dB, stabilizált)
        F5: entropy (stabilizált)
        F6: contrast (stabilizált)
        """
        eps = 1e-8  # numerikus stabilitási konstans

        # Alap statisztikák
        max_val = float(np.max(spec))
        mean_val = float(np.mean(spec))
        std_val = float(np.std(spec))
        min_val = float(np.min(spec))

        # F4: dynamic range [dB] – elkerüljük a log(0)-t
        dynamic_range = 20.0 * np.log10((max_val + eps) / (min_val + eps))

        # F5: entropy – normalizált, pozitív eloszlásból
        flat = spec.flatten().astype(float)
        flat = flat + eps          # mindenhol > 0
        flat = flat / np.sum(flat) # normált eloszlás
        entropy = float(stats.entropy(flat))

        # F6: contrast – elkerüljük az osztást 0-val
        contrast = (max_val - mean_val) / (max_val + mean_val + eps)

        return [
            max_val,       # F1
            mean_val,      # F2
            std_val,       # F3
            dynamic_range, # F4
            entropy,       # F5
            contrast       # F6
        ]

    def frequency_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória II – Frekvencia domain jellemzők (F7–F22)
        """
        eps = 1e-8

        # 1) Ha 2D spektrogram jön, átlagoljuk időben
        if spec.ndim == 2:
            spectrum = np.mean(spec, axis=1)
        else:
            spectrum = spec.copy()

        spectrum = np.asarray(spectrum, dtype=float)
        spectrum = np.nan_to_num(spectrum, nan=0.0, posinf=0.0, neginf=0.0)

        # 2) FFT
        fft_vals = np.abs(np.fft.rfft(spectrum)) + eps
        freqs = np.fft.rfftfreq(len(spectrum))

        # Normalizált spektrum
        P = fft_vals / np.sum(fft_vals)

        # F7: centroid
        centroid = float(np.sum(freqs * P))

        # F8: spread
        spread = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * P)))

        # F9: skewness
        skewness = float(np.sum(((freqs - centroid) ** 3) * P) / (spread**3 + eps))

        # F10: kurtosis
        kurtosis = float(np.sum(((freqs - centroid) ** 4) * P) / (spread**4 + eps))

        # F11: spectral flatness
        geometric_mean = float(np.exp(np.mean(np.log(fft_vals))))
        arithmetic_mean = float(np.mean(fft_vals))
        flatness = geometric_mean / (arithmetic_mean + eps)

        # F12: spectral rolloff (85%)
        rolloff_threshold = 0.85 * np.sum(fft_vals)
        cumulative = np.cumsum(fft_vals)
        rolloff_idx = int(np.searchsorted(cumulative, rolloff_threshold))
        rolloff = float(freqs[min(rolloff_idx, len(freqs) - 1)])

        # F13: HNR
        max_val = float(np.max(fft_vals))
        noise_mean = float(np.mean(fft_vals[fft_vals < max_val])) + eps
        hnr = max_val / noise_mean

        # F14: spectral flux
        shifted = np.roll(fft_vals, 1)
        flux = float(np.sum((fft_vals - shifted) ** 2))

        # F15: spectral decrease
        k = np.arange(1, len(fft_vals) + 1)
        decrease = float(np.sum((fft_vals[1:] - fft_vals[0]) / k[1:]) / (np.sum(fft_vals[1:]) + eps))

        # F16: spectral slope
        slope = float(np.polyfit(freqs, fft_vals, 1)[0])

        # F17: spectral entropy
        entropy = float(stats.entropy(P))

        # F18: spectral energy
        energy = float(np.sum(fft_vals**2))

        # F19: low/high energy ratio
        mid = len(fft_vals) // 2
        low_energy = float(np.sum(fft_vals[:mid]))
        high_energy = float(np.sum(fft_vals[mid:]) + eps)
        energy_ratio = low_energy / high_energy

        # F20: dominant frequency
        dom_idx = int(np.argmax(fft_vals))
        dominant_freq = float(freqs[dom_idx])

        # F21: peak-to-average ratio
        peak_to_avg = max_val / (arithmetic_mean + eps)

        # F22: spectral crest factor
        crest = max_val / (np.mean(np.abs(fft_vals)) + eps)

        return [
            centroid,
            spread,
            skewness,
            kurtosis,
            flatness,
            rolloff,
            hnr,
            flux,
            decrease,
            slope,
            entropy,
            energy,
            energy_ratio,
            dominant_freq,
            peak_to_avg,
            crest
        ]

    def temporal_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória III – Időbeli jellemzők (F23–F44)
        Stabil, integer-biztos, NaN-mentes időtartománybeli jellemzők.
        """

        eps = 1e-8

        # Ha 2D spektrogram jön, időirányban átlagoljuk
        if spec.ndim == 2:
            signal = np.mean(spec, axis=0)
        else:
            signal = spec.copy()

        signal = np.asarray(signal, dtype=float)
        signal = np.nan_to_num(signal, nan=0.0, posinf=0.0, neginf=0.0)

        N = len(signal)
        t = np.arange(N)

        # F23: időbeli centroid
        centroid = float(np.sum(t * signal) / (np.sum(signal) + eps))

        # F24: időbeli spread
        spread = float(np.sqrt(np.sum(((t - centroid) ** 2) * signal) / (np.sum(signal) + eps)))

        # F25: időbeli skewness
        skewness = float(np.sum(((t - centroid) ** 3) * signal) / ((spread**3 + eps) * (np.sum(signal) + eps)))

        # F26: időbeli kurtosis
        kurtosis = float(np.sum(((t - centroid) ** 4) * signal) / ((spread**4 + eps) * (np.sum(signal) + eps)))

        # F27: zero-crossing rate
        zero_crossings = np.where(np.diff(np.sign(signal)))[0]
        zcr = float(len(zero_crossings) / (N + eps))

        # F28: short-time energy
        ste = float(np.sum(signal**2))

        # F29: RMS
        rms = float(np.sqrt(np.mean(signal**2)))

        # F30: peak amplitude
        peak = float(np.max(np.abs(signal)))

        # F31: peak-to-RMS ratio
        peak_to_rms = peak / (rms + eps)

        # F32: temporal entropy
        P = np.abs(signal) + eps
        P = P / np.sum(P)
        entropy = float(stats.entropy(P))

        # F33: temporal flatness
        geometric_mean = float(np.exp(np.mean(np.log(np.abs(signal) + eps))))
        arithmetic_mean = float(np.mean(np.abs(signal)))
        flatness = geometric_mean / (arithmetic_mean + eps)

        # F34: temporal crest factor
        crest = peak / (arithmetic_mean + eps)

        # F35: temporal rolloff (85%)
        cumulative = np.cumsum(np.abs(signal))
        rolloff_threshold = 0.85 * cumulative[-1]
        rolloff_idx = int(np.searchsorted(cumulative, rolloff_threshold))
        rolloff = float(rolloff_idx)

        # F36: temporal slope (lineáris regresszió)
        slope = float(np.polyfit(t, signal, 1)[0])

        # F37: temporal flux
        shifted = np.roll(signal, 1)
        flux = float(np.sum((signal - shifted) ** 2))

        # F38: temporal decrease
        k = np.arange(1, N + 1)
        decrease = float(np.sum((signal[1:] - signal[0]) / k[1:]) / (np.sum(signal[1:]) + eps))

        # F39: temporal energy ratio (first half / second half)
        mid = N // 2
        low_energy = float(np.sum(signal[:mid] ** 2))
        high_energy = float(np.sum(signal[mid:] ** 2) + eps)
        energy_ratio = low_energy / high_energy

        # F40: dominant time index
        dom_idx = int(np.argmax(signal))
        dominant_time = float(dom_idx)

        # F41: mean absolute derivative
        mad = float(np.mean(np.abs(np.diff(signal))))

        # F42: variance of derivative
        var_deriv = float(np.var(np.diff(signal)))

        # F43: temporal smoothness
        smoothness = float(np.mean((signal[1:] - signal[:-1]) ** 2))

        # F44: temporal stability
        stability = float(1.0 / (smoothness + eps))

        return [
            centroid,       # F23
            spread,         # F24
            skewness,       # F25
            kurtosis,       # F26
            zcr,            # F27
            ste,            # F28
            rms,            # F29
            peak,           # F30
            peak_to_rms,    # F31
            entropy,        # F32
            flatness,       # F33
            crest,          # F34
            rolloff,        # F35
            slope,          # F36
            flux,           # F37
            decrease,       # F38
            energy_ratio,   # F39
            dominant_time,  # F40
            mad,            # F41
            var_deriv,      # F42
            smoothness,     # F43
            stability       # F44
        ]

    def geometric_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória IV – Geometriai forma jellemzők (F45–F56)
        Stabil, bináris maszk-biztos, kontúr-biztos implementáció.
        """

        eps = 1e-8

        # 1) Ha 2D spektrogram jön, normalizáljuk 0–255 közé
        if spec.ndim == 2:
            img = spec.copy()
        else:
            img = np.asarray(spec, dtype=float)

        img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)

        # Normalizálás 0–255 közé
        img_norm = img - np.min(img)
        img_norm = img_norm / (np.max(img_norm) + eps)
        img_norm = (img_norm * 255).astype(np.uint8)

        # 2) Binarizálás (Otsu)
        try:
            _, binary = cv2.threshold(img_norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        except:
            binary = (img_norm > 128).astype(np.uint8) * 255

        # 3) Kontúrok keresése
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            # Ha nincs kontúr → minden érték 0
            return [0.0] * 12

        # Legnagyobb kontúr
        cnt = max(contours, key=cv2.contourArea)

        area = float(cv2.contourArea(cnt))
        perimeter = float(cv2.arcLength(cnt, True))

        # F45: area
        F45 = area

        # F46: perimeter
        F46 = perimeter

        # F47: circularity
        F47 = 4 * np.pi * area / (perimeter**2 + eps)

        # F48: bounding box aspect ratio
        x, y, w, h = cv2.boundingRect(cnt)
        F48 = float(w / (h + eps))

        # F49: extent (area / bounding box area)
        F49 = float(area / (w * h + eps))

        # F50: solidity (area / convex hull area)
        hull = cv2.convexHull(cnt)
        hull_area = float(cv2.contourArea(hull) + eps)
        F50 = float(area / hull_area)

        # F51: equivalent diameter
        F51 = float(np.sqrt(4 * area / np.pi))

        # F52: major axis length
        try:
            (cx, cy), (MA, ma), angle = cv2.fitEllipse(cnt)
            F52 = float(ma)
        except:
            F52 = 0.0

        # F53: minor axis length
        try:
            (cx, cy), (MA, ma), angle = cv2.fitEllipse(cnt)
            F53 = float(MA)
        except:
            F53 = 0.0

        # F54: eccentricity
        F54 = float(np.sqrt(1 - (F53**2) / (F52**2 + eps))) if F52 > 0 else 0.0

        # F55: orientation angle
        try:
            (cx, cy), (MA, ma), angle = cv2.fitEllipse(cnt)
            F55 = float(angle)
        except:
            F55 = 0.0

        # F56: convexity (perimeter / convex hull perimeter)
        try:
            hull_perimeter = float(cv2.arcLength(hull, True))
            F56 = float(perimeter / (hull_perimeter + eps))
        except:
            F56 = 0.0

        return [
            F45, F46, F47, F48, F49, F50,
            F51, F52, F53, F54, F55, F56
        ]                                                                                                                                                                   
    def wavelet_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória V – Wavelet jellemzők (F57–F81)
        Stabil, integer-biztos, NaN-mentes wavelet alapú jellemzők.
        25 darab jellemzőt ad vissza.
        """

        import pywt
        eps = 1e-8

        # Ha 2D spektrogram jön → időirányban átlagoljuk
        if spec.ndim == 2:
            signal = np.mean(spec, axis=0)
        else:
            signal = spec.copy()

        signal = np.asarray(signal, dtype=float)
        signal = np.nan_to_num(signal, nan=0.0, posinf=0.0, neginf=0.0)

        # Normalizálás
        max_abs = np.max(np.abs(signal))
        if max_abs > 0:
            signal = signal / (max_abs + eps)

        # 3 szintű wavelet dekompozíció (Daubechies 4)
        try:
            coeffs = pywt.wavedec(signal, "db4", level=3)
        except Exception:
            return [0.0] * 25

        features = []

        # Subband jellemzők (4 subband × 5 jellemző = 20)
        for band in coeffs:
            band = np.asarray(band, dtype=float)
            band = np.nan_to_num(band, nan=0.0, posinf=0.0, neginf=0.0)

            # Energia
            energy = float(np.sum(band ** 2))

            # Átlag abszolút érték
            mean_abs = float(np.mean(np.abs(band)))

            # Szórás
            std = float(np.std(band))

            # Entropia
            P = np.abs(band) + eps
            P = P / np.sum(P)
            entropy = float(np.sum(-P * np.log(P + eps)))

            # RMS
            rms = float(np.sqrt(np.mean(band ** 2)))

            features.extend([energy, mean_abs, std, entropy, rms])

        # Globális wavelet statisztikák (5 jellemző)
        all_coeffs = np.concatenate(coeffs)
        all_coeffs = np.nan_to_num(all_coeffs, nan=0.0, posinf=0.0, neginf=0.0)

        g_energy = float(np.sum(all_coeffs ** 2))
        g_mean_abs = float(np.mean(np.abs(all_coeffs)))
        g_std = float(np.std(all_coeffs))

        P = np.abs(all_coeffs) + eps
        P = P / np.sum(P)
        g_entropy = float(np.sum(-P * np.log(P + eps)))

        g_rms = float(np.sqrt(np.mean(all_coeffs ** 2)))

        features.extend([g_energy, g_mean_abs, g_std, g_entropy, g_rms])

        return features
    def texture_features(self, spec: np.ndarray) -> list[float]:
        """
        Kategória VI – Textúra jellemzők (F82–F92)
        GLCM alapú, numerikusan stabil, NaN-mentes implementáció.
        11 darab jellemzőt ad vissza.
        """

        eps = 1e-8

        # Ha 2D spektrogram → normalizáljuk 0–255 közé
        if spec.ndim == 2:
            img = spec.copy()
        else:
            img = np.asarray(spec, dtype=float)

        img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)

        img_norm = img - np.min(img)
        img_norm = img_norm / (np.max(img_norm) + eps)
        img_norm = (img_norm * 255).astype(np.uint8)

        # GLCM számítása 4 irányban
        glcm = greycomatrix(
            img_norm,
            distances=[1],
            angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
            levels=256,
            symmetric=True,
            normed=True
        )

        contrast = greycoprops(glcm, 'contrast').mean()
        dissimilarity = greycoprops(glcm, 'dissimilarity').mean()
        homogeneity = greycoprops(glcm, 'homogeneity').mean()
        ASM = greycoprops(glcm, 'ASM').mean()
        energy = greycoprops(glcm, 'energy').mean()
        correlation = greycoprops(glcm, 'correlation').mean()

        # Saját textúra statisztikák
        flat = img_norm.flatten().astype(float)
        flat = flat + eps
        flat = flat / np.sum(flat)

        entropy = float(stats.entropy(flat))
        mean_val = float(np.mean(flat))
        std_val = float(np.std(flat))
        skewness = float(stats.skew(flat))
        kurtosis = float(stats.kurtosis(flat))

        return [
            float(contrast),      # F82
            float(dissimilarity), # F83
            float(homogeneity),   # F84
            float(ASM),           # F85
            float(energy),        # F86
            float(correlation),   # F87
            entropy,              # F88
            mean_val,             # F89
            std_val,              # F90
            skewness,             # F91
            kurtosis              # F92
        ]
           
