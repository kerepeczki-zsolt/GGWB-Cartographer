import numpy as np

def extract_geometry_features(data):
    """
    Kiszámítja az adatok geometriai és textúra jellemzőit.
    (Geometriai szűrő v13)
    """
    if data is None or 'Whitened_Confidence' not in data.columns:
        return None
    
    print("📐 Morfometriai elemzés (Geometria + Textúra)...")
    
    signal = data['Whitened_Confidence'].values
    
    # Kiszámoljuk az alapvető geometriai jellemzőket
    features = {
        "fractal_dimension": np.std(np.diff(signal)), # Egyszerűsített fraktál-indikátor
        "texture_entropy": np.sum(np.square(signal)) / len(signal), # Energia/Entrópia
        "peak_count": np.sum(signal > 2.0) # Kimagasló csúcsok száma
    }
    
    return features