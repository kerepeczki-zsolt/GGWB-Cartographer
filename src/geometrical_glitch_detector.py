import numpy as np
import logging
from typing import Optional
from pydantic import BaseModel, Field

# --- Szigorú Fizikai Beállítások ---
class DetectorSettings(BaseModel):
    """
    Tudományos küszöbértékek a GW és a Glitch szétválasztásához.
    """
    # Ha a tilt (energia) > 0.45, az már túl hangos földi zaj
    max_energy_threshold: float = Field(default=0.45)
    # Ha a jel < 0.008 ms, az csak egy elektromos tüske (Blip)
    min_width_ms: float = Field(default=0.008)
    # A GGWB jellemzően ebben a sávban keresendő
    gw_freq_min: float = Field(default=15.0)
    gw_freq_max: float = Field(default=85.0)
    enable_logging: bool = True

class GeometricalExpertSystem:
    def __init__(self, settings: Optional[DetectorSettings] = None):
        self.settings = settings or DetectorSettings()
        self._setup_logger()
        
    def _setup_logger(self) -> None:
        self.logger = logging.getLogger("GGWB.GeometricalExpert")
        if not self.logger.handlers and self.settings.enable_logging:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def classify_modification(self, ifo: str, run: str, width: float, height: float, freq: float, tilt: float) -> str:
        """
        KRITIKUS OSZTÁLYOZÁS: Tűpontos elkülönítés.
        """
        # 1. Hibaellenőrzés
        if any(v < 0 for v in [width, height, freq]):
            return f"[{ifo}] ERROR: Érvénytelen negatív fizikai érték!"

        # 2. GLITCH DETEKCIÓ (Azonnali kiszűrés)
        
        # Túl nagy energia = Földi zaj (pl. teherautó, villám)
        if tilt >= self.settings.max_energy_threshold:
            return f"[{ifo}] GLITCH: Extrém energia (Tilt: {tilt}) - ELVETVE"

        # Túl rövid jel = Elektromos hiba (Blip glitch)
        if width < self.settings.min_width_ms:
            return f"[{ifo}] GLITCH: Geometriai Blip (Idő: {width}) - ELVETVE"

        # Túl magas frekvencia = Műszerzaj
        if freq > 150.0:
            return f"[{ifo}] GLITCH: Magas frekvenciás műszerzaj ({freq}Hz) - ELVETVE"

        # 3. GW JELÖLT KERESÉSE (Szigorú feltételek)
        # Csak ha a frekvencia a cél sávban van ÉS az energia mérsékelt
        if (self.settings.gw_freq_min <= freq <= self.settings.gw_freq_max) and (0.05 < tilt < 0.3):
            return f"[{ifo}] !!! GW JELÖLT !!! - Tiszta geometriájú jel ({freq}Hz)"

        # 4. MINDEN MÁS = HÁTTÉRZAJ
        return f"[{ifo}] STATISZTIKA: Alacsony prioritású háttérzaj"

    def get_feature_vector(self, width: float, height: float, freq: float, tilt: float) -> np.ndarray:
        return np.array([width, height, freq, tilt], dtype=np.float64)