import numpy as np

def classify_signal(data, r_value):
    if r_value > 0.2:
        # Chirp trend figyelése (emelkedő frekvencia/energia)
        if np.mean(data[-50:]) > np.mean(data[:50]):
            return "GW-CANDIDATE", "Gravitációs Hullám"
    return "GLITCH", "UNCATEGORIZED"