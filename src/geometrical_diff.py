import numpy as np

def calculate_absolute_precision(current_geo, reference_no_glic):
    """
    Kiszámítja a 92 geometriai jellemző közötti abszolút eltérést.
    Cél: 100%-os hiba-beazonosítás az al-populációk szintjén.
    """
    # 92 dimenziós vektorok összehasonlítása
    diff_vector = np.abs(current_geo - reference_no_glic)
    
    # A 'tisztaság' indexe (minél kisebb, annál közelebb vagyunk a téridő szövetéhez)
    purity_index = np.sum(diff_vector)
    
    return purity_index, diff_vector

# Példa a LISA és LIGO közötti váltásra a logikában
print("[SYSTEM] Geometriai differenciál-analízis készen áll.")