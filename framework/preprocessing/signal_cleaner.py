import numpy as np

def whiten_data(data):
    """
    Egyszerűsített fehérítés: az adatokat 0 középértékre és 1 szórásra hozzuk.
    (LIGO-grade alapművelet)
    """
    if data is None or len(data) == 0:
        return None
    
    # Csak a numerikus oszlopokat tisztítjuk (pl. 'Confidence' vagy 'Result')
    # A stressz tesztedben a 'Confidence' oszlop a mérvadó
    print("🧹 Adatfehérítés folyamatban...")
    
    # Ha van Confidence oszlop, azt normalizáljuk
    if 'Confidence' in data.columns:
        mean = data['Confidence'].mean()
        std = data['Confidence'].std()
        data['Whitened_Confidence'] = (data['Confidence'] - mean) / std
        return data
    return data