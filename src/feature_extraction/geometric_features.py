
import numpy as np
from scipy import stats


class GeometricFeatureExtractor:
    """
    GGWB-Cartographer – Geometric Feature Extractor (F1–F14)
    92 paraméteres rendszer első két kategóriája a disszertáció alapján. [file:363]
    """

    def __init__(self):
        pass

    def _validate_spectrogram(self, spec: np.ndarray) -> None:
        """Szigorú input ellenőrzés – minden függvény hívja."""
        if spec is None or not isinstance(spec, np.ndarray) or spec.ndim != 2 or spec.size == 0:
            raise ValueError("Érvénytelen spektrogram.")
        if not np.isfinite(spec).all():
            raise ValueError("NaN/inf értékek a spektrogramban.")

    def _compute_frequency_spectrum(self, spec: np.ndarray, freq_axis=None) -> tuple[np.ndarray, np.ndarray]:
        """P(f) = Σ_t S(f,t) – frekvencia spektrum."""
        self._validate_spectrogram(spec)
        S = spec.astype(np.float64)
        S = S - np.min(S)  # non-negative
        
        n_freq = S.shape[0]
        if freq_axis is None:
            freqs = np.arange(n_freq, dtype=np.float64)
        else:
            freqs = np.asarray(freq_axis, dtype=np.float64)
            if len(freqs) != n_freq:
                raise ValueError("freq_axis hossza nem egyezik.")
        P = np.sum(S, axis=1)
        return freqs, P

    # I. KATEGÓRIA F1–F6
    def F1_max_intensity(self, spec): 
        self._validate_spectrogram(spec)
        return float(np.max(spec))

    def F2_mean_intensity(self, spec): 
        self._validate_spectrogram(spec)
        return float(np.mean(spec))

    def F3_std_intensity(self, spec): 
        self._validate_spectrogram(spec)
        return float(np.std(spec))

    def F4_dynamic_range(self, spec):
        self._validate_spectrogram(spec)
        I_max, I_min = float(np.max(spec)), float(np.min(spec))
        eps = 1e-12
        return 20.0 * np.log10(max(abs(I_max), eps) / max(abs(I_min), eps))

    def F5_entropy(self, spec):
        self._validate_spectrogram(spec)
        S = spec.astype(np.float64) - np.min(spec)
        total = np.sum(S)
        if total <= 0:
            return 0.0
        p = S / total
        p = p[p > 0]
        return float(-np.sum(p * np.log2(p)))

    def F6_contrast_ratio(self, spec):
        self._validate_spectrogram(spec)
        flat = spec.ravel()
        sorted_vals = np.sort(flat)
        n, k = len(sorted_vals), max(1, n // 10)
        I_bg, I_fg = np.mean(sorted_vals[:k]), np.mean(sorted_vals[-k:])
        eps = 1e-12
        return float((I_fg - I_bg) / (I_fg + I_bg + eps))

    def extract_basic_features(self, spec):
        return [self.F1_max_intensity(spec), self.F2_mean_intensity(spec),
                self.F3_std_intensity(spec), self.F4_dynamic_range(spec),
                self.F5_entropy(spec), self.F6_contrast_ratio(spec)]

    # II. KATEGÓRIA F7–F14
    def F7_frequency_centroid(self, spec, freq_axis=None):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        total_power = np.sum(P)
        return 0.0 if total_power <= 0 else float(np.sum(freqs * P) / total_power)

    def F8_spectral_spread(self, spec, freq_axis=None):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        total_power = np.sum(P)
        if total_power <= 0:
            return 0.0
        fc = self.F7_frequency_centroid(spec, freq_axis)
        variance = np.sum(((freqs - fc)**2 * P)) / total_power
        return float(np.sqrt(max(variance, 0.0)))

    def F9_spectral_skewness(self, spec, freq_axis=None):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        total_power = np.sum(P)
        if total_power <= 0:
            return 0.0
        fc = self.F7_frequency_centroid(spec, freq_axis)
        sigma_f = self.F8_spectral_spread(spec, freq_axis)
        if sigma_f <= 0:
            return 0.0
        m3 = np.sum(((freqs - fc)**3 * P)) / total_power
        return float(m3 / (sigma_f**3 + 1e-18))

    def F10_spectral_kurtosis(self, spec, freq_axis=None):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        total_power = np.sum(P)
        if total_power <= 0:
            return 0.0
        fc = self.F7_frequency_centroid(spec, freq_axis)
        sigma_f = self.F8_spectral_spread(spec, freq_axis)
        if sigma_f <= 0:
            return 0.0
        m4 = np.sum(((freqs - fc)**4 * P)) / total_power
        return float(m4 / (sigma_f**4 + 1e-18) - 3.0)

    def F11_peak_frequency(self, spec, freq_axis=None):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        if P.size == 0 or np.all(P == 0):
            return 0.0
        idx = np.argmax(P)
        return float(freqs[idx])

    def F12_spectral_rolloff(self, spec, freq_axis=None, rolloff_ratio=0.85):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        total_power = np.sum(P)
        if total_power <= 0:
            return 0.0
        target = rolloff_ratio * total_power
        cumulative = np.cumsum(P)
        idx = np.searchsorted(cumulative, target, side='left')
        idx = min(idx, len(freqs) - 1)
        return float(freqs[idx])

    def F13_harmonic_to_noise_ratio(self, spec, freq_axis=None, prominence_threshold=0.1):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        if P.size == 0:
            return 0.0
        median_power = np.median(P)
        if median_power <= 0:
            return 0.0
        threshold = (1 + prominence_threshold) * median_power
        harmonic_mask = P > threshold
        P_harmonic = np.sum(P[harmonic_mask])
        P_noise = np.sum(P[~harmonic_mask])
        eps = 1e-12
        return float(10.0 * np.log10(max(P_harmonic + eps, eps) / max(P_noise + eps, eps)))

    def F14_spectral_flatness(self, spec, freq_axis=None):
        freqs, P = self._compute_frequency_spectrum(spec, freq_axis)
        if P.size == 0:
            return 0.0
        eps = 1e-12
        arith_mean = np.mean(P)
        if arith_mean <= 0:
            return 0.0
        geo_mean = np.exp(np.mean(np.log(P + eps)))
        return float(geo_mean / arith_mean)

    def extract_frequency_features(self, spec, freq_axis=None):
        """F7–F14 összes frekvencia jellemzője."""
        return [
            self.F7_frequency_centroid(spec, freq_axis),
            self.F8_spectral_spread(spec, freq_axis),
            self.F9_spectral_skewness(spec, freq_axis),
            self.F10_spectral_kurtosis(spec, freq_axis),
            self.F11_peak_frequency(spec, freq_axis),
            self.F12_spectral_rolloff(spec, freq_axis),
            self.F13_harmonic_to_noise_ratio(spec, freq_axis),
            self.F14_spectral_flatness(spec, freq_axis)
        ]

    def extract_all_features(self, spec, freq_axis=None):
        """F1–F14 összes jellemzője – főmetódus a disszertáció szerint."""
        return self.extract_basic_features(spec) + self.extract_frequency_features(spec, freq_axis)
