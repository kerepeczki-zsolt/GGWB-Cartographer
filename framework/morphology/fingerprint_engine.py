import numpy as np
from skimage.feature import greycomatrix, greycoprops, local_binary_pattern
from skimage.measure import label, regionprops
from scipy.stats import entropy
from framework.config.features import FEATURE_FLAGS

class GGWBFingerprintExtractor:
    """
    GGWB-Cartographer Morfológiai Jellegzetesség Kinyerő
    VI. Texture & Pattern blokk (F82–F91) + Experimental F92
    """

    # -----------------------------
    # Utility
    # -----------------------------
    def _normalize_uint8(self, spec):
        """ Normalizálás a textúra-analízishez (uint8) """
        spec_min = np.min(spec)
        spec_range = np.max(spec) - spec_min
        if spec_range > 0:
            spec = (spec - spec_min) / spec_range
        return (spec * 255).astype(np.uint8)

    # -----------------------------
    # F82–F89: GLCM texture features
    # -----------------------------
    def F82_to_F89_glcm(self, spec):
        spec_u8 = self._normalize_uint8(spec)
        glcm = greycomatrix(
            spec_u8, distances=[1], angles=[0], levels=256, 
            symmetric=True, normed=True
        )
        
        features = {}
        features["F82_glcm_contrast"] = greycoprops(glcm, "contrast")[0, 0]
        features["F83_glcm_dissimilarity"] = greycoprops(glcm, "dissimilarity")[0, 0]
        features["F84_glcm_homogeneity"] = greycoprops(glcm, "homogeneity")[0, 0]
        features["F85_glcm_energy"] = greycoprops(glcm, "energy")[0, 0]
        features["F86_glcm_correlation"] = greycoprops(glcm, "correlation")[0, 0]
        features["F87_glcm_ASM"] = greycoprops(glcm, "ASM")[0, 0]
        
        glcm_flat = glcm[:, :, 0, 0].flatten()
        features["F88_glcm_entropy"] = entropy(glcm_flat + 1e-12)
        features["F89_glcm_anisotropy"] = np.std(glcm_flat)
        return features

    # -----------------------------
    # F90: Local Binary Pattern entropy
    # -----------------------------
    def F90_lbp_entropy(self, spec):
        spec_u8 = self._normalize_uint8(spec)
        lbp = local_binary_pattern(spec_u8, P=8, R=1, method="uniform")
        hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 11), density=True)
        return entropy(hist + 1e-12)

    # -----------------------------
    # F91: Fractal dimension (box-counting)
    # -----------------------------
    def F91_fractal_dimension(self, spec):
        def boxcount(Z, k):
            S = np.add.reduceat(
                np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                np.arange(0, Z.shape[1], k), axis=1
            )
            return np.count_nonzero(S)

        Z = spec > np.mean(spec)
        Z = Z.astype(np.uint8)
        p = int(np.log2(min(Z.shape)))
        sizes = 2 ** np.arange(1, p - 1)
        counts = np.array([boxcount(Z, size) for size in sizes])
        
        if len(counts) < 2: return 0.0
        coeffs = np.polyfit(np.log(sizes), np.log(counts + 1e-12), 1)
        return -coeffs[0]

    # -----------------------------
    # F92: Experimental Geometry (Opcionális)
    # -----------------------------
    def F92_geometric_morphology(self, spec):
        threshold = np.mean(spec) + 0.5 * np.std(spec)
        binary_map = spec > threshold
        labeled = label(binary_map)
        regions = regionprops(labeled)

        if len(regions) == 0:
            return {"F92_geom_area_ratio": 0.0, "F92_geom_compactness": 0.0, "F92_geom_eccentricity": 0.0}

        region = max(regions, key=lambda r: r.area)
        area = region.area
        perimeter = region.perimeter if region.perimeter > 0 else 1.0
        compactness = 4 * np.pi * area / (perimeter ** 2)
        total_area = spec.shape[0] * spec.shape[1]

        return {
            "F92_geom_area_ratio": float(area / total_area),
            "F92_geom_compactness": float(compactness),
            "F92_geom_eccentricity": float(region.eccentricity)
        }

    # -----------------------------
    # MASTER CALL
    # -----------------------------
    def extract(self, spec):
        features = {}
        # VI. Texture & pattern block
        features.update(self.F82_to_F89_glcm(spec))
        features["F90_lbp_entropy"] = self.F90_lbp_entropy(spec)
        features["F91_fractal_dimension"] = self.F91_fractal_dimension(spec)

        # VII. Experimental geometry (OFF by default)
        if FEATURE_FLAGS.get("ENABLE_F92_GEOMETRIC_MORPHOLOGY", False):
            features.update(self.F92_geometric_morphology(spec))

        return features