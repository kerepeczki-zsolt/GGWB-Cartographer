import numpy as np
import os

def calculate_cross_correlation(strain1, strain2):
    """
    Kiszámítja két detektor (pl. H1 és L1) adatának kereszt-korrelációját.
    Ez a módszer segít kiszűrni a helyi zajokat és megtalálni a közös 
    gravitációs hullám hátteret (SGWB).
    """
    print("[CORRELATOR] Kereszt-korrelációs együttható számítása...")
    
    # Pearson-féle korrelációs együttható számítása a két adatsor között
    correlation = np.corrcoef(strain1, strain2)[0, 1]
    
    # Meghatározunk egy szignifikanciai küszöböt (0.1 felett már gyanús)
    is_significant = abs(correlation) > 0.1
    
    print(f"[CORRELATOR] Mért korreláció: {correlation:.6f}")
    return correlation, is_significant