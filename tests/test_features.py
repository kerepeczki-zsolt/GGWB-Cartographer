import numpy as np
import cv2
from scipy import stats
from skimage.feature import greycomatrix, greycoprops


class GeometricFeatureExtractor:
    def __init__(self):
        self.feature_count = 92

    def extract_all_features(self, spectrogram: np.ndarray) -> np.ndarray:
        spec = np.asarray(spectrogram, dtype=float)
        spec = np.nan_to_num(spec, nan=0.0, posinf=0.0, neginf=0.0)

        features = []
        features.extend(self.basic_features(spec))
        features.extend(self.frequency_features(spec))
        features.extend(self.temporal_features(spec))
        features.extend(self.geometric_features(spec))
        features.extend(self.wavelet_features(spec))
        features.extend(self.texture_features(spec))

        return np.asarray(features, dtype=float)

    def basic_features(self, spec: np.ndarray) -> list[float]:
        eps = 1e-8
        max_val = float(np.max(spec))
        mean_val = float(np.mean(spec))
        std_val = float(np.std(spec))
        min_val = float(np.min(spec))

        dynamic_range = 20.0 * np.log10((max_val + eps) / (min_val + eps))

        flat = spec.flatten().astype(float)
        flat = flat + eps
        flat = flat / np.sum(flat)
        entropy = float(stats.entropy(flat))

        contrast = (max_val - mean_val) / (max_val + mean_val + eps)

        return [
            max_val,
            mean_val,
            std_val,
            dynamic_range,
            entropy,
            contrast
        ]

    def frequency_features(self, spec: np.ndarray) -> list[float]:
        eps = 1e-8

        if spec.ndim == 2:
            spectrum = np.mean(spec, axis=1)
        else:
            spectrum = spec.copy()

        spectrum = np.asarray(spectrum, dtype=float)
        spectrum = np.nan_to_num(spectrum, nan=0.0, posinf=0.0, neginf=0.0)

        fft_vals = np.abs(np.fft.rfft(spectrum)) + eps
        freqs = np.fft.rfftfreq(len(spectrum))
        P = fft_vals / np.sum(fft_vals)

        centroid = float(np.sum(freqs * P))
        spread = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * P)))
        skewness = float(np.sum(((freqs - centroid) ** 3) * P) / (spread**3 + eps))
        kurtosis = float(np.sum(((freqs - centroid) ** 4) * P) / (spread**4 + eps))

        geometric_mean = float(np.exp(np.mean(np.log(fft_vals))))
        arithmetic_mean = float(np.mean(fft_vals))
        flatness = geometric_mean / (arithmetic_mean + eps)

        rolloff_threshold = 0.85 * np.sum(fft_vals)
        cumulative = np.cumsum(fft_vals)
        rolloff_idx = int(np.searchsorted(cumulative, rolloff_threshold))
        rolloff = float(freqs[min(rolloff_idx, len(freqs) - 1)])

        max_val = float(np.max(fft_vals))
        noise_mean = float(np.mean(fft_vals[fft_vals < max_val])) + eps
        hnr = max_val / noise_mean

        shifted = np.roll(fft_vals, 1)
        flux = float(np.sum((fft_vals - shifted) ** 2))

        k = np.arange(1, len(fft_vals) + 1)
        decrease = float(np.sum((fft_vals[1:] - fft_vals[0]) / k[1:]) / (np.sum(fft_vals[1:]) + eps))

        slope = float(np.polyfit(freqs, fft_vals, 1)[0])
        entropy = float(stats.entropy(P))
        energy = float(np.sum(fft_vals**2))

        mid = len(fft_vals) // 2
        low_energy = float(np.sum(fft_vals[:mid]))
        high_energy = float(np.sum(fft_vals[mid:]) + eps)
        energy_ratio = low_energy / high_energy

        dom_idx = int(np.argmax(fft_vals))
        dominant_freq = float(freqs[dom_idx])

        peak_to_avg = max_val / (arithmetic_mean + eps)
        crest = max_val / (np.mean(np.abs(fft_vals)) + eps)

        return [
            centroid, spread, skewness, kurtosis,
            flatness, rolloff, hnr, flux,
            decrease, slope, entropy, energy,
            energy_ratio, dominant_freq, peak_to_avg, crest
        ]

    def temporal_features(self, spec: np.ndarray) -> list[float]:
        eps = 1e-8

        if spec.ndim == 2:
            signal = np.mean(spec, axis=0)
        else:
            signal = spec.copy()

        signal = np.asarray(signal, dtype=float)
        signal = np.nan_to_num(signal, nan=0.0, posinf=0.0, neginf=0.0)

        N = len(signal)
        t = np.arange(N)

        centroid = float(np.sum(t * signal) / (np.sum(signal) + eps))
        spread = float(np.sqrt(np.sum(((t - centroid) ** 2) * signal) / (np.sum(signal) + eps)))
        skewness = float(np.sum(((t - centroid) ** 3) * signal) / ((spread**3 + eps) * (np.sum(signal) + eps)))
        kurtosis = float(np.sum(((t - centroid) ** 4) * signal) / ((spread**4 + eps) * (np.sum(signal) + eps)))

        zero_crossings = np.where(np.diff(np.sign(signal)))[0]
        zcr = float(len(zero_crossings) / (N + eps))

        ste = float(np.sum(signal**2))
        rms = float(np.sqrt(np.mean(signal**2)))
        peak = float(np.max(np.abs(signal)))
        peak_to_rms = peak / (rms + eps)

        P = np.abs(signal) + eps
        P = P / np.sum(P)
        entropy = float(stats.entropy(P))

        geometric_mean = float(np.exp(np.mean(np.log(np.abs(signal) + eps))))
        arithmetic_mean = float(np.mean(np.abs(signal)))
        flatness = geometric_mean / (arithmetic_mean + eps)

        crest = peak / (arithmetic_mean + eps)

        cumulative = np.cumsum(np.abs(signal))
        rolloff_threshold = 0.85 * cumulative[-1]
        rolloff_idx = int(np.searchsorted(cumulative, rolloff_threshold))
        rolloff = float(rolloff_idx)

        slope = float(np.polyfit(t, signal, 1)[0])

        shifted = np.roll(signal, 1)
        flux = float(np.sum((signal - shifted) ** 2))

        k = np.arange(1, N + 1)
        decrease = float(np.sum((signal[1:] - signal[0]) / k[1:]) / (np.sum(signal[1:]) + eps))

        mid = N // 2
        low_energy = float(np.sum(signal[:mid] ** 2))
        high_energy = float(np.sum(signal[mid:] ** 2) + eps)
        energy_ratio = low_energy / high_energy

        dom_idx = int(np.argmax(signal))
        dominant_time = float(dom_idx)

        mad = float(np.mean(np.abs(np.diff(signal))))
        var_deriv = float(np.var(np.diff(signal)))
        smoothness = float(np.mean((signal[1:] - signal[:-1]) ** 2))
        stability = float(1.0 / (smoothness + eps))

        return [
            centroid, spread, skewness, kurtosis,
            zcr, ste, rms, peak,
            peak_to_rms, entropy, flatness, crest,
            rolloff, slope, flux, decrease,
            energy_ratio, dominant_time, mad, var_deriv,
            smoothness, stability
        ]

    def geometric_features(self, spec: np.ndarray) -> list[float]:
        eps = 1e-8

        if spec.ndim == 2:
            img = spec.copy()
        else:
            img = np.asarray(spec, dtype=float)

        img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)

        img_norm = img - np.min(img)
        img_norm = img_norm / (np.max(img_norm) + eps)
        img_norm = (img_norm * 255).astype(np.uint8)

        try:
            _, binary = cv2.threshold(img_norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        except:
            binary = (img_norm > 128).astype(np.uint8) * 255

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return [0.0] * 12

        cnt = max(contours, key=cv2.contourArea)

        area = float(cv2.contourArea(cnt))
        perimeter = float(cv2.arcLength(cnt, True))

        F45 = area
        F46 = perimeter
        F47 = 4 * np.pi * area / (perimeter**2 + eps)

        x, y, w, h = cv2.boundingRect(cnt)
        F48 = float(w / (h + eps))
        F49 = float(area / (w * h + eps))

        hull = cv2.convexHull(cnt)
        hull_area = float(cv2.contourArea(hull) + eps)
        F50 = float(area / hull_area)

        F51 = float(np.sqrt(4 * area / np.pi))

        try:
            (cx, cy), (MA, ma), angle = cv2.fitEllipse(cnt)
            F52 = float(ma)
            F53 = float(MA)
            F55 = float(angle)
        except:
            F52 = F53 = F55 = 0.0

        F54 = float(np.sqrt(1 - (F53**2) / (F52**2 + eps))) if F52 > 0 else 0.0

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
        import pywt
        eps = 1e-8

        if spec.ndim == 2:
            signal = np.mean(spec, axis=0)
        else:
            signal = spec.copy()

        signal = np.asarray(signal, dtype=float)
        signal = np.nan_to_num(signal, nan=0.0, posinf=0.0, neginf=0.0)

        coeffs = pywt.wavedec(signal, "db4", level=3)
        energies = []

        for c in coeffs:
            c = np.asarray(c, dtype=float)
            energies.append(float(np.sum(c**2)))

        while len(energies) < 25:
            energies.append(0.0)

        return energies[:25]

    def texture_features(self, spec: np.ndarray) -> list[float]:
        eps = 1e-8

        img = np.asarray(spec, dtype=float)
        img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)

        img_norm = img - np.min(img)
        img_norm = img_norm / (np.max(img_norm) + eps)
        img_norm = (img_norm * 255).astype(np.uint8)

        glcm = greycomatrix(
            img_norm,
            distances=[1],
            angles=[0],
            levels=256,
            symmetric=True,
            normed=True
        )

        energy = float(greycoprops(glcm, "energy")[0, 0])
        contrast = float(greycoprops(glcm, "contrast")[0, 0])
        homogeneity = float(greycoprops(glcm, "homogeneity")[0, 0])
        correlation = float(greycoprops(glcm, "correlation")[0, 0])
        asm = float(greycoprops(glcm, "ASM")[0, 0])

        entropy = float(-np.sum(glcm * np.log2(glcm + eps)))

        variance = float(np.var(img_norm))

        return [
            energy, contrast, homogeneity, correlation,
            asm, entropy, variance, 0.0, 0.0, 0.0, 0.0
        ]

