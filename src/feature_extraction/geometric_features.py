import numpy as np
from scipy.stats import entropy
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern
from skimage.filters import threshold_otsu
from skimage.measure import (
    find_contours,
    moments,
    moments_central,
    moments_normalized,
    moments_hu,
    label,
    regionprops,
)
from scipy.signal import cwt, morlet
import pywt  # Requires installation: pip install PyWavelets
from typing import Optional, Tuple, Dict


class GeometricFeatureExtractor:
    """
    Extracts the 92 geometric/physical features defined in the GGWB-Cartographer v2.0 documentation.
    """
    EPS = 1e-12  # Small value to avoid division by zero

    def __init__(self):
        pass

    # ------------------------- Core helpers -------------------------

    def _validate_spectrogram(
        self,
        spec: np.ndarray,
        freq_axis: Optional[np.ndarray] = None,
        time_axis: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Validates the spectrogram and axes; returns non-negative spec, freq_axis, time_axis.
        """
        if not isinstance(spec, np.ndarray) or spec.ndim != 2 or spec.size == 0:
            raise ValueError("Spectrogram must be a non-empty 2D numpy array.")
        if np.isnan(spec).any() or np.isinf(spec).any():
            raise ValueError("Spectrogram contains NaN or Inf values.")

        # Shift to non-negative
        spec_nonneg = spec - np.min(spec)
        spec_nonneg = np.maximum(spec_nonneg, 0)

        if freq_axis is None:
            freq_axis = np.arange(spec.shape[0], dtype=float)
        elif len(freq_axis) != spec.shape[0]:
            raise ValueError("freq_axis length does not match spectrogram frequency dimension.")

        if time_axis is None:
            time_axis = np.arange(spec.shape[1], dtype=float)
        elif len(time_axis) != spec.shape[1]:
            raise ValueError("time_axis length does not match spectrogram time dimension.")

        return spec_nonneg, freq_axis, time_axis

    def _compute_prob_density(self, spec: np.ndarray) -> np.ndarray:
        """Compute normalized probability density P(t,f)."""
        total = np.sum(spec) + self.EPS
        return spec / total

    def _compute_frequency_pdf(self, spec: np.ndarray) -> np.ndarray:
        """Frequency marginal P(f) = sum_t P(t,f)."""
        total = np.sum(spec) + self.EPS
        return np.sum(spec, axis=1) / total

    def _compute_temporal_pdf(self, spec: np.ndarray) -> np.ndarray:
        """Temporal marginal P(t) = sum_f P(t,f)."""
        total = np.sum(spec) + self.EPS
        return np.sum(spec, axis=0) / total

    def _get_binary_image(self, spec: np.ndarray) -> np.ndarray:
        """Binarize spectrogram using Otsu's threshold."""
        thresh = threshold_otsu(spec)
        return spec > thresh

    def _get_largest_region_props(self, binary: np.ndarray):
        """Label and get properties of the largest region."""
        labeled = label(binary)
        props = regionprops(labeled)
        if not props:
            raise ValueError("No regions found in binary image.")
        largest = max(props, key=lambda p: p.area)
        return largest

    # ------------------------- Category I: Basic features (F1-F6) -------------------------

    def F1_max_intensity(self, spec: np.ndarray) -> float:
        """F1: Maximum intensity."""
        return float(np.max(spec))

    def F2_mean_intensity(self, spec: np.ndarray) -> float:
        """F2: Mean intensity."""
        return float(np.mean(spec))

    def F3_std_intensity(self, spec: np.ndarray) -> float:
        """F3: Intensity standard deviation."""
        return float(np.std(spec))

    def F4_dynamic_range(self, spec: np.ndarray) -> float:
        """F4: Dynamic range in dB."""
        I_max = np.max(spec)
        I_min = np.min(spec) + self.EPS
        return float(20 * np.log10((I_max + self.EPS) / I_min))

    def F5_entropy(self, spec: np.ndarray) -> float:
        """F5: Spectrogram entropy."""
        P = self._compute_prob_density(spec)
        return float(-np.sum(P * np.log2(P + self.EPS)))

    def F6_contrast_ratio(self, spec: np.ndarray) -> float:
        """F6: Contrast ratio using Otsu-based foreground/background."""
        thresh = threshold_otsu(spec)
        foreground = np.mean(spec[spec > thresh]) if np.any(spec > thresh) else 0.0
        background = np.mean(spec[spec <= thresh]) if np.any(spec <= thresh) else 0.0
        denom = foreground + background + self.EPS
        return float((foreground - background) / denom)

    # ------------------------- Category II: Frequency domain (F7-F14) -------------------------

    def F7_frequency_centroid(self, spec: np.ndarray, freq_axis: np.ndarray) -> float:
        """F7: Spectral centroid."""
        P_f = self._compute_frequency_pdf(spec)
        num = np.sum(freq_axis * P_f)
        den = np.sum(P_f) + self.EPS
        return float(num / den)

    def F8_spectral_spread(self, spec: np.ndarray, freq_axis: np.ndarray) -> float:
        """F8: Spectral spread (std)."""
        fc = self.F7_frequency_centroid(spec, freq_axis)
        P_f = self._compute_frequency_pdf(spec)
        num = np.sum(P_f * (freq_axis - fc) ** 2)
        den = np.sum(P_f) + self.EPS
        return float(np.sqrt(num / den))

    def F9_spectral_skewness(self, spec: np.ndarray, freq_axis: np.ndarray) -> float:
        """F9: Spectral skewness."""
        fc = self.F7_frequency_centroid(spec, freq_axis)
        sigma_f = self.F8_spectral_spread(spec, freq_axis) + self.EPS
        P_f = self._compute_frequency_pdf(spec)
        num = np.sum(P_f * (freq_axis - fc) ** 3)
        return float(num / (sigma_f ** 3))

    def F10_spectral_kurtosis(self, spec: np.ndarray, freq_axis: np.ndarray) -> float:
        """F10: Spectral kurtosis."""
        fc = self.F7_frequency_centroid(spec, freq_axis)
        sigma_f = self.F8_spectral_spread(spec, freq_axis) + self.EPS
        P_f = self._compute_frequency_pdf(spec)
        num = np.sum(P_f * (freq_axis - fc) ** 4)
        return float(num / (sigma_f ** 4) - 3.0)

    def F11_peak_frequency(self, spec: np.ndarray, freq_axis: np.ndarray) -> float:
        """F11: Peak frequency."""
        P_f = self._compute_frequency_pdf(spec)
        return float(freq_axis[np.argmax(P_f)])

    def F12_spectral_rolloff(self, spec: np.ndarray, freq_axis: np.ndarray) -> float:
        """F12: Spectral roll-off at 85%."""
        P_f = self._compute_frequency_pdf(spec)
        cumsum = np.cumsum(P_f) / (np.sum(P_f) + self.EPS)
        idx = np.searchsorted(cumsum, 0.85)
        idx = min(idx, len(freq_axis) - 1)
        return float(freq_axis[idx])

    def F13_hnr(self, spec: np.ndarray) -> float:
        """F13: Harmonic-to-noise ratio (simplified: max / std)."""
        return float(10.0 * np.log10((np.max(spec) + self.EPS) / (np.std(spec) + self.EPS)))

    def F14_spectral_flatness(self, spec: np.ndarray) -> float:
        """F14: Spectral flatness."""
        P_f = self._compute_frequency_pdf(spec)
        geo_mean = np.exp(np.mean(np.log(P_f + self.EPS)))
        arith_mean = np.mean(P_f)
        return float(geo_mean / (arith_mean + self.EPS))

    # ------------------------- Category III: Temporal domain (F15-F22) -------------------------

    def F15_temporal_centroid(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F15: Temporal centroid."""
        P_t = self._compute_temporal_pdf(spec)
        num = np.sum(time_axis * P_t)
        den = np.sum(P_t) + self.EPS
        return float(num / den)

    def F16_temporal_spread(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F16: Temporal spread (std)."""
        tc = self.F15_temporal_centroid(spec, time_axis)
        P_t = self._compute_temporal_pdf(spec)
        num = np.sum(P_t * (time_axis - tc) ** 2)
        den = np.sum(P_t) + self.EPS
        return float(np.sqrt(num / den))

    def F17_temporal_skewness(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F17: Temporal skewness."""
        tc = self.F15_temporal_centroid(spec, time_axis)
        sigma_t = self.F16_temporal_spread(spec, time_axis) + self.EPS
        P_t = self._compute_temporal_pdf(spec)
        num = np.sum(P_t * (time_axis - tc) ** 3)
        return float(num / (sigma_t ** 3))

    def F18_temporal_kurtosis(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F18: Temporal kurtosis."""
        tc = self.F15_temporal_centroid(spec, time_axis)
        sigma_t = self.F16_temporal_spread(spec, time_axis) + self.EPS
        P_t = self._compute_temporal_pdf(spec)
        num = np.sum(P_t * (time_axis - tc) ** 4)
        return float(num / (sigma_t ** 4) - 3.0)

    def F19_onset_time(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F19: Onset time."""
        P_t = self._compute_temporal_pdf(spec)
        max_P = np.max(P_t)
        idxs = np.where(P_t > 0.1 * max_P)[0]
        if len(idxs) == 0:
            return float(time_axis[0])
        return float(time_axis[idxs[0]])

    def F20_offset_time(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F20: Offset time."""
        P_t = self._compute_temporal_pdf(spec)
        max_P = np.max(P_t)
        idxs = np.where(P_t > 0.1 * max_P)[0]
        if len(idxs) == 0:
            return float(time_axis[-1])
        return float(time_axis[idxs[-1]])

    def F21_duration(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F21: Signal duration."""
        return float(self.F20_offset_time(spec, time_axis) - self.F19_onset_time(spec, time_axis))

    def F22_rise_time(self, spec: np.ndarray, time_axis: np.ndarray) -> float:
        """F22: Average rise time."""
        P_t = self._compute_temporal_pdf(spec)
        t_peak = float(time_axis[np.argmax(P_t)])
        t_onset = self.F19_onset_time(spec, time_axis)
        return float(t_peak - t_onset)

    # ------------------------- Category IV: Geometric shape (F23-F44) -------------------------

    def _compute_moments(self, binary: np.ndarray) -> Dict[str, float]:
        """Compute raw and central moments needed for the features."""
        m = moments(binary)
        mu = moments_central(binary)
        # no need for normalized here except Hu
        return {
            'M00': m[0, 0],
            'M10': m[1, 0],
            'M01': m[0, 1],
            'M20': m[2, 0],
            'M11': m[1, 1],
            'M02': m[0, 2],
            'mu20': mu[2, 0],
            'mu11': mu[1, 1],
            'mu02': mu[0, 2],
        }

    def F23_to_F29_moments(self, spec: np.ndarray) -> Dict[str, float]:
        """
        F23-F29: Image moments.
        Mapping (7 features, consistent with doc):
          F23: M00
          F24: M10
          F25: M01
          F26: M20
          F27: M11
          F28: M02
          F29: mu20
        """
        binary = self._get_binary_image(spec)
        moms = self._compute_moments(binary)
        return {
            'F23': float(moms['M00']),
            'F24': float(moms['M10']),
            'F25': float(moms['M01']),
            'F26': float(moms['M20']),
            'F27': float(moms['M11']),
            'F28': float(moms['M02']),
            'F29': float(moms['mu20']),
        }

    def F30_to_F36_hu_moments(self, spec: np.ndarray) -> Dict[str, float]:
        """F30-F36: 7 Hu invariant moments."""
        binary = self._get_binary_image(spec).astype(float)
        mu = moments_central(binary)
        nu = moments_normalized(mu)
        hu = moments_hu(nu)
        return {f'F{30 + i}': float(hu[i]) for i in range(7)}

    def F37_area(self, spec: np.ndarray) -> float:
        """F37: Area (M00)."""
        binary = self._get_binary_image(spec)
        return float(moments(binary)[0, 0])

    def F38_perimeter(self, spec: np.ndarray) -> float:
        """F38: Perimeter (approximate via largest contour length)."""
        binary = self._get_binary_image(spec)
        contours = find_contours(binary, 0.5)
        if not contours:
            return 0.0
        # Better approximation: sum of distances
        c = max(contours, key=len)
        perimeter = 0.0
        for i in range(len(c) - 1):
            perimeter += np.linalg.norm(c[i] - c[i+1])
        perimeter += np.linalg.norm(c[-1] - c[0])  # close the contour
        return float(perimeter)

    def F39_eccentricity(self, spec: np.ndarray) -> float:
        """F39: Eccentricity of largest region."""
        binary = self._get_binary_image(spec)
        props = self._get_largest_region_props(binary)
        return float(props.eccentricity)

    def F40_extent(self, spec: np.ndarray) -> float:
        """F40: Extent of largest region."""
        binary = self._get_binary_image(spec)
        props = self._get_largest_region_props(binary)
        return float(props.extent)

    def F41_compactness(self, spec: np.ndarray) -> float:
        """F41: Compactness P^2 / A."""
        A = self.F37_area(spec)
        P = self.F38_perimeter(spec)
        return float(P ** 2 / (A + self.EPS))

    def F42_convexity(self, spec: np.ndarray) -> float:
        """F42: Convex hull ratio A / A_convex."""
        binary = self._get_binary_image(spec)
        props = self._get_largest_region_props(binary)
        return float(props.area / (props.convex_area + self.EPS))

    def F43_solidity(self, spec: np.ndarray) -> float:
        """F43: Solidity (same formula as convexity in original doc)."""
        return self.F42_convexity(spec)

    def F44_orientation(self, spec: np.ndarray) -> float:
        """F44: Orientation of largest region."""
        binary = self._get_binary_image(spec)
        props = self._get_largest_region_props(binary)
        return float(props.orientation)
    def extract_shape_features(
        self,
        spec_nonneg: np.ndarray,
        threshold: float = 0.1,
    ) -> Dict[str, float]:
        """Collect F23–F44 geometric shape features into a flat dict."""
        features: Dict[str, float] = {}

        # F23–F29: image moments
        features.update(self.F23_to_F29_moments(spec_nonneg))

        # F30–F36: Hu invariant moments
        features.update(self.F30_to_F36_hu_moments(spec_nonneg))

        # F37–F44: single‑value region shape features
        features["F37"] = self.F37_area(spec_nonneg)
        features["F38"] = self.F38_perimeter(spec_nonneg)
        features["F39"] = self.F39_eccentricity(spec_nonneg)
        features["F40"] = self.F40_extent(spec_nonneg)
        features["F41"] = self.F41_compactness(spec_nonneg)
        features["F42"] = self.F42_convexity(spec_nonneg)
        features["F43"] = self.F43_solidity(spec_nonneg)
        features["F44"] = self.F44_orientation(spec_nonneg)

        return features
    # ------------------------- Category V: Wavelet transform (F45-F81) -------------------------

    def _compute_wavelet_energies_db4(self, spec: np.ndarray) -> np.ndarray:
        """
        Compute Daubechies db4 energies.
        Returns 16-dimensional vector (F45-F60).
        """
        coeffs = pywt.wavedec2(spec, 'db4', level=3)
        energies = []
        cA3, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs
        energies.append(np.sum(np.abs(cA3) ** 2))
        for cset in [(cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)]:
            for c in cset:
                energies.append(np.sum(np.abs(c) ** 2))
        energies = np.array(energies, dtype=float)
        if energies.size < 16:
            energies = np.pad(energies, (0, 16 - energies.size), mode='constant')
        else:
            energies = energies[:16]
        return energies

    def _compute_wavelet_energies_haar(self, spec: np.ndarray) -> np.ndarray:
        """
        Compute Haar energies.
        Returns 8-dimensional vector (F61-F68).
        """
        coeffs = pywt.wavedec2(spec, 'haar', level=3)  # Adjust level if needed
        energies = []
        for c in coeffs:
            if isinstance(c, tuple):
                for sub in c:
                    energies.append(np.sum(np.abs(sub) ** 2))
            else:
                energies.append(np.sum(np.abs(c) ** 2))
        energies = np.array(energies, dtype=float)
        if energies.size < 8:
            energies = np.pad(energies, (0, 8 - energies.size), mode='constant')
        else:
            energies = energies[:8]
        return energies

    def F45_to_F60_db4_energies(self, spec: np.ndarray) -> Dict[str, float]:
        """F45-F60: Daubechies db4 energies on 16 scales/components."""
        energies = self._compute_wavelet_energies_db4(spec)
        return {f'F{45 + i}': float(e) for i, e in enumerate(energies)}

    def F61_to_F68_haar_energies(self, spec: np.ndarray) -> Dict[str, float]:
        """F61-F68: Haar energies on 8 scales/components."""
        energies = self._compute_wavelet_energies_haar(spec)
        return {f'F{61 + i}': float(e) for i, e in enumerate(energies)}

    def F69_to_F80_morlet_coeffs(self, spec: np.ndarray) -> Dict[str, float]:
        """F69-F80: Morlet wavelet coefficients on 12 frequency bands (1D CWT over time-averaged signal)."""
        sig = np.mean(spec, axis=0)  # average over frequency → temporal signal
        widths = np.arange(1, 13).astype(float)  # Use integers cast to float to ensure compatibility
        cwtmatr = cwt(sig, morlet, widths)
        coeffs = np.mean(np.abs(cwtmatr), axis=1)
        return {f'F{69 + i}': float(c) for i, c in enumerate(coeffs)}

    def F81_wavelet_entropy(self, spec: np.ndarray) -> float:
        """F81: Wavelet entropy (using db4 energies)."""
        energies = self._compute_wavelet_energies_db4(spec)
        Etot = np.sum(energies) + self.EPS
        Pj = energies / Etot
        return float(-np.sum(Pj * np.log2(Pj + self.EPS)))

    # ------------------------- Category VI: Texture and pattern (F82-F92) -------------------------

    def _compute_glcm_props(self, spec: np.ndarray) -> Dict[str, float]:
        """Compute GLCM properties (8 gray levels, distance=1, angle=0)."""
        levels = 8
        vmin, vmax = np.min(spec), np.max(spec)
        if vmax == vmin:
            spec_quant = np.zeros_like(spec, dtype=np.uint8)
        else:
            # Scale to 0 to levels-1
            spec_quant = np.floor((spec - vmin) / (vmax - vmin + self.EPS) * (levels - 1)).astype(np.uint8)
        glcm = graycomatrix(
            spec_quant,
            distances=[1],
            angles=[0],
            levels=levels,
            symmetric=True,
            normed=True,
        )
        energy = graycoprops(glcm, 'energy')[0, 0]
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
        asm = graycoprops(glcm, 'ASM')[0, 0]
        glcm_vals = glcm.astype(float)
        glcm_entropy = -np.sum(glcm_vals * np.log2(glcm_vals + self.EPS))
        variance = float(np.var(spec_quant))
        return {
            'energy': float(energy),
            'contrast': float(contrast),
            'correlation': float(correlation),
            'homogeneity': float(homogeneity),
            'entropy': float(glcm_entropy),
            'variance': variance,
            'dissimilarity': float(dissimilarity),
            'ASM': float(asm),
        }

    def F82_to_F89_glcm(self, spec: np.ndarray) -> Dict[str, float]:
        """F82-F89: GLCM features."""
        props = self._compute_glcm_props(spec)
        return {
            'F82': props['energy'],
            'F83': props['contrast'],
            'F84': props['correlation'],
            'F85': props['homogeneity'],
            'F86': props['entropy'],
            'F87': props['variance'],
            'F88': props['dissimilarity'],
            'F89': props['ASM'],
        }

    def F90_lbp_entropy(self, spec: np.ndarray) -> float:
        """F90: LBP histogram entropy (P=8, R=1, uniform)."""
        lbp = local_binary_pattern(spec, P=8, R=1, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 10), density=True)
        return float(entropy(hist + self.EPS))

    def F91_fractal_dimension(self, spec: np.ndarray) -> float:
        """F91: Fractal dimension via simple box-counting."""
        binary = self._get_binary_image(spec)
        max_box = min(binary.shape) // 2
        if max_box < 2:
            return 0.0
        sizes = 2 ** np.arange(1, int(np.log2(max_box)) + 1)
        counts = []
        for s in sizes:
            cnt = 0
            for i in range(0, binary.shape[0], s):
                for j in range(0, binary.shape[1], s):
                    block = binary[i:i + s, j:j + s]
                    if block.size > 0 and np.any(block):
                        cnt += 1
            counts.append(max(cnt, 1))
        sizes = np.array(sizes, dtype=float)
        counts = np.array(counts, dtype=float)
        p = np.polyfit(np.log(sizes), np.log(counts), 1)
        return float(-p[0])

    def F92_lacunarity(self, spec: np.ndarray) -> float:
        """F92: Lacunarity averaged over several box sizes."""
        binary = self._get_binary_image(spec)
        sizes = [2, 4, 8, 16]
        sizes = [s for s in sizes if s <= min(binary.shape)]
        if not sizes:
            return 0.0
        lacs = []
        for r in sizes:
            masses = []
            for i in range(0, binary.shape[0] - r + 1, r):
                for j in range(0, binary.shape[1] - r + 1, r):
                    mass = np.sum(binary[i:i + r, j:j + r])
                    masses.append(mass)
            masses = np.array(masses, dtype=float)
            if masses.size == 0:
                continue
            mu = np.mean(masses)
            sigma = np.std(masses)
            lacs.append((sigma ** 2) / (mu ** 2 + self.EPS))
        if not lacs:
            return 0.0
        return float(np.mean(lacs))

            # ------------------------- Main public API -------------------------

    def extract_all_features(
        self,
        spec: np.ndarray,
        freq_axis: Optional[np.ndarray] = None,
        time_axis: Optional[np.ndarray] = None,
        threshold: float = 0.1,
    ) -> Dict[str, float]:
        """Compute all F1–F92 features and return as a flat dict."""
        # Spektrogram ellenőrzése + nemnegatívvá alakítás + tengelyek
        spec_nonneg, freq_axis, time_axis = self._validate_spectrogram(
            spec, freq_axis, time_axis
        )

        features: Dict[str, float] = {}

        # I. Basic intensity features (F1–F6)
        features.update({
            "F1": self.F1_max_intensity(spec),
            "F2": self.F2_mean_intensity(spec),
            "F3": self.F3_std_intensity(spec),
            "F4": self.F4_dynamic_range(spec),
            "F5": self.F5_entropy(spec),
            "F6": self.F6_contrast_ratio(spec),
        })

        # II. Spectral domain (F7–F14)
        if freq_axis is None:
            freq_axis = np.arange(spec.shape[0], dtype=float)
        features.update({
            "F7": self.F7_frequency_centroid(spec, freq_axis),
            "F8": self.F8_spectral_spread(spec, freq_axis),
            "F9": self.F9_spectral_skewness(spec, freq_axis),
            "F10": self.F10_spectral_kurtosis(spec, freq_axis),
            "F11": self.F11_peak_frequency(spec, freq_axis),
            "F12": self.F12_spectral_rolloff(spec, freq_axis),
            "F13": self.F13_hnr(spec_nonneg),
            "F14": self.F14_spectral_flatness(spec_nonneg),
        })

        # III. Temporal domain (F15–F22)
        if time_axis is None:
            time_axis = np.arange(spec.shape[1], dtype=float)
        features.update({
            "F15": self.F15_temporal_centroid(spec_nonneg, time_axis),
            "F16": self.F16_temporal_spread(spec_nonneg, time_axis),
            "F17": self.F17_temporal_skewness(spec_nonneg, time_axis),
            "F18": self.F18_temporal_kurtosis(spec_nonneg, time_axis),
            "F19": self.F19_onset_time(spec_nonneg, time_axis),
            "F20": self.F20_offset_time(spec_nonneg, time_axis),
            "F21": self.F21_duration(spec_nonneg, time_axis),
            "F22": self.F22_rise_time(spec_nonneg, time_axis),
        })

        # IV. Geometriai alak jellemzők (F23–F44)
        features.update(
            self.extract_shape_features(spec_nonneg, threshold=threshold)
        )

        # V. Időbeli alak / borítás jellemzők (F45–F48)
        features.update(
            self.extract_temporal_shape_features(spec_nonneg, time_axis)
        )

        # VI. Frekvencia‑sáv / blob / region jellemzők (F49–F62)
        features.update(
            self.extract_band_features(spec_nonneg, freq_axis)
        )
        features.update(
            self.extract_blob_features(spec_nonneg)
        )

        # VII. Textúra és mintázat (F82–F92)
        features.update(
            self.extract_texture_features(spec_nonneg)
        )

        # Végső takarítás: NaN / inf -> 0
        for k, v in features.items():
            if not np.isfinite(v):
                features[k] = 0.0

        return features
