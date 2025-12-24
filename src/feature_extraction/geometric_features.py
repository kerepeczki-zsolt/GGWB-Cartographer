
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
# ============================================================
    # III. KATEGÓRIA (F15–F22) – IDŐTARTOMÁNY JELLEMZŐK [file:363]
    # ============================================================

    def _compute_temporal_spectrum(self, spec: np.ndarray, time_axis: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
        """Q(t) = Σ_f S(f,t) – időtengely spektrum: időbeli energia eloszlás."""
        self._validate_spectrogram(spec)
        S = spec.astype(np.float64)
        S = S - np.min(S)  # non-negative
        
        n_time = S.shape[1]
        if time_axis is None:
            times = np.arange(n_time, dtype=np.float64)
        else:
            times = np.asarray(time_axis, dtype=np.float64)
            if len(times) != n_time:
                raise ValueError("time_axis hossza nem egyezik.")
        Q = np.sum(S, axis=0)
        return times, Q

    def F15_temporal_centroid(self, spec: np.ndarray, time_axis=None) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        total_energy = np.sum(Q)
        return 0.0 if total_energy <= 0 else float(np.sum(times * Q) / total_energy)

    def F16_temporal_spread(self, spec: np.ndarray, time_axis=None) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        total_energy = np.sum(Q)
        if total_energy <= 0:
            return 0.0
        tc = self.F15_temporal_centroid(spec, time_axis)
        variance = np.sum(((times - tc)**2 * Q)) / total_energy
        return float(np.sqrt(max(variance, 0.0)))

    def F17_temporal_skewness(self, spec: np.ndarray, time_axis=None) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        total_energy = np.sum(Q)
        if total_energy <= 0:
            return 0.0
        tc = self.F15_temporal_centroid(spec, time_axis)
        sigma_t = self.F16_temporal_spread(spec, time_axis)
        if sigma_t <= 0:
            return 0.0
        m3 = np.sum(((times - tc)**3 * Q)) / total_energy
        return float(m3 / (sigma_t**3 + 1e-18))

    def F18_temporal_kurtosis(self, spec: np.ndarray, time_axis=None) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        total_energy = np.sum(Q)
        if total_energy <= 0:
            return 0.0
        tc = self.F15_temporal_centroid(spec, time_axis)
        sigma_t = self.F16_temporal_spread(spec, time_axis)
        if sigma_t <= 0:
            return 0.0
        m4 = np.sum(((times - tc)**4 * Q)) / total_energy
        return float(m4 / (sigma_t**4 + 1e-18) - 3.0)

    def F19_temporal_rolloff(self, spec: np.ndarray, time_axis=None, rolloff_ratio: float = 0.85) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        total_energy = np.sum(Q)
        if total_energy <= 0:
            return 0.0
        target = rolloff_ratio * total_energy
        cumulative = np.cumsum(Q)
        idx = np.searchsorted(cumulative, target, side='left')
        idx = min(idx, len(times) - 1)
        return float(times[idx])

    def F20_temporal_flatness(self, spec: np.ndarray, time_axis=None) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        if Q.size == 0:
            return 0.0
        eps = 1e-12
        arith_mean = np.mean(Q)
        if arith_mean <= 0:
            return 0.0
        geo_mean = np.exp(np.mean(np.log(Q + eps)))
        return float(geo_mean / arith_mean)

    def F21_temporal_impulsivity(self, spec: np.ndarray, time_axis=None) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        if Q.size == 0 or np.sum(Q) == 0:
            return 0.0
        peak_energy = np.max(Q)
        mean_energy = np.mean(Q)
        eps = 1e-12
        return float(peak_energy / max(mean_energy, eps))

    def F22_temporal_hnr(self, spec: np.ndarray, time_axis=None, prominence_threshold: float = 0.1) -> float:
        times, Q = self._compute_temporal_spectrum(spec, time_axis)
        if Q.size == 0:
            return 0.0
        median_energy = np.median(Q)
        if median_energy <= 0:
            return 0.0
        threshold = (1 + prominence_threshold) * median_energy
        harmonic_mask = Q > threshold
        Q_harmonic = np.sum(Q[harmonic_mask])
        Q_noise = np.sum(Q[~harmonic_mask])
        eps = 1e-12
        return 10.0 * np.log10(max(Q_harmonic + eps, eps) / max(Q_noise + eps, eps))

    def extract_temporal_features(self, spec: np.ndarray, time_axis=None) -> list[float]:
        return [
            self.F15_temporal_centroid(spec, time_axis),
            self.F16_temporal_spread(spec, time_axis),
            self.F17_temporal_skewness(spec, time_axis),
            self.F18_temporal_kurtosis(spec, time_axis),
            self.F19_temporal_rolloff(spec, time_axis),
            self.F20_temporal_flatness(spec, time_axis),
            self.F21_temporal_impulsivity(spec, time_axis),
            self.F22_temporal_hnr(spec, time_axis),
        ]

    def extract_features_up_to_F22(self, spec: np.ndarray, freq_axis=None, time_axis=None) -> list[float]:
        return (self.extract_basic_features(spec) + 
                self.extract_frequency_features(spec, freq_axis) + 
                self.extract_temporal_features(spec, time_axis))
# ============================================================
    # IV. KATEGÓRIA (F23–F34) – IDŐ-FREKVENCIJA ALAKJELLEMZŐK [file:363]
    # ============================================================

    def _preprocess_spectrogram_for_shape(self, spec: np.ndarray, threshold: float = 0.1) -> tuple[np.ndarray, np.ndarray]:
        """Spektrogram előfeldolgozás alakanalízishez: threshold + largest connected component."""
        self._validate_spectrogram(spec)
        S = spec.astype(np.float64)
        S_norm = (S - np.min(S)) / (np.max(S) - np.min(S) + 1e-12)
        binary = S_norm > threshold  # foreground pixels
        
        from scipy.ndimage import label
        labeled, num_features = label(binary)
        if num_features == 0:
            rows, cols = spec.shape
            return np.zeros((rows, cols)), np.zeros((rows, cols))
        
        sizes = np.bincount(labeled.ravel())[1:]  # skip background
        largest_label = np.argmax(sizes) + 1
        mask = (labeled == largest_label)
        
        return mask.astype(np.float64), binary.astype(np.float64)

    def F23_spectrogram_area(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F23 – Spektrogram terület: foreground pixel szám."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        return float(np.sum(mask))

    def F24_spectrogram_perimeter(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F24 – Peremhossz: contour hossza."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 0.0
        
        from skimage.measure import find_contours
        contours = find_contours(mask, 0.5)
        if len(contours) == 0:
            return 0.0
        perimeter = sum(np.sqrt(np.sum(np.diff(c, axis=0)**2, axis=1)) for c in contours)
        return float(perimeter)

    def F25_compactness(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F25 – Kompaktitás: 4π*terület/perem²."""
        area = self.F23_spectrogram_area(spec, threshold)
        perimeter = self.F24_spectrogram_perimeter(spec, threshold)
        if perimeter <= 0:
            return 0.0
        return float(4 * np.pi * area / (perimeter**2 + 1e-12))

    def F26_eccentricity(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F26 – Excentricitás: sqrt(1 - b²/a²), ahol a,b főtengelyek."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 0.0
        
        from skimage.measure import regionprops
        props = regionprops(mask.astype(bool))[0]
        return float(props.eccentricity)

    def F27_orientation(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F27 – Orientáció: főtengely szög (radián)."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 0.0
        
        from skimage.measure import regionprops
        props = regionprops(mask.astype(bool))[0]
        return float(props.orientation)

    def F28_bounding_box_ratio(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F28 – Bounding box arány: szélesség/magasság."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 1.0
        
        from skimage.measure import regionprops
        props = regionprops(mask.astype(bool))[0]
        bbox = props.bbox
        height, width = bbox[2] - bbox[0], bbox[3] - bbox[1]
        return float(width / max(height, 1e-12))

    def F29_energy_ellipse_axes(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F29 – Energia-ellipszis főtengely aránya (a/b)."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 1.0
        
        rows, cols = np.nonzero(mask)
        if len(rows) < 2:
            return 1.0
        
        cov = np.cov(rows, cols)
        eigvals = np.linalg.eigvalsh(cov)
        a, b = np.sqrt(np.maximum(eigvals[::-1], 1e-12))  # nagyobb, kisebb
        return float(a / max(b, 1e-12))

    def F30_tf_skewness(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F30 – TF ferdeség: 2D súlyozott skewness."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        rows, cols = np.nonzero(mask)
        if len(rows) == 0:
            return 0.0
        
        mu_row, mu_col = np.mean(rows), np.mean(cols)
        m3_row = np.mean((rows - mu_row)**3)
        m3_col = np.mean((cols - mu_col)**3)
        sigma_row = np.std(rows)
        sigma_col = np.std(cols)
        skew_row = m3_row / (sigma_row**3 + 1e-12)
        skew_col = m3_col / (sigma_col**3 + 1e-12)
        return float((skew_row + skew_col) / 2)

    def F31_tf_kurtosis(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F31 – TF kurtosis: 2D súlyozott kurtosis - 3."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        rows, cols = np.nonzero(mask)
        if len(rows) == 0:
            return 0.0
        
        mu_row, mu_col = np.mean(rows), np.mean(cols)
        m4_row = np.mean((rows - mu_row)**4)
        m4_col = np.mean((cols - mu_col)**4)
        sigma_row = np.std(rows)
        sigma_col = np.std(cols)
        kurt_row = m4_row / (sigma_row**4 + 1e-12) - 3
        kurt_col = m4_col / (sigma_col**4 + 1e-12) - 3
        return float((kurt_row + kurt_col) / 2)

    def F32_tf_entropy(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F32 – TF entropia: -Σ p(f,t) log p(f,t)."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 0.0
        p = mask / np.sum(mask)
        eps = 1e-12
        return float(-np.sum(p * np.log(p + eps)))

    def F33_tf_contrast(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F33 – TF kontraszt: std(S)/mean(S) a maszk területén."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 0.0
        S_masked = spec * mask
        values = S_masked[S_masked > 0]
        if len(values) == 0:
            return 0.0
        return float(np.std(values) / np.mean(values))

    def F34_tf_flatness(self, spec: np.ndarray, threshold: float = 0.1) -> float:
        """F34 – TF laposság: geo_mean/arith_mean 2D."""
        mask, _ = self._preprocess_spectrogram_for_shape(spec, threshold)
        if np.sum(mask) == 0:
            return 0.0
        values = spec[mask > 0]
        if len(values) == 0:
            return 0.0
        eps = 1e-12
        arith_mean = np.mean(values)
        geo_mean = np.exp(np.mean(np.log(values + eps)))
        return float(geo_mean / arith_mean)

    def extract_shape_features(self, spec: np.ndarray, threshold: float = 0.1) -> list[float]:
        """F23–F34 összes alakjellemzője."""
        return [
            self.F23_spectrogram_area(spec, threshold),
            self.F24_spectrogram_perimeter(spec, threshold),
            self.F25_compactness(spec, threshold),
            self.F26_eccentricity(spec, threshold),
            self.F27_orientation(spec, threshold),
            self.F28_bounding_box_ratio(spec, threshold),
            self.F29_energy_ellipse_axes(spec, threshold),
            self.F30_tf_skewness(spec, threshold),
            self.F31_tf_kurtosis(spec, threshold),
            self.F32_tf_entropy(spec, threshold),
            self.F33_tf_contrast(spec, threshold),
            self.F34_tf_flatness(spec, threshold),
        ]

    def extract_features_up_to_F34(self, spec: np.ndarray, freq_axis=None, time_axis=None, threshold: float = 0.1) -> list[float]:
        """F1–F34 összes jellemzője (I+II+III+IV kategória)."""
        return (self.extract_features_up_to_F22(spec, freq_axis, time_axis) +
                self.extract_shape_features(spec, threshold))
