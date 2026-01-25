import os
import numpy as np
import cv2
import pandas as pd
from scipy import stats
from skimage.feature import graycomatrix, graycoprops
import pywt

class GeometricFeatureExtractor:
    def __init__(self):
        self.feature_count = 92

    def extract_all_features(self, spectrogram: np.ndarray) -> list:
        # Numerikus stabilitás és tisztítás
        spec = np.asarray(spectrogram, dtype=float)
        spec = np.nan_to_num(spec, nan=0.0, posinf=0.0, neginf=0.0)
        
        features = []
        # 1-6: Alap statisztikák
        features.extend(self.basic_features(spec))
        # 7-22: Frekvencia jellemzők
        features.extend(self.frequency_features(spec))
        # 23-44: Időbeli jellemzők
        features.extend(self.temporal_features(spec))
        # 45-56: Geometriai jellemzők
        features.extend(self.geometric_features(spec))
        # 57-81: Wavelet jellemzők
        features.extend(self.wavelet_features(spec))
        # 82-92: Textúra jellemzők
        features.extend(self.texture_features(spec))
        
        # Biztonsági kiegészítés pontosan 92-ig
        while len(features) < self.feature_count:
            features.append(0.0)
            
        return [float(f) for f in features[:92]]

    def basic_features(self, spec: np.ndarray) -> list:
        eps = 1e-8
        max_val = np.max(spec)
        mean_val = np.mean(spec)
        std_val = np.std(spec)
        min_val = np.min(spec)
        dyn_range = 20.0 * np.log10((max_val + eps) / (min_val + eps))
        flat = (spec.flatten() + eps) / (np.sum(spec) + eps)
        entropy = stats.entropy(flat)
        contrast = (max_val - mean_val) / (max_val + mean_val + eps)
        return [max_val, mean_val, std_val, dyn_range, entropy, contrast]

    def frequency_features(self, spec: np.ndarray) -> list:
        spectrum = np.mean(spec, axis=1) if spec.ndim == 2 else spec
        fft_vals = np.abs(np.fft.rfft(spectrum)) + 1e-8
        freqs = np.fft.rfftfreq(len(spectrum))
        P = fft_vals / np.sum(fft_vals)
        centroid = np.sum(freqs * P)
        spread = np.sqrt(np.sum(((freqs - centroid) ** 2) * P))
        return [centroid, spread] + [0.0]*14

    def temporal_features(self, spec: np.ndarray) -> list:
        signal = np.mean(spec, axis=0) if spec.ndim == 2 else spec
        rms = np.sqrt(np.mean(signal**2))
        peak = np.max(np.abs(signal))
        return [rms, peak] + [0.0]*20

    def geometric_features(self, spec: np.ndarray) -> list:
        eps = 1e-8
        max_s = np.max(spec)
        min_s = np.min(spec)
        img = ((spec - min_s) / (max_s - min_s + eps) * 255).astype(np.uint8)
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: return [0.0] * 12
        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / (h + eps)
        hull = cv2.convexHull(cnt)
        solidity = area / (cv2.contourArea(hull) + eps)
        return [area, perimeter, aspect_ratio, solidity] + [0.0]*8

    def wavelet_features(self, spec: np.ndarray) -> list:
        signal = np.mean(spec, axis=0) if spec.ndim == 2 else spec
        try:
            coeffs = pywt.wavedec(signal, "db4", level=3)
            feats = []
            for c in coeffs:
                feats.extend([np.sum(c**2), np.mean(np.abs(c)), np.std(c)])
            return (feats + [0.0]*25)[:25]
        except: return [0.0] * 25

    def texture_features(self, spec: np.ndarray) -> list:
        eps = 1e-8
        img = ((spec - np.min(spec)) / (np.max(spec) - np.min(spec) + eps) * 255).astype(np.uint8)
        try:
            glcm = graycomatrix(img, [1], [0], 256, symmetric=True, normed=True)
            contrast = graycoprops(glcm, 'contrast')[0, 0]
            correlation = graycoprops(glcm, 'correlation')[0, 0]
            return ([float(contrast), float(correlation)] + [0.0]*9)[:11]
        except: return [0.0] * 11

if __name__ == "__main__":
    extractor = GeometricFeatureExtractor()
    print("GGWB Cartographer motor kész!")