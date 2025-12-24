import numpy as np
from scipy import stats


class GeometricFeatureExtractor:
    """
    GGWB-Cartographer – Geometric Feature Extractor
    ------------------------------------------------
    A spektrogramokból 92 geometriai és fizikai jellemzőt számító modul
    vázlatos első verziója. A teljes rendszer moduláris felépítésű:
    minden jellemzőkategória külön függvénycsoportban található.

    A jelenlegi implementáció az I. kategóriát (F1–F6) tartalmazza.
    A bemenet elvárt formája: 2D numpy array (float32/float64),
    ahol a dimenziók frekvencia × idő.
    """

    def __init__(self):
        pass

    # ============================================================
    # 0. INPUT VALIDÁCIÓ
    # ============================================================

    def _validate_spectrogram(self, spec: np.ndarray) -> None:
        """
        Ellenőrzi, hogy a bemenet érvényes spektrogram-e.

        Elvárt forma:
        - 2D numpy array (float típus),
        - nem üres,
        - nem tartalmaz NaN vagy inf értékeket.

        Parameters
        ----------
        spec : np.ndarray
            Spektrogram mátrix (frekvencia × idő).

        Raises
        ------
        ValueError
            Ha a bemenet bármely feltételnek nem felel meg.
        """
        if spec is None:
            raise ValueError("A spektrogram None értékű.")
        if not isinstance(spec, np.ndarray):
            raise ValueError("A spektrogramnak numpy array-nek kell lennie.")
        if spec.ndim != 2:
            raise ValueError("A spektrogramnak 2D mátrixnak kell lennie.")
        if spec.size == 0:
            raise ValueError("A spektrogram üres.")
        if not np.isfinite(spec).all():
            raise ValueError("A spektrogram NaN vagy inf értékeket tartalmaz.")

    # ============================================================
    # I. KATEGÓRIA – ALAPVETŐ JELLEMZŐK (F1–F6)
    # ============================================================

    def F1_max_intensity(self, spec: np.ndarray) -> float:
        """
        F1 – Maximális intenzitás
        -------------------------
        Definíció:
            I_max = max_{t,f} S(t,f)

        Returns
        -------
        float
            A spektrogram legnagyobb amplitúdója.
        """
        self._validate_spectrogram(spec)
        return float(np.max(spec))

    def F2_mean_intensity(self, spec: np.ndarray) -> float:
        """
        F2 – Átlagos intenzitás
        ------------------------
        Definíció:
            I_mean = (1/N) * Σ S(t,f)

        Returns
        -------
        float
            A spektrogram elemeinek átlaga.
        """
        self._validate_spectrogram(spec)
        return float(np.mean(spec))

    def F3_std_intensity(self, spec: np.ndarray) -> float:
        """
        F3 – Intenzitás szórása
        ------------------------
        Definíció:
            σ_I = sqrt( (1/N) * Σ (S - I_mean)^2 )

        Returns
        -------
        float
            Az intenzitásértékek szórása.
        """
        self._validate_spectrogram(spec)
        return float(np.std(spec))

    def F4_dynamic_range(self, spec: np.ndarray) -> float:
        """
        F4 – Dinamikus tartomány (dB)
        ------------------------------
        Definíció (lineáris amplitúdóból):
            DR = 20 * log10(|I_max| / (|I_min| + ε))

        Numerikus stabilitás:
            - Ha I_min ≈ 0, kis epsilont adunk hozzá.
            - Abszolút értéket használunk, hogy ne okozzon gondot
              esetleges negatív érték (pl. whitenelt spektrumnál).

        Returns
        -------
        float
            A dinamikus tartomány decibelben.
        """
        self._validate_spectrogram(spec)
        I_max = float(np.max(spec))
        I_min = float(np.min(spec))

        eps = 1e-12
        num = abs(I_max) + eps
        den = abs(I_min) + eps
        return float(20.0 * np.log10(num / den))

    def F5_entropy(self, spec: np.ndarray) -> float:
        """
        F5 – Spektrogram Shannon-entrópiája
        -----------------------------------
        Definíció:
            p_ij = S_ij / Σ_kl S_kl
            H = - Σ_ij p_ij * log2(p_ij)

        Implementáció:
            - A spektrogramot eltoljuk úgy, hogy minden elem ≥ 0 legyen.
            - Nullösszeg esetén H = 0-t adunk vissza.
            - A log2(0) elkerülésére csak p>0 elemeket használunk.

        Returns
        -------
        float
            A normalizált spektrális eloszlás Shannon-entrópiája.
        """
        self._validate_spectrogram(spec)
        S = spec.astype(float)

        S = S - np.min(S)
        total = float(np.sum(S))

        if total <= 0.0:
            return 0.0

        p = S / total
        p = p[p > 0.0]
        return float(-np.sum(p * np.log2(p)))

    def F6_contrast_ratio(self, spec: np.ndarray) -> float:
        """
        F6 – Kontraszt arány
        ---------------------
        Koncepció:
            A „foreground” (legnagyobb intenzitású) és „background”
            (legalacsonyabb intenzitású) pixelek átlagát hasonlítjuk össze.

        Definíció:
            I_fg  = felső q% intenzitás átlaga
            I_bg  = alsó q% intenzitás átlaga
            CR    = (I_fg - I_bg) / (I_fg + I_bg + ε)

        Jelen implementáció:
            q = 10% (ha nagyon kevés pixel van, legalább 1 elem / oldal).

        Returns
        -------
        float
            Dimenzió nélküli kontrasztmutató [-1, 1] körüli tartományban.
        """
        self._validate_spectrogram(spec)
        flat = spec.astype(float).ravel()
        sorted_vals = np.sort(flat)

        n = len(sorted_vals)
        if n == 0:
            return 0.0

        k = max(1, n // 10)

        I_bg = float(np.mean(sorted_vals[:k]))
        I_fg = float(np.mean(sorted_vals[-k:]))

        eps = 1e-12
        return float((I_fg - I_bg) / (I_fg + I_bg + eps))

    # ============================================================
    # ÖSSZESÍTŐ FÜGGVÉNY – I. kategória
    # ============================================================

    def extract_basic_features(self, spec: np.ndarray) -> list[float]:
        """
        Az I. kategória (F1–F6) összes jellemzőjét visszaadja.

        Returns
        -------
        list of float
            [F1, F2, F3, F4, F5, F6] sorrendben.
        """
        return [
            self.F1_max_intensity(spec),
            self.F2_mean_intensity(spec),
            self.F3_std_intensity(spec),
            self.F4_dynamic_range(spec),
            self.F5_entropy(spec),
            self.F6_contrast_ratio(spec),
      ]
