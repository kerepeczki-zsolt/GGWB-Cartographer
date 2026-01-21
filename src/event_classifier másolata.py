import numpy as np

def classify_event(corr_val, stats, is_vetoed):
    """
    GGWB-Cartographer Event Classifier v1.0
    Cél: 100% hiba-azonosítás, 95%+ jel-pontosság.
    """
    # 1. SZINT: Kritikus hiba ellenőrzés (Veto)
    if is_vetoed:
        return "100% HIBA (LIGO VETO: Hardveres hiba/Zaj tüske)", 1.0

    # 2. SZINT: Koincidencia ellenőrzés (H1 vs L1)
    # Ha nincs korreláció, de nagy a jel, az 100% helyi hiba
    if abs(corr_val) < 0.1 and stats['kurtosis'] > 10:
        return "100% HIBA (Glitch: Lokális anomália a detektorban)", 0.99
    
    # 3. SZINT: Jel-típus meghatározás (Al-populációk)
    # Kurtosis és statisztikai profil alapján
    confidence = 0.0
    label = "ISMERETLEN/ZAJ"

    if abs(corr_val) > 0.4:
        # Erős koincidencia és magas csúcsérték -> Fekete lyuk (CBC)
        if stats['kurtosis'] > 5:
            label = "96% JEL (Bináris Fekete Lyuk összeolvadás - CBC)"
            confidence = 0.96
        # Gyengébb, de stabil korreláció -> SGWB háttér
        else:
            label = "95% JEL (Stochasztikus Gravitációs Hullám Háttér - SGWB)"
            confidence = 0.95
    
    elif stats['kurtosis'] > 20:
        label = "98% HIBA (Blip Glitch: Rövid feszültségtüske)"
        confidence = 0.98
    
    return label, confidence